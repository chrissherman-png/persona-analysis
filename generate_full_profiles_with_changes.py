"""
Team Review Generator - Collaborative Persona Review with Real-Time Feedback
Extends the Final/Stakeholder page with voting, comments, and change tracking
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import the Final page generator (source of truth for design)
from generate_final_clean_personas import generate_final_html

# =============================================================================
# GOOGLE SHEETS CONFIGURATION
# =============================================================================
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwg4G6Mm2934GC3o3VHHjkHJFce3tjnNproUZkHl6teY9DBwmbznn3zoSG7sBGxRKbpPA/exec"
SHEET_ID = "1S4ePwUL3wCA84frDlO7G0sGLSwY64YIrKJJAA6G9ok0"


class CollaborativePersonaGenerator:
    """Extends Final page with collaborative features for team review"""

    def __init__(self, base_dir=None):
        if base_dir is None:
            base_dir = str(Path(__file__).parent)
        self.base_dir = Path(base_dir)
        self.versions_dir = self.base_dir / "versions"
        self.reports_dir = self.base_dir / "reports"
        self.data_dir = self.base_dir / "data"

        self.versions_dir.mkdir(exist_ok=True)
        self.reports_dir.mkdir(exist_ok=True)

        # Load change data
        self.changes_data = self.load_changes_data()
        self.change_reasons = self.load_change_reasons()
        self.pipeline_metadata = self.load_pipeline_metadata()

    def load_changes_data(self) -> List[Dict]:
        """Load changes detected by the pipeline"""
        # Changes are stored in pending_changes directory with date-stamped filenames
        pending_dir = self.base_dir / "pending_changes"
        if pending_dir.exists():
            # Get most recent changes file
            changes_files = sorted(pending_dir.glob("changes_*.json"), reverse=True)
            if changes_files:
                with open(changes_files[0], 'r') as f:
                    data = json.load(f)
                    return data.get('changes', [])
        return []

    def load_change_reasons(self) -> Dict:
        """Load change reasons generated during persona update"""
        reasons_file = self.data_dir / "change_reasons.json"
        if reasons_file.exists():
            with open(reasons_file, 'r') as f:
                return json.load(f)
        return {}

    def load_pipeline_metadata(self) -> Dict:
        """Load pipeline run metadata"""
        metadata_file = self.base_dir / "pipeline_run_metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                return json.load(f)
        return {}

    def generate_collaborative_features(self) -> str:
        """Generate JavaScript for collaborative features (voting, comments, change tracking)"""

        # Get run_quarter from metadata
        run_quarter = self.pipeline_metadata.get('run_quarter', 'Q2 2026')

        # Prepare data for injection
        # Note: PERSONAS_DATA, SEGMENT_INSIGHTS, and PIPELINE_METADATA are already
        # declared by the Final page template, so we only declare Team Review-specific data
        changes_json = json.dumps(self.changes_data)
        reasons_json = json.dumps(self.change_reasons)

        js_code = f"""
    <!-- COLLABORATIVE FEATURES - TEAM REVIEW ONLY -->
    <script>
        // Configuration
        const APPS_SCRIPT_URL = "{APPS_SCRIPT_URL}";
        const SHEET_ID = "{SHEET_ID}";
        const RUN_QUARTER = "{run_quarter}";

        // Team Review-specific data (PERSONAS_DATA, SEGMENT_INSIGHTS, PIPELINE_METADATA already declared by Final page)
        const CHANGE_REASONS = {reasons_json};

        console.log('Team Review Mode: Collaborative features enabled');
        console.log('CHANGE_REASONS:', Object.keys(CHANGE_REASONS).length, 'reasons');
        console.log('Run Quarter:', RUN_QUARTER);
        console.log('Inherited from Final page: PERSONAS_DATA, SEGMENT_INSIGHTS, PIPELINE_METADATA');

        // =================================================================
        // STEP 2.1: CHANGE TRACKING INDICATORS
        // =================================================================

        // Add CSS for change badges (scoped to Team Review only)
        const changeBadgeStyles = document.createElement('style');
        changeBadgeStyles.textContent = `
            .team-review-change-badge {{
                display: inline-block;
                margin-left: 8px;
                padding: 2px 8px;
                border-radius: 12px;
                font-size: 11px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s;
            }}
            .team-review-change-badge:hover {{
                transform: scale(1.1);
            }}
            .team-review-change-badge.new {{
                background: #d1fae5;
                color: #065f46;
                border: 1px solid #10b981;
            }}
            .team-review-change-badge.updated {{
                background: #fef3c7;
                color: #92400e;
                border: 1px solid #f59e0b;
            }}
            .team-review-change-badge.deleted {{
                background: #fee2e2;
                color: #991b1b;
                border: 1px solid #ef4444;
            }}
            .team-review-change-tooltip {{
                display: none;
                position: absolute;
                bottom: 100%;
                left: 50%;
                transform: translateX(-50%);
                background: #1f2937;
                color: white;
                padding: 12px;
                border-radius: 6px;
                font-size: 13px;
                white-space: normal;
                max-width: 300px;
                margin-bottom: 8px;
                z-index: 1000;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                line-height: 1.4;
            }}
            .team-review-change-badge:hover .team-review-change-tooltip {{
                display: block;
            }}
            .team-review-change-tooltip::after {{
                content: '';
                position: absolute;
                top: 100%;
                left: 50%;
                transform: translateX(-50%);
                border: 6px solid transparent;
                border-top-color: #1f2937;
            }}
        `;
        document.head.appendChild(changeBadgeStyles);

        /**
         * Find change reason and type for a specific item by its index
         * Uses CHANGE_REASONS which has keys like "SMB.CX Champion.goals[0]"
         */
        function findChangeForItem(segment, persona, section, itemIndex) {{
            // Build the key to look up in CHANGE_REASONS
            // Note: section is already the underscore version (e.g., "pain_points")
            const key = `${{segment}}.${{persona}}.${{section}}[${{itemIndex}}]`;
            const reason = CHANGE_REASONS[key];

            if (!reason) return null;

            // Parse the reason to determine change type
            let changeType = 'kept';
            if (reason.startsWith('ADDED:')) {{
                changeType = 'added';
            }} else if (reason.startsWith('UPDATED:')) {{
                changeType = 'modified';
            }} else if (reason.startsWith('KEPT:')) {{
                changeType = 'kept';
            }}

            return {{
                type: changeType,
                reason: reason,
                key: key
            }};
        }}

        /**
         * Add change tracking indicators to all persona items
         */
        function addChangeIndicators() {{
            // Guard: Only run on Team Review page
            if (typeof CHANGE_REASONS === 'undefined') {{
                return;
            }}

            console.log('=== CHANGE INDICATOR DEBUG ===');
            console.log('Using CHANGE_REASONS for badge matching');
            console.log('Total change reasons:', Object.keys(CHANGE_REASONS).length);
            console.log('Sample keys:', Object.keys(CHANGE_REASONS).slice(0, 3));

            let matchAttempts = 0;
            let successfulMatches = 0;

            // Find all persona cards
            const cards = document.querySelectorAll('.persona-card');
            console.log('Found persona cards:', cards.length);

            cards.forEach(card => {{
                const personaTitle = card.querySelector('.persona-title');
                if (!personaTitle) return;

                const personaName = personaTitle.textContent.trim();

                // Find which segment this persona belongs to
                let segment = null;
                const segmentSection = card.closest('.tab-content');
                if (segmentSection) {{
                    const segmentId = segmentSection.id;
                    if (segmentId.includes('Digital')) segment = 'Digital';
                    else if (segmentId.includes('SMB')) segment = 'SMB';
                    else if (segmentId.includes('Commercial')) segment = 'Commercial';
                    else if (segmentId.includes('Enterprise')) segment = 'Enterprise';
                }}

                if (!segment) {{
                    console.log('⚠️ Could not determine segment for persona:', personaName);
                    return;
                }}

                console.log('Processing:', segment, '-', personaName);

                // Process each section in the persona card
                const sectionHeaders = card.querySelectorAll('.section-header');
                console.log('  Found section headers:', sectionHeaders.length);

                sectionHeaders.forEach(sectionHeader => {{
                    const sectionName = sectionHeader.textContent.trim();

                    // Map display section headers to change_reasons field names
                    // Note: Section headers include emojis, change_reasons uses the actual data field names
                    const sectionText = sectionName.replace(/^[^a-zA-Z]+/, '').trim();
                    const fieldMap = {{
                        'Pain Points': 'challenges',  // Pain Points section displays "challenges" field
                        'Goals': 'goals',
                        'Objections': 'objections',
                        'Success Metrics': 'success_metrics',
                        'Product Requirements': 'product_requirements',
                        'Information Sources': 'information_sources',
                        'Messaging Preferences': 'messaging_preferences',
                        'Key Messages to Land': 'key_messages',
                        'Key Messages': 'key_messages'
                    }};

                    const fieldName = fieldMap[sectionText];
                    if (!fieldName) {{
                        console.log('  ⚠️ No field mapping for section:', sectionName, '→', sectionText);
                        return;
                    }}

                    console.log('  Section:', sectionText, '→ field:', fieldName);

                    // Find list items in this section
                    let currentElement = sectionHeader.nextElementSibling;
                    let itemsInSection = 0;
                    while (currentElement && !currentElement.classList.contains('section-header')) {{
                        if (currentElement.tagName === 'UL') {{
                            const listItems = currentElement.querySelectorAll('li');
                            itemsInSection += listItems.length;

                            listItems.forEach((li, itemIndex) => {{
                                matchAttempts++;
                                const itemText = li.textContent.trim();
                                const change = findChangeForItem(segment, personaName, fieldName, itemIndex);

                                if (change && change.type !== 'kept') {{
                                    successfulMatches++;
                                    console.log('    ✓ MATCH:', change.key, '→', change.type);
                                    // Determine badge type
                                    let badgeType = 'updated';
                                    let badgeText = '🟡 UPDATED';
                                    if (change.type === 'added') {{
                                        badgeType = 'new';
                                        badgeText = '🟢 NEW';
                                    }} else if (change.type === 'modified') {{
                                        badgeType = 'updated';
                                        badgeText = '🟡 UPDATED';
                                    }}

                                    const reason = change.reason;

                                    // Create badge with tooltip
                                    const badge = document.createElement('span');
                                    badge.className = `team-review-change-badge ${{badgeType}}`;
                                    badge.innerHTML = `
                                        ${{badgeText}}
                                        <span class="team-review-change-tooltip">${{reason}}</span>
                                    `;
                                    badge.style.position = 'relative';

                                    li.appendChild(badge);
                                }}
                            }});
                        }}
                        currentElement = currentElement.nextElementSibling;
                    }}

                    if (itemsInSection > 0) {{
                        console.log('    Processed', itemsInSection, 'items in', sectionText);
                    }}
                }});
            }});

            const badgeCount = document.querySelectorAll('.team-review-change-badge').length;
            console.log('=== SUMMARY ===');
            console.log('Match attempts:', matchAttempts);
            console.log('Successful matches:', successfulMatches);
            console.log('Badges in DOM:', badgeCount);
            console.log('Test selector: document.querySelectorAll(".team-review-change-badge").length');
        }}

        // Run change indicators after DOM loads
        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', addChangeIndicators);
        }} else {{
            addChangeIndicators();
        }}

        // =================================================================
        // STEP 2.3: VOTING BUTTONS
        // =================================================================

        // Add CSS for voting buttons and sync indicator
        const votingStyles = document.createElement('style');
        votingStyles.textContent = `
            .team-review-vote-container {{
                display: inline-flex;
                align-items: center;
                gap: 4px;
                margin-left: 12px;
                font-size: 14px;
            }}
            .team-review-vote-btn {{
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                padding: 4px 8px;
                cursor: pointer;
                font-size: 16px;
                transition: all 0.2s;
                display: inline-flex;
                align-items: center;
                gap: 4px;
            }}
            .team-review-vote-btn:hover:not(:disabled) {{
                background: #f3f4f6;
                transform: scale(1.05);
            }}
            .team-review-vote-btn:disabled {{
                opacity: 0.5;
                cursor: not-allowed;
            }}
            .team-review-vote-btn.active {{
                border-color: #3b82f6;
                background: #eff6ff;
            }}
            .team-review-vote-count {{
                font-size: 12px;
                color: #6b7280;
                font-weight: 500;
            }}
            .team-review-sync-status {{
                position: fixed;
                top: 10px;
                right: 10px;
                padding: 8px 16px;
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 500;
                display: flex;
                align-items: center;
                gap: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                z-index: 1000;
            }}
            .team-review-sync-status.online {{
                border-color: #10b981;
                background: #f0fdf4;
            }}
            .team-review-sync-status.offline {{
                border-color: #ef4444;
                background: #fef2f2;
            }}
            .team-review-vote-loading {{
                opacity: 0.6;
                pointer-events: none;
            }}
            .team-review-file-protocol-banner {{
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                background: #fef3c7;
                border-bottom: 2px solid #f59e0b;
                padding: 16px;
                text-align: center;
                font-size: 14px;
                z-index: 2000;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            .team-review-file-protocol-banner strong {{
                color: #92400e;
            }}
            .team-review-file-protocol-banner code {{
                background: white;
                padding: 2px 8px;
                border-radius: 4px;
                font-family: monospace;
                font-size: 13px;
            }}
        `;
        document.head.appendChild(votingStyles);

        // =================================================================
        // STEP 2.4: COMMENT BUTTONS
        // =================================================================

        // Add CSS for comment buttons and modal
        const commentStyles = document.createElement('style');
        commentStyles.textContent = `
            .team-review-comment-btn {{
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                padding: 4px 8px;
                cursor: pointer;
                font-size: 16px;
                transition: all 0.2s;
                display: inline-flex;
                align-items: center;
                gap: 4px;
                margin-left: 4px;
            }}
            .team-review-comment-btn:hover {{
                background: #f3f4f6;
                transform: scale(1.05);
            }}
            .team-review-comment-btn.has-comments {{
                background: #dbeafe;
                border-color: #3b82f6;
            }}
            .team-review-comment-count {{
                font-size: 12px;
                color: #6b7280;
                font-weight: 500;
            }}
            .team-review-comment-modal-overlay {{
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.5);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 10000;
                padding: 20px;
            }}
            .team-review-comment-modal {{
                background: white;
                border-radius: 12px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                max-width: 600px;
                width: 100%;
                max-height: 80vh;
                display: flex;
                flex-direction: column;
            }}
            .team-review-comment-modal-header {{
                padding: 20px;
                border-bottom: 1px solid #e5e7eb;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 12px 12px 0 0;
            }}
            .team-review-comment-modal-title {{
                font-size: 18px;
                font-weight: 600;
                margin: 0 0 8px 0;
            }}
            .team-review-comment-modal-subtitle {{
                font-size: 14px;
                opacity: 0.9;
                margin: 0;
                line-height: 1.4;
            }}
            .team-review-comment-modal-body {{
                padding: 20px;
                overflow-y: auto;
                flex: 1;
            }}
            .team-review-comment-thread {{
                margin-bottom: 20px;
            }}
            .team-review-comment-item {{
                background: #f9fafb;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 12px;
                margin-bottom: 12px;
            }}
            .team-review-comment-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 8px;
            }}
            .team-review-comment-author {{
                font-weight: 600;
                color: #1f2937;
                font-size: 14px;
            }}
            .team-review-comment-timestamp {{
                font-size: 12px;
                color: #6b7280;
            }}
            .team-review-comment-text {{
                color: #374151;
                font-size: 14px;
                line-height: 1.5;
                white-space: pre-wrap;
                word-wrap: break-word;
            }}
            .team-review-comment-empty {{
                text-align: center;
                color: #9ca3af;
                font-size: 14px;
                padding: 40px 20px;
            }}
            .team-review-comment-input-section {{
                border-top: 1px solid #e5e7eb;
                padding: 16px;
            }}
            .team-review-comment-input {{
                width: 100%;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                font-family: inherit;
                resize: vertical;
                min-height: 80px;
                margin-bottom: 12px;
            }}
            .team-review-comment-input:focus {{
                outline: none;
                border-color: #3b82f6;
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
            }}
            .team-review-comment-actions {{
                display: flex;
                justify-content: flex-end;
                gap: 8px;
            }}
            .team-review-comment-btn-primary {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: 500;
                cursor: pointer;
                transition: transform 0.2s;
            }}
            .team-review-comment-btn-primary:hover {{
                transform: scale(1.05);
            }}
            .team-review-comment-btn-secondary {{
                background: white;
                color: #6b7280;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.2s;
            }}
            .team-review-comment-btn-secondary:hover {{
                background: #f3f4f6;
            }}
            .team-review-comment-delete {{
                background: none;
                border: none;
                color: #ef4444;
                cursor: pointer;
                font-size: 16px;
                padding: 0;
                margin-left: 8px;
                opacity: 0.6;
                transition: opacity 0.2s;
            }}
            .team-review-comment-delete:hover {{
                opacity: 1;
            }}
            .team-review-comment-delete-confirm {{
                margin-top: 8px;
                padding: 8px;
                background: #fef2f2;
                border: 1px solid #fecaca;
                border-radius: 4px;
                font-size: 13px;
            }}
            .team-review-comment-delete-confirm button {{
                margin-left: 8px;
                padding: 4px 12px;
                border-radius: 4px;
                font-size: 12px;
                cursor: pointer;
                border: none;
            }}
            .team-review-comment-delete-confirm .yes {{
                background: #ef4444;
                color: white;
            }}
            .team-review-comment-delete-confirm .cancel {{
                background: #e5e7eb;
                color: #374151;
            }}
        `;
        document.head.appendChild(commentStyles);

        // =================================================================
        // STEP 2.5: UPDATE LIVE VERSION BUTTON
        // =================================================================

        const updateLiveStyles = document.createElement('style');
        updateLiveStyles.textContent = `
            .team-review-update-btn {{
                position: fixed;
                bottom: 24px;
                right: 24px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 16px 24px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
                transition: transform 0.2s, box-shadow 0.2s;
                z-index: 9999;
                display: flex;
                align-items: center;
                gap: 8px;
            }}
            .team-review-update-btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 12px 32px rgba(102, 126, 234, 0.5);
            }}
            .team-review-update-modal-overlay {{
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.6);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 10000;
                padding: 20px;
            }}
            .team-review-update-modal {{
                background: white;
                border-radius: 12px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                max-width: 800px;
                width: 100%;
                max-height: 90vh;
                display: flex;
                flex-direction: column;
            }}
            .team-review-update-modal-header {{
                padding: 24px;
                border-bottom: 1px solid #e5e7eb;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 12px 12px 0 0;
            }}
            .team-review-update-modal-title {{
                font-size: 24px;
                font-weight: 700;
                margin: 0;
            }}
            .team-review-update-modal-body {{
                padding: 24px;
                overflow-y: auto;
                flex: 1;
            }}
            .team-review-update-section {{
                margin-bottom: 32px;
            }}
            .team-review-update-section-title {{
                font-size: 18px;
                font-weight: 600;
                margin: 0 0 16px 0;
                color: #1f2937;
                display: flex;
                align-items: center;
                gap: 8px;
            }}
            .team-review-update-summary-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 16px;
                margin-bottom: 16px;
            }}
            .team-review-update-stat {{
                background: #f9fafb;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 16px;
            }}
            .team-review-update-stat-value {{
                font-size: 32px;
                font-weight: 700;
                color: #667eea;
                margin: 0;
            }}
            .team-review-update-stat-label {{
                font-size: 14px;
                color: #6b7280;
                margin: 4px 0 0 0;
            }}
            .team-review-update-contested {{
                background: #fef3c7;
                border: 1px solid #f59e0b;
                border-radius: 8px;
                padding: 16px;
                margin-top: 16px;
            }}
            .team-review-update-contested-title {{
                font-size: 16px;
                font-weight: 600;
                color: #92400e;
                margin: 0 0 12px 0;
            }}
            .team-review-update-contested-item {{
                background: white;
                border-radius: 6px;
                padding: 12px;
                margin-bottom: 8px;
                font-size: 14px;
            }}
            .team-review-update-contested-item strong {{
                color: #1f2937;
            }}
            .team-review-update-code-block {{
                background: #1f2937;
                color: #f9fafb;
                border-radius: 8px;
                padding: 16px;
                font-family: monospace;
                font-size: 13px;
                line-height: 1.6;
                white-space: pre;
                overflow-x: auto;
                position: relative;
            }}
            .team-review-update-copy-btn {{
                position: absolute;
                top: 12px;
                right: 12px;
                background: #374151;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 12px;
                cursor: pointer;
                transition: background 0.2s;
            }}
            .team-review-update-copy-btn:hover {{
                background: #4b5563;
            }}
            .team-review-update-reminder {{
                background: #fef2f2;
                border: 2px solid #ef4444;
                border-radius: 8px;
                padding: 16px;
                font-size: 15px;
                font-weight: 500;
                color: #991b1b;
                text-align: center;
            }}
            .team-review-update-loading {{
                text-align: center;
                padding: 40px;
                color: #6b7280;
            }}
            .team-review-update-spinner {{
                border: 3px solid #e5e7eb;
                border-top: 3px solid #667eea;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto 16px;
            }}
            @keyframes spin {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
            .team-review-update-close-btn {{
                background: #e5e7eb;
                color: #374151;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 500;
                cursor: pointer;
                margin-top: 24px;
                display: block;
                width: 100%;
            }}
            .team-review-update-close-btn:hover {{
                background: #d1d5db;
            }}
            .team-review-git-push-section {{
                margin-top: 16px;
                padding-top: 16px;
                border-top: 1px solid #e5e7eb;
            }}
            .team-review-git-push-btn {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 15px;
                font-weight: 600;
                cursor: pointer;
                display: block;
                width: 100%;
                transition: transform 0.2s, box-shadow 0.2s;
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            }}
            .team-review-git-push-btn:hover:not(:disabled) {{
                transform: translateY(-1px);
                box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
            }}
            .team-review-git-push-btn:disabled {{
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
            }}
            .team-review-git-push-note {{
                font-size: 13px;
                color: #6b7280;
                text-align: center;
                margin-top: 8px;
            }}
            .team-review-git-push-success {{
                background: #d1fae5;
                border: 1px solid #10b981;
                border-radius: 8px;
                padding: 16px;
                text-align: center;
                font-size: 14px;
                color: #065f46;
            }}
            .team-review-git-push-success strong {{
                display: block;
                font-size: 16px;
                margin-bottom: 8px;
            }}
            .team-review-git-push-success a {{
                color: #059669;
                text-decoration: underline;
                font-weight: 500;
            }}
            .team-review-git-push-success a:hover {{
                color: #047857;
            }}
            .team-review-git-push-error {{
                background: #fee2e2;
                border: 1px solid #ef4444;
                border-radius: 8px;
                padding: 16px;
                text-align: center;
                font-size: 14px;
                color: #991b1b;
                margin-top: 12px;
            }}
            .team-review-git-push-confirm {{
                background: #fef3c7;
                border: 1px solid #f59e0b;
                border-radius: 8px;
                padding: 16px;
                margin-bottom: 12px;
                text-align: center;
            }}
            .team-review-git-push-confirm-text {{
                font-size: 14px;
                color: #92400e;
                margin-bottom: 12px;
                font-weight: 500;
            }}
            .team-review-git-push-confirm-actions {{
                display: flex;
                gap: 8px;
                justify-content: center;
            }}
            .team-review-git-push-confirm-yes {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 24px;
                font-size: 14px;
                font-weight: 600;
                cursor: pointer;
            }}
            .team-review-git-push-confirm-cancel {{
                background: #9ca3af;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 24px;
                font-size: 14px;
                font-weight: 600;
                cursor: pointer;
            }}
        `;
        document.head.appendChild(updateLiveStyles);

        // =================================================================
        // PHASE 3: INLINE EDITING UI
        // =================================================================

        const editStyles = document.createElement('style');
        editStyles.textContent = `
            .team-review-edit-mode {{
                background: #fef9c3 !important;
                padding: 8px;
                border-radius: 4px;
                position: relative;
            }}
            .team-review-edit-textarea {{
                width: 100%;
                min-height: 60px;
                padding: 8px;
                border: 2px solid #a16207;
                border-radius: 4px;
                font-size: 14px;
                font-family: inherit;
                resize: vertical;
                box-sizing: border-box;
            }}
            .team-review-edit-textarea:focus {{
                outline: none;
                border-color: #ea580c;
                box-shadow: 0 0 0 3px rgba(234, 88, 12, 0.1);
            }}
            .team-review-edit-actions {{
                display: inline-flex;
                gap: 4px;
                margin-left: 8px;
                vertical-align: middle;
            }}
            .team-review-edit-btn {{
                border: none;
                border-radius: 4px;
                padding: 4px 12px;
                font-size: 14px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
            }}
            .team-review-edit-btn-save {{
                background: #22c55e;
                color: white;
            }}
            .team-review-edit-btn-save:hover {{
                background: #16a34a;
            }}
            .team-review-edit-btn-cancel {{
                background: #9ca3af;
                color: white;
            }}
            .team-review-edit-btn-cancel:hover {{
                background: #6b7280;
            }}
            .team-review-edit-error {{
                display: inline-block;
                margin-left: 8px;
                color: #dc2626;
                font-size: 13px;
                font-weight: 500;
            }}
            .team-review-edited-indicator {{
                display: inline-block;
                margin-left: 8px;
                padding: 2px 8px;
                background: #dbeafe;
                border: 1px solid #3b82f6;
                border-radius: 12px;
                font-size: 11px;
                font-weight: 600;
                color: #1e40af;
                cursor: help;
                position: relative;
            }}
            .team-review-edited-tooltip {{
                display: none;
                position: absolute;
                bottom: 100%;
                left: 50%;
                transform: translateX(-50%);
                background: #1f2937;
                color: white;
                padding: 12px;
                border-radius: 6px;
                font-size: 13px;
                white-space: normal;
                max-width: 300px;
                margin-bottom: 8px;
                z-index: 1000;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                line-height: 1.4;
            }}
            .team-review-edited-indicator:hover .team-review-edited-tooltip {{
                display: block;
            }}
            .team-review-edited-tooltip::after {{
                content: '';
                position: absolute;
                top: 100%;
                left: 50%;
                transform: translateX(-50%);
                border: 6px solid transparent;
                border-top-color: #1f2937;
            }}
            .team-review-edit-server-error {{
                display: inline-block;
                margin-left: 8px;
                padding: 4px 12px;
                background: #fee2e2;
                border: 1px solid #ef4444;
                border-radius: 6px;
                font-size: 13px;
                color: #991b1b;
                font-weight: 500;
            }}
        `;
        document.head.appendChild(editStyles);

        // =================================================================
        // PHASE 4: ADD/DELETE ITEMS UI
        // =================================================================

        const addDeleteStyles = document.createElement('style');
        addDeleteStyles.textContent = `
            .team-review-edit-add-btn {{
                display: block;
                margin: 12px 0 16px 0;
                padding: 8px 16px;
                background: white;
                border: 1px dashed #d1d5db;
                border-radius: 6px;
                color: #6b7280;
                font-size: 14px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.2s;
                text-align: center;
            }}
            .team-review-edit-add-btn:hover {{
                background: #f9fafb;
                border-color: #9ca3af;
                color: #374151;
            }}
            .team-review-edit-add-container {{
                background: #fef9c3;
                padding: 12px;
                border-radius: 6px;
                margin: 12px 0;
            }}
            .team-review-edit-delete-btn {{
                display: none;
                margin-left: 8px;
                padding: 4px 8px;
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                color: #ef4444;
                font-size: 16px;
                cursor: pointer;
                transition: all 0.2s;
                opacity: 0;
            }}
            li:hover .team-review-edit-delete-btn {{
                display: inline-block;
                opacity: 1;
            }}
            .team-review-edit-delete-btn:hover {{
                background: #fee2e2;
                border-color: #ef4444;
            }}
            .team-review-edit-delete-confirm {{
                display: block;
                margin-top: 8px;
                padding: 12px;
                background: #fef2f2;
                border: 1px solid #fecaca;
                border-radius: 6px;
                font-size: 14px;
            }}
            .team-review-edit-delete-confirm-text {{
                color: #991b1b;
                margin-bottom: 8px;
            }}
            .team-review-edit-delete-confirm-actions {{
                display: flex;
                gap: 8px;
            }}
            .team-review-edit-delete-confirm-yes {{
                background: #ef4444;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 16px;
                font-size: 13px;
                font-weight: 600;
                cursor: pointer;
                transition: background 0.2s;
            }}
            .team-review-edit-delete-confirm-yes:hover {{
                background: #dc2626;
            }}
            .team-review-edit-delete-confirm-cancel {{
                background: #9ca3af;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 16px;
                font-size: 13px;
                font-weight: 600;
                cursor: pointer;
                transition: background 0.2s;
            }}
            .team-review-edit-delete-confirm-cancel:hover {{
                background: #6b7280;
            }}
            .team-review-edit-fade-out {{
                animation: fadeOut 0.3s ease-out;
            }}
            @keyframes fadeOut {{
                from {{ opacity: 1; }}
                to {{ opacity: 0; }}
            }}
            .team-review-edit-new-badge {{
                display: inline-block;
                margin-left: 8px;
                padding: 2px 8px;
                background: #d1fae5;
                border: 1px solid #10b981;
                border-radius: 12px;
                font-size: 11px;
                font-weight: 600;
                color: #065f46;
            }}
        `;
        document.head.appendChild(addDeleteStyles);

        // Global state for voting and comments
        let votesCache = {{}};  // item_key -> {{thumbs_up: count, thumbs_down: count, user_vote: 'up'/'down'/null}}
        let commentsCache = {{}};  // item_key -> [{{reviewer_name, comment, timestamp}}]
        let syncOnline = false;
        let pollInterval = null;
        let currentCommentModal = null;
        let editsCache = {{}};  // Loaded from server on page load
        let currentEditingItem = null;  // Track which item is being edited

        /**
         * Build unique key for an item
         */
        function buildItemKey(segment, persona, field, index) {{
            return `${{segment}}.${{persona}}.${{field}}[${{index}}]`;
        }}

        /**
         * Fetch all votes from Google Sheets
         */
        async function fetchVotes() {{
            try {{
                const response = await fetch(`${{APPS_SCRIPT_URL}}?action=getVotes`, {{
                    method: 'GET'
                }});

                if (!response.ok) throw new Error('Failed to fetch votes');

                const data = await response.json();
                console.log('✓ Fetched votes from server');

                // Data format: {{item_key: {{thumbs_up: N, thumbs_down: N, votes: [...]}}}}
                votesCache = data;

                // Mark which items current user voted on
                const reviewerName = getReviewerName();
                if (reviewerName) {{
                    Object.keys(votesCache).forEach(key => {{
                        const userVote = votesCache[key].votes?.find(v => v.reviewer_name === reviewerName);
                        votesCache[key].user_vote = userVote ? userVote.vote_type : null;
                    }});
                }}

                updateSyncStatus(true);
                updateAllVoteCounts();

                // Also fetch comments
                await fetchComments();

                return true;
            }} catch (error) {{
                console.error('Error fetching votes:', error);
                updateSyncStatus(false);
                return false;
            }}
        }}

        /**
         * Submit a vote to Google Sheets
         */
        async function submitVote(itemKey, itemText, voteType) {{
            const reviewerName = getReviewerName();
            if (!reviewerName) {{
                alert('Please set your reviewer name first');
                return false;
            }}

            try {{
                // Use GET to avoid CORS preflight issues
                const params = new URLSearchParams({{
                    action: 'submitVote',
                    reviewer_name: reviewerName,
                    item_key: itemKey,
                    item_text: itemText,
                    vote_type: voteType || '',
                    timestamp: new Date().toISOString()
                }});

                const response = await fetch(`${{APPS_SCRIPT_URL}}?${{params}}`, {{
                    method: 'GET'
                }});

                if (!response.ok) throw new Error('Failed to submit vote');

                const result = await response.json();
                console.log('✓ Vote submitted:', itemKey, voteType);

                updateSyncStatus(true);
                return true;
            }} catch (error) {{
                console.error('Error submitting vote:', error);
                updateSyncStatus(false);
                return false;
            }}
        }}

        /**
         * Handle vote button click
         */
        async function handleVote(itemKey, itemText, voteType, buttonElement) {{
            // Optimistic update
            const container = buttonElement.closest('.team-review-vote-container');
            const buttons = container.querySelectorAll('.team-review-vote-btn');

            // Mark as loading
            container.classList.add('team-review-vote-loading');

            // Update cache optimistically
            if (!votesCache[itemKey]) {{
                votesCache[itemKey] = {{ thumbs_up: 0, thumbs_down: 0, user_vote: null }};
            }}

            const previousVote = votesCache[itemKey].user_vote;

            // If clicking same vote, remove it (toggle off)
            if (previousVote === voteType) {{
                votesCache[itemKey][voteType === 'thumbs_up' ? 'thumbs_up' : 'thumbs_down']--;
                votesCache[itemKey].user_vote = null;
                voteType = null; // Send null to remove vote
            }} else {{
                // Remove previous vote count if exists
                if (previousVote) {{
                    votesCache[itemKey][previousVote === 'thumbs_up' ? 'thumbs_up' : 'thumbs_down']--;
                }}
                // Add new vote count
                if (voteType) {{
                    votesCache[itemKey][voteType === 'thumbs_up' ? 'thumbs_up' : 'thumbs_down']++;
                }}
                votesCache[itemKey].user_vote = voteType;
            }}

            // Update UI immediately
            updateVoteDisplay(itemKey);

            // Submit to server
            const success = await submitVote(itemKey, itemText, voteType);

            // Always refresh votes after a short delay to get server state
            // (fire-and-forget means we don't get immediate confirmation)
            setTimeout(() => fetchVotes(), 2000);

            container.classList.remove('team-review-vote-loading');
        }}

        /**
         * Update vote display for a specific item
         */
        function updateVoteDisplay(itemKey) {{
            const containers = document.querySelectorAll(`[data-item-key="${{itemKey}}"]`);
            containers.forEach(container => {{
                const votes = votesCache[itemKey] || {{ thumbs_up: 0, thumbs_down: 0, user_vote: null }};

                const upBtn = container.querySelector('.team-review-vote-btn[data-vote-type="thumbs_up"]');
                const downBtn = container.querySelector('.team-review-vote-btn[data-vote-type="thumbs_down"]');
                const upCount = container.querySelector('.team-review-vote-count.up');
                const downCount = container.querySelector('.team-review-vote-count.down');

                if (upBtn) {{
                    upBtn.classList.toggle('active', votes.user_vote === 'thumbs_up');
                    if (upCount) upCount.textContent = votes.thumbs_up || 0;
                }}
                if (downBtn) {{
                    downBtn.classList.toggle('active', votes.user_vote === 'thumbs_down');
                    if (downCount) downCount.textContent = votes.thumbs_down || 0;
                }}
            }});
        }}

        /**
         * Update all vote counts in the UI
         */
        function updateAllVoteCounts() {{
            Object.keys(votesCache).forEach(itemKey => {{
                updateVoteDisplay(itemKey);
            }});
        }}

        /**
         * Update sync status indicator
         */
        function updateSyncStatus(online) {{
            syncOnline = online;
            let statusEl = document.querySelector('.team-review-sync-status');

            if (!statusEl) {{
                statusEl = document.createElement('div');
                statusEl.className = 'team-review-sync-status';
                document.body.appendChild(statusEl);
            }}

            statusEl.className = `team-review-sync-status ${{online ? 'online' : 'offline'}}`;
            statusEl.innerHTML = online
                ? '🟢 Live'
                : '🔴 Offline';

            // Disable/enable vote buttons based on status
            document.querySelectorAll('.team-review-vote-btn').forEach(btn => {{
                btn.disabled = !online;
                if (!online) {{
                    btn.title = 'Voting disabled - Apps Script unreachable';
                }} else {{
                    btn.title = '';
                }}
            }});
        }}

        /**
         * Add voting buttons to all list items
         */
        function addVotingButtons() {{
            console.log('Adding voting buttons to all items...');

            let buttonCount = 0;

            document.querySelectorAll('.persona-card').forEach(card => {{
                const personaTitle = card.querySelector('.persona-title');
                if (!personaTitle) return;

                const personaName = personaTitle.textContent.trim();

                // Find segment
                let segment = null;
                const segmentSection = card.closest('.tab-content');
                if (segmentSection) {{
                    const segmentId = segmentSection.id;
                    if (segmentId.includes('Digital')) segment = 'Digital';
                    else if (segmentId.includes('SMB')) segment = 'SMB';
                    else if (segmentId.includes('Commercial')) segment = 'Commercial';
                    else if (segmentId.includes('Enterprise')) segment = 'Enterprise';
                }}

                if (!segment) return;

                // Process each section
                card.querySelectorAll('.section-header').forEach(sectionHeader => {{
                    const sectionName = sectionHeader.textContent.trim();
                    const sectionText = sectionName.replace(/^[^a-zA-Z]+/, '').trim();

                    const fieldMap = {{
                        'Pain Points': 'challenges',
                        'Goals': 'goals',
                        'Objections': 'objections',
                        'Success Metrics': 'success_metrics',
                        'Product Requirements': 'product_requirements',
                        'Information Sources': 'information_sources',
                        'Messaging Preferences': 'messaging_preferences',
                        'Key Messages to Land': 'key_messages',
                        'Key Messages': 'key_messages',
                        'Profile Overview': 'profile_overview'
                    }};

                    const fieldName = fieldMap[sectionText];
                    if (!fieldName) return;

                    // Find list items
                    let currentElement = sectionHeader.nextElementSibling;
                    while (currentElement && !currentElement.classList.contains('section-header')) {{
                        if (currentElement.tagName === 'UL') {{
                            currentElement.querySelectorAll('li').forEach((li, index) => {{
                                // Skip if already has voting buttons
                                if (li.querySelector('.team-review-vote-container')) return;

                                const itemKey = buildItemKey(segment, personaName, fieldName, index);
                                const itemText = li.textContent.replace(/🟢 NEW|🟡 UPDATED|🔴 REMOVED/g, '').trim();

                                // Create voting container
                                const voteContainer = document.createElement('span');
                                voteContainer.className = 'team-review-vote-container';
                                voteContainer.setAttribute('data-item-key', itemKey);

                                // Thumbs up button
                                const upBtn = document.createElement('button');
                                upBtn.className = 'team-review-vote-btn';
                                upBtn.setAttribute('data-vote-type', 'thumbs_up');
                                upBtn.innerHTML = '👍 <span class="team-review-vote-count up">0</span>';
                                upBtn.onclick = () => handleVote(itemKey, itemText, 'thumbs_up', upBtn);

                                // Thumbs down button
                                const downBtn = document.createElement('button');
                                downBtn.className = 'team-review-vote-btn';
                                downBtn.setAttribute('data-vote-type', 'thumbs_down');
                                downBtn.innerHTML = '👎 <span class="team-review-vote-count down">0</span>';
                                downBtn.onclick = () => handleVote(itemKey, itemText, 'thumbs_down', downBtn);

                                voteContainer.appendChild(upBtn);
                                voteContainer.appendChild(downBtn);
                                li.appendChild(voteContainer);

                                buttonCount++;
                            }});
                        }}
                        currentElement = currentElement.nextElementSibling;
                    }}
                }});
            }});

            console.log('✓ Added voting buttons to', buttonCount, 'items');
        }}

        /**
         * Show warning banner if page is opened from file:// protocol
         */
        function checkFileProtocol() {{
            if (window.location.protocol === 'file:') {{
                const banner = document.createElement('div');
                banner.className = 'team-review-file-protocol-banner';
                banner.innerHTML = `
                    <strong>⚠️ For live feedback sync and inline editing, serve this page locally:</strong><br>
                    <code>cd persona_analysis && python3 simple_server.py</code><br>
                    Then open: <code>http://localhost:8080/Persona_Team_Review_Full.html</code>
                `;
                document.body.insertBefore(banner, document.body.firstChild);
                console.warn('Page opened from file:// - voting may not sync correctly. Serve locally for full functionality.');
            }}
        }}

        /**
         * Initialize voting system
         */
        async function initVoting() {{
            console.log('Initializing voting system...');

            // Check for file:// protocol and show warning
            checkFileProtocol();

            // Add voting buttons to all items
            addVotingButtons();

            // Add comment buttons to all items
            addCommentButtons();

            // Add Update Live Version button
            addUpdateLiveButton();

            // Phase 3: Add edit handlers to all items
            addEditHandlers();

            // Phase 3: Load existing edits from server
            await loadEdits();

            // Phase 4: Add delete buttons to all items
            addDeleteButtons();

            // Phase 4: Add "+ Add item" buttons to all sections
            addAddItemButtons();

            // Initial fetch
            await fetchVotes();

            // Poll every 20 seconds (fetches both votes and comments)
            pollInterval = setInterval(fetchVotes, 20000);

            console.log('✓ Voting system initialized');
        }}

        /**
         * Fetch all comments from Google Sheets
         */
        async function fetchComments() {{
            try {{
                const response = await fetch(`${{APPS_SCRIPT_URL}}?action=getFeedback`, {{
                    method: 'GET'
                }});

                if (!response.ok) throw new Error('Failed to fetch comments');

                const data = await response.json();
                console.log('✓ Fetched comments from server');

                // Group comments by item_key
                commentsCache = {{}};
                data.forEach(row => {{
                    if (row.comment) {{
                        if (!commentsCache[row.item_key]) {{
                            commentsCache[row.item_key] = [];
                        }}
                        commentsCache[row.item_key].push({{
                            reviewer_name: row.reviewer_name,
                            comment: row.comment,
                            timestamp: row.timestamp
                        }});
                    }}
                }});

                updateAllCommentCounts();
                return true;
            }} catch (error) {{
                console.error('Error fetching comments:', error);
                return false;
            }}
        }}

        /**
         * Submit a comment to Google Sheets
         */
        async function submitComment(itemKey, itemText, comment) {{
            const reviewerName = getReviewerName();
            if (!reviewerName) {{
                alert('Please set your reviewer name first');
                return false;
            }}

            try {{
                const params = new URLSearchParams({{
                    action: 'submitComment',
                    reviewer_name: reviewerName,
                    item_key: itemKey,
                    item_text: itemText,
                    comment: comment,
                    timestamp: new Date().toISOString()
                }});

                const response = await fetch(`${{APPS_SCRIPT_URL}}?${{params}}`, {{
                    method: 'GET'
                }});

                if (!response.ok) throw new Error('Failed to submit comment');

                const result = await response.json();
                console.log('✓ Comment submitted:', itemKey);

                return true;
            }} catch (error) {{
                console.error('Error submitting comment:', error);
                return false;
            }}
        }}

        /**
         * Delete a comment from Google Sheets
         */
        async function deleteComment(itemKey, reviewerName, timestamp) {{
            try {{
                const params = new URLSearchParams({{
                    action: 'deleteComment',
                    item_key: itemKey,
                    reviewer_name: reviewerName,
                    timestamp: timestamp
                }});

                const response = await fetch(`${{APPS_SCRIPT_URL}}?${{params}}`, {{
                    method: 'GET'
                }});

                if (!response.ok) throw new Error('Failed to delete comment');

                const result = await response.json();
                console.log('✓ Comment deleted:', itemKey);

                return true;
            }} catch (error) {{
                console.error('Error deleting comment:', error);
                return false;
            }}
        }}

        /**
         * Update comment count display for a specific item
         */
        function updateCommentCount(itemKey) {{
            const buttons = document.querySelectorAll(`[data-comment-key="${{itemKey}}"]`);
            const comments = commentsCache[itemKey] || [];
            const count = comments.length;

            buttons.forEach(btn => {{
                const countEl = btn.querySelector('.team-review-comment-count');
                if (countEl) {{
                    countEl.textContent = count || '';
                }}
                if (count > 0) {{
                    btn.classList.add('has-comments');
                }} else {{
                    btn.classList.remove('has-comments');
                }}
            }});
        }}

        /**
         * Update all comment counts in the UI
         */
        function updateAllCommentCounts() {{
            Object.keys(commentsCache).forEach(itemKey => {{
                updateCommentCount(itemKey);
            }});
        }}

        /**
         * Show comment modal for an item
         */
        function showCommentModal(itemKey, itemText) {{
            // Close existing modal if any
            if (currentCommentModal) {{
                currentCommentModal.remove();
            }}

            // Create modal overlay
            const overlay = document.createElement('div');
            overlay.className = 'team-review-comment-modal-overlay';

            // Create modal
            const modal = document.createElement('div');
            modal.className = 'team-review-comment-modal';

            // Modal header
            const header = document.createElement('div');
            header.className = 'team-review-comment-modal-header';
            header.innerHTML = `
                <h3 class="team-review-comment-modal-title">💬 Comments</h3>
                <p class="team-review-comment-modal-subtitle">${{itemText}}</p>
            `;

            // Modal body
            const body = document.createElement('div');
            body.className = 'team-review-comment-modal-body';

            // Comment thread
            const thread = document.createElement('div');
            thread.className = 'team-review-comment-thread';
            thread.id = `comment-thread-${{itemKey}}`;

            const comments = commentsCache[itemKey] || [];
            const currentReviewer = getReviewerName();

            if (comments.length === 0) {{
                thread.innerHTML = '<div class="team-review-comment-empty">No comments yet. Be the first to add one!</div>';
            }} else {{
                comments.forEach(c => {{
                    const commentEl = document.createElement('div');
                    commentEl.className = 'team-review-comment-item';
                    const timestamp = new Date(c.timestamp).toLocaleString();
                    const isOwnComment = c.reviewer_name === currentReviewer;

                    const deleteBtn = isOwnComment
                        ? `<button class="team-review-comment-delete" onclick="confirmDeleteComment('${{itemKey}}', '${{c.reviewer_name}}', '${{c.timestamp}}', this)" title="Delete comment">🗑</button>`
                        : '';

                    commentEl.innerHTML = `
                        <div class="team-review-comment-header">
                            <span class="team-review-comment-author">${{c.reviewer_name}}</span>
                            <span class="team-review-comment-timestamp">${{timestamp}}</span>
                            ${{deleteBtn}}
                        </div>
                        <div class="team-review-comment-text">${{c.comment}}</div>
                    `;
                    thread.appendChild(commentEl);
                }});
            }}

            body.appendChild(thread);

            // Input section
            const inputSection = document.createElement('div');
            inputSection.className = 'team-review-comment-input-section';
            inputSection.innerHTML = `
                <textarea class="team-review-comment-input" placeholder="Add your comment..."></textarea>
                <div class="team-review-comment-actions">
                    <button class="team-review-comment-btn-secondary" onclick="closeCommentModal()">Cancel</button>
                    <button class="team-review-comment-btn-primary" onclick="submitCommentFromModal('${{itemKey}}', \`${{itemText.replace(/`/g, '\\`')}}\`)">Post Comment</button>
                </div>
            `;

            // Assemble modal
            modal.appendChild(header);
            modal.appendChild(body);
            modal.appendChild(inputSection);
            overlay.appendChild(modal);

            // Close on overlay click
            overlay.addEventListener('click', (e) => {{
                if (e.target === overlay) {{
                    closeCommentModal();
                }}
            }});

            // Add to page
            document.body.appendChild(overlay);
            currentCommentModal = overlay;

            // Focus input
            setTimeout(() => {{
                const input = overlay.querySelector('.team-review-comment-input');
                if (input) input.focus();
            }}, 100);
        }}

        /**
         * Close comment modal
         */
        function closeCommentModal() {{
            if (currentCommentModal) {{
                currentCommentModal.remove();
                currentCommentModal = null;
            }}
        }}

        /**
         * Confirm comment deletion
         */
        function confirmDeleteComment(itemKey, reviewerName, timestamp, buttonElement) {{
            // Check if confirmation already exists
            const commentItem = buttonElement.closest('.team-review-comment-item');
            if (commentItem.querySelector('.team-review-comment-delete-confirm')) return;

            // Create confirmation UI
            const confirmEl = document.createElement('div');
            confirmEl.className = 'team-review-comment-delete-confirm';
            confirmEl.innerHTML = `
                Delete this comment?
                <button class="yes" onclick="executeDeleteComment('${{itemKey}}', '${{reviewerName}}', '${{timestamp}}')">Yes</button>
                <button class="cancel" onclick="this.closest('.team-review-comment-delete-confirm').remove()">Cancel</button>
            `;
            commentItem.appendChild(confirmEl);
        }}

        /**
         * Execute comment deletion
         */
        async function executeDeleteComment(itemKey, reviewerName, timestamp) {{
            const success = await deleteComment(itemKey, reviewerName, timestamp);

            if (success) {{
                // Refresh comments
                await fetchComments();

                // Update the thread display
                const thread = document.getElementById(`comment-thread-${{itemKey}}`);
                if (thread && currentCommentModal) {{
                    const currentReviewer = getReviewerName();
                    const comments = commentsCache[itemKey] || [];

                    thread.innerHTML = '';
                    if (comments.length === 0) {{
                        thread.innerHTML = '<div class="team-review-comment-empty">No comments yet. Be the first to add one!</div>';
                    }} else {{
                        comments.forEach(c => {{
                            const commentEl = document.createElement('div');
                            commentEl.className = 'team-review-comment-item';
                            const timestamp = new Date(c.timestamp).toLocaleString();
                            const isOwnComment = c.reviewer_name === currentReviewer;

                            const deleteBtn = isOwnComment
                                ? `<button class="team-review-comment-delete" onclick="confirmDeleteComment('${{itemKey}}', '${{c.reviewer_name}}', '${{c.timestamp}}', this)" title="Delete comment">🗑</button>`
                                : '';

                            commentEl.innerHTML = `
                                <div class="team-review-comment-header">
                                    <span class="team-review-comment-author">${{c.reviewer_name}}</span>
                                    <span class="team-review-comment-timestamp">${{timestamp}}</span>
                                    ${{deleteBtn}}
                                </div>
                                <div class="team-review-comment-text">${{c.comment}}</div>
                            `;
                            thread.appendChild(commentEl);
                        }});
                    }}
                }}

                // Update count in main UI
                updateCommentCount(itemKey);
            }} else {{
                alert('Failed to delete comment. Please try again.');
            }}
        }}

        /**
         * Submit comment from modal
         */
        async function submitCommentFromModal(itemKey, itemText) {{
            const input = currentCommentModal.querySelector('.team-review-comment-input');
            const comment = input.value.trim();

            if (!comment) {{
                alert('Please enter a comment');
                return;
            }}

            // Disable input while submitting
            input.disabled = true;
            const btn = currentCommentModal.querySelector('.team-review-comment-btn-primary');
            const originalText = btn.textContent;
            btn.textContent = 'Posting...';
            btn.disabled = true;

            const success = await submitComment(itemKey, itemText, comment);

            if (success) {{
                // Refresh comments
                await fetchComments();

                // Refresh the thread display
                const thread = document.getElementById(`comment-thread-${{itemKey}}`);
                if (thread) {{
                    const currentReviewer = getReviewerName();
                    const comments = commentsCache[itemKey] || [];
                    thread.innerHTML = '';

                    if (comments.length === 0) {{
                        thread.innerHTML = '<div class="team-review-comment-empty">No comments yet. Be the first to add one!</div>';
                    }} else {{
                        comments.forEach(c => {{
                            const commentEl = document.createElement('div');
                            commentEl.className = 'team-review-comment-item';
                            const timestamp = new Date(c.timestamp).toLocaleString();
                            const isOwnComment = c.reviewer_name === currentReviewer;

                            const deleteBtn = isOwnComment
                                ? `<button class="team-review-comment-delete" onclick="confirmDeleteComment('${{itemKey}}', '${{c.reviewer_name}}', '${{c.timestamp}}', this)" title="Delete comment">🗑</button>`
                                : '';

                            commentEl.innerHTML = `
                                <div class="team-review-comment-header">
                                    <span class="team-review-comment-author">${{c.reviewer_name}}</span>
                                    <span class="team-review-comment-timestamp">${{timestamp}}</span>
                                    ${{deleteBtn}}
                                </div>
                                <div class="team-review-comment-text">${{c.comment}}</div>
                            `;
                            thread.appendChild(commentEl);
                        }});
                    }}
                }}

                // Clear input
                input.value = '';
                input.disabled = false;
                btn.textContent = originalText;
                btn.disabled = false;

                // Update count in main UI
                updateCommentCount(itemKey);
            }} else {{
                alert('Failed to post comment. Please try again.');
                input.disabled = false;
                btn.textContent = originalText;
                btn.disabled = false;
            }}
        }}

        /**
         * Add comment buttons to all list items
         */
        function addCommentButtons() {{
            console.log('Adding comment buttons to all items...');

            let buttonCount = 0;

            document.querySelectorAll('.persona-card').forEach(card => {{
                const personaTitle = card.querySelector('.persona-title');
                if (!personaTitle) return;

                const personaName = personaTitle.textContent.trim();

                // Find segment
                let segment = null;
                const segmentSection = card.closest('.tab-content');
                if (segmentSection) {{
                    const segmentId = segmentSection.id;
                    if (segmentId.includes('Digital')) segment = 'Digital';
                    else if (segmentId.includes('SMB')) segment = 'SMB';
                    else if (segmentId.includes('Commercial')) segment = 'Commercial';
                    else if (segmentId.includes('Enterprise')) segment = 'Enterprise';
                }}

                if (!segment) return;

                // Process each section
                card.querySelectorAll('.section-header').forEach(sectionHeader => {{
                    const sectionName = sectionHeader.textContent.trim();
                    const sectionText = sectionName.replace(/^[^a-zA-Z]+/, '').trim();

                    const fieldMap = {{
                        'Pain Points': 'challenges',
                        'Goals': 'goals',
                        'Objections': 'objections',
                        'Success Metrics': 'success_metrics',
                        'Product Requirements': 'product_requirements',
                        'Information Sources': 'information_sources',
                        'Messaging Preferences': 'messaging_preferences',
                        'Key Messages to Land': 'key_messages',
                        'Key Messages': 'key_messages',
                        'Profile Overview': 'profile_overview'
                    }};

                    const fieldName = fieldMap[sectionText];
                    if (!fieldName) return;

                    // Find list items
                    let currentElement = sectionHeader.nextElementSibling;
                    while (currentElement && !currentElement.classList.contains('section-header')) {{
                        if (currentElement.tagName === 'UL') {{
                            currentElement.querySelectorAll('li').forEach((li, index) => {{
                                // Skip if already has comment button
                                if (li.querySelector('.team-review-comment-btn')) return;

                                const itemKey = buildItemKey(segment, personaName, fieldName, index);
                                const itemText = li.textContent.replace(/🟢 NEW|🟡 UPDATED|🔴 REMOVED|👍|👎|[0-9]/g, '').trim();

                                // Find vote container to add comment button after it
                                const voteContainer = li.querySelector('.team-review-vote-container');
                                if (!voteContainer) return;

                                // Create comment button
                                const commentBtn = document.createElement('button');
                                commentBtn.className = 'team-review-comment-btn';
                                commentBtn.setAttribute('data-comment-key', itemKey);
                                commentBtn.innerHTML = '💬 <span class="team-review-comment-count"></span>';
                                commentBtn.onclick = () => showCommentModal(itemKey, itemText);

                                // Insert after vote container
                                voteContainer.parentNode.insertBefore(commentBtn, voteContainer.nextSibling);

                                buttonCount++;
                            }});
                        }}
                        currentElement = currentElement.nextElementSibling;
                    }}
                }});
            }});

            console.log('✓ Added comment buttons to', buttonCount, 'items');
        }}

        /**
         * Fetch feedback summary from Google Sheets
         */
        async function fetchFeedbackSummary() {{
            try {{
                const response = await fetch(`${{APPS_SCRIPT_URL}}?action=getFeedback`, {{
                    method: 'GET'
                }});

                if (!response.ok) throw new Error('Failed to fetch feedback');

                const data = await response.json();
                console.log('✓ Fetched feedback summary');

                // Analyze feedback
                const uniqueReviewers = new Set();
                const itemsWithVotes = new Set();
                const itemsWithComments = new Set();
                const votesByItem = {{}};
                const contestedItems = [];

                data.forEach(row => {{
                    if (row.reviewer_name) {{
                        uniqueReviewers.add(row.reviewer_name);
                    }}

                    if (row.item_key) {{
                        if (row.vote) {{
                            itemsWithVotes.add(row.item_key);

                            if (!votesByItem[row.item_key]) {{
                                votesByItem[row.item_key] = {{
                                    item_text: row.item_text,
                                    thumbs_up: 0,
                                    thumbs_down: 0,
                                    comments: []
                                }};
                            }}

                            if (row.vote === 'thumbs_up') {{
                                votesByItem[row.item_key].thumbs_up++;
                            }} else if (row.vote === 'thumbs_down') {{
                                votesByItem[row.item_key].thumbs_down++;
                            }}
                        }}

                        if (row.comment) {{
                            itemsWithComments.add(row.item_key);
                            if (!votesByItem[row.item_key]) {{
                                votesByItem[row.item_key] = {{
                                    item_text: row.item_text,
                                    thumbs_up: 0,
                                    thumbs_down: 0,
                                    comments: []
                                }};
                            }}
                            votesByItem[row.item_key].comments.push({{
                                reviewer: row.reviewer_name,
                                comment: row.comment
                            }});
                        }}
                    }}
                }});

                // Identify approved and contested items
                let approvedCount = 0;
                Object.entries(votesByItem).forEach(([key, data]) => {{
                    const isContested = data.thumbs_down >= data.thumbs_up || data.comments.length > 0;

                    if (isContested) {{
                        // Parse item key to get details
                        const pathMatch = key.match(/^(.+?)\\.(.+?)\\.(.+?)\\[(\\d+)\\]$/);
                        if (pathMatch) {{
                            contestedItems.push({{
                                segment: pathMatch[1],
                                persona: pathMatch[2],
                                section: pathMatch[3],
                                item_text: data.item_text,
                                votes: `${{data.thumbs_up}}👍 / ${{data.thumbs_down}}👎`,
                                comments: data.comments
                            }});
                        }}
                    }} else if (data.thumbs_up > data.thumbs_down) {{
                        approvedCount++;
                    }}
                }});

                return {{
                    uniqueReviewers: uniqueReviewers.size,
                    itemsVotedOn: itemsWithVotes.size,
                    approvedCount: approvedCount,
                    contestedItems: contestedItems
                }};
            }} catch (error) {{
                console.error('Error fetching feedback summary:', error);
                return null;
            }}
        }}

        /**
         * Show Update Live Version modal
         */
        async function showUpdateLiveModal() {{
            // Create modal overlay
            const overlay = document.createElement('div');
            overlay.className = 'team-review-update-modal-overlay';

            // Create modal
            const modal = document.createElement('div');
            modal.className = 'team-review-update-modal';

            // Modal header
            const header = document.createElement('div');
            header.className = 'team-review-update-modal-header';
            header.innerHTML = '<h2 class="team-review-update-modal-title">📤 Update Live Version</h2>';

            // Modal body
            const body = document.createElement('div');
            body.className = 'team-review-update-modal-body';
            body.innerHTML = '<div class="team-review-update-loading"><div class="team-review-update-spinner"></div>Loading feedback summary...</div>';

            // Assemble modal
            modal.appendChild(header);
            modal.appendChild(body);
            overlay.appendChild(modal);

            // Close on overlay click
            overlay.addEventListener('click', (e) => {{
                if (e.target === overlay) {{
                    overlay.remove();
                }}
            }});

            // Add to page
            document.body.appendChild(overlay);

            // Fetch feedback summary
            const summary = await fetchFeedbackSummary();

            if (!summary) {{
                body.innerHTML = `
                    <div class="team-review-update-section">
                        <p style="color: #ef4444;">❌ Failed to load feedback summary. Please check your connection and try again.</p>
                        <button class="team-review-update-close-btn" onclick="this.closest('.team-review-update-modal-overlay').remove()">Close</button>
                    </div>
                `;
                return;
            }}

            // Build modal content
            const runQuarter = PIPELINE_METADATA.run_quarter || 'Q2 2026';
            const today = new Date().toISOString().split('T')[0];

            const commands = `python3 aggregate_team_feedback.py --run-quarter ${{runQuarter}}
python3 apply_approved_changes.py
python3 generate_final_clean_personas.py
cd persona_analysis
git add reports/
git commit -m "Persona update — ${{runQuarter}} approved by team"
git push origin main`;

            let contestedHTML = '';
            if (summary.contestedItems.length > 0) {{
                contestedHTML = `
                    <div class="team-review-update-contested">
                        <h4 class="team-review-update-contested-title">⚠️ Contested Items (${{summary.contestedItems.length}})</h4>
                        <p style="margin: 0 0 12px 0; font-size: 14px; color: #6b7280;">Review these items before pushing to live:</p>
                        ${{summary.contestedItems.map(item => `
                            <div class="team-review-update-contested-item">
                                <strong>${{item.segment}} → ${{item.persona}} → ${{item.section}}</strong><br>
                                ${{item.item_text}}<br>
                                <span style="color: #6b7280; font-size: 13px;">Votes: ${{item.votes}}</span>
                                ${{item.comments.length > 0 ? `<br><span style="color: #6b7280; font-size: 13px;">💬 ${{item.comments.length}} comment(s)</span>` : ''}}
                            </div>
                        `).join('')}}
                    </div>
                `;
            }}

            body.innerHTML = `
                <!-- Section 1: Feedback Summary -->
                <div class="team-review-update-section">
                    <h3 class="team-review-update-section-title">📊 Feedback Summary</h3>
                    <div class="team-review-update-summary-grid">
                        <div class="team-review-update-stat">
                            <p class="team-review-update-stat-value">${{summary.uniqueReviewers}}</p>
                            <p class="team-review-update-stat-label">Unique Reviewers</p>
                        </div>
                        <div class="team-review-update-stat">
                            <p class="team-review-update-stat-value">${{summary.itemsVotedOn}}</p>
                            <p class="team-review-update-stat-label">Items Voted On</p>
                        </div>
                        <div class="team-review-update-stat">
                            <p class="team-review-update-stat-value">${{summary.approvedCount}}</p>
                            <p class="team-review-update-stat-label">Approved Items</p>
                        </div>
                        <div class="team-review-update-stat">
                            <p class="team-review-update-stat-value">${{summary.contestedItems.length}}</p>
                            <p class="team-review-update-stat-label">Contested Items</p>
                        </div>
                    </div>
                    ${{contestedHTML}}
                </div>

                <!-- Section 2: Terminal Commands -->
                <div class="team-review-update-section">
                    <h3 class="team-review-update-section-title">💻 Terminal Commands</h3>
                    <div class="team-review-update-code-block">
                        <button class="team-review-update-copy-btn" onclick="copyCommands()">📋 Copy all commands</button>${{commands}}</div>

                    <!-- Push Live Now Button -->
                    <div class="team-review-git-push-section" id="gitPushSection">
                        <button class="team-review-git-push-btn" onclick="confirmGitPush()">🚀 Push Live Now</button>
                        <p class="team-review-git-push-note">Or run the commands above manually in your terminal</p>
                    </div>
                </div>

                <!-- Section 3: Reminder -->
                <div class="team-review-update-section">
                    <div class="team-review-update-reminder">
                        ⚠️ Nothing goes live until you run these commands in your terminal.
                    </div>
                </div>

                <button class="team-review-update-close-btn" onclick="this.closest('.team-review-update-modal-overlay').remove()">Close</button>
            `;
        }}

        /**
         * Copy commands to clipboard
         */
        function copyCommands() {{
            const runQuarter = PIPELINE_METADATA.run_quarter || 'Q2 2026';
            const commands = `python3 aggregate_team_feedback.py --run-quarter ${{runQuarter}}
python3 apply_approved_changes.py
python3 generate_final_clean_personas.py
cd persona_analysis
git add reports/
git commit -m "Persona update — ${{runQuarter}} approved by team"
git push origin main`;

            navigator.clipboard.writeText(commands).then(() => {{
                const btn = document.querySelector('.team-review-update-copy-btn');
                if (btn) {{
                    const originalText = btn.textContent;
                    btn.textContent = '✓ Copied!';
                    setTimeout(() => {{
                        btn.textContent = originalText;
                    }}, 2000);
                }}
            }});
        }}

        /**
         * Show confirmation before pushing to GitHub
         */
        function confirmGitPush() {{
            const section = document.getElementById('gitPushSection');

            // Replace button with confirmation UI
            section.innerHTML = `
                <div class="team-review-git-push-confirm">
                    <div class="team-review-git-push-confirm-text">
                        This will push changes directly to the live site. Are you sure?
                    </div>
                    <div class="team-review-git-push-confirm-actions">
                        <button class="team-review-git-push-confirm-yes" onclick="executeGitPush()">Yes, push live</button>
                        <button class="team-review-git-push-confirm-cancel" onclick="cancelGitPush()">Cancel</button>
                    </div>
                </div>
                <p class="team-review-git-push-note">Or run the commands above manually in your terminal</p>
            `;
        }}

        /**
         * Cancel git push and restore button
         */
        function cancelGitPush() {{
            const section = document.getElementById('gitPushSection');
            section.innerHTML = `
                <button class="team-review-git-push-btn" onclick="confirmGitPush()">🚀 Push Live Now</button>
                <p class="team-review-git-push-note">Or run the commands above manually in your terminal</p>
            `;
        }}

        /**
         * Execute git push via Flask endpoint
         */
        async function executeGitPush() {{
            const section = document.getElementById('gitPushSection');

            // Show loading state
            section.innerHTML = `
                <button class="team-review-git-push-btn" disabled>Pushing to GitHub...</button>
                <p class="team-review-git-push-note">Or run the commands above manually in your terminal</p>
            `;

            // Build commit message
            const today = new Date().toISOString().split('T')[0];
            // Count changes applied from edits cache
            let changesApplied = 0;
            Object.keys(editsCache).forEach(segment => {{
                Object.keys(editsCache[segment]).forEach(persona => {{
                    Object.keys(editsCache[segment][persona]).forEach(field => {{
                        const sectionData = editsCache[segment][persona][field];
                        if (sectionData.has_changes && sectionData.change_log) {{
                            changesApplied += sectionData.change_log.length;
                        }}
                    }});
                }});
            }});

            const commitMessage = `Persona update: ${{changesApplied}} changes applied — ${{today}}`;

            try {{
                const response = await fetch('http://localhost:8080/api/git_push', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        commit_message: commitMessage
                    }})
                }});

                const result = await response.json();

                if (result.success) {{
                    // Show success message
                    section.innerHTML = `
                        <div class="team-review-git-push-success">
                            <strong>✅ Live site updated!</strong>
                            View the live page:<br>
                            <a href="https://chrissherman-png.github.io/persona-analysis/reports/Persona_Profiles_FINAL.html" target="_blank">
                                https://chrissherman-png.github.io/persona-analysis/reports/Persona_Profiles_FINAL.html
                            </a>
                        </div>
                    `;
                }} else {{
                    // Show error message
                    section.innerHTML = `
                        <div class="team-review-git-push-error">
                            ❌ Auto-push failed — use the manual commands above instead<br>
                            <small>${{result.error}}</small>
                        </div>
                        <button class="team-review-git-push-btn" onclick="confirmGitPush()" style="margin-top: 12px;">🚀 Try Again</button>
                        <p class="team-review-git-push-note">Or run the commands above manually in your terminal</p>
                    `;
                }}
            }} catch (error) {{
                console.error('Error pushing to GitHub:', error);

                // Show error message
                section.innerHTML = `
                    <div class="team-review-git-push-error">
                        ❌ Auto-push failed — use the manual commands above instead<br>
                        <small>Server not running or network error</small>
                    </div>
                    <button class="team-review-git-push-btn" onclick="confirmGitPush()" style="margin-top: 12px;">🚀 Try Again</button>
                    <p class="team-review-git-push-note">Or run the commands above manually in your terminal</p>
                `;
            }}
        }}

        /**
         * Add Update Live Version button
         */
        function addUpdateLiveButton() {{
            const button = document.createElement('button');
            button.className = 'team-review-update-btn';
            button.innerHTML = '📤 Update Live Version';
            button.onclick = showUpdateLiveModal;
            document.body.appendChild(button);
            console.log('✓ Update Live Version button added');
        }}

        // =================================================================
        // PHASE 3: INLINE EDITING FUNCTIONS
        // =================================================================

        /**
         * Load edits from server on page load
         */
        async function loadEdits() {{
            try {{
                const response = await fetch(`http://localhost:8080/api/get_edits?run_quarter=${{encodeURIComponent(RUN_QUARTER)}}`);

                if (!response.ok) {{
                    console.warn('Could not load edits (server may not be running)');
                    return;
                }}

                const data = await response.json();
                editsCache = data.edits || {{}};

                console.log('✓ Loaded edits from server');

                // Apply edited text and indicators to UI
                applyEditsToUI();
            }} catch (error) {{
                console.warn('Error loading edits:', error);
            }}
        }}

        /**
         * Apply loaded edits to the UI (replace text, show indicators, render added items)
         */
        function applyEditsToUI() {{
            console.log('Applying edits to UI...');

            Object.keys(editsCache).forEach(segment => {{
                Object.keys(editsCache[segment]).forEach(persona => {{
                    Object.keys(editsCache[segment][persona]).forEach(field => {{
                        const sectionData = editsCache[segment][persona][field];

                        if (!sectionData.has_changes) return;

                        // Find the UL element for this section
                        const cards = document.querySelectorAll('.persona-card');
                        let targetUL = null;

                        cards.forEach(card => {{
                            const personaTitle = card.querySelector('.persona-title');
                            if (!personaTitle || personaTitle.textContent.trim() !== persona) return;

                            // Check segment
                            const segmentSection = card.closest('.tab-content');
                            if (!segmentSection) return;
                            const segmentId = segmentSection.id;
                            let cardSegment = null;
                            if (segmentId.includes('Digital')) cardSegment = 'Digital';
                            else if (segmentId.includes('SMB')) cardSegment = 'SMB';
                            else if (segmentId.includes('Commercial')) cardSegment = 'Commercial';
                            else if (segmentId.includes('Enterprise')) cardSegment = 'Enterprise';

                            if (cardSegment !== segment) return;

                            // Find section header matching field
                            const fieldMap = {{
                                'challenges': 'Pain Points',
                                'goals': 'Goals',
                                'objections': 'Objections',
                                'success_metrics': 'Success Metrics',
                                'product_requirements': 'Product Requirements',
                                'information_sources': 'Information Sources',
                                'messaging_preferences': 'Messaging Preferences',
                                'key_messages': 'Key Messages'
                            }};

                            const displayName = fieldMap[field];
                            if (!displayName) return;

                            const sectionHeaders = card.querySelectorAll('.section-header');
                            sectionHeaders.forEach(header => {{
                                const headerText = header.textContent.replace(/^[^a-zA-Z]+/, '').trim();
                                if (headerText === displayName) {{
                                    // Find UL after this header
                                    let currentElement = header.nextElementSibling;
                                    while (currentElement && !currentElement.classList.contains('section-header')) {{
                                        if (currentElement.tagName === 'UL') {{
                                            targetUL = currentElement;
                                            break;
                                        }}
                                        currentElement = currentElement.nextElementSibling;
                                    }}
                                }}
                            }});
                        }});

                        if (!targetUL) {{
                            console.warn('Could not find UL for', segment, persona, field);
                            return;
                        }}

                        // Count how many items are already in the DOM (pipeline-generated, capped at 5)
                        const existingItems = targetUL.querySelectorAll('li');
                        const originalCount = existingItems.length;

                        console.log('  Section:', segment, '→', persona, '→', field);
                        console.log('    Existing items in DOM:', originalCount);
                        console.log('    Items in edits file:', sectionData.items.length);

                        // Process all items
                        sectionData.items.forEach((editedText, index) => {{
                            const itemKey = buildItemKey(segment, persona, field, index);

                            if (index < originalCount) {{
                                // This is an existing item (within the original cap) - update it
                                const li = existingItems[index];
                                const voteContainer = li.querySelector(`[data-item-key="${{itemKey}}"]`);

                                if (voteContainer) {{
                                    // Update text
                                    const textNode = Array.from(li.childNodes).find(node => node.nodeType === Node.TEXT_NODE);
                                    if (textNode) {{
                                        textNode.textContent = editedText + ' ';
                                    }}

                                    // Check if edited
                                    const wasEdited = sectionData.change_log?.some(log =>
                                        log.index === index && log.action === 'edit'
                                    );

                                    if (wasEdited) {{
                                        if (!li.querySelector('.team-review-edited-indicator')) {{
                                            const editLog = sectionData.change_log.find(log =>
                                                log.index === index && log.action === 'edit'
                                            );
                                            addEditedIndicator(li, editLog);
                                        }}
                                    }}
                                }}
                            }} else {{
                                // This is an added item (beyond the original cap) - create new li
                                // Check if this was added
                                const wasAdded = sectionData.change_log?.some(log =>
                                    log.index === index && log.action === 'add'
                                );

                                if (wasAdded) {{
                                    console.log('    Creating new <li> for added item at index', index);

                                    const newLi = document.createElement('li');
                                    newLi.textContent = editedText + ' ';

                                    // Add 🟢 NEW badge
                                    const newBadge = document.createElement('span');
                                    newBadge.className = 'team-review-edit-new-badge';
                                    newBadge.textContent = '🟢 NEW';
                                    newLi.appendChild(newBadge);

                                    // Add voting container
                                    const voteContainer = document.createElement('span');
                                    voteContainer.className = 'team-review-vote-container';
                                    voteContainer.setAttribute('data-item-key', itemKey);

                                    const upBtn = document.createElement('button');
                                    upBtn.className = 'team-review-vote-btn';
                                    upBtn.setAttribute('data-vote-type', 'thumbs_up');
                                    upBtn.innerHTML = '👍 <span class="team-review-vote-count up">0</span>';
                                    upBtn.onclick = () => handleVote(itemKey, editedText, 'thumbs_up', upBtn);

                                    const downBtn = document.createElement('button');
                                    downBtn.className = 'team-review-vote-btn';
                                    downBtn.setAttribute('data-vote-type', 'thumbs_down');
                                    downBtn.innerHTML = '👎 <span class="team-review-vote-count down">0</span>';
                                    downBtn.onclick = () => handleVote(itemKey, editedText, 'thumbs_down', downBtn);

                                    voteContainer.appendChild(upBtn);
                                    voteContainer.appendChild(downBtn);
                                    newLi.appendChild(voteContainer);

                                    // Add comment button
                                    const commentBtn = document.createElement('button');
                                    commentBtn.className = 'team-review-comment-btn';
                                    commentBtn.setAttribute('data-comment-key', itemKey);
                                    commentBtn.innerHTML = '💬 <span class="team-review-comment-count"></span>';
                                    commentBtn.onclick = () => showCommentModal(itemKey, editedText);
                                    newLi.appendChild(commentBtn);

                                    // Add delete button
                                    const deleteBtn = document.createElement('button');
                                    deleteBtn.className = 'team-review-edit-delete-btn';
                                    deleteBtn.textContent = '🗑';
                                    deleteBtn.onclick = () => showDeleteConfirm(newLi, itemKey, segment, persona, field, index, editedText);
                                    newLi.appendChild(deleteBtn);

                                    // Add double-click handler
                                    newLi.addEventListener('dblclick', () => {{
                                        enterEditMode(newLi, itemKey, segment, persona, field, index);
                                    }});

                                    // Append to UL
                                    targetUL.appendChild(newLi);
                                }}
                            }}
                        }});
                    }});
                }});
            }});

            console.log('✓ Edits applied to UI');
        }}

        /**
         * Add edited indicator badge to an item
         */
        function addEditedIndicator(li, editLog) {{
            const indicator = document.createElement('span');
            indicator.className = 'team-review-edited-indicator';

            const timestamp = new Date(editLog.timestamp).toLocaleString();
            const tooltip = `
                <div class="team-review-edited-tooltip">
                    <strong>Edited by:</strong> ${{editLog.edited_by}}<br>
                    <strong>At:</strong> ${{timestamp}}<br>
                    <strong>Original:</strong> ${{editLog.original_value}}
                </div>
            `;

            indicator.innerHTML = '✏️ Edited' + tooltip;

            // Insert after vote/comment buttons
            const commentBtn = li.querySelector('.team-review-comment-btn');
            if (commentBtn) {{
                commentBtn.parentNode.insertBefore(indicator, commentBtn.nextSibling);
            }}
        }}

        /**
         * Enter edit mode for an item
         */
        function enterEditMode(li, itemKey, segment, persona, field, index) {{
            // Prevent multiple edits at once
            if (currentEditingItem) {{
                alert('Please finish editing the current item first');
                return;
            }}

            currentEditingItem = itemKey;

            // Get current text (strip badges and buttons)
            const textNode = Array.from(li.childNodes).find(node => node.nodeType === Node.TEXT_NODE);
            const currentText = textNode ? textNode.textContent.trim() : '';

            // Store original text for cancel
            li.dataset.originalText = currentText;
            li.dataset.itemKey = itemKey;
            li.dataset.segment = segment;
            li.dataset.persona = persona;
            li.dataset.field = field;
            li.dataset.index = index;

            // Add edit mode class
            li.classList.add('team-review-edit-mode');

            // Create textarea
            const textarea = document.createElement('textarea');
            textarea.className = 'team-review-edit-textarea';
            textarea.value = currentText;

            // Keyboard shortcuts
            textarea.addEventListener('keydown', (e) => {{
                if (e.key === 'Enter' && !e.shiftKey) {{
                    e.preventDefault();
                    saveEdit(li);
                }} else if (e.key === 'Escape') {{
                    cancelEdit(li);
                }}
            }});

            // Replace text with textarea
            textNode.textContent = '';
            li.insertBefore(textarea, li.firstChild);

            // Create action buttons
            const actions = document.createElement('span');
            actions.className = 'team-review-edit-actions';

            const saveBtn = document.createElement('button');
            saveBtn.className = 'team-review-edit-btn team-review-edit-btn-save';
            saveBtn.textContent = '✓';
            saveBtn.onclick = () => saveEdit(li);

            const cancelBtn = document.createElement('button');
            cancelBtn.className = 'team-review-edit-btn team-review-edit-btn-cancel';
            cancelBtn.textContent = '✗';
            cancelBtn.onclick = () => cancelEdit(li);

            actions.appendChild(saveBtn);
            actions.appendChild(cancelBtn);

            li.insertBefore(actions, textarea.nextSibling);

            // Focus textarea
            textarea.focus();
            textarea.setSelectionRange(textarea.value.length, textarea.value.length);
        }}

        /**
         * Save edit
         */
        async function saveEdit(li) {{
            const textarea = li.querySelector('.team-review-edit-textarea');
            const newValue = textarea.value.trim();
            const originalValue = li.dataset.originalText;

            // Validation: empty text
            if (!newValue) {{
                const errorMsg = document.createElement('span');
                errorMsg.className = 'team-review-edit-error';
                errorMsg.textContent = 'Item text cannot be empty';
                textarea.parentNode.insertBefore(errorMsg, textarea.nextSibling);
                setTimeout(() => errorMsg.remove(), 3000);
                return;
            }}

            // If unchanged, treat as cancel
            if (newValue === originalValue) {{
                cancelEdit(li);
                return;
            }}

            const itemKey = li.dataset.itemKey;
            const segment = li.dataset.segment;
            const persona = li.dataset.persona;
            const field = li.dataset.field;
            const index = parseInt(li.dataset.index);

            const reviewerName = getReviewerName();
            if (!reviewerName) {{
                alert('Please set your reviewer name first');
                cancelEdit(li);
                return;
            }}

            // Disable textarea during save
            textarea.disabled = true;
            const saveBtn = li.querySelector('.team-review-edit-btn-save');
            saveBtn.disabled = true;
            saveBtn.textContent = '...';

            try {{
                const response = await fetch('http://localhost:8080/api/save_edit', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        run_quarter: RUN_QUARTER,
                        segment: segment,
                        persona: persona,
                        field: field,
                        index: index,
                        action: 'edit',
                        new_value: newValue,
                        original_value: originalValue,
                        edited_by: reviewerName
                    }})
                }});

                if (!response.ok) {{
                    throw new Error('Server returned error');
                }}

                const result = await response.json();

                if (result.success) {{
                    // Update UI
                    exitEditMode(li, newValue);

                    // Add edited indicator
                    const editLog = {{
                        edited_by: reviewerName,
                        timestamp: new Date().toISOString(),
                        original_value: originalValue
                    }};

                    // Remove old indicator if exists
                    const oldIndicator = li.querySelector('.team-review-edited-indicator');
                    if (oldIndicator) oldIndicator.remove();

                    addEditedIndicator(li, editLog);

                    console.log('✓ Edit saved:', itemKey);
                }} else {{
                    throw new Error('Save failed');
                }}
            }} catch (error) {{
                console.error('Error saving edit:', error);

                // Show error message
                const errorMsg = document.createElement('span');
                errorMsg.className = 'team-review-edit-server-error';
                errorMsg.textContent = 'Failed to save — Server not running? Try again';
                li.appendChild(errorMsg);

                // Re-enable textarea
                textarea.disabled = false;
                saveBtn.disabled = false;
                saveBtn.textContent = '✓';
            }}
        }}

        /**
         * Cancel edit
         */
        function cancelEdit(li) {{
            const originalText = li.dataset.originalText;
            exitEditMode(li, originalText);
        }}

        /**
         * Exit edit mode and restore normal display
         */
        function exitEditMode(li, text) {{
            // Remove edit mode class
            li.classList.remove('team-review-edit-mode');

            // Remove textarea and buttons
            const textarea = li.querySelector('.team-review-edit-textarea');
            const actions = li.querySelector('.team-review-edit-actions');
            const errorMsg = li.querySelector('.team-review-edit-server-error');

            if (textarea) textarea.remove();
            if (actions) actions.remove();
            if (errorMsg) errorMsg.remove();

            // Restore text
            const textNode = Array.from(li.childNodes).find(node => node.nodeType === Node.TEXT_NODE);
            if (textNode) {{
                textNode.textContent = text + ' ';
            }} else {{
                li.insertBefore(document.createTextNode(text + ' '), li.firstChild);
            }}

            // Clear current editing state
            currentEditingItem = null;
        }}

        /**
         * Enter edit mode for Profile Overview field-item
         */
        function enterProfileFieldEditMode(fieldItem, segment, personaName, fieldName, labelText) {{
            // Prevent multiple edits at once
            if (currentEditingItem) {{
                alert('Please finish editing the current item first');
                return;
            }}

            const itemKey = `${{segment}}:${{personaName}}:profile_overview:${{fieldName}}`;
            currentEditingItem = itemKey;

            // Get current value (strip label)
            const valueSpan = fieldItem.querySelector('.field-value') || fieldItem;
            let currentValue = '';

            if (fieldName === 'job_titles') {{
                // For job_titles, get text after the label, split by comma
                const fullText = fieldItem.textContent.trim();
                const labelPrefix = labelText + ':';
                if (fullText.startsWith(labelPrefix)) {{
                    currentValue = fullText.substring(labelPrefix.length).trim();
                }}
            }} else {{
                // For single-value fields, get text after the label
                const fullText = fieldItem.textContent.trim();
                const labelPrefix = labelText + ':';
                if (fullText.startsWith(labelPrefix)) {{
                    currentValue = fullText.substring(labelPrefix.length).trim();
                }}
            }}

            // Store original data
            fieldItem.dataset.originalValue = currentValue;
            fieldItem.dataset.itemKey = itemKey;
            fieldItem.dataset.segment = segment;
            fieldItem.dataset.persona = personaName;
            fieldItem.dataset.fieldName = fieldName;

            // Add edit mode class
            fieldItem.classList.add('team-review-edit-mode');

            // Create textarea
            const textarea = document.createElement('textarea');
            textarea.className = 'team-review-edit-textarea';
            textarea.value = currentValue;

            // Keyboard shortcuts
            textarea.addEventListener('keydown', (e) => {{
                if (e.key === 'Enter' && !e.shiftKey) {{
                    e.preventDefault();
                    saveProfileFieldEdit(fieldItem);
                }} else if (e.key === 'Escape') {{
                    cancelProfileFieldEdit(fieldItem);
                }}
            }});

            // Replace content with textarea
            fieldItem.innerHTML = '';
            fieldItem.appendChild(textarea);

            // Create action buttons
            const actions = document.createElement('span');
            actions.className = 'team-review-edit-actions';

            const saveBtn = document.createElement('button');
            saveBtn.className = 'team-review-edit-btn team-review-edit-btn-save';
            saveBtn.textContent = '✓';
            saveBtn.onclick = () => saveProfileFieldEdit(fieldItem);

            const cancelBtn = document.createElement('button');
            cancelBtn.className = 'team-review-edit-btn team-review-edit-btn-cancel';
            cancelBtn.textContent = '✗';
            cancelBtn.onclick = () => cancelProfileFieldEdit(fieldItem);

            actions.appendChild(saveBtn);
            actions.appendChild(cancelBtn);

            fieldItem.appendChild(actions);

            // Focus textarea
            textarea.focus();
            textarea.setSelectionRange(textarea.value.length, textarea.value.length);
        }}

        /**
         * Save Profile Overview field edit
         */
        async function saveProfileFieldEdit(fieldItem) {{
            const textarea = fieldItem.querySelector('.team-review-edit-textarea');
            const newValue = textarea.value.trim();
            const originalValue = fieldItem.dataset.originalValue;

            // Validation: empty text (except for optional fields)
            if (!newValue) {{
                const errorMsg = document.createElement('span');
                errorMsg.className = 'team-review-edit-error';
                errorMsg.textContent = 'Field cannot be empty';
                textarea.parentNode.insertBefore(errorMsg, textarea.nextSibling);
                setTimeout(() => errorMsg.remove(), 3000);
                return;
            }}

            // If unchanged, treat as cancel
            if (newValue === originalValue) {{
                cancelProfileFieldEdit(fieldItem);
                return;
            }}

            const segment = fieldItem.dataset.segment;
            const persona = fieldItem.dataset.persona;
            const fieldName = fieldItem.dataset.fieldName;

            const reviewerName = getReviewerName();
            if (!reviewerName) {{
                alert('Please set your reviewer name first');
                cancelProfileFieldEdit(fieldItem);
                return;
            }}

            // Disable textarea during save
            textarea.disabled = true;
            const saveBtn = fieldItem.querySelector('.team-review-edit-btn-save');
            saveBtn.disabled = true;
            saveBtn.textContent = '...';

            try {{
                const response = await fetch('http://localhost:8080/api/save_edit', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        run_quarter: RUN_QUARTER,
                        segment: segment,
                        persona: persona,
                        field: 'profile_overview',
                        subfield: fieldName,
                        action: 'edit',
                        new_value: fieldName === 'job_titles' ? newValue.split(',').map(s => s.trim()).filter(s => s) : newValue,
                        original_value: fieldName === 'job_titles' ? originalValue.split(',').map(s => s.trim()).filter(s => s) : originalValue,
                        edited_by: reviewerName
                    }})
                }});

                if (!response.ok) {{
                    throw new Error('Server returned error');
                }}

                const result = await response.json();

                if (result.success) {{
                    // Exit edit mode and restore display
                    exitProfileFieldEditMode(fieldItem, fieldName, newValue);

                    // Add edited indicator
                    const editLog = {{
                        edited_by: reviewerName,
                        timestamp: new Date().toISOString(),
                        original_value: originalValue
                    }};

                    // Remove old indicator if exists
                    const oldIndicator = fieldItem.querySelector('.team-review-edited-indicator');
                    if (oldIndicator) oldIndicator.remove();

                    addEditedIndicatorToField(fieldItem, editLog);

                    console.log('✓ Profile field edit saved:', fieldName);
                }} else {{
                    throw new Error('Save failed');
                }}
            }} catch (error) {{
                console.error('Error saving profile field edit:', error);

                // Show error message
                const errorMsg = document.createElement('span');
                errorMsg.className = 'team-review-edit-server-error';
                errorMsg.textContent = 'Failed to save — Server not running? Try again';
                fieldItem.appendChild(errorMsg);

                // Re-enable textarea
                textarea.disabled = false;
                saveBtn.disabled = false;
                saveBtn.textContent = '✓';
            }}
        }}

        /**
         * Cancel Profile Overview field edit
         */
        function cancelProfileFieldEdit(fieldItem) {{
            const originalValue = fieldItem.dataset.originalValue;
            const fieldName = fieldItem.dataset.fieldName;
            exitProfileFieldEditMode(fieldItem, fieldName, originalValue);
        }}

        /**
         * Exit edit mode for Profile Overview field and restore normal display
         */
        function exitProfileFieldEditMode(fieldItem, fieldName, value) {{
            // Remove edit mode class
            fieldItem.classList.remove('team-review-edit-mode');

            // Remove textarea and buttons
            const textarea = fieldItem.querySelector('.team-review-edit-textarea');
            const actions = fieldItem.querySelector('.team-review-edit-actions');
            const errorMsg = fieldItem.querySelector('.team-review-edit-server-error');

            if (textarea) textarea.remove();
            if (actions) actions.remove();
            if (errorMsg) errorMsg.remove();

            // Restore field display with label
            const fieldLabels = {{
                'job_titles': 'Job Titles',
                'reports_to': 'Reports To',
                'team_size': 'Team Size',
                'prevalence': 'Prevalence in Deals',
                'role_in_deal': 'Role in Buying Process'
            }};

            const label = fieldLabels[fieldName] || fieldName;
            fieldItem.innerHTML = `<span class="field-label">${{label}}:</span>${{value}}`;

            // Clear current editing state
            currentEditingItem = null;
        }}

        /**
         * Add edited indicator to Profile Overview field-item
         */
        function addEditedIndicatorToField(fieldItem, editLog) {{
            const indicator = document.createElement('span');
            indicator.className = 'team-review-edited-indicator';
            indicator.textContent = '✎';
            indicator.title = `Edited by ${{editLog.edited_by}} at ${{new Date(editLog.timestamp).toLocaleString()}}\\nOriginal: ${{editLog.original_value}}`;
            fieldItem.appendChild(indicator);
        }}

        /**
         * Add double-click handlers to all items
         */
        function addEditHandlers() {{
            console.log('Adding double-click edit handlers to all items...');

            let handlerCount = 0;

            document.querySelectorAll('.persona-card').forEach(card => {{
                const personaTitle = card.querySelector('.persona-title');
                if (!personaTitle) return;

                const personaName = personaTitle.textContent.trim();

                // Find segment
                let segment = null;
                const segmentSection = card.closest('.tab-content');
                if (segmentSection) {{
                    const segmentId = segmentSection.id;
                    if (segmentId.includes('Digital')) segment = 'Digital';
                    else if (segmentId.includes('SMB')) segment = 'SMB';
                    else if (segmentId.includes('Commercial')) segment = 'Commercial';
                    else if (segmentId.includes('Enterprise')) segment = 'Enterprise';
                }}

                if (!segment) return;

                // Process each section
                card.querySelectorAll('.section-header').forEach(sectionHeader => {{
                    const sectionName = sectionHeader.textContent.trim();
                    const sectionText = sectionName.replace(/^[^a-zA-Z]+/, '').trim();

                    const fieldMap = {{
                        'Pain Points': 'challenges',
                        'Goals': 'goals',
                        'Objections': 'objections',
                        'Success Metrics': 'success_metrics',
                        'Product Requirements': 'product_requirements',
                        'Information Sources': 'information_sources',
                        'Messaging Preferences': 'messaging_preferences',
                        'Key Messages to Land': 'key_messages',
                        'Key Messages': 'key_messages',
                        'Profile Overview': 'profile_overview'
                    }};

                    const fieldName = fieldMap[sectionText];
                    if (!fieldName) return;

                    // Special handling for Profile Overview (uses field-item divs instead of UL)
                    if (fieldName === 'profile_overview') {{
                        let currentElement = sectionHeader.nextElementSibling;
                        while (currentElement && !currentElement.classList.contains('section-header')) {{
                            if (currentElement.classList && currentElement.classList.contains('field-item')) {{
                                const label = currentElement.querySelector('.field-label');
                                if (label) {{
                                    const labelText = label.textContent.trim().replace(':', '');
                                    const profileFieldMap = {{
                                        'Job Titles': 'job_titles',
                                        'Reports To': 'reports_to',
                                        'Team Size': 'team_size',
                                        'Prevalence in Deals': 'prevalence',
                                        'Role in Buying Process': 'role_in_deal'
                                    }};
                                    const profileFieldName = profileFieldMap[labelText];
                                    if (profileFieldName) {{
                                        // Add double-click handler for Profile Overview fields
                                        currentElement.addEventListener('dblclick', () => {{
                                            enterProfileFieldEditMode(currentElement, segment, personaName, profileFieldName, labelText);
                                        }});
                                        currentElement.style.cursor = 'pointer';
                                        handlerCount++;
                                    }}
                                }}
                            }}
                            currentElement = currentElement.nextElementSibling;
                        }}
                        return;
                    }}

                    // Find list items (standard sections)
                    let currentElement = sectionHeader.nextElementSibling;
                    while (currentElement && !currentElement.classList.contains('section-header')) {{
                        if (currentElement.tagName === 'UL') {{
                            currentElement.querySelectorAll('li').forEach((li, index) => {{
                                const itemKey = buildItemKey(segment, personaName, fieldName, index);

                                // Add double-click handler
                                li.addEventListener('dblclick', () => {{
                                    enterEditMode(li, itemKey, segment, personaName, fieldName, index);
                                }});

                                handlerCount++;
                            }});
                        }}
                        currentElement = currentElement.nextElementSibling;
                    }}
                }});
            }});

            console.log('✓ Added edit handlers to', handlerCount, 'items');
        }}

        // =================================================================
        // PHASE 4: ADD/DELETE FUNCTIONS
        // =================================================================

        /**
         * Add "+ Add item" buttons to all sections
         */
        function addAddItemButtons() {{
            console.log('Adding "+ Add item" buttons to all sections...');

            let buttonCount = 0;

            document.querySelectorAll('.persona-card').forEach(card => {{
                const personaTitle = card.querySelector('.persona-title');
                if (!personaTitle) return;

                const personaName = personaTitle.textContent.trim();

                // Find segment
                let segment = null;
                const segmentSection = card.closest('.tab-content');
                if (segmentSection) {{
                    const segmentId = segmentSection.id;
                    if (segmentId.includes('Digital')) segment = 'Digital';
                    else if (segmentId.includes('SMB')) segment = 'SMB';
                    else if (segmentId.includes('Commercial')) segment = 'Commercial';
                    else if (segmentId.includes('Enterprise')) segment = 'Enterprise';
                }}

                if (!segment) return;

                // Process each section
                card.querySelectorAll('.section-header').forEach(sectionHeader => {{
                    const sectionName = sectionHeader.textContent.trim();
                    const sectionText = sectionName.replace(/^[^a-zA-Z]+/, '').trim();

                    const fieldMap = {{
                        'Pain Points': 'challenges',
                        'Goals': 'goals',
                        'Objections': 'objections',
                        'Success Metrics': 'success_metrics',
                        'Product Requirements': 'product_requirements',
                        'Information Sources': 'information_sources',
                        'Messaging Preferences': 'messaging_preferences',
                        'Key Messages to Land': 'key_messages',
                        'Key Messages': 'key_messages',
                        'Profile Overview': 'profile_overview'
                    }};

                    const fieldName = fieldMap[sectionText];
                    if (!fieldName) return;

                    // Find the UL for this section
                    let currentElement = sectionHeader.nextElementSibling;
                    while (currentElement && !currentElement.classList.contains('section-header')) {{
                        if (currentElement.tagName === 'UL') {{
                            // Check if "+ Add item" button already exists
                            if (currentElement.nextElementSibling?.classList.contains('team-review-edit-add-btn')) {{
                                return;
                            }}

                            // Create "+ Add item" button
                            const addBtn = document.createElement('button');
                            addBtn.className = 'team-review-edit-add-btn';
                            addBtn.textContent = '+ Add item';
                            addBtn.onclick = () => showAddItemUI(currentElement, segment, personaName, fieldName);

                            // Insert after the UL
                            currentElement.parentNode.insertBefore(addBtn, currentElement.nextSibling);

                            buttonCount++;
                            break;
                        }}
                        currentElement = currentElement.nextElementSibling;
                    }}
                }});
            }});

            console.log('✓ Added "+ Add item" buttons to', buttonCount, 'sections');
        }}

        /**
         * Show add item UI (textarea + buttons)
         */
        function showAddItemUI(ulElement, segment, persona, field) {{
            // Check if already adding
            if (ulElement.parentNode.querySelector('.team-review-edit-add-container')) {{
                return;
            }}

            // Hide "+ Add item" button
            const addBtn = ulElement.nextElementSibling;
            if (addBtn?.classList.contains('team-review-edit-add-btn')) {{
                addBtn.style.display = 'none';
            }}

            // Create container
            const container = document.createElement('div');
            container.className = 'team-review-edit-add-container';

            // Create textarea
            const textarea = document.createElement('textarea');
            textarea.className = 'team-review-edit-textarea';
            textarea.placeholder = 'Enter new item text...';

            // Keyboard shortcuts
            textarea.addEventListener('keydown', (e) => {{
                if (e.key === 'Enter' && !e.shiftKey) {{
                    e.preventDefault();
                    saveAddItem(ulElement, segment, persona, field, textarea, container);
                }} else if (e.key === 'Escape') {{
                    cancelAddItem(container, addBtn);
                }}
            }});

            // Create action buttons
            const actions = document.createElement('span');
            actions.className = 'team-review-edit-actions';

            const saveBtn = document.createElement('button');
            saveBtn.className = 'team-review-edit-btn team-review-edit-btn-save';
            saveBtn.textContent = '✓';
            saveBtn.onclick = () => saveAddItem(ulElement, segment, persona, field, textarea, container);

            const cancelBtn = document.createElement('button');
            cancelBtn.className = 'team-review-edit-btn team-review-edit-btn-cancel';
            cancelBtn.textContent = '✗';
            cancelBtn.onclick = () => cancelAddItem(container, addBtn);

            actions.appendChild(saveBtn);
            actions.appendChild(cancelBtn);

            container.appendChild(textarea);
            container.appendChild(actions);

            // Insert after UL
            ulElement.parentNode.insertBefore(container, addBtn);

            // Focus textarea
            textarea.focus();
        }}

        /**
         * Save add item
         */
        async function saveAddItem(ulElement, segment, persona, field, textarea, container) {{
            const newValue = textarea.value.trim();

            // Validation
            if (!newValue) {{
                const errorMsg = document.createElement('span');
                errorMsg.className = 'team-review-edit-error';
                errorMsg.textContent = 'Item text cannot be empty';
                container.appendChild(errorMsg);
                setTimeout(() => errorMsg.remove(), 3000);
                return;
            }}

            const reviewerName = getReviewerName();
            if (!reviewerName) {{
                alert('Please set your reviewer name first');
                return;
            }}

            // Disable textarea during save
            textarea.disabled = true;
            const saveBtn = container.querySelector('.team-review-edit-btn-save');
            saveBtn.disabled = true;
            saveBtn.textContent = '...';

            try {{
                const response = await fetch('http://localhost:8080/api/save_edit', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        run_quarter: RUN_QUARTER,
                        segment: segment,
                        persona: persona,
                        field: field,
                        action: 'add',
                        new_value: newValue,
                        edited_by: reviewerName
                    }})
                }});

                if (!response.ok) {{
                    throw new Error('Server returned error');
                }}

                const result = await response.json();

                if (result.success) {{
                    // Create new li element
                    const newLi = document.createElement('li');
                    newLi.textContent = newValue + ' ';

                    // Add 🟢 NEW badge
                    const newBadge = document.createElement('span');
                    newBadge.className = 'team-review-edit-new-badge';
                    newBadge.textContent = '🟢 NEW';
                    newLi.appendChild(newBadge);

                    // Get new index (count current items)
                    const currentItems = ulElement.querySelectorAll('li');
                    const newIndex = currentItems.length;

                    // Add item key for voting/comments
                    const itemKey = buildItemKey(segment, persona, field, newIndex);

                    // Add voting container
                    const voteContainer = document.createElement('span');
                    voteContainer.className = 'team-review-vote-container';
                    voteContainer.setAttribute('data-item-key', itemKey);

                    const upBtn = document.createElement('button');
                    upBtn.className = 'team-review-vote-btn';
                    upBtn.setAttribute('data-vote-type', 'thumbs_up');
                    upBtn.innerHTML = '👍 <span class="team-review-vote-count up">0</span>';
                    upBtn.onclick = () => handleVote(itemKey, newValue, 'thumbs_up', upBtn);

                    const downBtn = document.createElement('button');
                    downBtn.className = 'team-review-vote-btn';
                    downBtn.setAttribute('data-vote-type', 'thumbs_down');
                    downBtn.innerHTML = '👎 <span class="team-review-vote-count down">0</span>';
                    downBtn.onclick = () => handleVote(itemKey, newValue, 'thumbs_down', downBtn);

                    voteContainer.appendChild(upBtn);
                    voteContainer.appendChild(downBtn);
                    newLi.appendChild(voteContainer);

                    // Add comment button
                    const commentBtn = document.createElement('button');
                    commentBtn.className = 'team-review-comment-btn';
                    commentBtn.setAttribute('data-comment-key', itemKey);
                    commentBtn.innerHTML = '💬 <span class="team-review-comment-count"></span>';
                    commentBtn.onclick = () => showCommentModal(itemKey, newValue);
                    newLi.appendChild(commentBtn);

                    // Add delete button
                    const deleteBtn = document.createElement('button');
                    deleteBtn.className = 'team-review-edit-delete-btn';
                    deleteBtn.textContent = '🗑';
                    deleteBtn.onclick = () => showDeleteConfirm(newLi, itemKey, segment, persona, field, newIndex, newValue);
                    newLi.appendChild(deleteBtn);

                    // Add double-click handler
                    newLi.addEventListener('dblclick', () => {{
                        enterEditMode(newLi, itemKey, segment, persona, field, newIndex);
                    }});

                    // Append to list
                    ulElement.appendChild(newLi);

                    // Remove container and show "+ Add item" button again
                    const addBtn = container.nextElementSibling;
                    container.remove();
                    if (addBtn?.classList.contains('team-review-edit-add-btn')) {{
                        addBtn.style.display = 'block';
                    }}

                    console.log('✓ Added new item:', itemKey);
                }} else {{
                    throw new Error('Save failed');
                }}
            }} catch (error) {{
                console.error('Error saving add:', error);

                // Show error message
                const errorMsg = document.createElement('span');
                errorMsg.className = 'team-review-edit-server-error';
                errorMsg.textContent = 'Failed to save — Server not running? Try again';
                container.appendChild(errorMsg);

                // Re-enable textarea
                textarea.disabled = false;
                saveBtn.disabled = false;
                saveBtn.textContent = '✓';
            }}
        }}

        /**
         * Cancel add item
         */
        function cancelAddItem(container, addBtn) {{
            container.remove();
            if (addBtn?.classList.contains('team-review-edit-add-btn')) {{
                addBtn.style.display = 'block';
            }}
        }}

        /**
         * Add delete buttons to all items
         */
        function addDeleteButtons() {{
            console.log('Adding delete buttons to all items...');

            let buttonCount = 0;

            document.querySelectorAll('.persona-card').forEach(card => {{
                const personaTitle = card.querySelector('.persona-title');
                if (!personaTitle) return;

                const personaName = personaTitle.textContent.trim();

                // Find segment
                let segment = null;
                const segmentSection = card.closest('.tab-content');
                if (segmentSection) {{
                    const segmentId = segmentSection.id;
                    if (segmentId.includes('Digital')) segment = 'Digital';
                    else if (segmentId.includes('SMB')) segment = 'SMB';
                    else if (segmentId.includes('Commercial')) segment = 'Commercial';
                    else if (segmentId.includes('Enterprise')) segment = 'Enterprise';
                }}

                if (!segment) return;

                // Process each section
                card.querySelectorAll('.section-header').forEach(sectionHeader => {{
                    const sectionName = sectionHeader.textContent.trim();
                    const sectionText = sectionName.replace(/^[^a-zA-Z]+/, '').trim();

                    const fieldMap = {{
                        'Pain Points': 'challenges',
                        'Goals': 'goals',
                        'Objections': 'objections',
                        'Success Metrics': 'success_metrics',
                        'Product Requirements': 'product_requirements',
                        'Information Sources': 'information_sources',
                        'Messaging Preferences': 'messaging_preferences',
                        'Key Messages to Land': 'key_messages',
                        'Key Messages': 'key_messages',
                        'Profile Overview': 'profile_overview'
                    }};

                    const fieldName = fieldMap[sectionText];
                    if (!fieldName) return;

                    // Find list items
                    let currentElement = sectionHeader.nextElementSibling;
                    while (currentElement && !currentElement.classList.contains('section-header')) {{
                        if (currentElement.tagName === 'UL') {{
                            currentElement.querySelectorAll('li').forEach((li, index) => {{
                                // Skip if already has delete button
                                if (li.querySelector('.team-review-edit-delete-btn')) return;

                                const itemKey = buildItemKey(segment, personaName, fieldName, index);
                                const itemText = li.childNodes[0]?.textContent?.trim() || '';

                                // Create delete button
                                const deleteBtn = document.createElement('button');
                                deleteBtn.className = 'team-review-edit-delete-btn';
                                deleteBtn.textContent = '🗑';
                                deleteBtn.onclick = () => showDeleteConfirm(li, itemKey, segment, personaName, fieldName, index, itemText);

                                li.appendChild(deleteBtn);
                                buttonCount++;
                            }});
                        }}
                        currentElement = currentElement.nextElementSibling;
                    }}
                }});
            }});

            console.log('✓ Added delete buttons to', buttonCount, 'items');
        }}

        /**
         * Show delete confirmation inline
         */
        function showDeleteConfirm(li, itemKey, segment, persona, field, index, itemText) {{
            // If in edit mode, exit it first
            if (li.classList.contains('team-review-edit-mode')) {{
                cancelEdit(li);
            }}

            // Check if confirmation already exists
            if (li.querySelector('.team-review-edit-delete-confirm')) {{
                return;
            }}

            // Create confirmation UI
            const confirmEl = document.createElement('div');
            confirmEl.className = 'team-review-edit-delete-confirm';

            const textEl = document.createElement('div');
            textEl.className = 'team-review-edit-delete-confirm-text';
            textEl.textContent = 'Remove this item? This can be undone by refreshing before applying edits.';

            const actionsEl = document.createElement('div');
            actionsEl.className = 'team-review-edit-delete-confirm-actions';

            const yesBtn = document.createElement('button');
            yesBtn.className = 'team-review-edit-delete-confirm-yes';
            yesBtn.textContent = 'Yes, remove';
            yesBtn.onclick = () => executeDelete(li, itemKey, segment, persona, field, index, itemText);

            const cancelBtn = document.createElement('button');
            cancelBtn.className = 'team-review-edit-delete-confirm-cancel';
            cancelBtn.textContent = 'Cancel';
            cancelBtn.onclick = () => confirmEl.remove();

            actionsEl.appendChild(yesBtn);
            actionsEl.appendChild(cancelBtn);
            confirmEl.appendChild(textEl);
            confirmEl.appendChild(actionsEl);

            li.appendChild(confirmEl);
        }}

        /**
         * Execute delete
         */
        async function executeDelete(li, itemKey, segment, persona, field, index, itemText) {{
            const reviewerName = getReviewerName();
            if (!reviewerName) {{
                alert('Please set your reviewer name first');
                return;
            }}

            // Disable buttons during delete
            const confirmEl = li.querySelector('.team-review-edit-delete-confirm');
            const yesBtn = confirmEl.querySelector('.team-review-edit-delete-confirm-yes');
            yesBtn.disabled = true;
            yesBtn.textContent = 'Removing...';

            try {{
                const response = await fetch('http://localhost:8080/api/save_edit', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        run_quarter: RUN_QUARTER,
                        segment: segment,
                        persona: persona,
                        field: field,
                        index: index,
                        action: 'delete',
                        original_value: itemText,
                        edited_by: reviewerName
                    }})
                }});

                if (!response.ok) {{
                    throw new Error('Server returned error');
                }}

                const result = await response.json();

                if (result.success) {{
                    // Fade out and remove
                    li.classList.add('team-review-edit-fade-out');
                    setTimeout(() => {{
                        li.remove();
                        console.log('✓ Deleted item:', itemKey);
                    }}, 300);
                }} else {{
                    throw new Error('Delete failed');
                }}
            }} catch (error) {{
                console.error('Error deleting item:', error);

                // Show error message
                const errorMsg = document.createElement('span');
                errorMsg.className = 'team-review-edit-error';
                errorMsg.textContent = 'Failed to delete — try again';
                confirmEl.appendChild(errorMsg);

                // Re-enable button
                yesBtn.disabled = false;
                yesBtn.textContent = 'Yes, remove';
            }}
        }}

        // =================================================================
        // STEP 2.2: REVIEWER IDENTIFICATION
        // =================================================================

        const REVIEWER_STORAGE_KEY = 'persona_reviewer_name';
        let currentReviewerName = null;

        // Add CSS for reviewer modal and header (scoped to Team Review only)
        const reviewerStyles = document.createElement('style');
        reviewerStyles.textContent = `
            .team-review-modal-overlay {{
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.6);
                z-index: 9998;
                animation: fadeIn 0.2s;
            }}
            .team-review-modal-overlay.show {{
                display: block;
            }}
            .team-review-modal {{
                display: none;
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: white;
                border-radius: 12px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                z-index: 9999;
                max-width: 500px;
                width: 90%;
                animation: slideIn 0.3s;
            }}
            .team-review-modal.show {{
                display: block;
            }}
            @keyframes fadeIn {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
            }}
            @keyframes slideIn {{
                from {{ transform: translate(-50%, -60%); opacity: 0; }}
                to {{ transform: translate(-50%, -50%); opacity: 1; }}
            }}
            .team-review-modal-header {{
                background: linear-gradient(135deg, #2D4C33 0%, #203524 100%);
                color: #D1F470;
                padding: 24px;
                border-radius: 12px 12px 0 0;
            }}
            .team-review-modal-header h2 {{
                margin: 0;
                font-size: 24px;
                font-weight: 700;
            }}
            .team-review-modal-body {{
                padding: 24px;
            }}
            .team-review-modal-body p {{
                margin: 0 0 20px 0;
                color: #4b5563;
                line-height: 1.6;
            }}
            .team-review-modal-body label {{
                display: block;
                font-weight: 600;
                color: #374151;
                margin-bottom: 8px;
            }}
            .team-review-modal-body input {{
                width: 100%;
                padding: 12px;
                border: 2px solid #d1d5db;
                border-radius: 8px;
                font-size: 16px;
                transition: border-color 0.2s;
            }}
            .team-review-modal-body input:focus {{
                outline: none;
                border-color: #2D4C33;
            }}
            .team-review-modal-footer {{
                padding: 0 24px 24px 24px;
                text-align: right;
            }}
            .team-review-modal-footer button {{
                background: linear-gradient(135deg, #A1D78F 0%, #88c478 100%);
                color: white;
                border: none;
                padding: 12px 32px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s, box-shadow 0.2s;
            }}
            .team-review-modal-footer button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(161, 215, 143, 0.4);
            }}
            .team-review-modal-footer button:disabled {{
                opacity: 0.5;
                cursor: not-allowed;
                transform: none;
            }}
            .team-review-header-info {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px 20px;
                text-align: center;
                font-size: 14px;
                font-weight: 600;
                box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
            }}
            .team-review-header-info .reviewer-name {{
                font-weight: 700;
                font-size: 16px;
            }}
            .team-review-header-info .change-name-link {{
                color: #D1F470;
                text-decoration: underline;
                cursor: pointer;
                margin-left: 12px;
                font-size: 13px;
            }}
            .team-review-header-info .change-name-link:hover {{
                color: white;
            }}
        `;
        document.head.appendChild(reviewerStyles);

        /**
         * Get reviewer name from localStorage
         */
        function getReviewerName() {{
            return localStorage.getItem(REVIEWER_STORAGE_KEY);
        }}

        /**
         * Save reviewer name to localStorage
         */
        function saveReviewerName(name) {{
            localStorage.setItem(REVIEWER_STORAGE_KEY, name);
            currentReviewerName = name;
        }}

        /**
         * Show reviewer name modal
         */
        function showReviewerModal() {{
            const overlay = document.getElementById('reviewerModalOverlay');
            const modal = document.getElementById('reviewerModal');
            const input = document.getElementById('reviewerNameInput');

            overlay.classList.add('show');
            modal.classList.add('show');
            input.focus();
        }}

        /**
         * Hide reviewer name modal
         */
        function hideReviewerModal() {{
            const overlay = document.getElementById('reviewerModalOverlay');
            const modal = document.getElementById('reviewerModal');

            overlay.classList.remove('show');
            modal.classList.remove('show');
        }}

        /**
         * Submit reviewer name
         */
        function submitReviewerName() {{
            const input = document.getElementById('reviewerNameInput');
            const name = input.value.trim();

            if (!name) {{
                alert('Please enter your name');
                input.focus();
                return;
            }}

            saveReviewerName(name);
            hideReviewerModal();
            displayReviewerHeader();

            console.log('✓ Reviewer identified:', name);
        }}

        /**
         * Display reviewer header with name
         */
        function displayReviewerHeader() {{
            const name = currentReviewerName || getReviewerName();
            if (!name) return;

            // Check if header already exists
            let header = document.getElementById('reviewerHeader');
            if (!header) {{
                header = document.createElement('div');
                header.id = 'reviewerHeader';
                header.className = 'team-review-header-info';

                // Insert after the main header
                const mainHeader = document.querySelector('.header');
                if (mainHeader) {{
                    mainHeader.after(header);
                }}
            }}

            header.innerHTML = `
                📝 Reviewing as: <span class="reviewer-name">${{name}}</span>
                <span class="change-name-link" onclick="changeReviewerName()">Change name</span>
            `;
        }}

        /**
         * Change reviewer name (show modal again)
         */
        window.changeReviewerName = function() {{
            const input = document.getElementById('reviewerNameInput');
            input.value = currentReviewerName || getReviewerName() || '';
            showReviewerModal();
        }};

        /**
         * Initialize reviewer identification
         */
        function initReviewerIdentification() {{
            // Guard: Only run on Team Review page
            if (typeof APPS_SCRIPT_URL === 'undefined') {{
                return;
            }}

            // Create modal HTML
            const modalHTML = `
                <div id="reviewerModalOverlay" class="team-review-modal-overlay"></div>
                <div id="reviewerModal" class="team-review-modal">
                    <div class="team-review-modal-header">
                        <h2>👋 Welcome to Team Review</h2>
                    </div>
                    <div class="team-review-modal-body">
                        <p>Enter your name to start reviewing. Your feedback will be saved to the shared Google Sheet so the team can see all input in real-time.</p>
                        <label for="reviewerNameInput">Your Name</label>
                        <input
                            type="text"
                            id="reviewerNameInput"
                            placeholder="e.g., Chris Sherman"
                            onkeypress="if(event.key === 'Enter') submitReviewerName()"
                        />
                    </div>
                    <div class="team-review-modal-footer">
                        <button onclick="submitReviewerName()">Start Reviewing</button>
                    </div>
                </div>
            `;

            // Add modal to body
            const container = document.createElement('div');
            container.innerHTML = modalHTML;
            document.body.appendChild(container);

            // Check if reviewer name exists
            currentReviewerName = getReviewerName();

            if (!currentReviewerName) {{
                // First visit - show modal
                console.log('First visit - requesting reviewer name');
                showReviewerModal();
            }} else {{
                // Returning reviewer - show header
                console.log('✓ Returning reviewer:', currentReviewerName);
                displayReviewerHeader();
            }}

            // Make submit function globally available
            window.submitReviewerName = submitReviewerName;
        }}

        // Run all features after DOM loads
        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', async () => {{
                initReviewerIdentification();
                await initVoting();
            }});
        }} else {{
            (async () => {{
                initReviewerIdentification();
                await initVoting();
            }})();
        }}

        // TODO: Phase 2 remaining steps
        // - Step 2.4: Comment buttons
        // - Step 2.5: Update Live Version button
    </script>
