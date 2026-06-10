#!/bin/bash
# Persona Intelligence Agent - Setup Script
# Date: 2026-03-25

set -e  # Exit on error

echo "=================================================="
echo "Persona Intelligence Agent - Setup"
echo "=================================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Found Python $python_version"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Create directory structure
echo "Creating directory structure..."
mkdir -p data
mkdir -p logs
mkdir -p reports
mkdir -p downstream_inputs
mkdir -p archive
echo "✓ Directories created"
echo ""

# Setup environment file
echo "Setting up environment configuration..."
if [ ! -f ".env" ]; then
    cp .env.template .env
    echo "✓ Created .env file from template"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your Snowflake credentials:"
    echo "   nano .env"
else
    echo "✓ .env file already exists"
fi
echo ""

# Check config file
echo "Checking configuration..."
if [ -f "config.yaml" ]; then
    echo "✓ config.yaml found"
    echo ""
    echo "⚠️  IMPORTANT: Review config.yaml and customize for your environment:"
    echo "   1. Update Snowflake connection details"
    echo "   2. Verify CRM field mappings match your schema"
    echo "   3. Adjust analysis settings as needed"
else
    echo "✗ config.yaml not found!"
    exit 1
fi
echo ""

# Test imports
echo "Testing Python imports..."
python3 -c "import pandas; import snowflake.connector; import yaml; print('✓ Core dependencies import successfully')"
echo ""

# Check SQL queries
echo "Checking SQL query files..."
if [ -d "../sql_queries" ]; then
    query_count=$(ls -1 ../sql_queries/*.sql 2>/dev/null | wc -l)
    echo "✓ Found $query_count SQL query files"
else
    echo "⚠️  SQL queries directory not found at ../sql_queries"
    echo "   Make sure sql_queries/ is in the parent directory"
fi
echo ""

# Setup complete
echo "=================================================="
echo "Setup Complete!"
echo "=================================================="
echo ""
echo "Next Steps:"
echo ""
echo "1. Configure Credentials:"
echo "   nano .env"
echo "   # Add your SNOWFLAKE_PASSWORD and other credentials"
echo ""
echo "2. Customize Configuration:"
echo "   nano config.yaml"
echo "   # Update Snowflake connection details"
echo ""
echo "3. Identify CRM Field Names (First Time):"
echo "   source venv/bin/activate"
echo "   python run_persona_analysis.py --explore"
echo "   # Review output to identify your CRM field names"
echo "   # Update config.yaml with actual field names"
echo ""
echo "4. Validate Data Quality (Optional):"
echo "   python run_persona_analysis.py --quality-check"
echo "   # Review output to ensure sufficient data volume"
echo ""
echo "5. Run Full Analysis:"
echo "   python run_persona_analysis.py"
echo "   # Agent automatically connects to Snowflake and runs all queries"
echo ""
echo "6. Review Outputs:"
echo "   ls -l reports/"
echo "   ls -l downstream_inputs/"
echo ""
echo "For more details, see README.md"
echo ""
