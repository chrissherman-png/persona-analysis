"""
Persona Intelligence Agent for Zendesk Product Marketing
Analyzes Gong call data and CRM data to validate and update buyer personas

Date: 2026-03-25
"""

import pandas as pd
import json
import re
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PersonaIntelligenceAgent:
    """
    Analyzes conversation data to validate and update buyer personas
    according to the specification in the persona framework.
    """

    def __init__(self, data_file_path: str):
        """
        Initialize the agent with extracted data from SQL queries.

        Args:
            data_file_path: Path to CSV file from main extraction query
        """
        self.data_file_path = data_file_path
        self.raw_data = None
        self.processed_data = None
        self.persona_insights = defaultdict(lambda: defaultdict(list))
        self.data_quality_flags = []

        # Title normalization rules from Section 2A
        self.title_normalization_rules = {
            'C-Suite': [
                r'\bCEO\b', r'\bFounder\b', r'\bCOO\b', r'\bPresident\b',
                r'\bChief Operating Officer\b'
            ],
            'C-Suite (Tech)': [
                r'\bCTO\b', r'\bCIO\b', r'\bChief Technology\b',
                r'\bChief Information\b', r'\bChief Technical\b'
            ],
            'Finance': [
                r'\bCFO\b', r'\bChief Financial\b', r'\bVP.*Finance\b',
                r'\bFinance Director\b', r'\bDirector.*Finance\b',
                r'\bController\b', r'\bVP.*Financial\b'
            ],
            'CX Leader': [
                r'\bVP.*Customer Service\b', r'\bVP.*Support\b',
                r'\bVP.*Customer Experience\b', r'\bVP.*CX\b',
                r'\bDirector.*Customer Service\b', r'\bDirector.*Support\b',
                r'\bDirector.*Customer Experience\b', r'\bDirector.*CX\b',
                r'\bHead.*Customer Service\b', r'\bHead.*Support\b',
                r'\bHead.*Customer Experience\b', r'\bHead.*CX\b',
                r'\bManager.*Customer Service\b', r'\bManager.*Support\b',
                r'\bManager.*Customer Experience\b', r'\bManager.*CX\b',
                r'\bCustomer Care\b', r'\bContact Center\b',
                r'\bDigital Care\b'
            ],
            'IT Leader': [
                r'\bVP.*IT\b', r'\bVP.*Information Technology\b',
                r'\bDirector.*IT\b', r'\bDirector.*Information Technology\b',
                r'\bHead.*IT\b', r'\bHead.*Information Technology\b',
                r'\bManager.*IT\b', r'\bManager.*Information Technology\b',
                r'\bIT Manager\b', r'\bIT Director\b',
                r'\bInfrastructure\b', r'\bSecurity\b', r'\bEngineering\b'
            ],
            'Operations Leader': [
                r'\bVP.*Operations\b', r'\bDirector.*Operations\b',
                r'\bHead.*Operations\b', r'\bManager.*Operations\b',
                r'\bVP.*Business.*Ops\b', r'\bDirector.*Business.*Ops\b',
                r'\bVP.*Service.*Ops\b', r'\bDirector.*Service.*Ops\b',
                r'\bService Delivery\b', r'\bBusiness Operations\b'
            ],
            'Finance/Gatekeeper': [
                r'\bProcurement\b', r'\bPurchasing\b',
                r'\bVendor Management\b', r'\bSourcing\b'
            ]
        }

    def load_data(self) -> pd.DataFrame:
        """Load and validate input data."""
        logger.info(f"Loading data from {self.data_file_path}")

        try:
            self.raw_data = pd.read_csv(self.data_file_path)
            logger.info(f"Loaded {len(self.raw_data)} rows")

            # Validate required columns
            required_columns = [
                'CONVERSATION_KEY', 'SEGMENT', 'JOB_TITLE_RAW',
                'PARTICIPANT_EMAIL', 'RECENCY_TAG'
            ]

            missing_columns = [
                col for col in required_columns
                if col not in self.raw_data.columns
            ]

            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")

            return self.raw_data

        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise

    def preprocess_data(self) -> pd.DataFrame:
        """
        Apply preprocessing rules from Section 2.
        - Title Normalization (2A)
        - Company Size Tagging (2B) - already done in SQL
        - Entity Deduplication (2C)
        - Motion Tagging (2D) - already done in SQL
        """
        logger.info("Starting data preprocessing...")

        df = self.raw_data.copy()

        # 2A: Title Normalization
        logger.info("Applying title normalization rules...")
        df['NORMALIZED_PERSONA'] = df['JOB_TITLE_RAW'].apply(
            self._normalize_title
        )

        # Track unclassified titles
        unclassified = df[df['NORMALIZED_PERSONA'] == 'UNCLASSIFIED']
        unclassified_pct = (len(unclassified) / len(df)) * 100

        if unclassified_pct > 20:
            self.data_quality_flags.append(
                f"⚠️ DATA QUALITY ISSUE: {unclassified_pct:.1f}% of titles "
                f"are unclassified (threshold: 20%)"
            )
            logger.warning(
                f"{unclassified_pct:.1f}% of titles are unclassified"
            )

        logger.info(f"Title normalization complete. "
                   f"{len(unclassified)} unclassified out of {len(df)}")

        # 2C: Entity Deduplication
        logger.info("Deduplicating entities...")
        df['SOURCE_COUNT'] = df.groupby('PARTICIPANT_EMAIL')[
            'CONVERSATION_KEY'
        ].transform('nunique')

        # 2B & 2D: Already done in SQL (SEGMENT and DEAL_MOTION columns)
        # Validate segment values
        valid_segments = ['SMB', 'Commercial']
        df = df[df['SEGMENT'].isin(valid_segments)]

        logger.info(f"Preprocessing complete. {len(df)} rows after filtering.")

        self.processed_data = df
        return df

    def _normalize_title(self, title: str) -> str:
        """
        Normalize a job title to a canonical persona role.
        Implements Section 2A Title Normalization Rules.
        """
        if pd.isna(title) or title == '':
            return 'UNCLASSIFIED'

        title_upper = title.upper()

        # Check each persona pattern
        for persona, patterns in self.title_normalization_rules.items():
            for pattern in patterns:
                if re.search(pattern, title, re.IGNORECASE):
                    return persona

        return 'UNCLASSIFIED'

    def extract_verbatim_quotes(self, transcript_json: str,
                                speaker_id: int,
                                participant_name: str) -> List[Dict]:
        """
        Extract verbatim quotes from transcript JSON for a specific speaker.

        Args:
            transcript_json: JSON string from TRANSCRIPT column
            speaker_id: Speaker ID to filter for
            participant_name: Name of participant (for context)

        Returns:
            List of dicts with quote text, timestamp, and metadata
        """
        if pd.isna(transcript_json):
            return []

        try:
            transcript_array = json.loads(transcript_json)

            quotes = []
            for segment in transcript_array:
                if segment.get('speaker_id') == speaker_id:
                    quotes.append({
                        'text': segment.get('text', ''),
                        'start_time_ms': segment.get('start_time_ms', 0),
                        'speaker_name': participant_name,
                        'type': 'VERBATIM'
                    })

            return quotes

        except (json.JSONDecodeError, TypeError) as e:
            logger.warning(f"Error parsing transcript JSON: {e}")
            return []

    def analyze_persona(self, segment: str, persona: str) -> Dict:
        """
        Analyze a single persona within a segment.
        Implements Step 3 from Section 5: Analyze by Persona.

        Args:
            segment: 'SMB' or 'Commercial'
            persona: Normalized persona role

        Returns:
            Dict with persona analysis results
        """
        logger.info(f"Analyzing {segment} - {persona}")

        # Filter data for this segment and persona
        df = self.processed_data[
            (self.processed_data['SEGMENT'] == segment) &
            (self.processed_data['NORMALIZED_PERSONA'] == persona)
        ]

        if len(df) < 5:
            return {
                'status': 'INSUFFICIENT_DATA',
                'message': f'Only {len(df)} signals found. Minimum 5 required.',
                'signal_count': len(df)
            }

        # Calculate recency distribution
        recency_counts = df['RECENCY_TAG'].value_counts()
        pct_current = (recency_counts.get('CURRENT', 0) / len(df)) * 100

        # Extract insights by attribute
        insights = {
            'segment': segment,
            'persona': persona,
            'total_signals': len(df),
            'unique_people': df['PARTICIPANT_EMAIL'].nunique(),
            'unique_conversations': df['CONVERSATION_KEY'].nunique(),
            'recency': {
                'CURRENT': recency_counts.get('CURRENT', 0),
                'DATED': recency_counts.get('DATED', 0),
                'pct_current': pct_current
            },
            'titles': self._analyze_titles(df),
            'industries': self._analyze_industries(df),
            'deal_motions': self._analyze_deal_motions(df),
            'deal_stages': self._analyze_deal_stages(df),
            'quotes': self._extract_persona_quotes(df),
            'call_briefs': self._extract_call_briefs(df)
        }

        return insights

    def _analyze_titles(self, df: pd.DataFrame) -> Dict:
        """Analyze common job titles for this persona."""
        title_counts = df['JOB_TITLE_RAW'].value_counts()

        return {
            'top_titles': title_counts.head(10).to_dict(),
            'unique_title_count': len(title_counts)
        }

    def _analyze_industries(self, df: pd.DataFrame) -> Dict:
        """Analyze top industries for this persona."""
        if 'INDUSTRY' not in df.columns:
            return {'top_industries': [], 'message': 'Industry data not available'}

        industry_counts = df['INDUSTRY'].value_counts()

        return {
            'top_industries': industry_counts.head(5).to_dict(),
            'unique_industry_count': len(industry_counts)
        }

    def _analyze_deal_motions(self, df: pd.DataFrame) -> Dict:
        """Analyze deal motion distribution (New Business vs Expansion)."""
        if 'DEAL_MOTION' not in df.columns:
            return {'distribution': {}, 'message': 'Deal motion data not available'}

        motion_counts = df['DEAL_MOTION'].value_counts()

        return {
            'distribution': motion_counts.to_dict(),
            'primary_motion': motion_counts.idxmax() if len(motion_counts) > 0 else None
        }

    def _analyze_deal_stages(self, df: pd.DataFrame) -> Dict:
        """Analyze when personas enter the buying cycle."""
        if 'DEAL_STAGE_CATEGORY' not in df.columns:
            return {'distribution': {}, 'message': 'Deal stage data not available'}

        stage_counts = df['DEAL_STAGE_CATEGORY'].value_counts()

        return {
            'distribution': stage_counts.to_dict(),
            'most_active_stage': stage_counts.idxmax() if len(stage_counts) > 0 else None
        }

    def _extract_persona_quotes(self, df: pd.DataFrame) -> List[Dict]:
        """Extract top verbatim quotes for this persona."""
        quotes = []

        # Sample up to 20 conversations for quote extraction
        sample_conversations = df.sample(n=min(20, len(df)))

        for _, row in sample_conversations.iterrows():
            if pd.notna(row.get('TRANSCRIPT')):
                speaker_quotes = self.extract_verbatim_quotes(
                    row['TRANSCRIPT'],
                    row.get('SPEAKER_ID'),
                    row['PARTICIPANT_NAME']
                )
                quotes.extend(speaker_quotes[:3])  # Top 3 quotes per call

        return quotes[:10]  # Return top 10 overall

    def _extract_call_briefs(self, df: pd.DataFrame) -> List[str]:
        """Extract AI-generated call briefs for pattern analysis."""
        if 'CALL_SPOTLIGHT_BRIEF' not in df.columns:
            return []

        briefs = df['CALL_SPOTLIGHT_BRIEF'].dropna().unique().tolist()
        return briefs[:10]  # Return sample of 10

    def validate_persona_attribute(self, current_definition: str,
                                   findings: List[str],
                                   total_signals: int) -> Tuple[str, str, str]:
        """
        Validate a persona attribute against findings.
        Implements Section 4: Validation and Update Thresholds.

        Args:
            current_definition: Current persona attribute text
            findings: List of findings from data
            total_signals: Total number of signals analyzed

        Returns:
            Tuple of (status, confidence, evidence)
            status: '✅ VALIDATED', '⚠️ UPDATED', or '🆕 NEW SIGNAL'
            confidence: 'HIGH', 'MEDIUM', or 'LOW'
            evidence: Supporting evidence string
        """
        if not findings or total_signals == 0:
            return ('🆕 NEW SIGNAL', 'LOW', 'No data found')

        # Count confirming signals
        confirming_count = len(findings)

        # Calculate confirmation percentage
        confirmation_pct = (confirming_count / total_signals) * 100

        # Determine status based on thresholds
        if confirmation_pct >= 60:
            status = '✅ VALIDATED'
        elif confirmation_pct >= 40:
            status = '⚠️ UPDATED'
        else:
            status = '🆕 NEW SIGNAL'

        # Determine confidence tier
        if total_signals >= 10:
            confidence = 'HIGH CONFIDENCE'
        elif total_signals >= 5:
            confidence = 'MEDIUM CONFIDENCE'
        else:
            confidence = 'LOW CONFIDENCE'

        evidence = f"{confirming_count}/{total_signals} signals ({confirmation_pct:.1f}%)"

        return (status, confidence, evidence)

    def generate_persona_report(self, segment: str, persona: str,
                               insights: Dict) -> str:
        """
        Generate a formatted persona report.
        Implements Section 6: Per-Persona Report format.
        """
        if insights.get('status') == 'INSUFFICIENT_DATA':
            return f"""
---
**PERSONA REPORT: {segment} — {persona}**
**Status:** INSUFFICIENT DATA — {insights.get('message')}
---
"""

        report = f"""
---
**PERSONA REPORT: {segment} — {persona}**
**Total signals:** {insights['total_signals']} (across {insights['unique_conversations']} conversations, {insights['unique_people']} unique people)
**Recency:** {insights['recency']['pct_current']:.1f}% CURRENT signals (< 6 months)
**Data sources:** Gong calls with CRM context

## Signal Breakdown

### Job Titles
Top titles observed:
"""

        for title, count in list(insights['titles']['top_titles'].items())[:5]:
            report += f"- {title}: {count} occurrences\n"

        report += f"\n### Industries\n"
        if insights['industries'].get('top_industries'):
            report += "Top 3 industries:\n"
            for industry, count in list(insights['industries']['top_industries'].items())[:3]:
                report += f"- {industry}: {count} accounts\n"
        else:
            report += "Industry data not available\n"

        report += f"\n### Deal Context\n"
        if insights['deal_motions'].get('distribution'):
            report += f"Primary motion: {insights['deal_motions']['primary_motion']}\n"
            report += "Motion distribution:\n"
            for motion, count in insights['deal_motions']['distribution'].items():
                report += f"- {motion}: {count} conversations\n"

        if insights['deal_stages'].get('distribution'):
            report += f"\nMost active in: {insights['deal_stages']['most_active_stage']} stage\n"

        report += f"\n### Sample Verbatim Quotes\n"
        if insights['quotes']:
            for i, quote in enumerate(insights['quotes'][:3], 1):
                report += f"{i}. \"{quote['text'][:200]}...\" [{quote['type']}]\n\n"
        else:
            report += "No transcript quotes available\n"

        report += f"\n### AI-Generated Call Insights\n"
        if insights['call_briefs']:
            for i, brief in enumerate(insights['call_briefs'][:3], 1):
                report += f"{i}. {brief[:200]}...\n\n"
        else:
            report += "No call briefs available\n"

        report += "\n---\n"

        return report

    def generate_downstream_agent_input(self, segment: str,
                                       all_persona_insights: Dict) -> str:
        """
        Generate Downstream Agent Input Block for marketing agents.
        Implements Section 6: Downstream Agent Input Block format.

        This output is purpose-built for the SMB/Commercial Persona Agents.
        """
        output = f"""
---
**DOWNSTREAM AGENT INPUT: {segment.upper()} PERSONA AGENT**
**Segment:** {segment} | {"50–249 Employees" if segment == "SMB" else "250–1,499 Employees"}
**Last updated:** {datetime.now().strftime('%Y-%m-%d')}
**Data freshness:** Last 6 months of Gong call data

"""

        for persona, insights in all_persona_insights.items():
            if insights.get('status') == 'INSUFFICIENT_DATA':
                continue

            output += f"""
**PERSONA: {persona}**

- **Who they are:** {persona} roles appear in {insights['unique_conversations']} conversations across {insights['unique_people']} unique individuals. They are {self._describe_persona_involvement(insights)}.

- **Common titles:** {', '.join(list(insights['titles']['top_titles'].keys())[:5])}

- **Top industries:** {', '.join(list(insights['industries'].get('top_industries', {}).keys())[:3]) or 'Data not available'}

- **Their goals:** [Extracted from call briefs and quotes - analyze patterns manually]

- **Their biggest challenges:** [Extracted from call transcripts - analyze pain points manually]

- **How they measure success (KPIs):** [Extracted from quotes mentioning metrics]

- **How they find and evaluate solutions:** [Review evaluation source data]

- **When they enter the buying cycle:** {insights['deal_stages'].get('most_active_stage', 'Unknown')} stage most common

- **Sample verbatim quotes:**
"""
            for quote in insights['quotes'][:3]:
                output += f"  - \"{quote['text'][:150]}...\" [VERBATIM]\n"

            output += "\n"

        output += "---\n"

        return output

    def _describe_persona_involvement(self, insights: Dict) -> str:
        """Helper to describe how a persona shows up in deals."""
        stage = insights['deal_stages'].get('most_active_stage', 'unknown')
        motion = insights['deal_motions'].get('primary_motion', 'unknown')

        return f"most active in {stage} stage deals, primarily in {motion} motions"

    def run_full_analysis(self) -> Dict:
        """
        Execute complete analysis workflow from Section 5.
        """
        logger.info("=== Starting Full Persona Analysis ===")

        # Step 1: Preprocess (already includes Step 1)
        self.load_data()
        self.preprocess_data()

        # Log data quality flags
        if self.data_quality_flags:
            logger.warning("Data Quality Flags:")
            for flag in self.data_quality_flags:
                logger.warning(flag)

        # Step 2-3: Classify and Analyze by Persona
        segments = ['SMB', 'Commercial']
        personas = [
            'C-Suite', 'C-Suite (Tech)', 'Finance', 'CX Leader',
            'IT Leader', 'Operations Leader', 'Finance/Gatekeeper'
        ]

        all_results = {}

        for segment in segments:
            segment_results = {}

            for persona in personas:
                insights = self.analyze_persona(segment, persona)
                segment_results[persona] = insights

                # Generate and save individual persona report
                report = self.generate_persona_report(segment, persona, insights)
                report_filename = f"persona_report_{segment}_{persona.replace('/', '_').replace(' ', '_')}.md"

                with open(report_filename, 'w') as f:
                    f.write(report)

                logger.info(f"Generated report: {report_filename}")

            all_results[segment] = segment_results

            # Step 6: Generate Downstream Agent Input
            downstream_input = self.generate_downstream_agent_input(
                segment, segment_results
            )

            downstream_filename = f"downstream_agent_input_{segment}.md"
            with open(downstream_filename, 'w') as f:
                f.write(downstream_input)

            logger.info(f"Generated downstream input: {downstream_filename}")

        logger.info("=== Analysis Complete ===")

        return all_results


def main():
    """Main execution function."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python persona_intelligence_agent.py <data_file.csv>")
        sys.exit(1)

    data_file = sys.argv[1]

    agent = PersonaIntelligenceAgent(data_file)
    results = agent.run_full_analysis()

    print("\n=== Analysis Summary ===")
    for segment, personas in results.items():
        print(f"\n{segment}:")
        for persona, insights in personas.items():
            if insights.get('status') == 'INSUFFICIENT_DATA':
                print(f"  {persona}: INSUFFICIENT DATA ({insights.get('signal_count', 0)} signals)")
            else:
                print(f"  {persona}: {insights['total_signals']} signals, "
                      f"{insights['unique_people']} people, "
                      f"{insights['recency']['pct_current']:.1f}% current")


if __name__ == "__main__":
    main()
