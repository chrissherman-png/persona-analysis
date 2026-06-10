"""
Simple test script to verify Snowflake connection
Run this before the full analysis to ensure credentials are correct

Date: 2026-03-25
"""

import os
import sys
import yaml
import snowflake.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_connection():
    """Test Snowflake connection with credentials from config and .env"""

    print("=" * 80)
    print("SNOWFLAKE CONNECTION TEST")
    print("=" * 80)
    print()

    # Load config
    try:
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        print("✓ Configuration file loaded")
    except Exception as e:
        print(f"✗ Failed to load config.yaml: {e}")
        return False

    # Check authentication method
    print("\nChecking credentials...")

    # Display connection details
    print("\nConnection details:")
    print(f"  Account:   {config['snowflake']['account']}")
    print(f"  User:      {config['snowflake']['user']}")
    print(f"  Warehouse: {config['snowflake']['warehouse']}")
    print(f"  Database:  {config['snowflake']['database']}")
    print(f"  Schema:    {config['snowflake']['schema']}")
    print(f"  Role:      {config['snowflake']['role']}")

    # Build connection parameters
    conn_params = {
        'account': config['snowflake']['account'],
        'user': config['snowflake']['user'],
        'warehouse': config['snowflake']['warehouse'],
        'database': config['snowflake']['database'],
        'schema': config['snowflake']['schema'],
        'role': config['snowflake']['role']
    }

    # Check if SSO authentication is configured
    if 'authenticator' in config['snowflake']:
        conn_params['authenticator'] = config['snowflake']['authenticator']
        print(f"  Auth:      {conn_params['authenticator']}")
        print()
        if conn_params['authenticator'] == 'externalbrowser':
            print("✓ Using SSO authentication")
            print("⚠️  A browser window will open for authentication...")
    else:
        # Use password-based authentication
        password = os.getenv('SNOWFLAKE_PASSWORD')
        if not password:
            print("✗ SNOWFLAKE_PASSWORD not found in environment")
            print("  Make sure you have created .env file with your password")
            return False
        conn_params['password'] = password
        print("✓ Using password authentication")

    print()

    # Attempt connection
    print("Attempting to connect to Snowflake...")

    try:
        conn = snowflake.connector.connect(**conn_params)

        print("✓ Successfully connected to Snowflake!")
        print()

        # Test a simple query
        print("Testing query execution...")
        cursor = conn.cursor()

        # Check if Gong tables exist
        cursor.execute("SHOW TABLES LIKE 'CONVERSATIONS'")
        result = cursor.fetchall()

        if result:
            print("✓ Found CONVERSATIONS table")
        else:
            print("⚠️  CONVERSATIONS table not found - check your schema name")

        cursor.execute("SHOW TABLES LIKE 'CALLS'")
        result = cursor.fetchall()

        if result:
            print("✓ Found CALLS table")
        else:
            print("⚠️  CALLS table not found - check your schema name")

        cursor.execute("SHOW TABLES LIKE 'CONVERSATION_PARTICIPANTS'")
        result = cursor.fetchall()

        if result:
            print("✓ Found CONVERSATION_PARTICIPANTS table")
        else:
            print("⚠️  CONVERSATION_PARTICIPANTS table not found - check your schema name")

        cursor.close()
        conn.close()

        print()
        print("=" * 80)
        print("CONNECTION TEST PASSED")
        print("=" * 80)
        print()
        print("Next steps:")
        print("  1. Run exploratory query: python run_persona_analysis.py --explore")
        print("  2. Update config.yaml with your CRM field names")
        print("  3. Run full analysis: python run_persona_analysis.py")
        print()

        return True

    except Exception as e:
        print(f"✗ Connection failed: {e}")
        print()
        print("Troubleshooting:")
        print("  1. Verify your SNOWFLAKE_PASSWORD in .env is correct")
        print("  2. Check that your account URL is correct (should end with .snowflakecomputing.com)")
        print("  3. Verify your user has access to the specified warehouse/database/schema")
        print("  4. Check if your IP is whitelisted in Snowflake network policies")
        print()
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
