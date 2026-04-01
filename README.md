# Persona Intelligence Agent

**Automated buyer persona validation and refresh system for Zendesk Product Marketing**

This agent analyzes Gong call transcripts and Salesforce CRM data to continuously validate and update buyer personas for SMB (50–249 employees) and Commercial (250–1,499 employees) segments.

---

## 🎯 Key Feature: Direct Snowflake Integration

**No manual SQL execution required!** The agent connects directly to Snowflake and executes all queries automatically.

```bash
# Configure once
nano .env  # Add your Snowflake password

# Run analysis (everything is automated)
python run_persona_analysis.py
```

The agent automatically:
- ✅ Connects to Snowflake
- ✅ Executes data quality checks (9 validations)
- ✅ Runs main extraction query
- ✅ Processes through persona framework
- ✅ Generates marketing-ready outputs

**One command. Fully automated. Production ready.**

---

## 📁 Project Structure

```
persona_analysis/
├── persona_intelligence_agent.py    # Core analysis engine
├── run_persona_analysis.py          # Orchestration script
├── config.yaml                       # Configuration file
├── requirements.txt                  # Python dependencies
├── .env.template                     # Environment variable template
├── README.md                         # This file
│
├── data/                             # Raw extraction data
├── logs/                             # Execution logs
├── reports/                          # Generated persona reports
├── downstream_inputs/                # Marketing agent inputs
└── archive/                          # Previous runs

sql_queries/
├── 01_exploratory_sample.sql        # Schema exploration
├── 02_main_extraction.sql           # Main data extraction
└── 03_data_quality_checks.sql       # Pre-analysis validation
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd persona_analysis
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy template and fill in your credentials
cp .env.template .env
nano .env  # or use your preferred editor
```

**Required variables:**
- `SNOWFLAKE_PASSWORD`
- `SNOWFLAKE_ACCOUNT`
- `SNOWFLAKE_USER`
- Other Snowflake connection details

### 3. Customize Configuration

Edit `config.yaml` to match your environment:

```yaml
snowflake:
  account: YOUR_ACCOUNT.snowflakecomputing.com
  database: YOUR_DATABASE
  schema: GONG_SCHEMA  # Where your Gong tables live

extraction:
  crm_fields:
    account:
      employee_count: "NumberOfEmployees"  # Adjust to match your CRM fields
```

### 4. Identify Your CRM Field Names (First Time)

The agent connects directly to Snowflake to identify field names:

```bash
source venv/bin/activate
python run_persona_analysis.py --explore
```

This will:
- Connect to Snowflake
- Query 10 sample conversations
- Parse and display all available JSON field names
- Help you identify the correct field mappings

Review the console output and update `config.yaml` with your actual field names.

### 5. Run Full Analysis

```bash
# Optional: Validate data quality first
python run_persona_analysis.py --quality-check

# Run full analysis
python run_persona_analysis.py
```

The agent will automatically:
1. Connect to Snowflake
2. Run data quality checks (9 automated validations)
3. Extract conversation and CRM data
4. Apply persona framework validation
5. Generate per-persona reports
6. Create downstream agent input files

**All SQL queries are executed automatically** - no manual Snowflake access required!

---

## 🎮 Usage

### Command-Line Options

```bash
# Show help and all options
python run_persona_analysis.py --help

# Exploratory mode: Identify CRM field names (run this first!)
python run_persona_analysis.py --explore

# Quality check mode: Validate data quality before full run
python run_persona_analysis.py --quality-check

# Full analysis (default)
python run_persona_analysis.py

# Use custom config file
python run_persona_analysis.py --config custom_config.yaml

# Exploratory mode with more samples
python run_persona_analysis.py --explore --sample-limit 50
```

### Typical Workflow

```bash
# First time setup
./setup.sh
nano .env  # Add credentials
nano config.yaml  # Review settings

# Step 1: Identify field names
python run_persona_analysis.py --explore
# Review output, update config.yaml with actual field names

# Step 2: Validate data quality
python run_persona_analysis.py --quality-check
# Review any warnings

# Step 3: Run full analysis
python run_persona_analysis.py
# Review reports in reports/ and downstream_inputs/

# Step 4: Schedule automated runs
crontab -e  # Add weekly cron job
```

