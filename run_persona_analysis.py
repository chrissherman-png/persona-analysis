"""
Orchestration script for Persona Intelligence Agent
Connects to Snowflake, runs extraction queries, and executes analysis

Date: 2026-03-25
"""

import os
import sys
import yaml
import logging
import pandas as pd
from datetime import datetime
from pathlib import Path
import snowflake.connector
from snowflake.connector import DictCursor
from dotenv import load_dotenv

# Import the persona analysis agent
from persona_intelligence_agent import PersonaIntelligenceAgent

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('./logs/persona_agent.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class PersonaAnalysisOrchestrator:
    """Orchestrates the full persona analysis pipeline."""

    def __init__(self, config_path: str = 'config.yaml'):
        """Initialize orchestrator with configuration."""
        logger.info("Initializing Persona Analysis Orchestrator")

        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # Setup directories
        self._setup_directories()

        # Snowflake connection
        self.conn = None

    def _setup_directories(self):
        """Create necessary directories if they don't exist."""
        directories = [
            'logs',
            'data',
            self.config['output']['report_dir'],
            self.config['output']['downstream_dir']
        ]

        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            logger.info(f"Ensured directory exists: {directory}")

    def connect_to_snowflake(self):
        """Establish connection to Snowflake."""
        logger.info("Connecting to Snowflake...")

        try:
            # Build connection parameters
            conn_params = {
                'account': self.config['snowflake']['account'],
                'user': self.config['snowflake']['user'],
                'warehouse': self.config['snowflake']['warehouse'],
                'database': self.config['snowflake']['database'],
                'schema': self.config['snowflake']['schema'],
                'role': self.config['snowflake']['role']
            }

            # Check if SSO authentication is configured
            if 'authenticator' in self.config['snowflake']:
                conn_params['authenticator'] = self.config['snowflake']['authenticator']
                logger.info(f"Using SSO authentication: {conn_params['authenticator']}")
                if conn_params['authenticator'] == 'externalbrowser':
                    logger.info("A browser window will open for SSO authentication...")
            else:
                # Use password-based authentication
                password = os.getenv('SNOWFLAKE_PASSWORD')
                if not password:
                    logger.error("SNOWFLAKE_PASSWORD not found in environment")
                    return False
                conn_params['password'] = password

            self.conn = snowflake.connector.connect(**conn_params)

            logger.info("Successfully connected to Snowflake")
            return True

        except Exception as e:
            logger.error(f"Failed to connect to Snowflake: {e}")
            return False

    def run_exploratory_query(self, limit: int = 10) -> pd.DataFrame:
        """
        Run exploratory query to identify CRM field names.
        This should be run FIRST to identify actual field names in your CRM.
        """
        logger.info("Running exploratory query to identify CRM fields...")

        try:
            # Load exploratory SQL
            sql_file = '../sql_queries/01_exploratory_sample.sql'

            if not os.path.exists(sql_file):
                logger.error(f"Exploratory SQL file not found: {sql_file}")
                return None

            with open(sql_file, 'r') as f:
                sql_query = f.read()

            # Replace LIMIT if needed
            if 'LIMIT' in sql_query:
                sql_query = sql_query.replace('LIMIT 10', f'LIMIT {limit}')

            logger.info(f"Executing exploratory query (limit {limit})...")

            # Execute query
            df = pd.read_sql(sql_query, self.conn)

            logger.info(f"Retrieved {len(df)} sample records")

            # Save sample data
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"./data/exploratory_sample_{timestamp}.csv"

            df.to_csv(output_file, index=False)
            logger.info(f"Saved sample data to: {output_file}")

            # Analyze and display field names found
            self._analyze_json_fields(df)

            return df

        except Exception as e:
            logger.error(f"Error running exploratory query: {e}")
            raise

    def _analyze_json_fields(self, df: pd.DataFrame):
        """Analyze JSON fields from exploratory query to help identify field names."""
        logger.info("\n" + "=" * 80)
        logger.info("JSON FIELD ANALYSIS")
        logger.info("=" * 80)

        # Analyze participant CRM snapshot
        if 'PARTICIPANT_CRM_SNAPSHOT' in df.columns:
            logger.info("\n📋 PARTICIPANT (Contact/Lead) Fields Found:")
            sample = df['PARTICIPANT_CRM_SNAPSHOT'].dropna().iloc[0] if len(df['PARTICIPANT_CRM_SNAPSHOT'].dropna()) > 0 else None

            if sample:
                try:
                    import json
                    fields = json.loads(sample)
                    for key in sorted(fields.keys()):
                        logger.info(f"  - {key}")
                except:
                    logger.warning("  Could not parse participant JSON")

        # Analyze account snapshot
        if 'ACCOUNT_SNAPSHOT' in df.columns:
            logger.info("\n🏢 ACCOUNT Fields Found:")
            sample = df['ACCOUNT_SNAPSHOT'].dropna().iloc[0] if len(df['ACCOUNT_SNAPSHOT'].dropna()) > 0 else None

            if sample:
                try:
                    import json
                    fields = json.loads(sample)
                    for key in sorted(fields.keys()):
                        logger.info(f"  - {key}")

                    # Highlight key fields
                    logger.info("\n  ⚠️  Key fields to configure in config.yaml:")
                    if 'NumberOfEmployees' in fields:
                        logger.info(f"     employee_count: 'NumberOfEmployees'")
                    else:
                        logger.info("     employee_count: <FIND EMPLOYEE COUNT FIELD ABOVE>")

                    if 'Industry' in fields:
                        logger.info(f"     industry: 'Industry'")

                except:
                    logger.warning("  Could not parse account JSON")

        # Analyze opportunity snapshot
        if 'OPPORTUNITY_SNAPSHOT' in df.columns:
            logger.info("\n💼 OPPORTUNITY Fields Found:")
            sample = df['OPPORTUNITY_SNAPSHOT'].dropna().iloc[0] if len(df['OPPORTUNITY_SNAPSHOT'].dropna()) > 0 else None

            if sample:
                try:
                    import json
                    fields = json.loads(sample)
                    for key in sorted(fields.keys()):
                        logger.info(f"  - {key}")

                    # Highlight key fields
                    logger.info("\n  ⚠️  Key fields to configure in config.yaml:")
                    if 'StageName' in fields:
                        logger.info(f"     stage: 'StageName'")
                    if 'Type' in fields:
                        logger.info(f"     type: 'Type'")

                except:
                    logger.warning("  Could not parse opportunity JSON")

        logger.info("\n" + "=" * 80)
        logger.info("✓ Analysis complete. Update config.yaml with these field names.")
        logger.info("=" * 80 + "\n")

    def run_data_quality_checks(self) -> dict:
        """
        Run data quality checks from 03_data_quality_checks.sql
        Returns dict with quality metrics
        """
        logger.info("Running data quality checks...")

        quality_results = {}

        try:
            # Load data quality SQL
            with open('../sql_queries/03_data_quality_checks.sql', 'r') as f:
                sql_script = f.read()

            # Split into individual queries (separated by CHECK comments)
            queries = self._split_quality_checks(sql_script)

            cursor = self.conn.cursor(DictCursor)

            for check_name, query in queries.items():
                logger.info(f"Running check: {check_name}")

                try:
                    cursor.execute(query)
                    results = cursor.fetchall()

                    quality_results[check_name] = results
                    logger.info(f"  ✓ {check_name} completed")

                except Exception as e:
                    logger.error(f"  ✗ {check_name} failed: {e}")
                    quality_results[check_name] = {'error': str(e)}

            cursor.close()

            # Evaluate quality issues
            issues = self._evaluate_quality_results(quality_results)

            if issues:
                logger.warning("Data Quality Issues Found:")
                for issue in issues:
                    logger.warning(f"  - {issue}")
            else:
                logger.info("✓ All data quality checks passed")

            return quality_results

        except Exception as e:
            logger.error(f"Error running data quality checks: {e}")
            return {}

    def _split_quality_checks(self, sql_script: str) -> dict:
        """Split SQL script into individual named checks."""
        checks = {}

        # Split by CHECK comments
        sections = sql_script.split('-- =============================================================================\n-- CHECK')

        for section in sections[1:]:  # Skip first section (header)
            lines = section.split('\n')

            # Extract check name from first line
            check_name = 'Unknown'
            if lines and ':' in lines[0]:
                check_name = lines[0].split(':', 1)[1].strip()

            # Find the SELECT statement and extract full query
            query_lines = []
            in_query = False
            paren_count = 0

            for line in lines:
                # Start capturing when we hit SELECT
                if not in_query and line.strip().upper().startswith('SELECT'):
                    in_query = True

                if in_query:
                    # Track parentheses to handle subqueries
                    paren_count += line.count('(') - line.count(')')
                    query_lines.append(line)

                    # Stop at semicolon when parentheses are balanced
                    if ';' in line and paren_count == 0:
                        break

                    # Stop if we hit another CHECK section or major delimiter
                    if line.strip().startswith('-- ===========') and len(query_lines) > 1:
                        query_lines.pop()  # Remove the delimiter line
                        break

            query = '\n'.join(query_lines).strip().rstrip(';')

            # Only add if we have a valid query
            if query and 'SELECT' in query.upper():
                checks[check_name] = query
                logger.debug(f"Parsed check: {check_name}")

        return checks

    def _evaluate_quality_results(self, results: dict) -> list:
        """Evaluate quality check results and return list of issues."""
        issues = []

        # Check 1: Employee Count Coverage
        if 'Employee Count Coverage' in results:
            data = results['Employee Count Coverage']
            if data and isinstance(data, list) and len(data) > 0:
                pct_missing = data[0].get('PCT_MISSING', 0)
                if pct_missing > 20:
                    issues.append(
                        f"Employee count missing for {pct_missing:.1f}% of conversations (threshold: 20%)"
                    )

        # Check 3: Job Title Coverage
        if 'Job Title Coverage' in results:
            data = results['Job Title Coverage']
            if data and isinstance(data, list) and len(data) > 0:
                pct_missing = data[0].get('PCT_MISSING', 0)
                if pct_missing > 20:
                    issues.append(
                        f"Job titles missing for {pct_missing:.1f}% of participants (threshold: 20%)"
                    )

        # Check 2: Segment Distribution - check for sufficient volume
        if 'Segment Distribution' in results:
            segments = results['Segment Distribution']
            if isinstance(segments, list):
                smb_count = next((s['CONVERSATION_COUNT'] for s in segments
                                 if s.get('SEGMENT') == 'SMB'), 0)
                commercial_count = next((s['CONVERSATION_COUNT'] for s in segments
                                        if s.get('SEGMENT') == 'Commercial'), 0)

                if smb_count < 100:
                    issues.append(f"Low SMB volume: {smb_count} conversations (target: 100+)")

                if commercial_count < 100:
                    issues.append(f"Low Commercial volume: {commercial_count} conversations (target: 100+)")

        return issues

    def run_main_extraction(self) -> pd.DataFrame:
        """
        Run main data extraction query from 02_main_extraction.sql
        Returns DataFrame with extracted data
        """
        logger.info("Running main data extraction...")

        try:
            # Load SQL query
            with open('../sql_queries/02_main_extraction.sql', 'r') as f:
                sql_query = f.read()

            # Customize query with config field mappings
            sql_query = self._customize_sql_fields(sql_query)

            logger.info("Executing main extraction query...")

            # Execute query
            df = pd.read_sql(sql_query, self.conn)

            logger.info(f"Extracted {len(df)} rows")

            # Save raw data
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"./data/persona_data_{timestamp}.csv"

            df.to_csv(output_file, index=False)
            logger.info(f"Saved raw data to: {output_file}")

            return df, output_file

        except Exception as e:
            logger.error(f"Error running main extraction: {e}")
            raise

    def _customize_sql_fields(self, sql_query: str) -> str:
        """
        Replace JSON field names in SQL with values from config.
        This handles different CRM field naming conventions.
        """
        field_mappings = self.config['extraction']['crm_fields']

        logger.info("Customizing SQL with CRM field mappings...")

        # Account fields
        if 'account' in field_mappings:
            account_fields = field_mappings['account']

            # Employee count - most critical for segmentation
            if 'employee_count' in account_fields:
                sql_query = sql_query.replace(
                    ':NumberOfEmployees',
                    f":{account_fields['employee_count']}"
                )
                logger.debug(f"  Employee count field: {account_fields['employee_count']}")

            # Industry
            if 'industry' in account_fields:
                sql_query = sql_query.replace(
                    ':Industry',
                    f":{account_fields['industry']}"
                )
                logger.debug(f"  Industry field: {account_fields['industry']}")

            # Account name
            if 'name' in account_fields:
                sql_query = sql_query.replace(
                    ':Name::STRING as account_name',
                    f":{account_fields['name']}::STRING as account_name"
                )

        # Opportunity fields
        if 'opportunity' in field_mappings:
            opp_fields = field_mappings['opportunity']

            if 'stage' in opp_fields:
                sql_query = sql_query.replace(
                    ':StageName',
                    f":{opp_fields['stage']}"
                )
                logger.debug(f"  Stage field: {opp_fields['stage']}")

            if 'type' in opp_fields:
                sql_query = sql_query.replace(
                    ':Type',
                    f":{opp_fields['type']}"
                )
                logger.debug(f"  Opportunity type field: {opp_fields['type']}")

            if 'amount' in opp_fields:
                sql_query = sql_query.replace(
                    ':Amount',
                    f":{opp_fields['amount']}"
                )

            if 'is_closed' in opp_fields:
                sql_query = sql_query.replace(
                    ':IsClosed',
                    f":{opp_fields['is_closed']}"
                )

            if 'is_won' in opp_fields:
                sql_query = sql_query.replace(
                    ':IsWon',
                    f":{opp_fields['is_won']}"
                )

            if 'close_date' in opp_fields:
                sql_query = sql_query.replace(
                    ':CloseDate',
                    f":{opp_fields['close_date']}"
                )

        # Contact/Lead fields
        if 'contact' in field_mappings:
            contact_fields = field_mappings['contact']

            if 'title' in contact_fields:
                sql_query = sql_query.replace(
                    ':Title',
                    f":{contact_fields['title']}"
                )
                logger.debug(f"  Title field: {contact_fields['title']}")

            if 'department' in contact_fields:
                sql_query = sql_query.replace(
                    ':Department',
                    f":{contact_fields['department']}"
                )

        logger.info("✓ Field customization complete")

        return sql_query

    def run_analysis(self, data_file: str) -> dict:
        """
        Run persona analysis using the PersonaIntelligenceAgent.
        """
        logger.info("Starting persona analysis...")

        try:
            agent = PersonaIntelligenceAgent(data_file)
            results = agent.run_full_analysis()

            logger.info("Persona analysis complete")

            return results

        except Exception as e:
            logger.error(f"Error running analysis: {e}")
            raise

    def archive_previous_reports(self):
        """Archive previous reports if configured."""
        if not self.config['output']['archive_previous']:
            return

        logger.info("Archiving previous reports...")

        archive_dir = Path('./archive') / datetime.now().strftime('%Y%m%d_%H%M%S')
        archive_dir.mkdir(parents=True, exist_ok=True)

        # Move files from report_dir to archive
        report_dir = Path(self.config['output']['report_dir'])

        if report_dir.exists():
            for file in report_dir.glob('*.md'):
                file.rename(archive_dir / file.name)
                logger.info(f"  Archived: {file.name}")

    def run_full_pipeline(self):
        """
        Execute the complete persona analysis pipeline:
        1. Connect to Snowflake
        2. Run data quality checks
        3. Run main extraction
        4. Execute persona analysis
        5. Generate reports and downstream inputs
        """
        logger.info("=" * 80)
        logger.info("STARTING PERSONA INTELLIGENCE AGENT PIPELINE")
        logger.info("=" * 80)

        try:
            # Step 1: Connect to Snowflake
            if not self.connect_to_snowflake():
                logger.error("Failed to connect to Snowflake. Aborting.")
                return False

            # Step 2: Run data quality checks
            quality_results = self.run_data_quality_checks()

            # Step 3: Archive previous reports
            self.archive_previous_reports()

            # Step 4: Run main extraction
            df, data_file = self.run_main_extraction()

            # Step 5: Run persona analysis
            results = self.run_analysis(data_file)

            # Step 6: Generate summary
            self._generate_summary(results, quality_results)

            logger.info("=" * 80)
            logger.info("PIPELINE COMPLETED SUCCESSFULLY")
            logger.info("=" * 80)

            return True

        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            return False

        finally:
            # Close Snowflake connection
            if self.conn:
                self.conn.close()
                logger.info("Closed Snowflake connection")

    def _generate_summary(self, analysis_results: dict, quality_results: dict):
        """Generate a summary report of the analysis run."""
        logger.info("Generating summary report...")

        summary = f"""
# Persona Intelligence Agent - Run Summary
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Data Quality Summary
"""

        # Add quality check results
        if quality_results:
            summary += "\n### Quality Checks:\n"
            for check_name, results in quality_results.items():
                if isinstance(results, dict) and 'error' in results:
                    summary += f"- ✗ {check_name}: FAILED\n"
                else:
                    summary += f"- ✓ {check_name}: PASSED\n"

        # Add analysis results summary
        summary += "\n## Analysis Results\n"

        for segment, personas in analysis_results.items():
            summary += f"\n### {segment}\n"

            for persona, insights in personas.items():
                if insights.get('status') == 'INSUFFICIENT_DATA':
                    summary += f"- {persona}: INSUFFICIENT DATA\n"
                else:
                    summary += (
                        f"- {persona}: {insights['total_signals']} signals, "
                        f"{insights['unique_people']} people, "
                        f"{insights['recency']['pct_current']:.1f}% current\n"
                    )

        # Save summary
        summary_file = f"{self.config['output']['report_dir']}/run_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        with open(summary_file, 'w') as f:
            f.write(summary)

        logger.info(f"Summary saved to: {summary_file}")


def main():
    """Main execution function."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Persona Intelligence Agent - Automated buyer persona validation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # First time: Identify CRM field names
  python run_persona_analysis.py --explore

  # Run data quality checks only
  python run_persona_analysis.py --quality-check

  # Run full analysis (default)
  python run_persona_analysis.py

  # Run full analysis with custom config
  python run_persona_analysis.py --config custom_config.yaml
        """
    )

    parser.add_argument(
        '--explore',
        action='store_true',
        help='Run exploratory query to identify CRM field names (run this first!)'
    )

    parser.add_argument(
        '--quality-check',
        action='store_true',
        help='Run data quality checks only (no full analysis)'
    )

    parser.add_argument(
        '--config',
        type=str,
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )

    parser.add_argument(
        '--sample-limit',
        type=int,
        default=10,
        help='Number of records to retrieve in exploratory mode (default: 10)'
    )

    args = parser.parse_args()

    # Create logs directory if it doesn't exist
    Path('./logs').mkdir(exist_ok=True)

    # Initialize orchestrator
    orchestrator = PersonaAnalysisOrchestrator(config_path=args.config)

    # Connect to Snowflake
    if not orchestrator.connect_to_snowflake():
        logger.error("Failed to connect to Snowflake. Check your credentials in .env")
        sys.exit(1)

    try:
        # Mode: Exploratory
        if args.explore:
            logger.info("=" * 80)
            logger.info("EXPLORATORY MODE: Identifying CRM Field Names")
            logger.info("=" * 80)

            df = orchestrator.run_exploratory_query(limit=args.sample_limit)

            if df is not None:
                logger.info("\n✓ Exploratory query complete!")
                logger.info("\nNext steps:")
                logger.info("1. Review the JSON fields listed above")
                logger.info("2. Update config.yaml with your actual field names")
                logger.info("3. Run full analysis: python run_persona_analysis.py")
                sys.exit(0)
            else:
                sys.exit(1)

        # Mode: Quality Check Only
        elif args.quality_check:
            logger.info("=" * 80)
            logger.info("QUALITY CHECK MODE")
            logger.info("=" * 80)

            quality_results = orchestrator.run_data_quality_checks()

            if quality_results:
                logger.info("\n✓ Quality checks complete!")
                logger.info("\nNext steps:")
                logger.info("- Review any warnings above")
                logger.info("- If quality looks good, run full analysis: python run_persona_analysis.py")
                sys.exit(0)
            else:
                sys.exit(1)

        # Mode: Full Analysis (default)
        else:
            success = orchestrator.run_full_pipeline()
            sys.exit(0 if success else 1)

    finally:
        # Close connection
        if orchestrator.conn:
            orchestrator.conn.close()
            logger.info("Closed Snowflake connection")


if __name__ == "__main__":
    main()
