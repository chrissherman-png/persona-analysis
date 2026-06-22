#!/usr/bin/env python3
"""
Third-Party Research Loader
Loads and indexes research from research_manifest.json for use in Claude analyzer
"""

import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Optional


class ResearchLoader:
    """Loads and provides access to third-party research sources."""

    VALID_PERSONAS = [
        'CX Champion', 'C-Suite Champion', 'IT Influencer',
        'Business Analyst', 'End User'
    ]

    VALID_SEGMENTS = ['Digital', 'SMB', 'Commercial', 'Enterprise']

    VALID_SECTIONS = [
        'pain_points', 'goals', 'objections', 'success_metrics',
        'key_messages_to_land', 'product_requirements', 'information_sources',
        'messaging_preferences', 'competitive_landscape', 'messaging_dos_and_donts'
    ]

    def __init__(self, manifest_path: Optional[str] = None):
        if manifest_path is None:
            manifest_path = Path(__file__).parent / 'third_party_research' / 'research_manifest.json'

        self.manifest_path = Path(manifest_path)
        self.sources = []
        self.research_by_persona = defaultdict(list)
        self.research_by_segment = defaultdict(list)
        self.research_by_section = defaultdict(list)
        self.errors = []

    def load(self) -> bool:
        """
        Load and validate research manifest.
        Returns True if successful, False if errors (check self.errors).
        """
        if not self.manifest_path.exists():
            self.errors.append(f"Manifest file not found: {self.manifest_path}")
            return False

        try:
            with open(self.manifest_path, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in manifest: {e}")
            return False

        if 'sources' not in data:
            self.errors.append("Manifest missing 'sources' array")
            return False

        # Validate and index each source
        for idx, source in enumerate(data['sources']):
            # Skip example/template sources
            if source.get('id', '').startswith('example-'):
                continue

            errors = self._validate_source(source, idx)
            if errors:
                self.errors.extend(errors)
                continue

            self.sources.append(source)
            self._index_source(source)

        return len(self.errors) == 0

    def _validate_source(self, source: Dict, idx: int) -> List[str]:
        """Validate a single research source. Returns list of error messages."""
        errors = []
        prefix = f"Source #{idx + 1}"

        # Required fields
        required = ['id', 'source_org', 'title', 'published_date',
                   'applicable_personas', 'applicable_segments',
                   'applicable_sections', 'excerpts']

        for field in required:
            if field not in source:
                errors.append(f"{prefix}: Missing required field '{field}'")

        if errors:
            return errors

        # Validate personas
        personas = source['applicable_personas']
        if not isinstance(personas, list):
            errors.append(f"{prefix}: 'applicable_personas' must be an array")
        elif 'all' not in personas:
            invalid = [p for p in personas if p not in self.VALID_PERSONAS]
            if invalid:
                errors.append(f"{prefix}: Invalid personas: {invalid}. Valid: {self.VALID_PERSONAS}")

        # Validate segments
        segments = source['applicable_segments']
        if not isinstance(segments, list):
            errors.append(f"{prefix}: 'applicable_segments' must be an array")
        elif 'all' not in segments:
            invalid = [s for s in segments if s not in self.VALID_SEGMENTS]
            if invalid:
                errors.append(f"{prefix}: Invalid segments: {invalid}. Valid: {self.VALID_SEGMENTS}")

        # Validate sections
        sections = source['applicable_sections']
        if not isinstance(sections, list):
            errors.append(f"{prefix}: 'applicable_sections' must be an array")
        elif 'all' not in sections:
            invalid = [s for s in sections if s not in self.VALID_SECTIONS]
            if invalid:
                errors.append(f"{prefix}: Invalid sections: {invalid}. Valid: {self.VALID_SECTIONS}")

        # Validate excerpts
        excerpts = source.get('excerpts', [])
        if not isinstance(excerpts, list) or len(excerpts) == 0:
            errors.append(f"{prefix}: Must have at least one excerpt")
        else:
            for e_idx, excerpt in enumerate(excerpts):
                if not isinstance(excerpt, dict):
                    errors.append(f"{prefix}, Excerpt #{e_idx + 1}: Must be an object")
                elif 'text' not in excerpt:
                    errors.append(f"{prefix}, Excerpt #{e_idx + 1}: Missing 'text' field")

        return errors

    def _index_source(self, source: Dict):
        """Index a source for fast lookup by persona, segment, and section."""
        personas = source['applicable_personas']
        segments = source['applicable_segments']
        sections = source['applicable_sections']

        # Expand 'all' wildcards
        if 'all' in personas:
            personas = self.VALID_PERSONAS
        if 'all' in segments:
            segments = self.VALID_SEGMENTS
        if 'all' in sections:
            sections = self.VALID_SECTIONS

        # Index by persona
        for persona in personas:
            self.research_by_persona[persona].append(source)

        # Index by segment
        for segment in segments:
            self.research_by_segment[segment].append(source)

        # Index by section
        for section in sections:
            self.research_by_section[section].append(source)

    def get_research_for(
        self,
        persona: Optional[str] = None,
        segment: Optional[str] = None,
        sections: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Get research filtered by persona, segment, and/or sections.
        Returns list of source dicts that match ALL specified criteria.
        """
        if not self.sources:
            return []

        # Start with all sources
        results = set(range(len(self.sources)))

        # Filter by persona
        if persona:
            persona_sources = self.research_by_persona.get(persona, [])
            persona_indices = {self.sources.index(s) for s in persona_sources}
            results &= persona_indices

        # Filter by segment
        if segment:
            segment_sources = self.research_by_segment.get(segment, [])
            segment_indices = {self.sources.index(s) for s in segment_sources}
            results &= segment_indices

        # Filter by sections (match ANY of the requested sections)
        if sections:
            section_indices = set()
            for section in sections:
                section_sources = self.research_by_section.get(section, [])
                section_indices.update({self.sources.index(s) for s in section_sources})
            results &= section_indices

        return [self.sources[i] for i in sorted(results)]

    def get_summary(self) -> str:
        """Generate a human-readable summary of loaded research."""
        lines = []
        lines.append("=" * 80)
        lines.append("THIRD-PARTY RESEARCH SUMMARY")
        lines.append("=" * 80)

        if self.errors:
            lines.append("\n⚠️  ERRORS FOUND:")
            for error in self.errors:
                lines.append(f"  • {error}")
            lines.append("")

        if not self.sources:
            lines.append("\n❌ No valid research sources loaded")
            return "\n".join(lines)

        lines.append(f"\n✓ Loaded {len(self.sources)} research sources")
        lines.append(f"  Manifest: {self.manifest_path}")
        lines.append("")

        # Summary table
        lines.append("SOURCE COVERAGE:")
        lines.append("-" * 80)

        for source in self.sources:
            lines.append(f"\n📄 {source['title']}")
            lines.append(f"   Publisher: {source['source_org']} ({source['published_date']})")

            # Expand wildcards for display
            personas = source['applicable_personas']
            if 'all' in personas:
                personas = ['ALL']
            lines.append(f"   Personas: {', '.join(personas)}")

            segments = source['applicable_segments']
            if 'all' in segments:
                segments = ['ALL']
            lines.append(f"   Segments: {', '.join(segments)}")

            sections = source['applicable_sections']
            if 'all' in sections:
                sections = ['ALL']
            lines.append(f"   Sections: {', '.join(sections)}")

            lines.append(f"   Excerpts: {len(source['excerpts'])}")

        lines.append("\n" + "=" * 80)
        lines.append("COVERAGE BY PERSONA:")
        lines.append("-" * 80)
        for persona in self.VALID_PERSONAS:
            count = len(self.research_by_persona.get(persona, []))
            lines.append(f"  {persona:<25} {count} sources")

        lines.append("\n" + "=" * 80)
        lines.append("COVERAGE BY SEGMENT:")
        lines.append("-" * 80)
        for segment in self.VALID_SEGMENTS:
            count = len(self.research_by_segment.get(segment, []))
            lines.append(f"  {segment:<25} {count} sources")

        lines.append("\n" + "=" * 80)
        lines.append("COVERAGE BY SECTION:")
        lines.append("-" * 80)
        for section in self.VALID_SECTIONS:
            count = len(self.research_by_section.get(section, []))
            lines.append(f"  {section:<35} {count} sources")

        lines.append("\n" + "=" * 80)
        return "\n".join(lines)


def main():
    """CLI entry point - load and display research summary."""
    loader = ResearchLoader()
    success = loader.load()

    print(loader.get_summary())

    if not success:
        print("\n❌ Validation failed. Fix errors above and try again.")
        return 1

    print("\n✅ All research sources validated successfully")
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
