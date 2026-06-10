#!/bin/bash
# Cron Job Template for Persona Intelligence Agent
# Date: 2026-03-25
#
# This script is designed to be run from cron for automated persona refresh
# It handles environment setup, logging, and error notifications

# Configuration
SCRIPT_DIR="/Users/chris.sherman/persona_analysis"
VENV_DIR="$SCRIPT_DIR/venv"
LOG_DIR="$SCRIPT_DIR/logs"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$LOG_DIR/cron_run_$TIMESTAMP.log"

# Email notification settings (optional)
NOTIFICATION_EMAIL="product-marketing@zendesk.com"
SEND_NOTIFICATIONS=false  # Set to true to enable email notifications

# Redirect all output to log file
exec > >(tee -a "$LOG_FILE") 2>&1

echo "=================================================="
echo "Persona Intelligence Agent - Scheduled Run"
echo "Started: $(date)"
echo "=================================================="
echo ""

# Change to script directory
cd "$SCRIPT_DIR" || {
    echo "ERROR: Failed to change to script directory: $SCRIPT_DIR"
    exit 1
}

# Activate virtual environment
if [ -d "$VENV_DIR" ]; then
    echo "Activating virtual environment..."
    source "$VENV_DIR/bin/activate"
else
    echo "ERROR: Virtual environment not found at $VENV_DIR"
    echo "Run setup.sh first to create the environment"
    exit 1
fi

# Load environment variables
if [ -f ".env" ]; then
    echo "Loading environment variables..."
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "ERROR: .env file not found"
    echo "Copy .env.template to .env and configure your credentials"
    exit 1
fi

# Run the analysis
echo ""
echo "Starting persona analysis..."
echo ""

if python run_persona_analysis.py; then
    EXIT_CODE=0
    STATUS="SUCCESS"
    echo ""
    echo "=================================================="
    echo "Analysis completed successfully"
    echo "Completed: $(date)"
    echo "=================================================="
else
    EXIT_CODE=$?
    STATUS="FAILED"
    echo ""
    echo "=================================================="
    echo "Analysis failed with exit code: $EXIT_CODE"
    echo "Completed: $(date)"
    echo "=================================================="
fi

# Deactivate virtual environment
deactivate

# Send notification email if enabled
if [ "$SEND_NOTIFICATIONS" = true ]; then
    SUBJECT="Persona Intelligence Agent: $STATUS"
    BODY="Automated persona analysis run completed with status: $STATUS\n\nLog file: $LOG_FILE\n\nTimestamp: $(date)"

    echo "$BODY" | mail -s "$SUBJECT" "$NOTIFICATION_EMAIL"
    echo "Notification sent to $NOTIFICATION_EMAIL"
fi

# Cleanup old log files (keep last 30 days)
echo ""
echo "Cleaning up old log files..."
find "$LOG_DIR" -name "cron_run_*.log" -mtime +30 -delete
echo "Cleanup complete"

exit $EXIT_CODE
