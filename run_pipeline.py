#!/usr/bin/env python3
"""
Master pipeline script for persona analysis.
Runs the full analysis and page generation in one command.

Usage:
    python3 run_pipeline.py
"""

import sys
import subprocess
import os
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

from extract_gong_data import extract_gong_data


def print_error(message):
    """Print error message and exit."""
    print(f"\n❌ {message}\n")
    sys.exit(1)


def print_step(message):
    """Print a step message."""
    print(f"\n{message}")


def run_command(cmd, description):
    """
    Run a command and stream output live.
    Returns True on success, False on failure.
    """
    print_step(description)

    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        # Stream output live
        for line in process.stdout:
            print(line, end='')

        # Wait for completion
        return_code = process.wait()

        if return_code != 0:
            print_error(f"{description} failed with exit code {return_code}")
            return False

        return True

    except Exception as e:
        print_error(f"{description} failed with error: {str(e)}")
        return False


def main():
    """Main pipeline execution."""
    start_time = time.time()

    # Get the directory where this script is located
    script_dir = Path(__file__).parent.resolve()

    # Load environment variables
    load_dotenv()

    # Print start banner
    print("\n" + "="*60)
    print("🚀 Starting persona pipeline run...")
    print("")
    print("📡 Step 1: Pulling fresh data from Snowflake")
    print("🤖 Step 2: Running Claude analysis (~25-35 min)")
    print("📄 Step 3: Generating Team Review page")
    print("")
    print("⏱  Estimated total time: 30-40 minutes")
    print("="*60)

    # Step 1: Extract fresh data from Snowflake
    try:
        csv_path = extract_gong_data(output_dir='.')
        if not csv_path:
            print_error("Data extraction failed. Pipeline stopped.")
    except Exception as e:
        print_error(f"Data extraction failed: {str(e)}")

    print_step(f"\n✅ Step 1 complete: Data saved to {Path(csv_path).name}")

    # Step 2: Run Claude analyzer
    analyzer_cmd = [
        "python3",
        str(script_dir / "claude_analyzer.py"),
        str(csv_path),
        "--output-dir",
        "."
    ]

    success = run_command(
        analyzer_cmd,
        "\n📊 Step 2: Running Claude analyzer..."
    )

    if not success:
        print_error("Analysis failed. Pipeline stopped.")

    print_step("\n✅ Step 2 complete: Claude analysis finished")

    # Step 3: Run Team Review generator
    generator_cmd = [
        "python3",
        str(script_dir / "generate_full_profiles_with_changes.py")
    ]

    success = run_command(
        generator_cmd,
        "\n📄 Step 3: Generating Team Review page..."
    )

    if not success:
        print_error("Page generation failed. Pipeline stopped.")

    print_step("\n✅ Step 3 complete: Team Review page generated")

    # Print completion summary
    end_time = time.time()
    duration_seconds = int(end_time - start_time)
    minutes = duration_seconds // 60
    seconds = duration_seconds % 60

    today = datetime.now().strftime("%Y-%m-%d")

    print("\n" + "="*60)
    print("✅ Pipeline complete!")
    print("="*60)
    print("\n📋 Next steps:")
    print("  1. Review the Team Review page locally:")
    print("     persona_analysis/reports/Persona_Team_Review_Full.html")
    print("\n  2. Push to GitHub to share with your team:")
    print("     git add .")
    print(f"     git commit -m 'Pipeline refresh: {today}'")
    print("     git push origin main")
    print("\n  3. Share this URL with reviewers:")
    print("     https://chrissherman-png.github.io/persona-analysis/reports/Persona_Team_Review_Full.html")
    print("\n" + "="*60)
    print(f"⏱  Total runtime: {minutes} minutes {seconds} seconds")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
