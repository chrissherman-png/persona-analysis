#!/usr/bin/env python3
"""
Extract Gong call data with account segmentation (transcripts are in JSON format)
Pulls last 6 months of Gong calls from Snowflake and saves to CSV.
"""
import os
import sys
import json
from datetime import datetime
from pathlib import Path

import snowflake.connector
import pandas as pd
from dotenv import load_dotenv


def extract_gong_data(output_dir: str) -> str:
    """
    Pulls last 6 months of Gong calls from Snowflake.

    Args:
        output_dir: Base output directory (e.g., 'persona_analysis')

    Returns:
        Path to the saved CSV file

    Raises:
        SystemExit: If SNOWFLAKE_USER environment variable is not set
    """
    # Load environment variables
    load_dotenv()

    # Check for required environment variable
    snowflake_user = os.environ.get('SNOWFLAKE_USER')
    if not snowflake_user:
        print("\n❌ SNOWFLAKE_USER not set. Please add it to your .env file.")
        print("   See README for setup instructions.\n")
        sys.exit(1)

    # Create output directory path
    output_path = Path(output_dir) / 'data'
    output_path.mkdir(parents=True, exist_ok=True)

    print("="*80)
    print("EXTRACTING GONG CALL DATA")
    print("="*80)

    # Connect to Snowflake
    print("\n🔐 Opening browser for Snowflake SSO login...")
    print("   Please log in with your Zendesk credentials")

    conn = snowflake.connector.connect(
        account='ZENDESK-GLOBAL',
        user=snowflake_user,
        authenticator='externalbrowser',
        warehouse='PUBLIC_ZENDESK_L',
        database='CLEANSED',
        schema='GONG',
        role='PUBLIC'
    )

    query = """
    WITH recent_calls AS (
        SELECT
            c.CONVERSATION_KEY,
            cl.TITLE AS call_title,
            cl.EFFECTIVE_START_DATETIME AS call_date,
            cl.BROWSER_DURATION_SEC as duration_seconds,
            cl.DIRECTION,
            cl.CALL_SPOTLIGHT_BRIEF,
            cl.CALL_SPOTLIGHT_KEY_POINTS
        FROM CLEANSED.GONG.GONG_CONVERSATIONS_BCV c
        JOIN CLEANSED.GONG.GONG_CALLS_BCV cl
            ON c.CONVERSATION_KEY = cl.CONVERSATION_KEY
        WHERE c.CONVERSATION_TYPE = 'call'
          AND cl.STATUS = 'COMPLETED'
          AND LOWER(cl.SCOPE) = 'external'
          AND cl.EFFECTIVE_START_DATETIME >= DATEADD(MONTH, -6, CURRENT_DATE())
          AND c.IS_DELETED = FALSE
          AND cl.IS_DELETED = FALSE
    ),
    accounts_raw AS (
        SELECT
            ctx.CONVERSATION_KEY,
            ctx.OBJECT_ID as account_id,
            ctx.FIELDS_SNAPSHOT:NumberOfEmployees::INTEGER as employee_count,
            ctx.FIELDS_SNAPSHOT:Owner_Market_Segment__c::STRING as market_segment,
            ctx.FIELDS_SNAPSHOT:Region__c::STRING as region,
            ctx.FIELDS_SNAPSHOT:Industry::STRING as industry,
            ctx.FIELDS_SNAPSHOT:Sub_Industry_picklist__c::STRING as sub_industry,
            CASE
                WHEN ctx.FIELDS_SNAPSHOT:NumberOfEmployees::INTEGER <= 49 THEN 'Digital'
                WHEN ctx.FIELDS_SNAPSHOT:NumberOfEmployees::INTEGER BETWEEN 50 AND 249 THEN 'SMB'
                WHEN ctx.FIELDS_SNAPSHOT:NumberOfEmployees::INTEGER BETWEEN 250 AND 1499 THEN 'Commercial'
                WHEN ctx.FIELDS_SNAPSHOT:NumberOfEmployees::INTEGER >= 1500 THEN 'Enterprise'
            END as segment,
            ROW_NUMBER() OVER (
                PARTITION BY ctx.CONVERSATION_KEY
                ORDER BY ctx.FIELDS_SNAPSHOT:NumberOfEmployees::INTEGER DESC
            ) as account_rank
        FROM CLEANSED.GONG.GONG_CONVERSATION_CONTEXTS_BCV ctx
        WHERE ctx.OBJECT_TYPE = 'account'
          AND ctx.IS_DELETED = FALSE
          AND ctx.FIELDS_SNAPSHOT:NumberOfEmployees::INTEGER > 0
    ),
    accounts AS (
        SELECT
            CONVERSATION_KEY,
            account_id,
            employee_count,
            market_segment,
            region,
            industry,
            sub_industry,
            segment
        FROM accounts_raw
        WHERE account_rank = 1
    ),
    participants_with_titles AS (
        SELECT
            p.CONVERSATION_KEY,
            p.USER_ID,
            p.NAME as speaker_name,
            p.EMAIL_ADDRESS,
            p.AFFILIATION,
            sf.TITLE as contact_title,
            sf.NAME as contact_name,
            ROW_NUMBER() OVER (
                PARTITION BY p.CONVERSATION_KEY
                ORDER BY
                    CASE WHEN LOWER(p.AFFILIATION) != 'internal' THEN 0 ELSE 1 END,
                    CASE WHEN sf.TITLE IS NOT NULL THEN 0 ELSE 1 END
            ) as participant_rank
        FROM CLEANSED.GONG.GONG_CONVERSATION_PARTICIPANTS_BCV p
        LEFT JOIN CLEANSED.SALESFORCE.SALESFORCE_CONTACT_BCV sf
            ON LOWER(TRIM(p.EMAIL_ADDRESS)) = LOWER(TRIM(sf.EMAIL))
            AND sf.IS_DELETED = FALSE
        WHERE p.IS_DELETED = FALSE
          AND LOWER(p.AFFILIATION) != 'internal'
          AND p.EMAIL_ADDRESS IS NOT NULL
    ),
    final_dedupe AS (
        SELECT
            c.CONVERSATION_KEY,
            c.call_date,
            c.call_title,
            c.duration_seconds,
            c.DIRECTION,
            c.CALL_SPOTLIGHT_BRIEF,
            c.CALL_SPOTLIGHT_KEY_POINTS,
            a.segment,
            a.employee_count,
            a.market_segment,
            a.region,
            COALESCE(a.industry, a.sub_industry) as industry,
            p.contact_title,
            p.contact_name,
            p.speaker_name,
            ROW_NUMBER() OVER (PARTITION BY c.CONVERSATION_KEY ORDER BY c.call_date DESC) as row_num
        FROM recent_calls c
        JOIN accounts a ON c.CONVERSATION_KEY = a.CONVERSATION_KEY
        LEFT JOIN participants_with_titles p
            ON c.CONVERSATION_KEY = p.CONVERSATION_KEY
            AND p.participant_rank = 1
        WHERE a.segment IS NOT NULL
    )
    SELECT
        CONVERSATION_KEY,
        call_date,
        call_title,
        duration_seconds,
        DIRECTION,
        CALL_SPOTLIGHT_BRIEF,
        CALL_SPOTLIGHT_KEY_POINTS,
        segment,
        employee_count,
        market_segment,
        region,
        industry,
        contact_title,
        contact_name,
        speaker_name
    FROM final_dedupe
    WHERE row_num = 1
    ORDER BY segment, call_date DESC
    """

    print("\nStep 1: Extracting call metadata with participant titles...")
    start_time = datetime.now()
    calls_df = pd.read_sql(query, conn)
    elapsed = (datetime.now() - start_time).total_seconds()
    print(f"\n✓ Query completed in {elapsed:.1f} seconds")
    print(f"\n📊 Call Dataset Summary:")
    print(f"  Total calls: {len(calls_df):,}")

    batch_size = 5000
    all_transcripts = []
    all_conv_keys = calls_df['CONVERSATION_KEY'].tolist()
    total_batches = (len(all_conv_keys) + batch_size - 1) // batch_size

    for i in range(0, len(all_conv_keys), batch_size):
        batch_num = (i // batch_size) + 1
        batch_keys = all_conv_keys[i:i + batch_size]
        print(f"  Batch {batch_num}/{total_batches}: Fetching {len(batch_keys)} transcripts...")
        transcript_query = f"""
        SELECT CONVERSATION_KEY, TRANSCRIPT
        FROM GONG_CALL_TRANSCRIPTS_BCV
        WHERE CONVERSATION_KEY IN ({','.join("'" + k + "'" for k in batch_keys)})
          AND IS_DELETED = FALSE
        """
        batch_df = pd.read_sql(transcript_query, conn)
        all_transcripts.append(batch_df)

    transcripts_df = pd.concat(all_transcripts, ignore_index=True) if all_transcripts else pd.DataFrame()

    transcript_texts = {}
    for idx, row in transcripts_df.iterrows():
        conv_key = row['CONVERSATION_KEY']
        all_text = []
        try:
            transcript_json = json.loads(row['TRANSCRIPT']) if isinstance(row['TRANSCRIPT'], str) else row['TRANSCRIPT']
            if isinstance(transcript_json, list):
                for segment in transcript_json:
                    if isinstance(segment, dict) and 'sentences' in segment:
                        for sent in segment.get('sentences', []):
                            if isinstance(sent, dict):
                                text = sent.get('text', '').strip()
                                if text:
                                    all_text.append(text)
            if all_text:
                transcript_texts[conv_key] = ' '.join(all_text)
        except:
            pass

    calls_df['TRANSCRIPT_TEXT'] = calls_df['CONVERSATION_KEY'].map(transcript_texts)

    calls_file = output_path / f'gong_calls_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    calls_df.to_csv(calls_file, index=False)
    conn.close()

    print(f"\n✓ Complete data saved to: {calls_file}")

    return str(calls_file)


if __name__ == '__main__':
    # Allow running standalone for testing
    extract_gong_data('persona_analysis')