---

## 📊 Outputs

### Per-Persona Reports
**Location:** `reports/persona_report_{segment}_{persona}.md`

Example: `reports/persona_report_SMB_CX_Leader.md`

Contains:
- Signal breakdown (conversations, people, recency)
- Top job titles observed
- Top industries
- Deal context (motion, stage)
- Verbatim quotes
- AI-generated call insights

### Downstream Agent Inputs
**Location:** `downstream_inputs/downstream_agent_input_{segment}.md`

Example: `downstream_inputs/downstream_agent_input_SMB.md`

Purpose-built for SMB and Commercial Persona Marketing Agents:
- Clean, self-contained persona definitions
- Written in marketing-ready language
- No methodology or confidence scores
- Structured for programmatic ingestion

### Run Summary
**Location:** `reports/run_summary_{timestamp}.md`

High-level summary of:
- Data quality check results
- Total signals per persona
- Data freshness metrics

---

## 🔄 Automated Refresh

### Option 1: Cron (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Add entry for weekly Tuesday 2am runs:
0 2 * * 2 cd /path/to/persona_analysis && /usr/bin/python3 run_persona_analysis.py >> logs/cron.log 2>&1
```

### Option 2: Scheduled Task (Windows)

```powershell
# Create a scheduled task
schtasks /create /tn "PersonaAnalysis" /tr "python C:\path\to\run_persona_analysis.py" /sc weekly /d TUE /st 02:00
```

### Option 3: Airflow DAG

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'product-marketing',
    'depends_on_past': False,
    'email': ['product-marketing@zendesk.com'],
    'email_on_failure': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'persona_intelligence_agent',
    default_args=default_args,
    description='Weekly persona validation refresh',
    schedule_interval='0 2 * * 2',  # Every Tuesday at 2am
    start_date=datetime(2026, 3, 25),
    catchup=False,
    tags=['personas', 'marketing'],
)

run_analysis = BashOperator(
    task_id='run_persona_analysis',
    bash_command='cd /path/to/persona_analysis && python run_persona_analysis.py',
    dag=dag,
)
```

---

## 🔍 Understanding the Analysis

### Data Sources

**1. Gong Tables (via Snowflake)**
- `Conversations` - Base conversation metadata
- `Calls` - Call details, AI-generated briefs
- `Call_Transcripts` - Full transcript with speaker segments (verbatim quotes)
- `Conversation_participants` - Who was on the call (titles, emails)
- `Conversation_contexts` - CRM associations (accounts, opportunities)

**2. CRM Data (embedded in Gong)**
- Account data: Employee count, industry (for segmentation)
- Opportunity data: Stage, type, win/loss (for motion tagging)
- Contact data: Titles, roles (for persona classification)

### Processing Pipeline

```
1. Data Extraction (SQL)
   ├── Filter for external, completed calls from last 6 months
   ├── Join CRM context (accounts, opportunities, contacts)
   └── Extract transcripts for verbatim quotes

2. Preprocessing (Python)
   ├── Title Normalization → Canonical persona roles
   ├── Segmentation → SMB (50-249) vs Commercial (250-1,499)
   ├── Entity Deduplication → Merge by email
   └── Motion Tagging → New Business vs Expansion

3. Persona Analysis (Python)
   ├── Group signals by segment + persona
   ├── Extract quotes, titles, industries, KPIs
   ├── Calculate confidence tiers
   └── Apply validation thresholds

4. Report Generation (Python)
   ├── Per-persona reports (internal)
   ├── Downstream agent inputs (for marketing agents)
   └── Data quality summary
```

### Validation Thresholds

From the persona specification (Section 4):

- **✅ VALIDATED:** ≥60% of signals confirm the current definition
- **⚠️ UPDATED:** ≥40% of signals contradict or refine the definition
- **🆕 NEW SIGNAL:** Pattern appears in ≥3 sources, not in current definition

