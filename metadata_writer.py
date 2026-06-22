#!/usr/bin/env python3
"""
Pipeline Metadata Writer
Helper functions for writing pipeline run metadata from different stages
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class MetadataWriter:
    """Writes pipeline metadata fragments and combines them into final metadata."""

    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = Path(__file__).parent

        self.base_dir = Path(base_dir)
        self.temp_dir = self.base_dir / 'temp_metadata'
        self.temp_dir.mkdir(exist_ok=True)

        self.final_path = self.base_dir / 'pipeline_run_metadata.json'

    def write_gong_metadata(
        self,
        calls_analyzed: int,
        date_range: tuple,  # (start_date, end_date)
        transcript_coverage_pct: float,
        title_coverage_pct: float,
        extraction_date: str
    ):
        """Write Gong extraction metadata to temp file."""
        metadata = {
            "calls_analyzed": calls_analyzed,
            "date_range": f"{date_range[0]} to {date_range[1]}",
            "transcript_coverage_pct": round(transcript_coverage_pct, 1),
            "title_coverage_pct": round(title_coverage_pct, 1),
            "extraction_date": extraction_date,
            "snowflake_tables": [
                "CLEANSED.GONG.GONG_CONVERSATIONS_BCV",
                "CLEANSED.GONG.GONG_CALLS_BCV",
                "CLEANSED.GONG.GONG_CONVERSATION_CONTEXTS_BCV",
                "CLEANSED.GONG.GONG_CONVERSATION_PARTICIPANTS_BCV",
                "CLEANSED.GONG.GONG_CALL_TRANSCRIPTS_BCV",
                "CLEANSED.SALESFORCE.SALESFORCE_CONTACT_BCV"
            ]
        }

        with open(self.temp_dir / 'gong_metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)

        print(f"✓ Gong metadata written to: {self.temp_dir / 'gong_metadata.json'}")

    def write_claude_metadata(
        self,
        model: str,
        analysis_date: str,
        batches_processed: int,
        personas_analyzed: int,
        segments_analyzed: int
    ):
        """Write Claude analysis metadata to temp file."""
        metadata = {
            "model": model,
            "analysis_date": analysis_date,
            "batches_processed": batches_processed,
            "personas_analyzed": personas_analyzed,
            "segments_analyzed": segments_analyzed
        }

        with open(self.temp_dir / 'claude_metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)

        print(f"✓ Claude metadata written to: {self.temp_dir / 'claude_metadata.json'}")

    def finalize_metadata(self, research_manifest_path: Optional[str] = None):
        """
        Combine all metadata fragments into final pipeline_run_metadata.json.
        Loads research sources from manifest if provided.
        """
        # Load Gong metadata
        gong_path = self.temp_dir / 'gong_metadata.json'
        if not gong_path.exists():
            print("⚠️  Warning: Gong metadata not found, using defaults")
            gong_meta = self._get_default_gong_metadata()
        else:
            with open(gong_path, 'r') as f:
                gong_meta = json.load(f)

        # Load Claude metadata
        claude_path = self.temp_dir / 'claude_metadata.json'
        if not claude_path.exists():
            print("⚠️  Warning: Claude metadata not found, using defaults")
            claude_meta = self._get_default_claude_metadata()
        else:
            with open(claude_path, 'r') as f:
                claude_meta = json.load(f)

        # Load research sources from manifest
        research_sources = []
        if research_manifest_path:
            research_path = Path(research_manifest_path)
            if research_path.exists():
                try:
                    with open(research_path, 'r') as f:
                        manifest = json.load(f)

                    # Extract summary info for each source (skip examples)
                    for source in manifest.get('sources', []):
                        if source.get('id', '').startswith('example-'):
                            continue

                        research_sources.append({
                            "source_org": source.get('source_org', 'Unknown'),
                            "title": source.get('title', 'Untitled'),
                            "published_date": source.get('published_date', 'Unknown')
                        })
                except Exception as e:
                    print(f"⚠️  Warning: Could not load research manifest: {e}")

        # Determine quarter
        now = datetime.now()
        quarter = f"Q{(now.month - 1) // 3 + 1} {now.year}"

        # Combine into final metadata
        final_metadata = {
            "run_date": now.strftime("%Y-%m-%d"),
            "run_quarter": quarter,
            "data_sources": {
                "gong": gong_meta,
                "claude_analysis": claude_meta,
                "third_party_research": research_sources
            },
            "_notes": "This file is auto-generated by the pipeline. Do not edit manually."
        }

        # Write final metadata
        with open(self.final_path, 'w') as f:
            json.dump(final_metadata, f, indent=2)

        print(f"\n✓ Final metadata written to: {self.final_path}")
        print(f"  Run date: {final_metadata['run_date']}")
        print(f"  Quarter: {final_metadata['run_quarter']}")
        print(f"  Gong calls: {gong_meta['calls_analyzed']:,}")
        print(f"  Claude batches: {claude_meta['batches_processed']}")
        print(f"  Research sources: {len(research_sources)}")

        return final_metadata

    def _get_default_gong_metadata(self) -> Dict:
        """Return default Gong metadata when temp file is missing."""
        return {
            "calls_analyzed": 0,
            "date_range": "Not available",
            "transcript_coverage_pct": 0.0,
            "title_coverage_pct": 0.0,
            "extraction_date": "Not available",
            "snowflake_tables": [
                "CLEANSED.GONG.GONG_CONVERSATIONS_BCV",
                "CLEANSED.GONG.GONG_CALLS_BCV",
                "CLEANSED.GONG.GONG_CONVERSATION_CONTEXTS_BCV",
                "CLEANSED.GONG.GONG_CONVERSATION_PARTICIPANTS_BCV",
                "CLEANSED.GONG.GONG_CALL_TRANSCRIPTS_BCV",
                "CLEANSED.SALESFORCE.SALESFORCE_CONTACT_BCV"
            ]
        }

    def _get_default_claude_metadata(self) -> Dict:
        """Return default Claude metadata when temp file is missing."""
        return {
            "model": "claude-3-5-sonnet-20241022",
            "analysis_date": "Not available",
            "batches_processed": 0,
            "personas_analyzed": 0,
            "segments_analyzed": 0
        }


def main():
    """CLI entry point for manual metadata finalization."""
    import sys

    writer = MetadataWriter()

    # Check if research manifest path was provided
    research_path = None
    if len(sys.argv) > 1:
        research_path = sys.argv[1]
    else:
        # Default location
        default_path = Path(__file__).parent / 'third_party_research' / 'research_manifest.json'
        if default_path.exists():
            research_path = str(default_path)

    writer.finalize_metadata(research_path)
    print("\n✅ Metadata finalization complete")


if __name__ == '__main__':
    main()
