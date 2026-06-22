#!/usr/bin/env python3
"""
Claude-Powered Persona Analyzer
Replaces persona_nlp_analyzer.py with Claude API for deeper insight extraction

Phase 2 of the major pipeline upgrade
"""

import os
import json
import time
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from collections import defaultdict, Counter

import pandas as pd
import httpx
from anthropic import Anthropic, AnthropicBedrock, APIError, RateLimitError
from dotenv import load_dotenv

from research_loader import ResearchLoader
from metadata_writer import MetadataWriter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ClaudeAnalyzer:
    """Analyzes Gong transcripts using Claude API to extract persona insights."""

    # Persona identification patterns (updated to match updated_personas.json keys)
    PERSONA_PATTERNS = {
        'CX Champion': [
            r'VP.*Customer.*Service', r'VP.*Support', r'VP.*CX', r'VP.*Customer.*Experience',
            r'Director.*Customer.*Service', r'Director.*Support', r'Director.*CX',
            r'Head.*Customer.*Service', r'Head.*Support', r'Head.*CX',
            r'Manager.*Customer.*Service', r'Customer.*Care.*Manager'
        ],
        'CX Executive': [
            r'VP.*Customer.*Service', r'VP.*Support', r'VP.*CX', r'VP.*Customer.*Experience',
            r'Director.*Customer.*Service', r'Director.*Support', r'Director.*CX',
            r'SVP.*Customer', r'EVP.*Customer', r'Chief.*Customer.*Officer'
        ],
        'C-Suite Decision Maker': [
            r'\bCEO\b', r'\bCOO\b', r'\bCTO\b', r'\bCIO\b', r'\bCFO\b',
            r'\bPresident\b', r'\bFounder\b', r'Chief.*Officer', r'CCO\b'
        ],
        'Founder/Owner': [
            r'\bFounder\b', r'\bOwner\b', r'\bCEO\b', r'\bPresident\b',
            r'Managing Director', r'Principal'
        ],
        'IT Influencer': [
            r'IT.*Manager', r'IT.*Director', r'Head.*IT', r'VP.*IT',
            r'CISO\b', r'Security', r'Infrastructure', r'Systems.*Admin',
            r'Director.*Technology', r'VP.*Technology'
        ],
        'Enterprise IT Architect': [
            r'IT.*Architect', r'Enterprise.*Architect', r'Solutions.*Architect',
            r'Technical.*Architect', r'Principal.*Engineer', r'Staff.*Engineer',
            r'VP.*Engineering', r'VP.*Technology', r'CTO\b'
        ],
        'Operations Leader': [
            r'VP.*Operations', r'Director.*Operations', r'Head.*Operations',
            r'COO\b', r'Operations.*Manager', r'Service.*Delivery',
            r'Business.*Operations'
        ],
        'Global Operations Leader': [
            r'Global.*Operations', r'VP.*Global.*Operations', r'VP.*Operations',
            r'COO\b', r'Head.*Operations', r'SVP.*Operations'
        ],
        'Finance/Procurement Gatekeeper': [
            r'Procurement', r'Purchasing', r'Vendor.*Management', r'Sourcing',
            r'CFO\b', r'Finance.*Director', r'Controller', r'VP.*Finance'
        ],
        'Customer Service Generalist': [
            r'Customer.*Service.*Rep', r'Support.*Specialist', r'Customer.*Support',
            r'Agent', r'Rep\b', r'Specialist', r'Customer.*Care',
            r'Support.*Agent', r'Service.*Agent'
        ]
    }

    # Segment-persona mapping (matches updated_personas.json keys exactly)
    SEGMENT_PERSONAS = {
        'Digital': ['Customer Service Generalist', 'Founder/Owner'],
        'SMB': ['C-Suite Decision Maker', 'CX Champion', 'Finance/Procurement Gatekeeper', 'IT Influencer', 'Operations Leader'],
        'Commercial': ['C-Suite Decision Maker', 'CX Champion', 'Finance/Procurement Gatekeeper', 'IT Influencer', 'Operations Leader'],
        'Enterprise': ['CX Executive', 'Enterprise IT Architect', 'Global Operations Leader']
    }

    # Italian language detection (from persona_nlp_analyzer.py)
    ITALIAN_WORDS = [
        'della', 'delle', 'degli', 'dell', 'nella', 'nelle', 'negli',
        'questo', 'questa', 'questi', 'queste', 'anche', 'sono', 'hanno',
        'nel', 'dal', 'una', 'uno', 'gli', 'alla', 'alle',
        'migliorare', 'ridurre', 'allineare', 'sistemare', 'vendita',
        'obiettivo', 'processi', 'accesso', 'nuove', 'interni', 'base'
    ]

    # German language detection
    GERMAN_WORDS = [
        'und', 'der', 'die', 'das', 'ist', 'nicht', 'auch', 'für',
        'auf', 'mit', 'bei', 'werden', 'kann', 'oder', 'aber',
        'wir', 'haben', 'dass', 'sind', 'von', 'zu', 'den', 'dem',
        'über', 'mehr', 'wurde', 'werden', 'können', 'durch'
    ]

    def __init__(
        self,
        gong_csv_path: str,
        output_dir: str = '.',
        dry_run: bool = False,
        cache_dir: Optional[str] = None
    ):
        """
        Initialize Claude analyzer.

        Args:
            gong_csv_path: Path to Gong extraction CSV
            output_dir: Directory for output files
            dry_run: If True, process only 1 persona from 1 segment
            cache_dir: Optional directory for caching API responses
        """
        self.gong_csv_path = Path(gong_csv_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.dry_run = dry_run

        self.cache_dir = Path(cache_dir) if cache_dir else self.output_dir / 'cache'
        self.cache_dir.mkdir(exist_ok=True)

        # Load API configuration
        load_dotenv()

        # Check for Zendesk AI Gateway (AWS Bedrock with bearer token)
        aws_endpoint = os.getenv('AWS_ENDPOINT_URL_BEDROCK_RUNTIME')
        aws_bearer_token = os.getenv('AWS_BEARER_TOKEN_BEDROCK')

        if aws_endpoint and aws_bearer_token:
            # Zendesk AI Gateway configuration
            # The endpoint format is: https://ai-gateway.zende.sk/bedrock
            # Model invocation: {endpoint}/model/{model_id}/invoke
            self.use_custom_gateway = True
            self.gateway_endpoint = aws_endpoint
            self.bearer_token = aws_bearer_token
            # Note: Model ID is used in the URL path, not in the request body
            self.model = os.getenv('ANTHROPIC_MODEL', 'us.anthropic.claude-sonnet-4-6')
            self.client = None  # We'll make custom HTTP requests
            logger.info(f"Using Zendesk AI Gateway: {aws_endpoint}")
            logger.info(f"Model: {self.model}")
        else:
            # Fallback to standard Anthropic SDK
            self.use_custom_gateway = False
            api_key = os.getenv('ANTHROPIC_API_KEY')
            custom_base_url = os.getenv('ANTHROPIC_BASE_URL')
            if custom_base_url == '':
                custom_base_url = None

            if not api_key:
                raise ValueError(
                    "API configuration not found.\n"
                    "For Zendesk AI Gateway, set:\n"
                    "  AWS_ENDPOINT_URL_BEDROCK_RUNTIME=https://ai-gateway.zende.sk/bedrock\n"
                    "  AWS_BEARER_TOKEN_BEDROCK=your_token\n"
                    "Or for direct Anthropic API, set:\n"
                    "  ANTHROPIC_API_KEY=sk-ant-your_key"
                )

            # Check if using AWS Bedrock directly
            use_bedrock = os.getenv('USE_AWS_BEDROCK', 'false').lower() == 'true'

            if use_bedrock:
                # AWS Bedrock configuration
                aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
                aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
                aws_region = os.getenv('AWS_REGION', 'us-east-1')

                if not aws_access_key or not aws_secret_key:
                    logger.info("AWS credentials not in .env, attempting to use AWS CLI/environment credentials")

                self.client = AnthropicBedrock(
                    aws_access_key=aws_access_key,
                    aws_secret_key=aws_secret_key,
                    aws_region=aws_region
                )
                self.model = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"
                logger.info(f"Using AWS Bedrock in region {aws_region}")

            elif custom_base_url:
                # Custom endpoint (e.g., company AI gateway)
                self.client = Anthropic(
                    api_key=api_key,
                    base_url=custom_base_url
                )
                self.model = os.getenv('ANTHROPIC_MODEL', 'claude-3-5-sonnet-20241022')
                logger.info(f"Using custom endpoint: {custom_base_url}")
                logger.info(f"Model: {self.model}")

            else:
                # Direct Anthropic API
                self.client = Anthropic(api_key=api_key)
                self.model = "claude-3-5-sonnet-20241022"
                logger.info(f"Using direct Anthropic API")

        # Load research
        self.research_loader = ResearchLoader()
        research_success = self.research_loader.load()
        if not research_success:
            logger.warning(f"Research loading had errors: {self.research_loader.errors}")

        # Metadata tracking
        self.metadata_writer = MetadataWriter(str(self.output_dir))
        self.batches_processed = 0
        self.personas_analyzed = 0
        self.segments_analyzed = 0

        # Data
        self.data = None
        self.gong_metadata = None

        # Load persona contexts from updated_personas.json
        self.persona_contexts = self._load_persona_contexts()

    def _load_persona_contexts(self) -> Dict:
        """
        Load persona context from updated_personas.json.
        Returns dict keyed by (segment, persona_name) tuple.
        """
        persona_contexts = {}
        personas_file = Path(__file__).parent / 'data' / 'updated_personas.json'

        if not personas_file.exists():
            logger.warning(f"Persona contexts file not found: {personas_file}")
            logger.warning("Will proceed without persona context in prompts")
            return persona_contexts

        try:
            with open(personas_file, 'r') as f:
                personas_data = json.load(f)

            # Extract context fields for each persona
            for segment, personas in personas_data.items():
                for persona_name, persona_data in personas.items():
                    key = (segment, persona_name)
                    persona_contexts[key] = {
                        'job_titles': persona_data.get('job_titles', []),
                        'role_in_deal': persona_data.get('role_in_deal', 'Unknown'),
                        'reports_to': persona_data.get('reports_to', 'Unknown'),
                        'team_size': persona_data.get('team_size', 'Unknown')
                    }

            logger.info(f"Loaded context for {len(persona_contexts)} personas from {personas_file}")

        except Exception as e:
            logger.warning(f"Error loading persona contexts: {e}")
            logger.warning("Will proceed without persona context in prompts")

        return persona_contexts

    def _infer_reports_to(self, job_titles: List[str]) -> str:
        """
        Infer reports_to field from job titles using seniority lookup.

        Args:
            job_titles: List of job title strings

        Returns:
            String indicating who this persona reports to
        """
        import re

        # Lookup table for reports_to inference
        # Check for most senior level first
        c_suite_patterns = [
            r'\bCEO\b', r'\bCOO\b', r'\bCFO\b', r'\bCTO\b', r'\bCPO\b',
            r'\bPresident\b', r'\bChief\b'
        ]

        vp_patterns = [
            r'\bVP\b', r'\bVice President\b', r'\bSVP\b', r'\bEVP\b'
        ]

        director_patterns = [
            r'\bDirector\b', r'\bSr\.?\s*Director\b', r'\bSenior Director\b'
        ]

        manager_ic_patterns = [
            r'\bManager\b', r'\bLead\b', r'\bSpecialist\b', r'\bAnalyst\b',
            r'\bAgent\b', r'\bEngineer\b', r'\bCoordinator\b', r'\bRep\b'
        ]

        # Determine highest seniority level present
        has_c_suite = False
        has_vp = False
        has_director = False
        has_manager_ic = False

        for title in job_titles:
            if any(re.search(pattern, title, re.IGNORECASE) for pattern in c_suite_patterns):
                has_c_suite = True
            elif any(re.search(pattern, title, re.IGNORECASE) for pattern in vp_patterns):
                has_vp = True
            elif any(re.search(pattern, title, re.IGNORECASE) for pattern in director_patterns):
                has_director = True
            elif any(re.search(pattern, title, re.IGNORECASE) for pattern in manager_ic_patterns):
                has_manager_ic = True

        # Return reports_to based on most senior level
        if has_c_suite:
            return "Board or CEO"
        elif has_vp:
            return "C-Suite"
        elif has_director:
            return "VP"
        elif has_manager_ic:
            return "Director or VP"
        else:
            return "Unknown"

    def generate_profile_overview_fields(self, segment: str, persona: str) -> Dict:
        """
        Generate Profile Overview fields (job_titles, prevalence, reports_to) from Gong data.

        Args:
            segment: Segment name (Digital, SMB, Commercial, Enterprise)
            persona: Persona name (e.g., 'CX Champion', 'Support Agent')

        Returns:
            Dict with job_titles, prevalence, reports_to
        """
        logger.info(f"Generating Profile Overview for {segment} - {persona}")

        # Filter data for this segment and persona
        segment_data = self.data[self.data['SEGMENT'] == segment]
        persona_data = self.data[
            (self.data['SEGMENT'] == segment) &
            (self.data['PERSONA'] == persona)
        ]

        # Extract job titles with frequency count
        raw_titles = persona_data['CONTACT_TITLE'].dropna().tolist()

        # Normalize titles using existing normalization (basic cleanup)
        normalized_titles = []
        for title in raw_titles:
            # Strip whitespace
            title = str(title).strip()
            if title and title.lower() != 'nan':
                normalized_titles.append(title)

        # Count frequency of each title and get top 10 most frequent
        from collections import Counter
        title_counts = Counter(normalized_titles)
        top_titles = [title for title, count in title_counts.most_common(10)]
        job_titles = top_titles

        # Calculate prevalence
        total_deals = segment_data['CONVERSATION_KEY'].nunique()
        persona_deals = persona_data['CONVERSATION_KEY'].nunique()

        if total_deals > 0:
            prevalence_pct = round((persona_deals / total_deals) * 100)
            prevalence = f"{prevalence_pct}% of {segment} deals"
        else:
            prevalence = "Unknown"

        # Infer reports_to from job titles
        reports_to = self._infer_reports_to(job_titles)

        logger.info(f"  Job titles: {len(job_titles)} unique titles")
        logger.info(f"  Prevalence: {prevalence}")
        logger.info(f"  Reports to: {reports_to}")

        return {
            'job_titles': job_titles,
            'prevalence': prevalence,
            'reports_to': reports_to
        }

    def write_profile_overview_to_personas(self, profile_data: Dict[Tuple[str, str], Dict]):
        """
        Write generated Profile Overview fields back to updated_personas.json.

        Args:
            profile_data: Dict mapping (segment, persona) tuples to profile field dicts
        """
        personas_file = Path(__file__).parent / 'data' / 'updated_personas.json'

        if not personas_file.exists():
            logger.warning(f"updated_personas.json not found at {personas_file}")
            logger.warning("Skipping Profile Overview write-back")
            return

        try:
            # Load existing personas
            with open(personas_file, 'r') as f:
                personas_data = json.load(f)

            # Track updates
            updated_count = 0
            skipped_count = 0

            # Write back generated fields
            for (segment, persona), fields in profile_data.items():
                if segment not in personas_data:
                    logger.warning(f"Segment '{segment}' not found in updated_personas.json")
                    skipped_count += 1
                    continue

                if persona not in personas_data[segment]:
                    logger.warning(f"Persona '{persona}' not found in {segment} segment")
                    skipped_count += 1
                    continue

                # Only overwrite these three fields
                personas_data[segment][persona]['job_titles'] = fields['job_titles']
                personas_data[segment][persona]['prevalence'] = fields['prevalence']
                personas_data[segment][persona]['reports_to'] = fields['reports_to']

                updated_count += 1
                logger.info(f"  Updated {segment} - {persona}")

            # Write back to file
            with open(personas_file, 'w') as f:
                json.dump(personas_data, f, indent=2)

            logger.info(f"✓ Profile Overview write-back complete: {updated_count} updated, {skipped_count} skipped")

        except Exception as e:
            logger.error(f"Error writing Profile Overview fields: {e}")
            raise

    def load_and_filter_data(self):
        """Load Gong CSV and apply pre-filtering."""
        logger.info(f"Loading data from {self.gong_csv_path}")

        self.data = pd.read_csv(self.gong_csv_path)
        total_rows = len(self.data)
        logger.info(f"Loaded {total_rows:,} rows")

        # Calculate Gong metadata for tracking
        self._extract_gong_metadata()

        # Filter: English only (not Italian)
        initial_count = len(self.data)
        self.data = self.data[self.data.apply(self._is_english_row, axis=1)]
        logger.info(f"After English filter: {len(self.data):,} rows ({initial_count - len(self.data):,} filtered)")

        # Filter: Not rep speech
        initial_count = len(self.data)
        # Assume rep speech is identified by SPEAKER_NAME matching Zendesk employees
        # For now, keep rows where we have CONTACT_TITLE (customer speakers)
        self.data = self.data[self.data['CONTACT_TITLE'].notna()]
        logger.info(f"After customer-only filter: {len(self.data):,} rows ({initial_count - len(self.data):,} filtered)")

        # Assign personas based on job titles
        self.data['PERSONA'] = self.data['CONTACT_TITLE'].apply(self._assign_persona)

        # Filter out unclassified
        initial_count = len(self.data)
        self.data = self.data[self.data['PERSONA'] != 'Unclassified']
        logger.info(f"After persona assignment: {len(self.data):,} rows ({initial_count - len(self.data):,} unclassified)")

        # Show distribution
        logger.info("\nData distribution:")
        for segment in ['Digital', 'SMB', 'Commercial', 'Enterprise']:
            seg_data = self.data[self.data['SEGMENT'] == segment]
            if len(seg_data) > 0:
                logger.info(f"  {segment}: {len(seg_data):,} rows")
                for persona in self.SEGMENT_PERSONAS[segment]:
                    persona_count = len(seg_data[seg_data['PERSONA'] == persona])
                    if persona_count > 0:
                        logger.info(f"    - {persona}: {persona_count:,}")

    def _extract_gong_metadata(self):
        """Extract metadata about Gong data for tracking."""
        # Date range
        self.data['CALL_DATE'] = pd.to_datetime(self.data['CALL_DATE'], format='mixed')
        min_date = self.data['CALL_DATE'].min().strftime('%Y-%m-%d')
        max_date = self.data['CALL_DATE'].max().strftime('%Y-%m-%d')

        # Counts
        calls_analyzed = len(self.data)

        # Coverage percentages
        has_transcript = self.data['CALL_SPOTLIGHT_KEY_POINTS'].notna().sum()
        has_title = self.data['CALL_TITLE'].notna().sum()

        transcript_coverage = (has_transcript / calls_analyzed * 100) if calls_analyzed > 0 else 0
        title_coverage = (has_title / calls_analyzed * 100) if calls_analyzed > 0 else 0

        self.gong_metadata = {
            'calls_analyzed': calls_analyzed,
            'date_range': (min_date, max_date),
            'transcript_coverage_pct': transcript_coverage,
            'title_coverage_pct': title_coverage,
            'extraction_date': datetime.now().strftime('%Y-%m-%d')
        }

    def _is_english_row(self, row) -> bool:
        """Check if row contains English text (not Italian or German)."""
        import re

        # Filter out rows with no transcript data
        brief = row.get('CALL_SPOTLIGHT_BRIEF')
        key_points = row.get('CALL_SPOTLIGHT_KEY_POINTS')

        if pd.isna(brief) and pd.isna(key_points):
            return False

        # Check CALL_SPOTLIGHT_BRIEF and KEY_POINTS
        texts = [
            str(brief) if pd.notna(brief) else '',
            str(key_points) if pd.notna(key_points) else ''
        ]

        for text in texts:
            if not text or text == 'nan':
                continue

            text_lower = text.lower()

            # Check for German diacritics (ä, ö, ü, ß)
            if any(char in text for char in ['ä', 'ö', 'ü', 'ß', 'Ä', 'Ö', 'Ü']):
                return False

            # Check for German words (using word boundaries)
            german_word_count = sum(
                1 for word in self.GERMAN_WORDS
                if re.search(r'\b' + re.escape(word) + r'\b', text_lower)
            )
            if german_word_count >= 3:  # At least 3 German words
                return False

            # Check for Italian words (using word boundaries to prevent false positives)
            italian_word_count = sum(
                1 for word in self.ITALIAN_WORDS
                if re.search(r'\b' + re.escape(word) + r'\b', text_lower)
            )
            if italian_word_count >= 2:  # At least 2 Italian words (prevents single false positives)
                return False

            # Check for Italian suffixes
            if re.search(r'\b\w+zione\b', text_lower):  # integrazione, automazione
                return False
            if re.search(r'\b\w+ità\b', text_lower):  # necessità, funzionalità
                return False
            if re.search(r'\b\w+mente\b', text_lower):  # chiaramente, direttamente
                return False

        return True

    def _assign_persona(self, job_title: str) -> str:
        """Assign persona based on job title."""
        import re

        if pd.isna(job_title):
            return 'Unclassified'

        title_str = str(job_title)

        for persona_name, patterns in self.PERSONA_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, title_str, re.IGNORECASE):
                    return persona_name

        return 'Unclassified'

    def _sample_statements(self, statements: List[str], max_tokens: int = 80000) -> List[str]:
        """
        Intelligently sample statements to fit within token budget.

        Assumes ~4 chars per token. Aims for ~300-400 statements per batch.
        """
        # Rough token estimation: 4 chars per token
        total_chars = sum(len(s) for s in statements)
        estimated_tokens = total_chars / 4

        if estimated_tokens <= max_tokens:
            return statements

        # Sample proportionally
        sample_ratio = max_tokens / estimated_tokens
        sample_size = int(len(statements) * sample_ratio * 0.95)  # 95% to leave buffer

        # Take evenly distributed samples
        import numpy as np
        indices = np.linspace(0, len(statements) - 1, sample_size, dtype=int)
        sampled = [statements[i] for i in indices]

        logger.info(f"  Sampled {len(sampled)} of {len(statements)} statements (est. {estimated_tokens:.0f} -> {len(sampled) * 4:.0f} tokens)")

        return sampled

    def _call_claude_api(self, prompt: str, max_tokens: int = 4096) -> str:
        """
        Call Claude API using either custom gateway or standard client.
        Returns the response text.
        """
        if self.use_custom_gateway:
            # Zendesk AI Gateway with bearer token
            url = f"{self.gateway_endpoint}/model/{self.model}/invoke"
            headers = {
                "Authorization": f"Bearer {self.bearer_token}",
                "Content-Type": "application/json"
            }
            payload = {
                "messages": [{
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}]
                }],
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens
            }

            response = httpx.post(url, headers=headers, json=payload, timeout=180.0)
            response.raise_for_status()

            data = response.json()

            # Log stop reason if available (helps diagnose truncation)
            if 'stop_reason' in data:
                logger.debug(f"Stop reason: {data['stop_reason']}")
                if data['stop_reason'] == 'max_tokens':
                    logger.warning(f"Response hit max_tokens limit ({max_tokens}), may be truncated")

            # Bedrock response format wraps the content
            if 'content' in data and len(data['content']) > 0:
                return data['content'][0]['text']
            else:
                raise ValueError(f"Unexpected response format: {data}")
        else:
            # Standard Anthropic SDK
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=0.0,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            return response.content[0].text

    def analyze_persona_segment(
        self,
        persona: str,
        segment: str,
        max_retries: int = 3
    ) -> Optional[Dict]:
        """
        Analyze a single persona-segment combination using Claude API.

        Returns structured insights for 9 persona sections.
        """
        logger.info(f"\n{'='*80}")
        logger.info(f"Analyzing: {persona} in {segment}")
        logger.info(f"{'='*80}")

        # Check cache first (sanitize filename to remove invalid characters)
        cache_key = f"{segment}_{persona}".replace(' ', '_').replace('/', '_')
        cache_file = self.cache_dir / f"{cache_key}.json"

        if cache_file.exists():
            logger.info(f"  Using cached result from {cache_file}")
            with open(cache_file, 'r') as f:
                return json.load(f)

        # Filter data
        seg_persona_data = self.data[
            (self.data['SEGMENT'] == segment) &
            (self.data['PERSONA'] == persona)
        ]

        if len(seg_persona_data) == 0:
            logger.warning(f"  No data for {persona} in {segment}")
            return None

        logger.info(f"  Found {len(seg_persona_data):,} rows")

        # Extract statements from KEY_POINTS
        statements = []
        for _, row in seg_persona_data.iterrows():
            key_points = row.get('CALL_SPOTLIGHT_KEY_POINTS', '')
            if pd.notna(key_points):
                # Split by sentence
                points = str(key_points).split('.')
                statements.extend([p.strip() for p in points if len(p.strip()) > 20])

        logger.info(f"  Extracted {len(statements)} statements")

        if len(statements) == 0:
            logger.warning(f"  No statements found for {persona} in {segment}")
            return None

        # Sample to fit token budget
        sampled_statements = self._sample_statements(statements)

        # Load research for this persona and segment
        research_sources = self.research_loader.get_research_for(
            persona=persona,
            segment=segment
        )

        logger.info(f"  Found {len(research_sources)} relevant research sources")

        # Build prompt
        prompt = self._build_persona_prompt(persona, segment, sampled_statements, research_sources)

        # Call Claude with retry logic
        for attempt in range(max_retries):
            try:
                logger.info(f"  Calling Claude API (attempt {attempt + 1}/{max_retries})...")

                response_text = self._call_claude_api(prompt, max_tokens=8192)
                self.batches_processed += 1

                # Parse response
                result = self._parse_claude_response(response_text, persona, segment)

                # Cache result
                with open(cache_file, 'w') as f:
                    json.dump(result, f, indent=2)

                logger.info(f"  ✓ Analysis complete, cached to {cache_file}")

                return result

            except RateLimitError as e:
                wait_time = 60 * (attempt + 1)
                logger.warning(f"  Rate limit hit, waiting {wait_time}s before retry...")
                time.sleep(wait_time)

            except APIError as e:
                logger.error(f"  API error: {e}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(10 * (attempt + 1))

            except httpx.HTTPStatusError as e:
                if e.response.status_code >= 500:
                    # Server error - retry with backoff
                    wait_time = 10 * (attempt + 1)
                    logger.warning(f"  Server error (500), waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                else:
                    # Client error (4xx) - don't retry
                    logger.error(f"  HTTP error: {e}")
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(5)

            except httpx.ReadTimeout as e:
                # Timeout - retry with backoff
                wait_time = 5 * (attempt + 1)
                logger.warning(f"  Request timed out, waiting {wait_time}s before retry...")
                time.sleep(wait_time)

        return None

    def _build_persona_prompt(
        self,
        persona: str,
        segment: str,
        statements: List[str],
        research_sources: List[Dict]
    ) -> str:
        """Build structured prompt for Claude to analyze persona."""

        # Format statements
        statements_text = "\n".join([f"- {s}" for s in statements[:400]])  # Cap at 400

        # Format research
        research_text = ""
        if research_sources:
            research_text = "\n\n## THIRD-PARTY RESEARCH (supplementary context)\n\n"
            for source in research_sources:
                research_text += f"**Source:** {source['title']} ({source['source_org']}, {source['published_date']})\n"
                for excerpt in source['excerpts']:
                    research_text += f"- {excerpt['text']}\n"
                research_text += "\n"

        # Get persona context
        context_key = (segment, persona)
        persona_context = self.persona_contexts.get(context_key)

        # Build persona context section
        persona_context_text = ""
        if persona_context:
            job_titles_str = ", ".join(persona_context['job_titles']) if persona_context['job_titles'] else "Not specified"
            persona_context_text = f"""
**Persona Context:**
- Job Titles: {job_titles_str}
- Reports To: {persona_context['reports_to']}
- Role in Deal: {persona_context['role_in_deal']}
- Team Size: {persona_context['team_size']}

Use this context to ensure your analysis reflects the specific perspective, priorities, and decision-making authority of this persona. A CFO has different success metrics than a CX Champion even when they appear in the same deals.
"""

        prompt = f"""You are analyzing customer conversations from Gong (sales call transcripts) to extract buyer persona insights.

**Persona:** {persona}
**Segment:** {segment}
**Data:** {len(statements)} customer statements extracted from real sales calls
{persona_context_text}
Your task: Analyze these statements and produce structured insights for this persona in JSON format.

---

## CUSTOMER STATEMENTS (from Gong transcripts)

{statements_text}

{research_text}

---

## OUTPUT FORMAT

Return ONLY valid JSON with this exact structure:

{{
  "pain_points": [
    {{
      "theme": "Brief theme name (2-5 words)",
      "description": "1-2 sentence explanation of this pain point",
      "frequency": "high|medium|low",
      "example_quote": "Direct quote from statements above"
    }}
  ],
  "goals": [
    {{
      "theme": "Brief theme name",
      "description": "What they want to achieve",
      "frequency": "high|medium|low",
      "example_quote": "Direct quote"
    }}
  ],
  "objections": [
    {{
      "objection": "The concern or hesitation",
      "type": "risk|cost|timing|capability|fit",
      "frequency": "high|medium|low",
      "example_quote": "Direct quote"
    }}
  ],
  "success_metrics": [
    {{
      "metric": "Canonical metric name (e.g., CSAT, NPS, First Response Time)",
      "importance": "high|medium|low",
      "context": "Why this metric matters to them"
    }}
  ],
  "key_messages_to_land": [
    {{
      "message": "Thematic message or concept that should land (e.g., 'AI amplifies what great agents already do')",
      "rationale": "Why this resonates based on pains/goals above"
    }}
  ],
  "product_requirements": [
    {{
      "requirement": "What they need the product to do",
      "priority": "must-have|important|nice-to-have",
      "example_quote": "Direct quote"
    }}
  ],
  "information_sources": [
    {{
      "source": "Where they research (e.g., G2, Gartner, peer recommendations)",
      "frequency": "high|medium|low",
      "notes": "How they use this source"
    }}
  ],
  "messaging_preferences": [
    {{
      "preference": "How they like to communicate or receive information",
      "example_quote": "Direct quote"
    }}
  ],
  "competitive_landscape": [
    {{
      "competitor": "Competitor name mentioned",
      "context": "What was said about them",
      "sentiment": "positive|negative|neutral"
    }}
  ]
}}

## IMPORTANT INSTRUCTIONS

1. **Prioritize Gong data over research** - The customer statements are ground truth. Use research only to fill gaps or validate patterns.
2. **Extract themes, don't invent them** - Every theme should be directly supported by the statements above.
3. **Use actual quotes** - example_quote fields must be verbatim from the statements.
4. **Be specific** - "Slow response times" not "Speed issues". "Can't integrate with Salesforce" not "Integration challenges".
5. **Focus on signal strength** - Mark high frequency only when 5+ statements support it, medium for 2-4, low for 1.
6. **For key messages** - These are thematic concepts, NOT statistics or percentages. Do not include numerical claims like "47% of agents report faster resolution". Instead articulate beliefs and values like "AI amplifies what great agents already do — it doesn't replace their judgment."
7. **Return ONLY the JSON** - No preamble, no markdown fences, no explanation. Just pure JSON.

## PERSONA-SPECIFIC DIFFERENTIATION (CRITICAL)

**Success Metrics**: Generate metrics specific to this persona's role and decision-making authority. A budget holder cares about cost-per-ticket and ROI. A hands-on practitioner cares about agent efficiency and workflow automation. Do not generate generic segment-wide metrics.

**Product Requirements**: Generate requirements that reflect this persona's specific workflow, technical access level, and priorities. Do not copy requirements that apply to all roles equally.

**Information Sources**: Generate sources that reflect where someone in this specific role at this seniority level would actually conduct research. A C-Suite executive reads analyst reports. A hands-on manager reads product documentation and community forums.

**Messaging Preferences**: Generate preferences specific to how someone in this role receives and processes information, not generic B2B buyer preferences. A CFO wants executive summaries. A technical practitioner wants detailed specs.

Analyze now."""

        return prompt

    def _parse_claude_response(self, response_text: str, persona: str, segment: str) -> Dict:
        """Parse Claude's JSON response and add metadata."""
        # Strip markdown fences if present
        response_text = response_text.strip()
        if response_text.startswith('```'):
            lines = response_text.split('\n')
            response_text = '\n'.join(lines[1:-1])

        # Parse JSON
        try:
            insights = json.loads(response_text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Claude response as JSON: {e}")
            logger.error(f"Response text: {response_text[:500]}")

            # Check if response was truncated (common issue)
            if len(response_text) > 15000 and not response_text.rstrip().endswith('}'):
                logger.error("Response appears truncated - increase max_tokens or reduce input")

            raise

        # Add metadata
        insights['_metadata'] = {
            'persona': persona,
            'segment': segment,
            'model': self.model,
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'batch_id': self.batches_processed
        }

        return insights

    def analyze_segment_level(self, segment: str) -> Optional[Dict]:
        """
        Analyze segment-level insights (cross-persona).

        Extracts:
        - Messaging dos and don'ts
        - Competitive landscape patterns
        """
        logger.info(f"\n{'='*80}")
        logger.info(f"Analyzing segment-level insights: {segment}")
        logger.info(f"{'='*80}")

        # Check cache
        cache_file = self.cache_dir / f"segment_{segment}.json"
        if cache_file.exists():
            logger.info(f"  Using cached result from {cache_file}")
            with open(cache_file, 'r') as f:
                return json.load(f)

        # Get all data for this segment
        seg_data = self.data[self.data['SEGMENT'] == segment]

        if len(seg_data) == 0:
            logger.warning(f"  No data for {segment}")
            return None

        logger.info(f"  Found {len(seg_data):,} rows across all personas")

        # Extract statements
        statements = []
        for _, row in seg_data.iterrows():
            key_points = row.get('CALL_SPOTLIGHT_KEY_POINTS', '')
            if pd.notna(key_points):
                points = str(key_points).split('.')
                statements.extend([p.strip() for p in points if len(p.strip()) > 20])

        logger.info(f"  Extracted {len(statements)} statements")

        # Sample
        sampled_statements = self._sample_statements(statements)

        # Load research for this segment (all personas, all sections)
        research_sources = self.research_loader.get_research_for(segment=segment)
        logger.info(f"  Found {len(research_sources)} relevant research sources")

        # Build prompt
        prompt = self._build_segment_prompt(segment, sampled_statements, research_sources)

        # Call Claude with retry logic
        for attempt in range(3):
            try:
                logger.info(f"  Calling Claude API for segment analysis (attempt {attempt + 1}/3)...")

                response_text = self._call_claude_api(prompt, max_tokens=4096)

                # Parse
                result = self._parse_segment_response(response_text, segment)

                # Cache
                with open(cache_file, 'w') as f:
                    json.dump(result, f, indent=2)

                logger.info(f"  ✓ Segment analysis complete")

                return result

            except json.JSONDecodeError as e:
                logger.error(f"  Segment analysis failed (JSON parse error): {e}")
                if attempt < 2:
                    logger.warning(f"  Retrying in 5s...")
                    time.sleep(5)
                else:
                    return None

            except Exception as e:
                logger.error(f"  Segment analysis failed: {e}")
                if attempt < 2:
                    time.sleep(5)
                else:
                    return None

        return None

    def _build_segment_prompt(
        self,
        segment: str,
        statements: List[str],
        research_sources: List[Dict]
    ) -> str:
        """Build prompt for segment-level analysis."""

        statements_text = "\n".join([f"- {s}" for s in statements[:400]])

        research_text = ""
        if research_sources:
            research_text = "\n\n## THIRD-PARTY RESEARCH\n\n"
            for source in research_sources:
                research_text += f"**{source['title']}** ({source['source_org']})\n"
                for excerpt in source['excerpts'][:2]:  # Limit excerpts
                    research_text += f"- {excerpt['text']}\n"
                research_text += "\n"

        prompt = f"""You are analyzing customer conversations to extract segment-level messaging guidance.

**Segment:** {segment}
**Data:** {len(statements)} customer statements from sales calls

Extract messaging patterns that apply across all personas in this segment.

---

## CUSTOMER STATEMENTS

{statements_text}

{research_text}

---

## OUTPUT FORMAT

Return ONLY valid JSON:

{{
  "messaging_dos_and_donts": {{
    "dos": [
      {{
        "guidance": "What messaging works well for this segment",
        "rationale": "Why this resonates"
      }}
    ],
    "donts": [
      {{
        "guidance": "What messaging to avoid",
        "rationale": "Why this backfires"
      }}
    ]
  }},
  "competitive_landscape": [
    {{
      "competitor": "Competitor name",
      "mention_count": "high|medium|low",
      "common_comparisons": "What customers compare",
      "sentiment_summary": "Overall sentiment"
    }}
  ]
}}

Focus on patterns, not isolated mentions. Return ONLY JSON."""

        return prompt

    def _parse_segment_response(self, response_text: str, segment: str) -> Dict:
        """Parse segment-level response."""
        response_text = response_text.strip()
        if response_text.startswith('```'):
            lines = response_text.split('\n')
            response_text = '\n'.join(lines[1:-1])

        insights = json.loads(response_text)
        insights['_metadata'] = {
            'segment': segment,
            'model': self.model,
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        return insights

    def run_full_analysis(self):
        """Run complete persona analysis across all segments."""
        logger.info("\n" + "="*80)
        logger.info("STARTING CLAUDE-POWERED PERSONA ANALYSIS")
        logger.info("="*80)

        if self.dry_run:
            logger.info("\n⚠️  DRY RUN MODE: Processing only 1 persona from 1 segment")

        # Load data
        self.load_and_filter_data()

        # Determine segments to process
        segments = ['Digital', 'SMB', 'Commercial', 'Enterprise']
        if self.dry_run:
            segments = ['Digital']  # Just one segment

        # Generate Profile Overview fields for all personas
        logger.info("\n" + "="*80)
        logger.info("GENERATING PROFILE OVERVIEW FIELDS")
        logger.info("="*80)

        profile_overview_data = {}

        for segment in segments:
            personas = self.SEGMENT_PERSONAS[segment]

            if self.dry_run:
                personas = personas[:1]  # Just one persona

            for persona in personas:
                # Check if persona has data
                persona_data = self.data[
                    (self.data['SEGMENT'] == segment) &
                    (self.data['PERSONA'] == persona)
                ]

                if len(persona_data) == 0:
                    logger.warning(f"No data for {segment} - {persona}, skipping Profile Overview generation")
                    continue

                # Generate profile fields
                profile_fields = self.generate_profile_overview_fields(segment, persona)
                profile_overview_data[(segment, persona)] = profile_fields

        # Write back to updated_personas.json
        if profile_overview_data:
            logger.info(f"\nWriting {len(profile_overview_data)} Profile Overview updates to updated_personas.json...")
            self.write_profile_overview_to_personas(profile_overview_data)
        else:
            logger.warning("No Profile Overview data generated")

        # Persona-level analysis
        persona_insights = {}

        for segment in segments:
            personas = self.SEGMENT_PERSONAS[segment]

            if self.dry_run:
                personas = personas[:1]  # Just one persona

            for persona in personas:
                result = self.analyze_persona_segment(persona, segment)

                if result:
                    key = f"{segment}_{persona}".replace(' ', '_')
                    persona_insights[key] = result
                    self.personas_analyzed += 1

        # Segment-level analysis
        segment_insights = {}

        for segment in segments:
            result = self.analyze_segment_level(segment)
            if result:
                segment_insights[segment] = result
                self.segments_analyzed += 1

        # Write outputs
        self._write_outputs(persona_insights, segment_insights)

        # Write metadata
        self._write_metadata()

        logger.info("\n" + "="*80)
        logger.info("ANALYSIS COMPLETE")
        logger.info("="*80)
        logger.info(f"Personas analyzed: {self.personas_analyzed}")
        logger.info(f"Segments analyzed: {self.segments_analyzed}")
        logger.info(f"Batches processed: {self.batches_processed}")
        logger.info(f"\nOutputs written to:")
        logger.info(f"  - {self.output_dir / 'persona_insights_claude.json'}")
        logger.info(f"  - {self.output_dir / 'segment_insights_claude.json'}")

    def _write_outputs(self, persona_insights: Dict, segment_insights: Dict):
        """Write structured outputs to JSON files."""
        persona_output = self.output_dir / 'persona_insights_claude.json'
        segment_output = self.output_dir / 'segment_insights_claude.json'

        with open(persona_output, 'w') as f:
            json.dump(persona_insights, f, indent=2)

        with open(segment_output, 'w') as f:
            json.dump(segment_insights, f, indent=2)

        logger.info(f"\n✓ Wrote persona insights to {persona_output}")
        logger.info(f"✓ Wrote segment insights to {segment_output}")

    def _write_metadata(self):
        """Write pipeline run metadata."""
        # Write Gong metadata
        self.metadata_writer.write_gong_metadata(**self.gong_metadata)

        # Write Claude metadata
        self.metadata_writer.write_claude_metadata(
            model=self.model,
            analysis_date=datetime.now().strftime('%Y-%m-%d'),
            batches_processed=self.batches_processed,
            personas_analyzed=self.personas_analyzed,
            segments_analyzed=self.segments_analyzed
        )

        # Finalize metadata
        research_manifest = Path(__file__).parent / 'third_party_research' / 'research_manifest.json'
        self.metadata_writer.finalize_metadata(str(research_manifest))


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Claude-powered persona analyzer for Gong transcripts'
    )
    parser.add_argument(
        'gong_csv',
        help='Path to Gong extraction CSV file'
    )
    parser.add_argument(
        '--output-dir',
        default='.',
        help='Output directory (default: current directory)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Process only 1 persona from 1 segment for testing'
    )
    parser.add_argument(
        '--cache-dir',
        help='Cache directory for API responses (default: output_dir/cache)'
    )

    args = parser.parse_args()

    analyzer = ClaudeAnalyzer(
        gong_csv_path=args.gong_csv,
        output_dir=args.output_dir,
        dry_run=args.dry_run,
        cache_dir=args.cache_dir
    )

    analyzer.run_full_analysis()


if __name__ == '__main__':
    main()