**Confidence Tiers:**
- **HIGH:** ≥10 Gong calls + ≥5 SF contacts + ≥1 web signal
- **MEDIUM:** 5–9 total sources
- **LOW:** <5 signals

---

## 🛠️ Customization

### Adding New Personas

Edit `config.yaml`:

```yaml
analysis:
  personas:
    - C-Suite
    - CX Leader
    - Your New Persona  # Add here
```

Then update title normalization rules in `persona_intelligence_agent.py`:

```python
self.title_normalization_rules = {
    'Your New Persona': [
        r'\bKeyword1\b',
        r'\bKeyword2\b',
    ],
    # ... existing personas
}
```

### Adjusting Time Windows

Edit `config.yaml`:

```yaml
extraction:
  lookback_months: 12  # Increase for broader analysis
```

### Custom CRM Field Names

If your CRM uses different field names:

1. Run exploratory query: `sql_queries/01_exploratory_sample.sql`
2. Identify field names in JSON output
3. Update `config.yaml`:

```yaml
extraction:
  crm_fields:
    account:
      employee_count: "Your_Custom_Field__c"
```

---

## 📝 Maintenance

### Weekly Checklist
- [ ] Review data quality summary
- [ ] Check for unclassified titles (>20% = issue)
- [ ] Verify segment distribution (SMB + Commercial > 100 each)
- [ ] Review new signals flagged for human evaluation
- [ ] Archive old reports

### Monthly Checklist
- [ ] Review downstream agent usage and feedback
- [ ] Update title normalization rules based on unclassified titles
- [ ] Validate CRM field mappings still correct
- [ ] Check for new personas emerging in data

### Quarterly Checklist
- [ ] Full persona framework review
- [ ] Rebuild thresholds if market changes
- [ ] Review web source integration (currently manual)
- [ ] Update documentation

---

## 🐛 Troubleshooting

### "Missing employee count for >20% of records"

**Cause:** CRM accounts don't have employee count populated

**Solutions:**
1. Enrich accounts using external data (LinkedIn, ZoomInfo)
2. Adjust SQL to use alternative size signals (revenue, user count)
3. Exclude unclassified accounts from analysis

### "Unclassified titles >20%"

**Cause:** Title normalization rules don't cover all variations

**Solutions:**
1. Review unclassified titles: Run Check 7 from `03_data_quality_checks.sql`
2. Add patterns to `title_normalization_rules` in `persona_intelligence_agent.py`
3. Consider fuzzy matching for similar titles

### "Insufficient data for persona"

**Cause:** <5 signals found for a persona in a segment

**Solutions:**
1. Expand time window (`lookback_months` in config)
2. Review if this persona truly exists in that segment
3. Consider removing from analysis or merging with similar persona

### "Snowflake connection failed"

**Cause:** Credentials incorrect or network issue

**Solutions:**
1. Verify `.env` credentials
2. Test connection: `snowsql -a YOUR_ACCOUNT -u YOUR_USER`
3. Check IP whitelisting if using Snowflake network policies

---

## 📚 Related Documentation

- **Persona Specification:** See your original prompt/specification document
- **Gong Schema Reference:** `gong_database_reference_all_tables (1).json`
- **Schema Analysis:** `gong_schema_analysis.md`
- **SQL Queries:** `sql_queries/` directory

---

## 🤝 Contributing

### Adding Web Source Integration

Web sources (G2 reviews, LinkedIn job posts, analyst reports) are currently manual. To automate:

1. Create `web_scraper.py` module
2. Add web source extraction to `run_persona_analysis.py`
3. Weight web signals appropriately (lowest weight per spec)
4. Always corroborate with Gong/SF data before promoting to VALIDATED

### Adding Email Notifications

Implement in `run_persona_analysis.py`:

```python
def send_notification(self, status: str, summary: str):
    """Send email notification on completion."""
    # Use SMTP settings from .env
    # Send summary + link to reports
```

---

## 📧 Support

**Product Marketing Team:** product-marketing@zendesk.com

**Data Engineering:** data-eng@zendesk.com

---

## 📄 License

Internal Zendesk tool. Not for external distribution.

---

**Last Updated:** 2026-03-25