"""
        return js_code

    def generate_team_review_html(self) -> str:
        """Generate Team Review HTML by extending the Final page"""

        # Get the base HTML from the Final page generator
        print("📄 Generating base HTML from Final page generator...")
        base_html = generate_final_html()

        # Generate collaborative features JavaScript
        print("🔧 Adding collaborative features layer...")
        collaborative_js = self.generate_collaborative_features()

        # Inject collaborative features before </body>
        enhanced_html = base_html.replace('</body>', f'{collaborative_js}\n</body>')

        print("✓ Team Review HTML generated (base + collaborative features)")
        return enhanced_html

    def save_version(self, personas: Dict) -> str:
        """Save a versioned snapshot of personas"""
        today = datetime.now().strftime('%Y-%m-%d')
        version_file = self.versions_dir / f"personas_{today}.json"

        with open(version_file, 'w') as f:
            json.dump(personas, f, indent=2)

        return str(version_file)


def main():
    """Generate Team Review page with collaborative features"""
    print("\n" + "="*80)
    print("🤝 TEAM REVIEW GENERATOR - Collaborative Persona Review")
    print("="*80)

    generator = CollaborativePersonaGenerator()

    # Generate Team Review HTML
    html = generator.generate_team_review_html()

    # Write to file
    output_file = Path(__file__).parent / "persona_analysis" / "reports" / "Persona_Team_Review_Full.html"
    with open(output_file, 'w') as f:
        f.write(html)

    print(f"\n✓ Team review generated")
    print(f"📍 Location: {output_file}")

    # Load personas for versioning
    data_file = Path(__file__).parent / "persona_analysis" / "data" / "updated_personas.json"
    if data_file.exists():
        with open(data_file, 'r') as f:
            data = json.load(f)
            personas = data.get('personas', data)

        # Save version
        version_file = generator.save_version(personas)
        print(f"\n✓ Version saved: {version_file}")

    print("\n" + "="*80)
    print("✨ FILES GENERATED")
    print("="*80)
    print(f"\n📤 Share link (after git push):")
    print(f"   https://chrissherman-png.github.io/persona-analysis/Persona_Team_Review_Full.html")
    print("\n" + "="*80)


if __name__ == "__main__":
    main()
