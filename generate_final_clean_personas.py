#!/usr/bin/env python3
"""
Generate final clean persona profiles HTML - no voting, no comments
This is what stakeholders would see as the final deliverable
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Use relative paths based on script location
BASE_DIR = Path(__file__).parent
sys.path.append(str(BASE_DIR))

def load_personas_with_edits():
    """Load persona data and apply edits if they exist"""

    # Load personas from updated_personas.json
    data_file = BASE_DIR / 'data' / 'updated_personas.json'
    if data_file.exists():
        with open(data_file, 'r') as f:
            data = json.load(f)
            # Check if it's the versioned format
            if 'personas' in data:
                personas = data['personas']
            else:
                personas = data
    else:
        # Fall back to static import
        from generate_persona_profiles import personas

    # Load pipeline metadata to get run_quarter
    metadata_file = BASE_DIR / 'pipeline_run_metadata.json'
    run_quarter = None
    if metadata_file.exists():
        try:
            with open(metadata_file, 'r') as f:
                pipeline_metadata = json.load(f)
                run_quarter = pipeline_metadata.get('run_quarter')
        except Exception as e:
            print(f"Warning: Could not read run_quarter from metadata: {e}")

    if not run_quarter:
        print("Warning: Could not read run_quarter from metadata — skipping edits merge")
        return personas, set()  # Return empty set of edited sections

    # Check if edits file exists
    edits_file = BASE_DIR / 'pending_changes' / f'edits_{run_quarter.replace(" ", "_")}.json'
    edited_sections = set()  # Track which sections have edits

    if edits_file.exists():
        try:
            with open(edits_file, 'r') as f:
                edits_data = json.load(f)

            print(f"Applying edits from {edits_file.name}...")

            # Apply edited items to personas
            for segment, personas_in_segment in edits_data.get('edits', {}).items():
                if segment not in personas:
                    continue

                for persona_name, fields in personas_in_segment.items():
                    if persona_name not in personas[segment]:
                        continue

                    for field, field_data in fields.items():
                        if field_data.get('has_changes'):
                            # Replace field with edited items array (no cap)
                            personas[segment][persona_name][field] = field_data['items']
                            # Track this section as edited
                            edited_sections.add(f"{segment}.{persona_name}.{field}")
                            print(f"  Applied edits: {segment} → {persona_name} → {field} ({len(field_data['items'])} items)")
        except Exception as e:
            print(f"Warning: Could not load edits: {e}")

    return personas, edited_sections

def generate_final_html():
    """Generate clean, polished HTML without collaboration features"""

    # Load personas with edits applied
    personas, edited_sections = load_personas_with_edits()

    # Load pipeline metadata
    metadata_file = BASE_DIR / 'pipeline_run_metadata.json'
    pipeline_metadata = {}
    if metadata_file.exists():
        with open(metadata_file, 'r') as f:
            pipeline_metadata = json.load(f)

    # Load segment insights
    segment_file = BASE_DIR / 'segment_insights_claude.json'
    segment_insights = {}
    if segment_file.exists():
        with open(segment_file, 'r') as f:
            segment_insights = json.load(f)

    # Extract metadata for hero badge
    gong_data = pipeline_metadata.get('data_sources', {}).get('gong', {})
    total_calls = gong_data.get('calls_analyzed', 69711)
    date_range = gong_data.get('date_range', '2025-10-12 to 2026-04-09')

    # Format for display
    total_calls_formatted = f"{total_calls:,}"
    if ' to ' in date_range:
        start, end = date_range.split(' to ')
        try:
            start_date = datetime.strptime(start.strip(), '%Y-%m-%d')
            end_date = datetime.strptime(end.strip(), '%Y-%m-%d')
            date_range_formatted = f"{start_date.strftime('%b %Y')} - {end_date.strftime('%b %Y')}"
        except:
            date_range_formatted = date_range
    else:
        date_range_formatted = date_range

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Buyer Persona Profiles - Final Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}

        .header {{
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }}

        .header h1 {{
            font-size: 36px;
            margin-bottom: 10px;
        }}

        .header p {{
            font-size: 16px;
            opacity: 0.95;
        }}

        .data-badge {{
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            margin-top: 10px;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        .tabs {{
            display: flex;
            background: #f8f9fa;
            border-bottom: 2px solid #e5e7eb;
        }}

        .tab {{
            flex: 1;
            padding: 16px 20px;
            background: none;
            border: none;
            cursor: pointer;
            font-size: 15px;
            font-weight: 600;
            color: #666;
            transition: all 0.3s ease;
            border-bottom: 3px solid transparent;
        }}

        .tab:hover {{
            background: #fff;
            color: #333;
        }}

        .tab.active {{
            background: white;
            color: #667eea;
            border-bottom-color: #667eea;
        }}

        .tab-content {{
            display: none;
            padding: 30px;
        }}

        .tab-content.active {{
            display: block;
        }}

        .segment-section {{
            margin-bottom: 30px;
        }}

        .segment-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 25px;
            border-radius: 8px;
            margin-bottom: 25px;
        }}

        .segment-title {{
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 5px;
        }}

        .segment-subtitle {{
            font-size: 16px;
            opacity: 0.9;
        }}

        .segment-section.digital .segment-header {{
            background: linear-gradient(135deg, #60A5FA 0%, #3B82F6 100%);
        }}

        .segment-section.smb .segment-header {{
            background: linear-gradient(135deg, #34D399 0%, #10B981 100%);
        }}

        .segment-section.commercial .segment-header {{
            background: linear-gradient(135deg, #FBBF24 0%, #F59E0B 100%);
        }}

        .segment-section.enterprise .segment-header {{
            background: linear-gradient(135deg, #A78BFA 0%, #8B5CF6 100%);
        }}

        .persona-card {{
            background: white;
            border-radius: 8px;
            margin-bottom: 25px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            border: 1px solid #e5e7eb;
            overflow: hidden;
        }}

        .persona-title {{
            font-size: 22px;
            font-weight: bold;
            color: white;
            padding: 16px 20px;
        }}

        .segment-section.digital .persona-title {{
            background: linear-gradient(135deg, #60A5FA 0%, #3B82F6 100%);
        }}

        .segment-section.smb .persona-title {{
            background: linear-gradient(135deg, #34D399 0%, #10B981 100%);
        }}

        .segment-section.commercial .persona-title {{
            background: linear-gradient(135deg, #FBBF24 0%, #F59E0B 100%);
        }}

        .segment-section.enterprise .persona-title {{
            background: linear-gradient(135deg, #A78BFA 0%, #8B5CF6 100%);
        }}

        .persona-content {{
            padding: 20px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 25px;
        }}

        .persona-column {{
            min-width: 0;
        }}

        .section-header {{
            font-size: 16px;
            font-weight: 700;
            margin: 15px 0 8px 0;
            padding-bottom: 4px;
            border-bottom: 2px solid #e5e7eb;
        }}

        .segment-section.digital .section-header {{
            color: #1E3A8A;
            border-bottom-color: #60A5FA;
        }}

        .segment-section.smb .section-header {{
            color: #065F46;
            border-bottom-color: #34D399;
        }}

        .segment-section.commercial .section-header {{
            color: #92400E;
            border-bottom-color: #FBBF24;
        }}

        .segment-section.enterprise .section-header {{
            color: #5B21B6;
            border-bottom-color: #A78BFA;
        }}

        .section-header:first-child {{
            margin-top: 0;
        }}

        .field-item {{
            margin: 8px 0;
            font-size: 14px;
            line-height: 1.6;
        }}

        .field-label {{
            font-weight: 600;
            color: #495057;
            margin-right: 8px;
        }}

        ul {{
            margin: 8px 0;
            padding-left: 20px;
        }}

        li {{
            margin: 6px 0;
            font-size: 14px;
            line-height: 1.6;
        }}

        .recommended-products {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-top: 10px;
            width: 100%;
        }}

        .product-card {{
            background: #f8f9fa;
            border-left: 4px solid #0275d8;
            padding: 14px;
            border-radius: 6px;
        }}

        .product-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}

        .product-name {{
            font-weight: 700;
            font-size: 15px;
            color: #11110D;
        }}

        .relevance-badge {{
            font-size: 11px;
            padding: 3px 10px;
            border-radius: 12px;
            font-weight: 600;
            text-transform: uppercase;
        }}

        .relevance-critical {{
            background: #dc3545;
            color: white;
        }}

        .relevance-high {{
            background: #ffc107;
            color: #333;
        }}

        .relevance-medium {{
            background: #17a2b8;
            color: white;
        }}

        .product-section {{
            margin-bottom: 10px;
        }}

        .product-section-title {{
            font-size: 11px;
            font-weight: 600;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
        }}

        .product-why {{
            font-size: 13px;
            color: #333;
            line-height: 1.6;
            font-weight: 500;
            margin-bottom: 8px;
        }}

        .product-challenge {{
            font-size: 13px;
            color: #555;
            line-height: 1.5;
            font-style: italic;
        }}

        /* Messaging Guide Card */
        .messaging-guide-card {{
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            border: 1px solid #e5e7eb;
            margin: 20px 0;
            padding: 20px;
        }}

        .messaging-guide-title {{
            font-size: 20px;
            font-weight: 700;
            color: #11110D;
            margin-bottom: 5px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .messaging-guide-subtitle {{
            font-size: 14px;
            color: #666;
            margin-bottom: 18px;
        }}

        .messaging-guide-content {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 18px;
            margin-bottom: 18px;
        }}

        .messaging-guide-column {{
            border-radius: 6px;
            padding: 16px;
        }}

        .messaging-guide-column.dos {{
            background: #f0f9f0;
            border-left: 4px solid #28a745;
        }}

        .messaging-guide-column.donts {{
            background: #fff5f5;
            border-left: 4px solid #dc3545;
        }}

        .messaging-guide-column-title {{
            font-size: 16px;
            font-weight: 700;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .messaging-guide-column.dos .messaging-guide-column-title {{
            color: #28a745;
        }}

        .messaging-guide-column.donts .messaging-guide-column-title {{
            color: #dc3545;
        }}

        .messaging-guide-list {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}

        .messaging-guide-list li {{
            font-size: 14px;
            line-height: 1.6;
            margin-bottom: 10px;
            color: #333;
        }}

        .messaging-guide-list li:last-child {{
            margin-bottom: 0;
        }}

        .messaging-guide-insight {{
            background: #fff9e6;
            border-left: 4px solid #ffc107;
            border-radius: 6px;
            padding: 14px 16px;
        }}

        .messaging-guide-insight-title {{
            font-size: 14px;
            font-weight: 700;
            color: #856404;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .messaging-guide-insight-text {{
            font-size: 14px;
            line-height: 1.6;
            color: #856404;
        }}

        /* Data Sources Tab */
        .data-sources {{
            max-width: 900px;
        }}

        .data-source-section {{
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
        }}

        .data-source-title {{
            font-size: 18px;
            font-weight: 700;
            color: #11110D;
            margin-bottom: 15px;
        }}

        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-top: 15px;
        }}

        .stat-card {{
            background: white;
            padding: 15px;
            border-radius: 6px;
            border: 1px solid #e5e7eb;
        }}

        .stat-number {{
            font-size: 28px;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 5px;
        }}

        .stat-label {{
            font-size: 13px;
            color: #666;
            font-weight: 500;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Buyer Persona Profiles</h1>
        <p>Data-Driven Customer Insights for Sales & Marketing</p>
        <div class="data-badge">Based on {total_calls_formatted} Gong Calls | {date_range_formatted}</div>
    </div>

    <div class="container">
        <div class="tabs" id="segmentTabs">
            <button class="tab active" onclick="switchTab('Digital', this)">Digital</button>
            <button class="tab" onclick="switchTab('SMB', this)">SMB</button>
            <button class="tab" onclick="switchTab('Commercial', this)">Commercial</button>
            <button class="tab" onclick="switchTab('Enterprise', this)">Enterprise</button>
            <button class="tab" onclick="switchTab('DataSources', this)">📊 Data Sources</button>
        </div>

        <div id="profilesContainer">
            <!-- Profiles will be injected here -->
        </div>
    </div>

    <script>
        const PERSONAS_DATA = ''' + json.dumps(personas) + ''';
        const PIPELINE_METADATA = ''' + json.dumps(pipeline_metadata) + ''';
        const SEGMENT_INSIGHTS = ''' + json.dumps(segment_insights) + ''';
        const EDITED_SECTIONS = ''' + json.dumps(list(edited_sections)) + ''';

        function getMessagingGuide(segment) {
            const guides = {
                'Digital': {
                    dos: [
                        '<strong>"Connect in minutes"</strong> - Emphasizes speed and simplicity',
                        '<strong>"No IT required"</strong> - Removes technical barriers',
                        '<strong>"Free for 14 days"</strong> - Low-risk trial language',
                        '<strong>"All-in-one platform"</strong> - Simplifies decision-making',
                        '<strong>"Live in 15 minutes"</strong> - Concrete, fast setup promise'
                    ],
                    donts: [
                        '<strong>"Enterprise-grade"</strong> - Too big/complex for their needs',
                        '<strong>"Comprehensive ecosystem"</strong> - Say "connects to your tools"',
                        '<strong>"Strategic partnership"</strong> - Use "support" or "help"',
                        '<strong>"Multi-year commitment"</strong> - Emphasize month-to-month',
                        '<strong>"Custom implementation"</strong> - Say "quick setup" or "ready to go"'
                    ],
                    keyInsight: 'Digital buyers (48% cite integration needs, 44% cost-pressured) want simple, fast, affordable. They\\'re often non-technical founders who need to get started today, not in 90 days.'
                },
                'SMB': {
                    dos: [
                        '<strong>"Automation"</strong> - More tangible than "AI" (your example!)',
                        '<strong>"30% productivity gain"</strong> - Concrete, measurable outcomes',
                        '<strong>"ROI in 6 months"</strong> - Fast payback that justifies budget',
                        '<strong>"Scale without hiring"</strong> - Addresses growth constraints',
                        '<strong>"Deflect 35% of tickets"</strong> - Specific efficiency metrics',
                        '<strong>"Live in 2-4 weeks"</strong> - Fast enough, but realistic'
                    ],
                    donts: [
                        '<strong>"AI-powered intelligence"</strong> - Too buzzwordy; say "smart automation"',
                        '<strong>"Digital transformation"</strong> - Too big and scary',
                        '<strong>"Strategic roadmap"</strong> - Use "plan" or "timeline"',
                        '<strong>"Best-in-class"</strong> - Vague superlatives; use proof points',
                        '<strong>"Ecosystem"</strong> - Say "integrations" or "connects to your tools"'
                    ],
                    keyInsight: 'SMB buyers (47% cost-pressured) respond to ROI-focused language. They want practical outcomes, not strategic visions. "Automation" resonates because it\\'s concrete; "AI" feels abstract.'
                },
                'Commercial': {
                    dos: [
                        '<strong>"AI"</strong> - They\\'re comfortable with technical terms',
                        '<strong>"Enterprise-grade"</strong> - Signals capability and scale',
                        '<strong>"40-60% automation rate"</strong> - Scaled impact metrics',
                        '<strong>"Multi-tier SLAs"</strong> - Shows sophistication',
                        '<strong>"Proven at 500+ agent deployments"</strong> - Scale validation'
                    ],
                    donts: [
                        '<strong>"Quick setup"</strong> - Sounds too simple for their complexity',
                        '<strong>"Easy to use"</strong> - They expect sophistication',
                        '<strong>"Small business"</strong> - They\\'re beyond this stage',
                        '<strong>"Basic features"</strong> - Emphasize advanced capabilities',
                        '<strong>"DIY"</strong> - They want professional implementation'
                    ],
                    keyInsight: 'Commercial buyers (62% cite integration needs) expect operational language. They\\'re solving process problems at scale, not just adding tools.'
                },
                'Enterprise': {
                    dos: [
                        '<strong>"Strategic transformation"</strong> - Board-level language',
                        '<strong>"SOC 2, ISO 27001, FedRAMP"</strong> - Compliance is critical',
                        '<strong>"18-24 month ROI"</strong> - Realistic enterprise timelines',
                        '<strong>"Fortune 500 scale"</strong> - Peer validation matters',
                        '<strong>"Board-ready analytics"</strong> - Executive stakeholder language'
                    ],
                    donts: [
                        '<strong>"Quick wins"</strong> - Too tactical; focus on strategic value',
                        '<strong>"Easy setup"</strong> - Enterprise deployments are complex',
                        '<strong>"Affordable"</strong> - Price isn\\'t the primary concern; value is',
                        '<strong>"Automation"</strong> - Say "AI" (they expect cutting-edge)',
                        '<strong>"Support team"</strong> - Say "global CX organization" or "service delivery"'
                    ],
                    keyInsight: 'Enterprise buyers (40% cite integration complexity, 38% cost pressure) speak in strategic terms. They\\'re justifying to boards and need governance, compliance, and transformation language.'
                }
            };
            return guides[segment];
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        /**
         * Apply cap to items array only if section was not manually edited
         */
        function applyItemCap(items, segment, personaName, field, maxItems = 5) {
            const sectionKey = `${segment}.${personaName}.${field}`;
            const isEdited = EDITED_SECTIONS.includes(sectionKey);

            if (isEdited) {
                // Section was manually edited - render all items without cap
                return items;
            } else {
                // Pipeline-generated section - apply cap
                return items.slice(0, maxItems);
            }
        }

        function renderProfiles() {
            const container = document.getElementById('profilesContainer');
            let html = '';

            const segmentInfo = {
                'Digital': { size: '≤49 employees', color: 'digital' },
                'SMB': { size: '50-249 employees', color: 'smb' },
                'Commercial': { size: '250-1,499 employees', color: 'commercial' },
                'Enterprise': { size: '1,500+ employees', color: 'enterprise' }
            };

            ['Digital', 'SMB', 'Commercial', 'Enterprise'].forEach((segment, index) => {
                const info = segmentInfo[segment];
                const isActive = index === 0 ? 'active' : '';

                html += `<div class="tab-content ${isActive}" id="tab-${segment}">`;
                html += `<div class="segment-section ${info.color}">`;
                html += `<div class="segment-header">`;
                html += `<div class="segment-title">${segment} Segment Personas</div>`;
                html += `<div class="segment-subtitle">Company Size: ${info.size}</div>`;
                html += `</div>`;

                // Add Messaging Guide
                const messagingGuide = getMessagingGuide(segment);
                if (messagingGuide) {
                    html += `<div class="messaging-guide-card">`;
                    html += `<div class="messaging-guide-title">💬 Messaging Dos & Don'ts for ${segment}</div>`;
                    html += `<div class="messaging-guide-subtitle">Language that resonates (and doesn't) with ${segment} buyers</div>`;
                    html += `<div class="messaging-guide-content">`;

                    // DOs column
                    html += `<div class="messaging-guide-column dos">`;
                    html += `<div class="messaging-guide-column-title">✅ DO Use This Language</div>`;
                    html += `<ul class="messaging-guide-list">`;
                    messagingGuide.dos.forEach(item => {
                        html += `<li>${item}</li>`;
                    });
                    html += `</ul>`;
                    html += `</div>`;

                    // DON'Ts column
                    html += `<div class="messaging-guide-column donts">`;
                    html += `<div class="messaging-guide-column-title">❌ DON'T Use This Language</div>`;
                    html += `<ul class="messaging-guide-list">`;
                    messagingGuide.donts.forEach(item => {
                        html += `<li>${item}</li>`;
                    });
                    html += `</ul>`;
                    html += `</div>`;

                    html += `</div>`; // close messaging-guide-content

                    // Key Insight
                    html += `<div class="messaging-guide-insight">`;
                    html += `<div class="messaging-guide-insight-title">💡 Key Insight</div>`;
                    html += `<div class="messaging-guide-insight-text">${messagingGuide.keyInsight}</div>`;
                    html += `</div>`;

                    html += `</div>`; // close messaging-guide-card
                }

                // Add Competitive Landscape if available (limit to top 5)
                const segmentData = SEGMENT_INSIGHTS[segment];
                if (segmentData && segmentData.competitive_landscape && segmentData.competitive_landscape.length > 0) {
                    html += `<div class="messaging-guide-card">`;
                    html += `<div class="messaging-guide-title">🎯 Competitive Landscape for ${segment}</div>`;
                    html += `<div class="messaging-guide-subtitle">Key competitors and how to position against them</div>`;
                    html += `<div style="margin-top: 15px;">`;

                    // Show top 5 competitors only
                    const topCompetitors = segmentData.competitive_landscape.slice(0, 5);

                    topCompetitors.forEach(comp => {
                        const threatLevel = comp.threat_level || 'Medium';
                        const threatColor = threatLevel === 'High' || threatLevel === 'Very High' ? '#dc2626' :
                                          threatLevel === 'Medium' ? '#f59e0b' : '#6b7280';
                        html += `<div style="background: #f9fafb; border-left: 4px solid ${threatColor}; padding: 14px; margin-bottom: 12px; border-radius: 6px;">`;
                        html += `<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">`;
                        html += `<div style="font-size: 16px; font-weight: 700; color: #111827;">${escapeHtml(comp.competitor)}</div>`;
                        html += `<div style="font-size: 12px; font-weight: 600; padding: 3px 8px; border-radius: 12px; background: ${threatColor}; color: white;">${escapeHtml(threatLevel)} Threat</div>`;
                        html += `</div>`;
                        const why = comp.common_comparisons || comp.context || '';
                        const counter = comp.zendesk_differentiator || comp.positioning || '';
                        if (why) html += `<div style="font-size: 14px; color: #4b5563; margin-bottom: 6px;"><strong>Why they compete:</strong> ${escapeHtml(why)}</div>`;
                        if (counter) html += `<div style="font-size: 14px; color: #0275d8;"><strong>How to counter:</strong> ${escapeHtml(counter)}</div>`;
                        html += `</div>`;
                    });

                    html += `</div>`;
                    html += `</div>`; // close messaging-guide-card
                }

                Object.keys(PERSONAS_DATA[segment]).forEach(personaName => {
                    const persona = PERSONAS_DATA[segment][personaName];
                    html += `<div class="persona-card">`;
                    html += `<div class="persona-title">${personaName}</div>`;
                    html += `<div class="persona-content">`;

                    // LEFT COLUMN
                    html += `<div class="persona-column">`;
                    html += `<div class="section-header">Profile Overview</div>`;
                    html += `<div class="field-item"><span class="field-label">Job Titles:</span>${escapeHtml(persona.job_titles.join(', '))}</div>`;
                    html += `<div class="field-item"><span class="field-label">Reports To:</span>${escapeHtml(persona.reports_to)}</div>`;
                    html += `<div class="field-item"><span class="field-label">Team Size:</span>${escapeHtml(persona.team_size)}</div>`;
                    html += `<div class="field-item"><span class="field-label">Prevalence in Deals:</span>${escapeHtml(persona.prevalence)}</div>`;
                    html += `<div class="field-item"><span class="field-label">Role in Buying Process:</span>${escapeHtml(persona.role_in_deal)}</div>`;

                    // SECTION 2: Pain Points (max 5 unless edited)
                    html += `<div class="section-header">😓 Pain Points</div>`;
                    html += '<ul>';
                    const painPoints = persona.challenges || persona.challenges_from_gong || [];
                    applyItemCap(painPoints, segment, personaName, 'challenges').forEach(pain => { html += `<li>${escapeHtml(pain)}</li>`; });
                    html += '</ul>';

                    // SECTION 3: Goals (max 5 unless edited)
                    html += `<div class="section-header">🎯 Goals</div>`;
                    html += '<ul>';
                    applyItemCap(persona.goals, segment, personaName, 'goals').forEach(goal => { html += `<li>${escapeHtml(goal)}</li>`; });
                    html += '</ul>';

                    // SECTION 4: Objections (max 5 unless edited)
                    html += `<div class="section-header">⚠️ Objections</div>`;
                    html += '<ul>';
                    applyItemCap(persona.objections, segment, personaName, 'objections').forEach(objection => { html += `<li>${escapeHtml(objection)}</li>`; });
                    html += '</ul>';

                    // SECTION 5: Trigger Events (max 5 unless edited)
                    if (persona.trigger_events_enhanced && persona.trigger_events_enhanced.length > 0) {
                        html += `<div class="section-header">🔔 Trigger Events</div>`;
                        html += '<ul>';
                        applyItemCap(persona.trigger_events_enhanced, segment, personaName, 'trigger_events_enhanced').forEach(trigger => {
                            const text = typeof trigger === 'string' ? trigger : trigger.text;
                            const frequency = trigger.frequency || 0;
                            html += `<li>${escapeHtml(text)}${frequency > 0 ? ` <span style="color: #7f8c8d; font-size: 0.9em;">(${frequency} mentions)</span>` : ''}</li>`;
                        });
                        html += '</ul>';
                    }
                    html += `</div>`; // left column

                    // RIGHT COLUMN
                    html += `<div class="persona-column">`;

                    // SECTION 6: Success Metrics (max 5 unless edited)
                    html += `<div class="section-header">📊 Success Metrics</div>`;
                    html += '<ul>';
                    const metrics = persona.success_metrics_enhanced || persona.success_metrics || [];
                    applyItemCap(metrics, segment, personaName, 'success_metrics').forEach(metric => {
                        const text = typeof metric === 'string' ? metric : metric.text;
                        const frequency = metric.frequency || 0;
                        html += `<li>${escapeHtml(text)}${frequency > 0 ? ` <span style="color: #7f8c8d; font-size: 0.9em;">(${frequency} mentions)</span>` : ''}</li>`;
                    });
                    html += '</ul>';

                    // SECTION 7: Product Requirements (max 5 unless edited)
                    if (persona.product_requirements_enhanced && persona.product_requirements_enhanced.length > 0) {
                        html += `<div class="section-header">✅ Product Requirements</div>`;
                        html += '<ul>';
                        applyItemCap(persona.product_requirements_enhanced, segment, personaName, 'product_requirements_enhanced').forEach(req => {
                            const text = typeof req === 'string' ? req : req.text;
                            const frequency = req.frequency || 0;
                            html += `<li>${escapeHtml(text)}${frequency > 0 ? ` <span style="color: #7f8c8d; font-size: 0.9em;">(${frequency} mentions)</span>` : ''}</li>`;
                        });
                        html += '</ul>';
                    }

                    // SECTION 8: Information Sources (max 5 unless edited)
                    if (persona.information_sources_enhanced && persona.information_sources_enhanced.length > 0) {
                        html += `<div class="section-header">📚 Information Sources</div>`;
                        html += '<ul>';
                        applyItemCap(persona.information_sources_enhanced, segment, personaName, 'information_sources_enhanced').forEach(source => {
                            const text = typeof source === 'string' ? source : source.text;
                            const frequency = source.frequency || 0;
                            html += `<li>${escapeHtml(text)}${frequency > 0 ? ` <span style="color: #7f8c8d; font-size: 0.9em;">(${frequency} mentions)</span>` : ''}</li>`;
                        });
                        html += '</ul>';
                    }

                    // SECTION 9: Messaging Preferences (max 5 unless edited)
                    if (persona.messaging_preferences_enhanced && persona.messaging_preferences_enhanced.length > 0) {
                        html += `<div class="section-header">💬 Messaging Preferences</div>`;
                        html += '<ul>';
                        applyItemCap(persona.messaging_preferences_enhanced, segment, personaName, 'messaging_preferences_enhanced').forEach(pref => {
                            const text = typeof pref === 'string' ? pref : pref.text;
                            const frequency = pref.frequency || 0;
                            html += `<li>${escapeHtml(text)}${frequency > 0 ? ` <span style="color: #7f8c8d; font-size: 0.9em;">(${frequency} mentions)</span>` : ''}</li>`;
                        });
                        html += '</ul>';
                    }

                    // SECTION 10: Key Messages to Land (max 5 unless edited)
                    if (persona.key_messages && persona.key_messages.length > 0) {
                        html += `<div class="section-header">✉️ Key Messages to Land</div>`;
                        html += '<ul>';
                        applyItemCap(persona.key_messages, segment, personaName, 'key_messages').forEach(message => {
                            html += `<li>${escapeHtml(message)}</li>`;
                        });
                        html += '</ul>';
                    }

                    html += `</div>`; // right column
                    html += `</div>`; // persona-content

                    // SECTION 10: Verbatim Quotes (max 5)
                    const allQuotes = [];
                    // Extract quotes from enhanced fields
                    const enhancedFields = [
                        persona.trigger_events_enhanced,
                        persona.success_metrics_enhanced,
                        persona.product_requirements_enhanced,
                        persona.information_sources_enhanced,
                        persona.messaging_preferences_enhanced
                    ];
                    enhancedFields.forEach(field => {
                        if (field && Array.isArray(field)) {
                            field.forEach(item => {
                                if (item.verbatim_quotes && Array.isArray(item.verbatim_quotes)) {
                                    item.verbatim_quotes.forEach(quoteObj => {
                                        if (quoteObj.quote && quoteObj.quote.length > 20) {
                                            allQuotes.push(quoteObj.quote);
                                        }
                                    });
                                }
                            });
                        }
                    });
                    // Get unique quotes and limit to 5
                    const uniqueQuotes = [...new Set(allQuotes)].slice(0, 5);
                    if (uniqueQuotes.length > 0) {
                        html += `<div style="padding: 0 20px 10px 20px;">`;
                        html += `<div class="section-header">🗣️ Verbatim Quotes</div>`;
                        uniqueQuotes.forEach(quote => {
                            html += `<div style="margin: 12px 0; padding: 12px 16px; background: #f8f9fa; border-left: 4px solid #3498db; border-radius: 4px; font-style: italic; color: #555; font-size: 14px;">"${escapeHtml(quote)}"</div>`;
                        });
                        html += `</div>`;
                    }

                    // Recommended Products
                    if (persona.recommended_products && persona.recommended_products.length > 0) {
                        html += `<div style="padding: 0 20px 20px 20px;">`;
                        html += `<div class="section-header">🎯 Recommended Zendesk Products</div>`;
                        html += `<div class="recommended-products">`;
                        persona.recommended_products.forEach((product, idx) => {
                            html += '<div class="product-card">';
                            html += '<div class="product-header">' +
                                '<span class="product-name">' + escapeHtml(product.zendesk_name) + '</span>' +
                                '<span class="relevance-badge relevance-' + product.relevance.toLowerCase() + '">' + escapeHtml(product.relevance) + '</span>' +
                            '</div>';
                            html += '<div class="product-section">';
                            html += '<div class="product-section-title">💡 Why This Matters</div>';
                            html += '<div class="product-why">' + escapeHtml(product.why) + '</div>';
                            html += '</div>';
                            html += '<div class="product-section">';
                            html += '<div class="product-section-title">🗣️ Customer Says</div>';
                            html += '<div class="product-challenge">"' + escapeHtml(product.addresses_challenge) + '"</div>';
                            html += '</div>';
                            html += '</div>';
                        });
                        html += `</div>`;
                        html += `</div>`;
                    }

                    html += `</div>`; // persona-card
                });

                html += `</div>`; // segment-section
                html += `</div>`; // tab-content
            });

            // Data Sources Tab
            html += `<div class="tab-content" id="tab-DataSources">`;
            html += `<div class="data-sources">`;
            html += `<h2 style="margin-bottom: 20px; color: #11110D;">📊 Data Sources & Methodology</h2>`;

            // Extract metadata for dynamic values
            const gongData = PIPELINE_METADATA?.data_sources?.gong || {};
            const claudeData = PIPELINE_METADATA?.data_sources?.claude_analysis || {};
            const totalCalls = (gongData.calls_analyzed || 69711).toLocaleString();
            const dateRange = gongData.date_range ? gongData.date_range.replace(' to ', ' - ') : 'Oct 2025 - Apr 2026';
            const claudeModel = claudeData.model || 'claude-3-5-sonnet-20241022';

            html += `<div class="data-source-section">`;
            html += `<div class="data-source-title">🎧 Primary Source: Gong Call Analysis</div>`;
            html += `<p style="margin-bottom: 15px; line-height: 1.6;">All persona insights are derived from analyzing ${totalCalls} sales and customer success calls captured in Gong (${dateRange}).</p>`;
            html += `<div class="stat-grid">`;
            html += `<div class="stat-card"><div class="stat-number">${totalCalls}</div><div class="stat-label">Total Calls Analyzed</div></div>`;
            html += `<div class="stat-card"><div class="stat-number">${dateRange}</div><div class="stat-label">Analysis Period</div></div>`;
            html += `</div>`;
            html += `</div>`;

            html += `<div class="data-source-section" style="border-left-color: #34D399;">`;
            html += `<div class="data-source-title">🔍 Analysis Methodology</div>`;
            html += `<ul style="margin-left: 20px; line-height: 1.8;">`;
            html += `<li><strong>Claude AI Analysis:</strong> Analysis powered by ${claudeModel}, which provides deep contextual understanding of conversation patterns, pain points, objections, and buying signals rather than keyword-based matching</li>`;
            html += `<li><strong>Data Pre-filtering:</strong> Transcripts filtered for customer speech only (English, non-representative, minimum word count, business context) to ensure signal quality</li>`;
            html += `<li><strong>Pattern Recognition:</strong> Claude identified recurring themes across thousands of conversations within each segment, with consistency assessed across multiple transcript batches</li>`;
            html += `<li><strong>Third-party Research Integration:</strong> Supplementary inputs from analyst research integrated into sections including Information Sources, Messaging Preferences, and Competitive Landscape</li>`;
            html += `<li><strong>Signal Strength:</strong> Insights rated as strong/moderate/weak based on consistency of patterns across transcript batches as assessed by Claude</li>`;
            html += `</ul>`;
            html += `</div>`;

            // Secondary Sources & References
            const researchSources = PIPELINE_METADATA?.data_sources?.third_party_research || [];
            html += `<div class="data-source-section" style="border-left-color: #8B5CF6;">`;
            html += `<div class="data-source-title">📚 Secondary Sources & References</div>`;
            if (researchSources.length > 0) {
                html += `<ul style="margin-left: 20px; line-height: 1.8;">`;
                researchSources.forEach(source => {
                    const title = source.title || source.name || 'Research Source';
                    const org = source.organization || source.source || '';
                    const date = source.date || '';
                    html += `<li><strong>${escapeHtml(title)}</strong>`;
                    if (org) html += ` (${escapeHtml(org)})`;
                    if (date) html += ` - ${escapeHtml(date)}`;
                    html += `</li>`;
                });
                html += `</ul>`;
            } else {
                html += `<p style="line-height: 1.6; color: #6b7280;">No third party research sources loaded for this pipeline run. Analysis is based solely on Gong call data and Claude AI interpretation.</p>`;
            }
            html += `</div>`;

            html += `<div class="data-source-section" style="border-left-color: #FBBF24;">`;
            html += `<div class="data-source-title">🔄 Refresh Cadence</div>`;
            html += `<p style="line-height: 1.6;">These personas are refreshed quarterly to ensure insights remain current with evolving market conditions and customer needs.</p>`;
            html += `<div style="margin-top: 15px; padding: 12px; background: white; border-radius: 6px; border: 1px solid #e5e7eb;">`;
            html += `<strong>Last Updated:</strong> ${new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}<br>`;
            html += `<strong>Next Refresh:</strong> July 1, 2026 (Q2 2026 data)`;
            html += `</div>`;
            html += `</div>`;

            html += `</div>`; // data-sources
            html += `</div>`; // tab-content

            container.innerHTML = html;
        }

        function switchTab(segment, clickedButton) {
            // Update tab buttons
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            if (clickedButton) {
                clickedButton.classList.add('active');
            }

            // Update tab content
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            document.getElementById('tab-' + segment).classList.add('active');
        }

        // Initialize on load
        renderProfiles();
    </script>
</body>
</html>
'''

    return html


def main():
    print("\n🎨 Generating Final Clean Persona Profiles")
    print("=" * 80)

    html = generate_final_html()

    output_file = BASE_DIR / "reports" / "Persona_Profiles_FINAL.html"
    with open(output_file, 'w') as f:
        f.write(html)

    print(f"✓ Final clean report generated")
    print(f"📍 Location: {output_file}")
    print(f"\nThis is what stakeholders see as the final deliverable.")
    print(f"No voting, no comments - just clean, professional persona profiles.")
    print("=" * 80)


if __name__ == "__main__":
    main()
