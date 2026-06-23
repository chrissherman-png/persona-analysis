# Persona Pipeline

## What This Is

The Persona Pipeline automatically analyzes customer conversations from Gong to build detailed buyer personas. It:

- **Extracts** 6 months of call data from Snowflake (79,000+ calls)
- **Analyzes** with Claude API to identify patterns, pain points, and goals
- **Generates** interactive Team Review page for collaborative editing
- **Publishes** final stakeholder-facing page to GitHub Pages

Used by Sales, Customer Success, and Product teams to understand buyer needs and tailor outreach.

## Quick Start

```bash
git clone https://github.com/[YOUR_USERNAME]/persona-analysis.git
cd persona-analysis
cp .env.example .env
# Edit .env and add your Zendesk email for SNOWFLAKE_USER
python3 run_pipeline.py
```

⏱️ **Expected runtime: 30-40 minutes**

## What You Get

- **Team Review Page** — Interactive interface for voting, commenting, and editing personas
- **Final Page** — Clean stakeholder-facing version published to GitHub Pages  
- **Persona Insights** — Raw Claude analysis in JSON format for reference

## Setup

For detailed setup instructions, see **[HANDOFF.md](HANDOFF.md)**.

### Quick Setup Steps

1. **Clone the repo**

```bash
git clone https://github.com/[YOUR_USERNAME]/persona-analysis.git
cd persona-analysis
```

2. **Create environment file**

```bash
cp .env.example .env
```

3. **Add your Zendesk email**

Edit `.env` and set:
```
SNOWFLAKE_USER=your.email@zendesk.com
```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

5. **Run the pipeline**

```bash
python3 run_pipeline.py
```

Browser will open for Snowflake SSO login. After login, the pipeline runs automatically.

## Project Structure

```
persona_analysis/
├── run_pipeline.py                          # Main script — START HERE
├── extract_gong_data.py                     # Extract from Snowflake
├── claude_analyzer.py                       # Analyze with Claude API
├── generate_full_profiles_with_changes.py   # Team Review page generator
├── generate_final_clean_personas.py         # Final page generator
├── simple_server.py                         # Flask server for editing
├── research_loader.py                       # Load external research
├── metadata_writer.py                       # Track pipeline metadata
│
├── HANDOFF.md                               # Complete guide ← READ THIS
├── GOOGLE_SHEETS_SETUP.md                   # Optional: Google Sheets
├── .env.example                             # Environment template
├── requirements.txt                         # Python dependencies
│
├── data/
│   ├── updated_personas.json                # Current persona definitions
│   ├── gong_calls_*.csv                     # Raw Gong data (generated)
│   └── ...
├── reports/
│   ├── Persona_Team_Review_Full.html        # Interactive review page
│   ├── Persona_Profiles_FINAL.html          # Stakeholder page
│   └── ...
├── pending_changes/
│   └── edits_Q2_2026.json                   # Edit tracking
└── cache/                                   # Claude API cache
```

## The Workflow

1. **Run pipeline** — Extracts and analyzes data
2. **Share Team Review URL** — Reviewers access the interactive page
3. **Edit & vote** — Team votes on personas and makes edits
4. **Apply edits** — Click "Update Live Version" to generate final page
5. **Publish** — Click "Push Live Now" to publish to GitHub Pages
6. **Stakeholders see changes** — Live within 1-2 minutes

## Documentation

- **[HANDOFF.md](HANDOFF.md)** — Comprehensive guide with setup, running, troubleshooting
- **[GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md)** — Optional Google Sheets integration

## Troubleshooting

See **[HANDOFF.md — Troubleshooting](HANDOFF.md#8-troubleshooting)** for solutions to common issues:

- SNOWFLAKE_USER not set error
- Pipeline timeouts
- Authentication failures
- And more

## Support

For questions or issues:

1. Check **[HANDOFF.md](HANDOFF.md)** first
2. Review troubleshooting guide
3. Contact your team lead or pipeline owner

## Cost & Frequency

- **Cost per run:** ~$150-200 (Claude API)
- **Frequency:** Recommended quarterly
- **Time:** 30-40 minutes per run
