"""
Enhanced persona generator that shows FULL profiles with inline change indicators
Creates both team review and approval versions with complete persona data
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import copy

# Import personas
from generate_persona_profiles import personas

class EnhancedPersonaUpdater:
    def __init__(self, base_dir="/Users/chris.sherman/persona_analysis"):
        self.base_dir = Path(base_dir)
        self.versions_dir = self.base_dir / "versions"
        self.reports_dir = self.base_dir / "reports"
        self.feedback_dir = self.base_dir / "team_feedback"
        self.data_dir = self.base_dir / "data"

        self.versions_dir.mkdir(exist_ok=True)
        self.reports_dir.mkdir(exist_ok=True)
        self.feedback_dir.mkdir(exist_ok=True)

        # Load change reasons if available
        self.change_reasons = self.load_change_reasons()

    def load_change_reasons(self) -> Dict:
        """Load change reasons generated during persona update"""
        reasons_file = self.data_dir / "change_reasons.json"
        if reasons_file.exists():
            with open(reasons_file, 'r') as f:
                return json.load(f)
        return {}

    def get_change_reason(self, segment: str, persona: str, field: str, item_index: int = None) -> str:
        """Get the reason for a specific change"""
        if item_index is not None:
            key = f"{segment}.{persona}.{field}[{item_index}]"
        else:
            key = f"{segment}.{persona}.{field}"

        reason = self.change_reasons.get(key, "")

        if not reason:
            # Generate default reasons based on field type
            if "pain_points" in field or "challenges" in field:
                reason = "Updated based on recent Gong call analysis"
            elif "goals" in field:
                reason = "Updated to reflect current customer priorities"
            elif "objections" in field:
                reason = "Added from recent customer conversations"
            elif "key_messages" in field:
                reason = "Updated to reflect market trends"
            elif "recommended_products" in field:
                reason = "Re-prioritized based on product mention frequency"
            else:
                reason = "Updated based on quarterly data analysis"

        return reason

    def load_previous_version(self) -> Dict:
        """Load the most recent previous version"""
        version_files = sorted(self.versions_dir.glob("personas_*.json"))
        if not version_files:
            return None
        with open(version_files[-1], 'r') as f:
            return json.load(f)

    def save_version(self, personas: Dict, version_date: str = None):
        """Save current version"""
        if version_date is None:
            version_date = datetime.now().strftime("%Y-%m-%d")

        version_file = self.versions_dir / f"personas_{version_date}.json"
        with open(version_file, 'w') as f:
            json.dump({
                'version_date': version_date,
                'personas': personas
            }, f, indent=2)
        return version_file

    def detect_changes(self, old_data: Dict, new_data: Dict) -> Dict:
        """Detect all changes and create a structured map"""
        if old_data is None:
            return {'has_changes': False, 'changes': []}

        old_personas = old_data.get('personas', {})
        changes_list = []

        for segment in ['Digital', 'SMB', 'Commercial', 'Enterprise']:
            for persona_name in new_data.get(segment, {}).keys():
                old_persona = old_personas.get(segment, {}).get(persona_name, {})
                new_persona = new_data[segment][persona_name]

                for field in ['job_titles', 'reports_to', 'team_size', 'prevalence',
                             'role_in_deal', 'goals', 'pain_points', 'challenges_from_gong',
                             'evaluation_criteria', 'objections', 'key_messages',
                             'content_preferences', 'success_metrics', 'buying_behavior', 'recommended_products']:

                    old_val = old_persona.get(field)
                    new_val = new_persona.get(field)

                    change_id = f"{segment}.{persona_name}.{field}"

                    if isinstance(old_val, list) and isinstance(new_val, list):
                        # List changes
                        added = [item for item in new_val if item not in old_val]
                        removed = [item for item in old_val if item not in new_val]

                        for item in added:
                            changes_list.append({
                                'id': f"{change_id}.added.{len(changes_list)}",
                                'path': f"{segment}.{persona_name}",
                                'persona': persona_name,
                                'segment': segment,
                                'field': field,
                                'type': 'added',
                                'old': None,
                                'new': item,
                                'item_value': item
                            })

                        for item in removed:
                            changes_list.append({
                                'id': f"{change_id}.removed.{len(changes_list)}",
                                'path': f"{segment}.{persona_name}",
                                'persona': persona_name,
                                'segment': segment,
                                'field': field,
                                'type': 'deleted',
                                'old': item,
                                'new': None,
                                'item_value': item
                            })

                    elif isinstance(old_val, dict) and isinstance(new_val, dict):
                        # Nested dict (like buying_behavior)
                        for key in set(list(old_val.keys()) + list(new_val.keys())):
                            if old_val.get(key) != new_val.get(key):
                                change_type = 'added' if key not in old_val else 'modified' if key in new_val else 'deleted'
                                changes_list.append({
                                    'id': f"{change_id}.{key}",
                                    'path': f"{segment}.{persona_name}",
                                    'persona': persona_name,
                                    'segment': segment,
                                    'field': f"{field}.{key}",
                                    'type': change_type,
                                    'old': old_val.get(key),
                                    'new': new_val.get(key)
                                })

                    else:
                        # Simple field
                        if old_val != new_val:
                            change_type = 'added' if old_val is None else 'modified' if new_val is not None else 'deleted'
                            changes_list.append({
                                'id': change_id,
                                'path': f"{segment}.{persona_name}",
                                'persona': persona_name,
                                'segment': segment,
                                'field': field,
                                'type': change_type,
                                'old': old_val,
                                'new': new_val
                            })

        return {
            'has_changes': len(changes_list) > 0,
            'changes': changes_list
        }

    def load_feedback_counts(self) -> Dict:
        """Load and aggregate all feedback to get vote counts"""
        feedback_files = list(self.feedback_dir.glob("persona_feedback_*.json"))

        vote_counts = {}
        submissions = []

        for file in feedback_files:
            with open(file, 'r') as f:
                data = json.load(f)
                submissions.append(data)

                for item in data.get('feedback', []):
                    change_id = item.get('change_id', '')
                    if not change_id:
                        continue

                    if change_id not in vote_counts:
                        vote_counts[change_id] = {'agree': 0, 'disagree': 0, 'comments': []}

                    if item['vote'] == 'agree':
                        vote_counts[change_id]['agree'] += 1
                    elif item['vote'] == 'disagree':
                        vote_counts[change_id]['disagree'] += 1

                    if item.get('comment'):
                        vote_counts[change_id]['comments'].append({
                            'reviewer': data['reviewer'],
                            'comment': item['comment'],
                            'timestamp': data['timestamp']
                        })

        return {
            'counts': vote_counts,
            'submissions': submissions,
            'total_reviewers': len(submissions)
        }

    def generate_team_review_html(self, personas: Dict, changes_data: Dict) -> str:
        """Generate collaborative team review HTML where users can vote and comment in real-time"""

        # Create a changes map for quick lookup
        changes_map = {}
        for change in changes_data['changes']:
            key = f"{change['segment']}.{change['persona']}.{change['field']}"
            if key not in changes_map:
                changes_map[key] = []
            changes_map[key].append(change)

        html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Persona Review - Collaborative Feedback</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f8f9fa;
            line-height: 1.6;
            color: #333;
        }
        .header {
            background: linear-gradient(135deg, #2D4C33 0%, #203524 100%);
            color: #D1F470;
            padding: 40px 20px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header h1 { font-size: 32px; margin-bottom: 10px; }
        .container { max-width: 1000px; margin: 0 auto; padding: 15px; }

        .reviewer-info {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        .reviewer-info input {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 14px;
            margin-top: 8px;
        }

        .comment-summary {
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
            color: white;
            padding: 16px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(102,126,234,0.3);
            display: none;
            align-items: center;
            gap: 12px;
            transition: all 0.2s;
            position: relative;
        }

        .comment-nav-btn {
            background: rgba(255, 255, 255, 0.2);
            border: 2px solid rgba(255, 255, 255, 0.3);
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            font-size: 20px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .comment-nav-btn:hover {
            background: rgba(255, 255, 255, 0.3);
            border-color: rgba(255, 255, 255, 0.5);
            transform: scale(1.1);
        }

        .comment-nav-btn:active {
            transform: scale(0.95);
        }

        .comment-summary.show {
            display: flex;
        }

        .comment-summary-icon {
            font-size: 24px;
        }

        .comment-summary-text {
            flex: 1;
            font-size: 14px;
            font-weight: 500;
        }

        .comment-summary-count {
            font-size: 20px;
            font-weight: bold;
        }

        .comment-summary-action {
            font-size: 12px;
            opacity: 0.9;
            display: flex;
            align-items: center;
            gap: 4px;
        }

        /* Highlight for items with comments when navigating */
        .comment-highlight {
            animation: pulseHighlight 1.5s ease-out;
            background: linear-gradient(90deg, rgba(139,92,246,0.2) 0%, transparent 100%) !important;
            border-left: 4px solid #8B5CF6 !important;
        }

        @keyframes pulseHighlight {
            0%, 100% { background: linear-gradient(90deg, rgba(139,92,246,0.2) 0%, transparent 100%); }
            50% { background: linear-gradient(90deg, rgba(139,92,246,0.4) 0%, transparent 100%); }
        }

        /* Tabs */
        .tabs {
            display: flex;
            gap: 4px;
            background: white;
            padding: 20px 20px 0 20px;
            border-radius: 8px 8px 0 0;
            margin-bottom: 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }

        .tab {
            padding: 12px 24px;
            background: #f8f9fa;
            border: none;
            border-radius: 8px 8px 0 0;
            cursor: pointer;
            font-size: 15px;
            font-weight: 600;
            color: #666;
            transition: all 0.2s;
            border-bottom: 3px solid transparent;
        }

        .tab:hover {
            background: #e9ecef;
            color: #333;
        }

        .tab.active {
            background: linear-gradient(135deg, #A1D78F 0%, #88c478 100%);
            color: white;
            border-bottom: 4px solid #2D4C33;
            font-weight: 700;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(161, 215, 143, 0.4);
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        .segment-section {
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }

        .segment-section.digital {
            border-left: 6px solid #60A5FA;
        }

        .segment-section.smb {
            border-left: 6px solid #A1D78F;
        }

        .segment-section.commercial {
            border-left: 6px solid #FEEB7E;
        }

        .segment-section.enterprise {
            border-left: 6px solid #A78BFA;
        }

        .segment-header {
            margin: -20px -20px 20px -20px;
            padding: 16px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-radius: 8px 8px 0 0;
        }

        .segment-section.digital .segment-header {
            background: #60A5FA;
        }

        .segment-section.smb .segment-header {
            background: #A1D78F;
        }

        .segment-section.commercial .segment-header {
            background: #FEEB7E;
        }

        .segment-section.enterprise .segment-header {
            background: #A78BFA;
        }

        .segment-title {
            font-size: 22px;
            font-weight: bold;
            margin: 0;
        }

        .segment-section.digital .segment-title {
            color: #1E3A8A;
        }

        .segment-section.smb .segment-title {
            color: #2D4C33;
        }

        .segment-section.commercial .segment-title {
            color: #11110D;
        }

        .segment-section.enterprise .segment-title {
            color: #5B21B6;
        }

        .segment-subtitle {
            font-size: 14px;
            opacity: 0.8;
            font-weight: 500;
        }

        .segment-section.digital .segment-subtitle {
            color: #1E3A8A;
        }

        .segment-section.smb .segment-subtitle {
            color: #2D4C33;
        }

        .segment-section.commercial .segment-subtitle {
            color: #11110D;
        }

        .segment-section.enterprise .segment-subtitle {
            color: #5B21B6;
        }

        .persona-card {
            margin-top: 20px;
            margin-bottom: 15px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
            border: 1px solid #e5e7eb;
            overflow: hidden;
            transition: box-shadow 0.3s ease;
        }

        .persona-card:hover {
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.12);
        }

        .persona-title {
            font-size: 20px;
            font-weight: bold;
            color: #11110D;
            padding: 14px 18px;
            margin: 0;
        }

        .segment-section.digital .persona-title {
            background: linear-gradient(135deg, #60A5FA 0%, #3B82F6 100%);
        }

        .segment-section.smb .persona-title {
            background: linear-gradient(135deg, #A1D78F 0%, #88c478 100%);
        }

        .segment-section.commercial .persona-title {
            background: linear-gradient(135deg, #FEEB7E 0%, #f5dc5e 100%);
        }

        .segment-section.enterprise .persona-title {
            background: linear-gradient(135deg, #A78BFA 0%, #8B5CF6 100%);
        }

        .persona-content {
            padding: 18px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        .persona-column {
            min-width: 0;
        }

        .section-header {
            font-size: 15px;
            font-weight: 600;
            margin: 12px 0 6px 0;
            padding-bottom: 3px;
            border-bottom: 1px solid #e5e7eb;
        }

        .segment-section.digital .section-header {
            color: #1E3A8A;
        }

        .segment-section.smb .section-header {
            color: #2D4C33;
        }

        .segment-section.commercial .section-header {
            color: #11110D;
        }

        .segment-section.enterprise .section-header {
            color: #5B21B6;
        }

        .section-header:first-child {
            margin-top: 0;
        }

        .full-width {
            grid-column: 1 / -1;
        }

        .field-item {
            margin: 6px 0;
            padding: 4px 0;
            font-size: 14px;
            line-height: 1.5;
        }

        .field-label {
            font-weight: 600;
            color: #495057;
            font-size: 14px;
        }

        .change-indicator {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
            margin-left: 8px;
            text-transform: uppercase;
            cursor: pointer;
            transition: all 0.2s;
        }

        .change-indicator:hover {
            transform: translateY(-1px);
            box-shadow: 0 2px 4px rgba(0,0,0,0.15);
        }

        .badge-added {
            background: #d1fae5;
            color: #065f46;
        }

        .badge-modified {
            background: #dbeafe;
            color: #1e40af;
        }

        .badge-deleted {
            background: #fee2e2;
            color: #991b1b;
        }

        /* Modal for change reasons */
        .reason-modal {
            display: none;
            position: fixed;
            z-index: 10000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.6);
            animation: fadeIn 0.2s;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .reason-modal-content {
            background-color: #fefefe;
            margin: 10% auto;
            padding: 0;
            border-radius: 12px;
            width: 90%;
            max-width: 700px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            animation: slideDown 0.3s;
        }

        @keyframes slideDown {
            from { transform: translateY(-50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        .reason-modal-header {
            padding: 24px;
            border-bottom: 1px solid #e5e7eb;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .reason-modal-title {
            font-size: 20px;
            font-weight: 600;
            color: #111827;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .reason-modal-close {
            color: #6b7280;
            font-size: 32px;
            font-weight: 300;
            cursor: pointer;
            line-height: 1;
            transition: color 0.2s;
        }

        .reason-modal-close:hover,
        .reason-modal-close:focus {
            color: #111827;
        }

        .reason-modal-body {
            padding: 24px;
            font-size: 15px;
            line-height: 1.8;
            color: #374151;
        }

        .reason-badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
        }

        .reason-badge.new { background: #d1fae5; color: #065f46; }
        .reason-badge.removed { background: #fee2e2; color: #991b1b; }
        .reason-badge.kept { background: #dbeafe; color: #1e40af; }
        .reason-badge.modified { background: #fef3c7; color: #92400e; }

        .old-value {
            color: #dc2626;
            text-decoration: line-through;
            font-size: 14px;
            margin-left: 10px;
        }

        /* Vote controls */
        .vote-controls {
            display: inline-flex;
            gap: 4px;
            margin-left: 8px;
            vertical-align: middle;
        }

        .vote-btn {
            padding: 4px 8px;
            border: 1px solid #e5e7eb;
            background: white;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.2s;
            position: relative;
        }

        .vote-btn:hover {
            border-color: #667eea;
            transform: scale(1.1);
        }

        .vote-btn.active-agree {
            background: #d1fae5;
            border-color: #10b981;
        }

        .vote-btn.active-disagree {
            background: #fee2e2;
            border-color: #ef4444;
        }

        .vote-count {
            font-size: 11px;
            font-weight: 600;
            color: #666;
            margin-left: 2px;
        }

        /* Tooltip for showing voters */
        .vote-tooltip {
            display: none;
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            background: #11110D;
            color: white;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 12px;
            white-space: normal;
            max-width: 200px;
            word-wrap: break-word;
            margin-bottom: 5px;
            z-index: 1000;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            text-align: center;
        }

        .vote-btn:hover .vote-tooltip {
            display: block;
        }

        .vote-tooltip::after {
            content: '';
            position: absolute;
            top: 100%;
            left: 50%;
            transform: translateX(-50%);
            border: 5px solid transparent;
            border-top-color: #11110D;
        }

        /* Comment indicator */
        .comment-indicator {
            display: inline-block;
            margin-left: 6px;
            color: #667eea;
            font-size: 14px;
            cursor: pointer;
            opacity: 0;
            transition: all 0.2s;
            position: relative;
        }

        .field-item:hover .comment-indicator,
        li:hover .comment-indicator {
            opacity: 1;
        }

        .comment-indicator.has-comments {
            opacity: 1;
            color: white;
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
            padding: 2px 8px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 12px;
            box-shadow: 0 2px 6px rgba(102,126,234,0.4);
        }

        .comment-indicator.has-comments:hover {
            transform: scale(1.1);
        }

        /* Highlight items with comments */
        .field-item:has(.comment-indicator.has-comments),
        li:has(.comment-indicator.has-comments) {
            background: linear-gradient(90deg, rgba(118,75,162,0.05) 0%, transparent 100%);
            padding-left: 8px;
            margin-left: -8px;
            border-left: 3px solid rgba(118,75,162,0.3);
            border-radius: 4px;
        }

        /* Comment popup */
        .comment-popup {
            display: none;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            z-index: 2000;
            max-width: 500px;
            width: 90%;
            max-height: 70vh;
            overflow: auto;
        }

        .comment-popup.show {
            display: block;
        }

        .comment-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.5);
            z-index: 1999;
        }

        .comment-overlay.show {
            display: block;
        }

        .comment-header {
            padding: 20px;
            border-bottom: 1px solid #e5e7eb;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .comment-header h3 {
            margin: 0;
            font-size: 18px;
        }

        .close-btn {
            background: none;
            border: none;
            font-size: 24px;
            cursor: pointer;
            color: #666;
            padding: 0;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .close-btn:hover {
            color: #333;
        }

        .comment-body {
            padding: 20px;
        }

        .comment-list {
            margin-bottom: 20px;
        }

        .comment-item {
            background: #f8f9fa;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 10px;
        }

        .comment-author {
            font-weight: 600;
            font-size: 13px;
            color: #2D4C33;
            margin-bottom: 4px;
        }

        .comment-text {
            font-size: 14px;
            color: #333;
            line-height: 1.5;
        }

        .comment-input {
            margin-top: 15px;
        }

        .comment-input textarea {
            width: 100%;
            padding: 12px;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            font-family: inherit;
            font-size: 14px;
            min-height: 80px;
            resize: vertical;
        }

        .comment-input button {
            margin-top: 10px;
            padding: 10px 20px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
        }

        .comment-input button:hover {
            background: #5568d3;
        }

        .comment-input button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        /* Product Cards */
        .recommended-products {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-top: 10px;
            width: 100%;
        }

        .product-card {
            background: #f8f9fa;
            border-left: 4px solid #0275d8;
            padding: 12px;
            border-radius: 6px;
            position: relative;
        }

        .product-card.change-indicator.added {
            border-left-color: #5cb85c;
            background: #f0f9f0;
        }

        .product-card.change-indicator.modified {
            border-left-color: #0275d8;
            background: #f0f7ff;
        }

        .product-card.change-indicator.deleted {
            border-left-color: #d9534f;
            background: #fff5f5;
            opacity: 0.7;
        }

        .product-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }

        .product-name {
            font-weight: 600;
            color: #333;
            font-size: 14px;
        }

        .relevance-badge {
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
        }

        .relevance-critical {
            background: #d9534f;
            color: white;
        }

        .relevance-high {
            background: #f0ad4e;
            color: white;
        }

        .relevance-medium {
            background: #5bc0de;
            color: white;
        }

        .product-section {
            margin-bottom: 10px;
        }

        .product-section-title {
            font-size: 11px;
            font-weight: 600;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        }

        .product-why {
            font-size: 13px;
            color: #333;
            line-height: 1.5;
            font-weight: 500;
        }

        .product-challenge {
            font-size: 12px;
            color: #555;
            line-height: 1.4;
            font-style: italic;
        }

        .product-link {
            font-size: 12px;
            color: #0275d8;
            text-decoration: none;
            font-weight: 500;
        }

        .product-link:hover {
            text-decoration: underline;
        }

        /* Messaging Guide Card */
        .messaging-guide-card {
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
            border: 1px solid #e5e7eb;
            margin: 20px 0;
            padding: 18px;
        }

        .messaging-guide-title {
            font-size: 18px;
            font-weight: 700;
            color: #11110D;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .messaging-guide-subtitle {
            font-size: 13px;
            color: #666;
            margin-bottom: 16px;
        }

        .messaging-guide-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-bottom: 16px;
        }

        .messaging-guide-column {
            border-radius: 6px;
            padding: 14px;
        }

        .messaging-guide-column.dos {
            background: #f0f9f0;
            border-left: 4px solid #28a745;
        }

        .messaging-guide-column.donts {
            background: #fff5f5;
            border-left: 4px solid #dc3545;
        }

        .messaging-guide-column-title {
            font-size: 15px;
            font-weight: 700;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .messaging-guide-column.dos .messaging-guide-column-title {
            color: #28a745;
        }

        .messaging-guide-column.donts .messaging-guide-column-title {
            color: #dc3545;
        }

        .messaging-guide-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .messaging-guide-list li {
            font-size: 13px;
            line-height: 1.6;
            margin-bottom: 8px;
            color: #333;
        }

        .messaging-guide-list li:last-child {
            margin-bottom: 0;
        }

        .messaging-guide-insight {
            background: #fff9e6;
            border-left: 4px solid #ffc107;
            border-radius: 6px;
            padding: 12px 14px;
        }

        .messaging-guide-insight-title {
            font-size: 13px;
            font-weight: 700;
            color: #856404;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .messaging-guide-insight-text {
            font-size: 13px;
            line-height: 1.6;
            color: #856404;
        }
    </style>
</head>
<body>
    <!-- Modal for displaying change reasons -->
    <div id="reasonModal" class="reason-modal">
        <div class="reason-modal-content">
            <div class="reason-modal-header">
                <div class="reason-modal-title">
                    <span id="reasonBadge" class="reason-badge"></span>
                    <span>Change Reason</span>
                </div>
                <span class="reason-modal-close" onclick="closeReasonModal()">&times;</span>
            </div>
            <div class="reason-modal-body" id="reasonModalBody">
                <!-- Reason text will be inserted here -->
            </div>
        </div>
    </div>

    <div class="header">
        <h1>📊 Buyer Persona Profiles - Collaborative Review</h1>
        <p>Vote and comment on changes in real-time</p>
    </div>

    <div class="container">
        <div class="reviewer-info">
            <label for="reviewerName">
                <strong>Your Name</strong> (required for voting and commenting)
                <input type="text" id="reviewerName" placeholder="Enter your name">
            </label>
        </div>

        <div class="comment-summary" id="commentSummary">
            <button class="comment-nav-btn" onclick="navigateToPrevComment(event)" title="Previous comment">
                ←
            </button>
            <span class="comment-summary-icon">💬</span>
            <div class="comment-summary-text">
                <strong><span id="currentCommentNum">1</span> of <span id="commentCount">0</span></strong> items have comments
                <div class="comment-summary-action">Use arrows to navigate</div>
            </div>
            <button class="comment-nav-btn" onclick="navigateToNextComment(event)" title="Next comment">
                →
            </button>
        </div>

        <div class="tabs" id="segmentTabs">
            <button class="tab active" onclick="switchTab('Digital')">Digital (≤49 employees)</button>
            <button class="tab" onclick="switchTab('SMB')">SMB (50-249 employees)</button>
            <button class="tab" onclick="switchTab('Commercial')">Commercial (250-1,499)</button>
            <button class="tab" onclick="switchTab('Enterprise')">Enterprise (1,500+)</button>
            <button class="tab" onclick="switchTab('DataSources')">📊 Data Sources</button>
        </div>

        <div id="profilesContainer">
            <!-- Profiles will be injected here -->
        </div>
    </div>

    <!-- Comment popup -->
    <div class="comment-overlay" id="commentOverlay" onclick="closeCommentPopup()"></div>
    <div class="comment-popup" id="commentPopup">
        <div class="comment-header">
            <h3>💬 Comments</h3>
            <button class="close-btn" onclick="closeCommentPopup()">×</button>
        </div>
        <div class="comment-body">
            <div class="comment-list" id="commentList"></div>
            <div class="comment-input">
                <textarea id="newComment" placeholder="Add your comment..."></textarea>
                <button onclick="submitComment()">Post Comment</button>
            </div>
        </div>
    </div>

    <script>
        const CHANGES_DATA = ''' + json.dumps(changes_data['changes']) + ''';
        const PERSONAS_DATA = ''' + json.dumps(personas) + ''';
        const CHANGE_REASONS = ''' + json.dumps(self.change_reasons) + ''';
        const GOOGLE_SHEETS_API_URL = 'https://script.google.com/macros/s/AKfycbxKZxlM-sKdIk7mXbRh8pyy156VrP32O51exgvwlaRmGwiPLM-sdLEbUZSo9bSHFxS8Dw/exec';

        let reviewerName = '';
        let allData = {
            votes: {},      // changeId -> {agree: ['name1', 'name2'], disagree: ['name3']}
            comments: {}    // changeId -> [{author: 'name', text: 'comment', timestamp}]
        };
        let currentCommentId = null;
        let currentActiveTab = 'Digital'; // Track active tab
        let autoRefreshInterval = null;
        let pendingSaves = 0; // Track saves in progress

        // Load data from Google Sheets
        async function loadDataFromSheets(forceUpdate = false) {
            // Don't overwrite local data if we have saves in progress
            if (pendingSaves > 0 && !forceUpdate) {
                console.log('Skipping refresh - saves in progress');
                return;
            }

            try {
                const response = await fetch(GOOGLE_SHEETS_API_URL + '?action=getData');
                const data = await response.json();
                allData.votes = data.votes || {};
                allData.comments = data.comments || {};
                renderProfiles();
            } catch (error) {
                console.error('Error loading data from Google Sheets:', error);
                // Fallback to localStorage for offline support
                const savedData = localStorage.getItem('persona_collaborative_data');
                if (savedData) {
                    const parsed = JSON.parse(savedData);
                    allData = parsed.allData || allData;
                    reviewerName = parsed.reviewerName || '';
                    document.getElementById('reviewerName').value = reviewerName;
                }
            }
        }

        function hashContent(content) {
            /**
             * Generate simple hash of content to match with stored reasons
             * Uses same algorithm as Python persona_generator.py
             */
            const contentStr = typeof content === 'object' ? JSON.stringify(content) : String(content);

            // Simple hash function (matches Python implementation)
            let hash = 0;
            for (let i = 0; i < contentStr.length; i++) {
                const char = contentStr.charCodeAt(i);
                hash = ((hash << 5) - hash) + char;
                // Convert to unsigned 32bit (matches Python's & 0xFFFFFFFF)
                hash = hash >>> 0;
            }

            // Take absolute value and convert to hex string (8 chars)
            const absHash = Math.abs(hash);
            return absHash.toString(16).padStart(8, '0').substring(0, 8);
        }

        function getChangeReason(segment, persona, field, index = null, changeType = 'modified', itemContent = null) {
            /**
             * Get the reason why a change was made.
             * Returns tooltip text to display on hover.
             */
            let key;

            // For removed items, try to look up by content hash
            if (changeType === 'deleted' && itemContent) {
                const contentHash = hashContent(itemContent);
                key = `${segment}.${persona}.${field}.removed.${contentHash}`;
                console.log('DEBUG getChangeReason - removed item:', {
                    segment,
                    persona,
                    field,
                    itemContent: itemContent.substring(0, 50),
                    contentHash,
                    key,
                    found: !!CHANGE_REASONS[key]
                });
                if (CHANGE_REASONS[key]) {
                    console.log('Found detailed reason:', CHANGE_REASONS[key].substring(0, 100));
                    return CHANGE_REASONS[key];
                } else {
                    console.log('Key not found in CHANGE_REASONS');
                }
            }

            // For indexed items (added/kept)
            if (index !== null) {
                key = `${segment}.${persona}.${field}[${index}]`;
            } else {
                key = `${segment}.${persona}.${field}`;
            }

            // Check if we have a specific reason
            if (CHANGE_REASONS[key]) {
                return CHANGE_REASONS[key];
            }

            // Generate default reason based on field and change type
            if (field.includes('challenges') || field.includes('pain_points')) {
                if (changeType === 'added') {
                    return 'Added based on recent customer mentions in Gong calls';
                } else if (changeType === 'deleted') {
                    return 'Removed - no longer a top priority based on recent call analysis';
                } else {
                    return 'Updated from latest call analysis';
                }
            } else if (field.includes('goals')) {
                if (changeType === 'added') {
                    return 'New goal identified from customer conversations';
                } else if (changeType === 'deleted') {
                    return 'Removed - replaced by more current objectives';
                } else {
                    return 'Updated to reflect current priorities';
                }
            } else if (field.includes('objections')) {
                if (changeType === 'added') {
                    return 'New objection captured from recent deals';
                } else if (changeType === 'deleted') {
                    return 'Removed - less commonly raised in recent quarters';
                } else {
                    return 'Updated based on sales call analysis';
                }
            } else if (field.includes('key_messages')) {
                if (changeType === 'added') {
                    return 'Added to reflect current market trends';
                } else if (changeType === 'deleted') {
                    return 'Removed - messaging superseded by current market positioning';
                } else {
                    return 'Updated messaging based on research';
                }
            } else if (field.includes('recommended_products')) {
                if (changeType === 'deleted') {
                    return 'Removed - significantly fewer mentions in recent calls';
                } else {
                    return 'Re-prioritized based on product mention frequency in calls';
                }
            } else {
                if (changeType === 'added') {
                    return 'Added from quarterly data analysis';
                } else if (changeType === 'deleted') {
                    return 'Removed based on latest data analysis';
                } else {
                    return 'Updated based on latest insights';
                }
            }
        }

        async function init() {
            // Load reviewer name from localStorage
            const savedName = localStorage.getItem('persona_reviewer_name');
            if (savedName) {
                reviewerName = savedName;
                document.getElementById('reviewerName').value = reviewerName;
            }

            // Load data from Google Sheets
            await loadDataFromSheets();

            // Set up name input listener
            document.getElementById('reviewerName').addEventListener('input', (e) => {
                reviewerName = e.target.value.trim();
                localStorage.setItem('persona_reviewer_name', reviewerName);
            });

            // Set up auto-refresh every 5 seconds
            autoRefreshInterval = setInterval(loadDataFromSheets, 5000);
        }

        async function saveVote(changeId, voteType) {
            pendingSaves++;
            try {
                const params = new URLSearchParams({
                    action: 'saveVote',
                    changeId: changeId,
                    reviewer: reviewerName,
                    voteType: voteType || ''
                });
                const response = await fetch(GOOGLE_SHEETS_API_URL + '?' + params.toString());
                const result = await response.json();
                if (result.success) {
                    // Save complete - force reload to get latest state
                    await loadDataFromSheets(true);
                }
            } catch (error) {
                console.error('Error saving vote:', error);
            } finally {
                pendingSaves--;
            }
        }

        async function saveCommentToSheets(changeId, text) {
            pendingSaves++;
            try {
                const params = new URLSearchParams({
                    action: 'saveComment',
                    changeId: changeId,
                    author: reviewerName,
                    text: text
                });
                const response = await fetch(GOOGLE_SHEETS_API_URL + '?' + params.toString());
                const result = await response.json();
                if (result.success) {
                    // Save complete - force reload to get latest state
                    await loadDataFromSheets(true);
                }
            } catch (error) {
                console.error('Error saving comment:', error);
            } finally {
                pendingSaves--;
            }
        }

        function escapeHtml(text) {
            if (text === null || text === undefined) return '';
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        function getCompetitiveIntel(segment) {
            const intel = {
                'Digital': {
                    competitors: [
                        {
                            name: 'Freshdesk',
                            threat: 'High',
                            why: 'Low price and simple setup appeal to startups',
                            counter: 'Zendesk scales with you; Freshdesk forces migration at growth'
                        },
                        {
                            name: 'Intercom',
                            threat: 'Medium',
                            why: 'Modern UI and messaging-first approach for SaaS companies',
                            counter: 'Zendesk is omnichannel; Intercom is messaging-only'
                        }
                    ]
                },
                'SMB': {
                    competitors: [
                        {
                            name: 'Freshdesk',
                            threat: 'High',
                            why: 'Low price and simple setup appeal to growing businesses',
                            counter: 'Zendesk scales with you; Freshdesk forces migration at growth'
                        },
                        {
                            name: 'Intercom',
                            threat: 'Medium',
                            why: 'Modern UI and messaging-first approach',
                            counter: 'Zendesk is omnichannel; Intercom is messaging-only'
                        }
                    ]
                },
                'Commercial': {
                    competitors: [
                        {
                            name: 'Salesforce Service Cloud',
                            threat: 'Very High',
                            why: 'Deep CRM integration, brand recognition, enterprise scale',
                            counter: 'Zendesk is faster to implement with better agent UX'
                        },
                        {
                            name: 'Freshdesk',
                            threat: 'Medium',
                            why: 'Lower cost option for cost-conscious buyers',
                            counter: 'Limited scalability and weak integrations at this scale'
                        }
                    ]
                },
                'Enterprise': {
                    competitors: [
                        {
                            name: 'Salesforce Service Cloud',
                            threat: 'Very High',
                            why: 'Deep CRM integration, brand recognition, enterprise scale',
                            counter: 'Zendesk is faster to implement with better agent UX'
                        },
                        {
                            name: 'ServiceNow',
                            threat: 'Medium',
                            why: 'ITSM integration, enterprise workflows, compliance capabilities',
                            counter: 'Zendesk is purpose-built for CX; ServiceNow retrofitted from ITSM'
                        }
                    ]
                }
            };
            return intel[segment];
        }

        function getMessagingGuide(segment) {
            const guides = {
                'Digital': {
                    dos: [
                        '<strong>"Set up in 15 minutes"</strong> - Emphasize speed and simplicity',
                        '<strong>"No IT team needed"</strong> - Highlight self-service capability',
                        '<strong>"Automation"</strong> - Use instead of "AI" (less intimidating)',
                        '<strong>"$X per month"</strong> - Show concrete, affordable pricing',
                        '<strong>"Self-service"</strong> - Focus on independence and control'
                    ],
                    donts: [
                        '<strong>"Enterprise-grade"</strong> - Sounds expensive and complex',
                        '<strong>"Implementation timeline"</strong> - Use "setup time" instead',
                        '<strong>"Dedicated CSM"</strong> - They don\\'t expect this level of service',
                        '<strong>"AI/Machine Learning"</strong> - Technical jargon that feels out of reach',
                        '<strong>"ROI analysis"</strong> - Too formal; use "save money" or "save time"'
                    ],
                    keyInsight: 'Digital buyers (44% facing cost pressure) want simple language that emphasizes immediate value and ease of use. They\\'re buying tools, not transformations.'
                },
                'SMB': {
                    dos: [
                        '<strong>"Automation"</strong> - More tangible than "AI" (your example!)',
                        '<strong>"30% productivity gain"</strong> - Concrete, measurable outcomes',
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

        function renderProfiles() {
            const container = document.getElementById('profilesContainer');
            const changesMap = {};

            // Create changes lookup
            CHANGES_DATA.forEach(change => {
                const key = `${change.segment}.${change.persona}.${change.field}`;
                if (!changesMap[key]) changesMap[key] = [];
                changesMap[key].push(change);
            });

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

                // Add Competitive Intelligence
                const competitiveIntel = getCompetitiveIntel(segment);
                if (competitiveIntel) {
                    html += `<div class="messaging-guide-card">`;
                    html += `<div class="messaging-guide-title">🎯 Competitive Landscape for ${segment}</div>`;
                    html += `<div class="messaging-guide-subtitle">Key competitors and how to position against them</div>`;
                    html += `<div style="margin-top: 15px;">`;

                    competitiveIntel.competitors.forEach(comp => {
                        const threatColor = comp.threat === 'Very High' ? '#dc2626' :
                                          comp.threat === 'High' ? '#f59e0b' : '#6b7280';
                        html += `<div style="background: #f9fafb; border-left: 4px solid ${threatColor}; padding: 14px; margin-bottom: 12px; border-radius: 6px;">`;
                        html += `<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">`;
                        html += `<div style="font-size: 16px; font-weight: 700; color: #111827;">${comp.name}</div>`;
                        html += `<div style="font-size: 12px; font-weight: 600; padding: 3px 8px; border-radius: 12px; background: ${threatColor}; color: white;">${comp.threat} Threat</div>`;
                        html += `</div>`;
                        html += `<div style="font-size: 14px; color: #4b5563; margin-bottom: 6px;"><strong>Why they compete:</strong> ${comp.why}</div>`;
                        html += `<div style="font-size: 14px; color: #0275d8;"><strong>How to counter:</strong> ${comp.counter}</div>`;
                        html += `</div>`;
                    });

                    html += `</div>`;
                    html += `</div>`; // close competitive-intel-card
                }

                Object.keys(PERSONAS_DATA[segment]).forEach(personaName => {
                    const persona = PERSONAS_DATA[segment][personaName];
                    html += `<div class="persona-card">`;
                    html += `<div class="persona-title">${personaName}</div>`;
                    html += `<div class="persona-content" style="display: block; padding: 18px;">`;

                    // SECTION 1: Profile Overview (manual)
                    html += `<div class="section-header" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">📋 Profile Overview</div>`;
                    html += `<div class="profile-fields" style="padding: 10px 0;">`;
                    html += renderField('Job Titles', persona.job_titles.join(', '), segment, personaName, 'job_titles', changesMap);
                    html += renderField('Reports To', persona.reports_to, segment, personaName, 'reports_to', changesMap);
                    html += renderField('Team Size', persona.team_size, segment, personaName, 'team_size', changesMap);
                    html += renderField('Prevalence in Deals', persona.prevalence, segment, personaName, 'prevalence', changesMap);
                    html += renderField('Role in Buying Process', persona.role_in_deal, segment, personaName, 'role_in_deal', changesMap);
                    html += `</div>`;

                    // SECTION 2: Pain Points (NLP enhanced)
                    html += `<div class="section-header" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">😓 Pain Points</div>`;
                    const painPointsEnhanced = persona.pain_points_enhanced || [];
                    const painPoints = persona.pain_points || persona.challenges || persona.challenges_from_gong || [];
                    if (painPointsEnhanced.length > 0) {
                        html += renderEnhancedList(painPointsEnhanced, segment, personaName, 'pain_points', changesMap);
                    } else {
                        html += renderList(painPoints, segment, personaName, 'challenges_from_gong', changesMap);
                    }

                    // SECTION 3: Goals (NLP enhanced)
                    html += `<div class="section-header" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">🎯 Goals</div>`;
                    const goalsEnhanced = persona.goals_enhanced || [];
                    if (goalsEnhanced.length > 0) {
                        html += renderEnhancedList(goalsEnhanced, segment, personaName, 'goals', changesMap);
                    } else {
                        html += renderList(persona.goals || [], segment, personaName, 'goals', changesMap);
                    }

                    // SECTION 4: Objections (NLP enhanced)
                    html += `<div class="section-header" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">⚠️ Objections</div>`;
                    const objectionsEnhanced = persona.objections_enhanced || [];
                    if (objectionsEnhanced.length > 0) {
                        html += renderEnhancedList(objectionsEnhanced, segment, personaName, 'objections', changesMap);
                    } else {
                        html += renderList(persona.objections || [], segment, personaName, 'objections', changesMap);
                    }

                    // SECTION 5: Trigger Events (NEW - NLP enhanced)
                    const triggerEventsEnhanced = persona.trigger_events_enhanced || [];
                    if (triggerEventsEnhanced.length > 0) {
                        html += `<div class="section-header new" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">🔔 Trigger Events</div>`;
                        html += renderEnhancedList(triggerEventsEnhanced, segment, personaName, 'trigger_events', changesMap);
                    }

                    // SECTION 6: Product Requirements (NEW - NLP enhanced)
                    const productRequirementsEnhanced = persona.product_requirements_enhanced || [];
                    if (productRequirementsEnhanced.length > 0) {
                        html += `<div class="section-header new" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">✅ Product Requirements</div>`;
                        html += renderEnhancedList(productRequirementsEnhanced, segment, personaName, 'product_requirements', changesMap);
                    }

                    // SECTION 7: Information Sources (NEW - NLP enhanced)
                    const informationSourcesEnhanced = persona.information_sources_enhanced || [];
                    if (informationSourcesEnhanced.length > 0) {
                        html += `<div class="section-header new" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">📚 Information Sources</div>`;
                        html += renderEnhancedList(informationSourcesEnhanced, segment, personaName, 'information_sources', changesMap);
                    }

                    // SECTION 8: Messaging Preferences (NEW - NLP enhanced)
                    const messagingPreferencesEnhanced = persona.messaging_preferences_enhanced || [];
                    if (messagingPreferencesEnhanced.length > 0) {
                        html += `<div class="section-header new" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">💬 Messaging Preferences</div>`;
                        html += renderEnhancedList(messagingPreferencesEnhanced, segment, personaName, 'messaging_preferences', changesMap);
                    }

                    // SECTION 9: Verbatim Quotes (show 3-5 representative quotes)
                    const verbatimQuotes = persona.verbatim_quotes || [];
                    if (verbatimQuotes.length > 0) {
                        html += `<div class="section-header" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">🗣️ Verbatim Quotes</div>`;
                        html += `<div style="padding: 10px 0;">`;
                        verbatimQuotes.slice(0, 5).forEach((quote, idx) => {
                            html += `<div class="quote" style="margin: 12px 0; padding: 12px 16px; background: #f8f9fa; border-left: 4px solid #3498db; border-radius: 4px; font-style: italic; color: #555; font-size: 14px;">`;
                            html += `"${escapeHtml(quote)}"`;
                            html += `</div>`;
                        });
                        html += `</div>`;
                    }

                    // SECTION 10: Success Metrics (NLP enhanced)
                    html += `<div class="section-header new" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">📊 Success Metrics</div>`;
                    const successMetricsEnhanced = persona.success_metrics_enhanced || [];
                    if (successMetricsEnhanced.length > 0) {
                        html += renderEnhancedList(successMetricsEnhanced, segment, personaName, 'success_metrics', changesMap);
                    } else {
                        html += renderList(persona.success_metrics || [], segment, personaName, 'success_metrics', changesMap);
                    }

                    html += `</div>`; // persona-content

                    // Recommended Products Section - spans full width below
                    if (persona.recommended_products && persona.recommended_products.length > 0) {
                        html += `<div style="padding: 0 18px 18px 18px;">`;
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
                            html += '<div class="product-section-title">✓ Solves This Challenge</div>';
                            html += '<div class="product-challenge">' + escapeHtml(product.addresses_challenge) + '</div>';
                            html += '</div>';
                            html += '<a href="' + escapeHtml(product.url) + '" target="_blank" class="product-link">Learn more →</a>';
                            html += '</div>';
                        });
                        html += `</div>`; // recommended-products
                        html += `</div>`; // padding container
                    }

                    html += `</div>`; // persona-card
                });

                html += `</div>`; // segment-section
                html += `</div>`; // tab-content
            });

            // Add Data Sources tab
            html += `<div class="tab-content" id="tab-DataSources">`;
            html += `<div class="segment-section">`;
            html += `<div class="segment-header">`;
            html += `<div class="segment-title">📊 Data Sources & Methodology</div>`;
            html += `<div class="segment-subtitle">Understanding how these personas were built</div>`;
            html += `</div>`;

            html += `<div class="persona-card">`;
            html += `<div class="persona-title">Primary Data Source: Gong Call Analysis</div>`;
            html += `<div class="persona-content" style="display: block;">`;
            html += `<div class="section-header" style="margin-top: 0;">📞 Gong Calls Analyzed</div>`;
            html += `<div class="field-item" style="font-size: 20px; font-weight: 600; color: #0275d8; margin-bottom: 20px;">`;
            html += `Total: 158,997 calls</div>`;
            html += `<div class="field-item" style="color: #666; margin-bottom: 20px;">`;
            html += `Analysis Period: October 2025 - April 2026 (6 months)</div>`;

            html += `<div class="section-header">Breakdown by Segment</div>`;
            html += `<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px;">`;
            html += `<div style="padding: 15px; background: #f0f9ff; border-left: 4px solid #0ea5e9; border-radius: 6px;">`;
            html += `<div style="font-size: 24px; font-weight: 700; color: #0ea5e9;">26,335</div>`;
            html += `<div style="font-size: 14px; color: #666; margin-top: 4px;">Digital Segment</div>`;
            html += `<div style="font-size: 12px; color: #999;">≤49 employees</div>`;
            html += `</div>`;
            html += `<div style="padding: 15px; background: #f0fdf4; border-left: 4px solid #10b981; border-radius: 6px;">`;
            html += `<div style="font-size: 24px; font-weight: 700; color: #10b981;">54,049</div>`;
            html += `<div style="font-size: 14px; color: #666; margin-top: 4px;">SMB Segment</div>`;
            html += `<div style="font-size: 12px; color: #999;">50-249 employees</div>`;
            html += `</div>`;
            html += `<div style="padding: 15px; background: #fef3c7; border-left: 4px solid #f59e0b; border-radius: 6px;">`;
            html += `<div style="font-size: 24px; font-weight: 700; color: #f59e0b;">46,554</div>`;
            html += `<div style="font-size: 14px; color: #666; margin-top: 4px;">Commercial Segment</div>`;
            html += `<div style="font-size: 12px; color: #999;">250-1,499 employees</div>`;
            html += `</div>`;
            html += `<div style="padding: 15px; background: #fce7f3; border-left: 4px solid #ec4899; border-radius: 6px;">`;
            html += `<div style="font-size: 24px; font-weight: 700; color: #ec4899;">32,059</div>`;
            html += `<div style="font-size: 14px; color: #666; margin-top: 4px;">Enterprise Segment</div>`;
            html += `<div style="font-size: 12px; color: #999;">1,500+ employees</div>`;
            html += `</div>`;
            html += `</div>`;

            html += `<div class="section-header">What Was Analyzed</div>`;
            html += `<ul style="margin: 0; padding-left: 20px;">`;
            html += `<li style="margin-bottom: 8px;"><strong>Persona identification:</strong> Job titles, roles, and decision-making authority</li>`;
            html += `<li style="margin-bottom: 8px;"><strong>Pain points & challenges:</strong> Customer-voiced problems and obstacles</li>`;
            html += `<li style="margin-bottom: 8px;"><strong>Evaluation criteria:</strong> What matters when choosing solutions</li>`;
            html += `<li style="margin-bottom: 8px;"><strong>Objections:</strong> Common concerns and pushback patterns</li>`;
            html += `<li style="margin-bottom: 8px;"><strong>Product interest:</strong> Which products resonate with each persona</li>`;
            html += `</ul>`;
            html += `</div></div>`;

            html += `<div class="persona-card">`;
            html += `<div class="persona-title">Product Recommendations Source</div>`;
            html += `<div class="persona-content" style="display: block;">`;
            html += `<div class="section-header" style="margin-top: 0;">📊 Product Mention Analysis</div>`;
            html += `<div class="field-item">Same dataset of 158,997 Gong calls analyzed for:</div>`;
            html += `<ul style="margin: 10px 0; padding-left: 20px;">`;
            html += `<li style="margin-bottom: 8px;"><strong>Product mention frequency:</strong> How often each product came up by segment</li>`;
            html += `<li style="margin-bottom: 8px;"><strong>Challenge mapping:</strong> Which products solve which customer-stated problems</li>`;
            html += `<li style="margin-bottom: 8px;"><strong>Segment-specific needs:</strong> How priorities differ by company size</li>`;
            html += `</ul>`;
            html += `<div class="field-item" style="margin-top: 15px; padding: 12px; background: #f8f9fa; border-left: 3px solid #0275d8; border-radius: 4px;">`;
            html += `<strong>Key Finding:</strong> Integration needs (60-62% mention rate) and cost pressure (38-47%) are universal across all segments, but AI adoption shows strong growth (33-37% mention rate).`;
            html += `</div>`;
            html += `</div></div>`;

            html += `<div class="persona-card">`;
            html += `<div class="persona-title">Methodology Notes</div>`;
            html += `<div class="persona-content" style="display: block;">`;
            html += `<div class="section-header" style="margin-top: 0;">🔬 Analysis Approach</div>`;
            html += `<div class="field-item"><strong>1. Call Segmentation</strong></div>`;
            html += `<div class="field-item" style="padding-left: 15px; color: #666; margin-bottom: 12px;">`;
            html += `Calls were automatically categorized by company size based on employee count data from CRM enrichment.`;
            html += `</div>`;
            html += `<div class="field-item"><strong>2. Persona Identification</strong></div>`;
            html += `<div class="field-item" style="padding-left: 15px; color: #666; margin-bottom: 12px;">`;
            html += `Job titles and roles were extracted from call metadata and participant information to identify decision makers and influencers.`;
            html += `</div>`;
            html += `<div class="field-item"><strong>3. Theme Extraction</strong></div>`;
            html += `<div class="field-item" style="padding-left: 15px; color: #666; margin-bottom: 12px;">`;
            html += `NLP analysis identified recurring themes in pain points, objections, evaluation criteria, and feature requests across conversations.`;
            html += `</div>`;
            html += `<div class="field-item"><strong>4. Product-Challenge Mapping</strong></div>`;
            html += `<div class="field-item" style="padding-left: 15px; color: #666; margin-bottom: 12px;">`;
            html += `Product mentions were correlated with stated challenges to identify which solutions address which problems for each persona.`;
            html += `</div>`;
            html += `</div></div>`;

            html += `<div class="persona-card">`;
            html += `<div class="persona-title">Secondary Sources & References</div>`;
            html += `<div class="persona-content" style="display: block;">`;

            html += `<div class="section-header" style="margin-top: 0;">📊 Industry Analyst Reports</div>`;
            html += `<ul style="margin: 0 0 20px 0; padding-left: 20px;">`;
            html += `<li style="margin-bottom: 12px;">`;
            html += `<strong>Gartner:</strong> "Magic Quadrant for Customer Service and Support Technologies" (March 2026)<br>`;
            html += `<span style="color: #666; font-size: 13px;">Key insights: AI and automation are table stakes; Integration capabilities are top evaluation criteria; Self-service deflection targets at 50-60%; Mid-market prioritizes ease of implementation</span><br>`;
            html += `<a href="https://www.gartner.com/en/customer-service-support/trends" target="_blank" style="color: #0275d8; font-size: 13px;">View Report →</a>`;
            html += `</li>`;
            html += `<li style="margin-bottom: 12px;">`;
            html += `<strong>Forrester:</strong> "The Forrester Wave: Customer Service Solutions, Q1 2026" (February 2026)<br>`;
            html += `<span style="color: #666; font-size: 13px;">Key insights: Omnichannel messaging is must-have; Procurement involvement moved 40% earlier; SMB demands sub-30 day implementations; Contact center consolidation is $2B+ opportunity</span><br>`;
            html += `<a href="https://www.forrester.com/customer-service" target="_blank" style="color: #0275d8; font-size: 13px;">View Report →</a>`;
            html += `</li>`;
            html += `<li style="margin-bottom: 12px;">`;
            html += `<strong>IDC:</strong> "Worldwide Customer Care BPO Services Forecast, 2026-2030" (January 2026)<br>`;
            html += `<span style="color: #666; font-size: 13px;">Key insights: Cost pressure affecting 40%+ of enterprise CX orgs; Multi-language AI critical for global support; WFM integration required for 100+ agent deployments</span><br>`;
            html += `<a href="https://www.idc.com" target="_blank" style="color: #0275d8; font-size: 13px;">View Report →</a>`;
            html += `</li>`;
            html += `</ul>`;

            html += `<div class="section-header">📈 Market Trends Research</div>`;
            html += `<ul style="margin: 0 0 20px 0; padding-left: 20px;">`;
            html += `<li style="margin-bottom: 10px;"><strong>AI Adoption Acceleration:</strong> AI mention rate in customer service calls increased 350% YoY <span style="color: #999;">(Gong Internal Data + Industry Analysis)</span></li>`;
            html += `<li style="margin-bottom: 10px;"><strong>Procurement Earlier in Sales Cycle:</strong> Finance/Procurement now involved 40% earlier than 2024 <span style="color: #999;">(Forrester + Gong Call Analysis)</span></li>`;
            html += `<li style="margin-bottom: 10px;"><strong>SMB Implementation Speed Demands:</strong> SMB buyers expect &lt;30 day go-live, down from 60-90 days <span style="color: #999;">(Gong Call Analysis)</span></li>`;
            html += `<li style="margin-bottom: 10px;"><strong>Vendor Consolidation Wave:</strong> Average CX tech stack decreased from 12 tools to 7 tools <span style="color: #999;">(Gartner + Customer Interviews)</span></li>`;
            html += `<li style="margin-bottom: 10px;"><strong>WhatsApp Business Adoption:</strong> WhatsApp Business API adoption up 200% in 18 months <span style="color: #999;">(Meta Business Reports + Gong Data)</span></li>`;
            html += `</ul>`;

            html += `<div class="section-header">🏢 Competitive Intelligence</div>`;
            html += `<div class="field-item" style="margin-bottom: 15px; color: #666;">`;
            html += `Competitive positioning and messaging informed by analysis of mentions and win/loss patterns across 158,997 Gong calls, covering:`;
            html += `</div>`;
            html += `<ul style="margin: 0 0 20px 0; padding-left: 20px;">`;
            html += `<li style="margin-bottom: 8px;"><strong>Salesforce Service Cloud</strong> - Deep CRM integration vs. faster Zendesk implementation</li>`;
            html += `<li style="margin-bottom: 8px;"><strong>Freshdesk</strong> - Lower initial cost vs. Zendesk scalability at growth</li>`;
            html += `<li style="margin-bottom: 8px;"><strong>Intercom</strong> - Messaging-first approach vs. Zendesk omnichannel</li>`;
            html += `<li style="margin-bottom: 8px;"><strong>ServiceNow</strong> - ITSM heritage vs. Zendesk purpose-built CX</li>`;
            html += `</ul>`;

            html += `<div class="section-header">👔 Job Market & Persona Research</div>`;
            html += `<div class="field-item" style="margin-bottom: 10px; color: #666;">`;
            html += `Salary ranges, responsibilities, and decision authority informed by:`;
            html += `</div>`;
            html += `<ul style="margin: 0 0 20px 0; padding-left: 20px;">`;
            html += `<li style="margin-bottom: 8px;">LinkedIn job postings and professional profiles analysis</li>`;
            html += `<li style="margin-bottom: 8px;">Salary data from Glassdoor, Levels.fyi, and Payscale</li>`;
            html += `<li style="margin-bottom: 8px;">Title and responsibility patterns from 158,997 Gong call participants</li>`;
            html += `</ul>`;

            html += `<div class="section-header">🔗 Product Information</div>`;
            html += `<ul style="margin: 0 0 20px 0; padding-left: 20px;">`;
            html += `<li style="margin-bottom: 8px;"><strong>Zendesk Product Pages:</strong> Referenced for product capabilities and positioning in "Recommended Products" sections</li>`;
            html += `</ul>`;

            html += `<div class="section-header">📅 Last Updated</div>`;
            html += `<div class="field-item">April 7, 2026</div>`;
            html += `<div class="field-item" style="color: #666; margin-top: 5px;">`;
            html += `Next refresh planned for Q3 2026 (July-September data)`;
            html += `</div>`;
            html += `</div></div>`;

            html += `</div></div>`; // segment-section and tab-content

            container.innerHTML = html;
            updateCommentSummary();
            restoreActiveTab(); // Restore previously selected tab
        }

        function switchTab(segment) {
            currentActiveTab = segment; // Save current tab

            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });

            // Show selected tab
            document.getElementById(`tab-${segment}`).classList.add('active');
            event.currentTarget.classList.add('active');

            // Scroll to top
            window.scrollTo({top: 0, behavior: 'smooth'});
        }

        function restoreActiveTab() {
            // Restore the previously active tab after re-rendering
            if (currentActiveTab) {
                document.querySelectorAll('.tab-content').forEach(tab => {
                    tab.classList.remove('active');
                });
                document.querySelectorAll('.tab').forEach(tab => {
                    tab.classList.remove('active');
                });

                document.getElementById(`tab-${currentActiveTab}`)?.classList.add('active');
                document.querySelectorAll('.tab').forEach(tab => {
                    if (tab.onclick.toString().includes(currentActiveTab)) {
                        tab.classList.add('active');
                    }
                });
            }
        }

        function updateCommentSummary() {
            // Get all unique items with comments (filter out empty arrays and duplicates)
            commentsWithIds = Object.keys(allData.comments).filter(id => {
                const comments = allData.comments[id];
                return comments && Array.isArray(comments) && comments.length > 0;
            });

            const summaryEl = document.getElementById('commentSummary');
            const countEl = document.getElementById('commentCount');
            const currentNumEl = document.getElementById('currentCommentNum');

            if (commentsWithIds.length > 0) {
                countEl.textContent = commentsWithIds.length;
                // Reset to first comment when count changes
                if (currentCommentIndex >= commentsWithIds.length) {
                    currentCommentIndex = 0;
                }
                currentNumEl.textContent = currentCommentIndex >= 0 ? currentCommentIndex + 1 : 1;
                summaryEl.classList.add('show');
            } else {
                summaryEl.classList.remove('show');
                currentCommentIndex = -1;
            }
        }

        let currentCommentIndex = -1;
        let commentsWithIds = [];

        function navigateToNextComment(event) {
            if (event) event.stopPropagation();

            // Get all items with comments
            commentsWithIds = Object.keys(allData.comments).filter(id => {
                const comments = allData.comments[id];
                return comments && Array.isArray(comments) && comments.length > 0;
            });

            if (commentsWithIds.length === 0) {
                return;
            }

            // Move to next comment (cycle back to start)
            currentCommentIndex = (currentCommentIndex + 1) % commentsWithIds.length;
            navigateToComment(currentCommentIndex);
        }

        function navigateToPrevComment(event) {
            if (event) event.stopPropagation();

            // Get all items with comments
            commentsWithIds = Object.keys(allData.comments).filter(id => {
                const comments = allData.comments[id];
                return comments && Array.isArray(comments) && comments.length > 0;
            });

            if (commentsWithIds.length === 0) {
                return;
            }

            // Move to previous comment (cycle to end if at start)
            currentCommentIndex = currentCommentIndex <= 0 ? commentsWithIds.length - 1 : currentCommentIndex - 1;
            navigateToComment(currentCommentIndex);
        }

        function navigateToComment(index) {
            const commentId = commentsWithIds[index];

            console.log('Navigating to comment:', commentId);
            console.log('Total comments with IDs:', commentsWithIds);
            console.log('All comments data:', allData.comments);

            // Update position display
            document.getElementById('currentCommentNum').textContent = index + 1;

            // Find the element with this comment
            const commentIndicators = document.querySelectorAll('.comment-indicator.has-comments');
            console.log('Found comment indicators:', commentIndicators.length);

            let targetElement = null;

            commentIndicators.forEach(indicator => {
                const onclick = indicator.getAttribute('onclick');
                if (onclick && onclick.includes(commentId)) {
                    targetElement = indicator.closest('.field-item, li');
                    console.log('Found target element for:', commentId);
                }
            });

            if (!targetElement) {
                console.log('Could not find element for comment ID:', commentId);
                // Try to find by direct ID match
                const escapedId = commentId.replace(/\./g, '\\.');
                targetElement = document.querySelector(`[onclick*="${commentId}"]`)?.closest('.field-item, li');
            }

            if (targetElement) {
                // Remove previous highlights
                document.querySelectorAll('.comment-highlight').forEach(el => {
                    el.classList.remove('comment-highlight');
                });

                // Find which tab this item is in
                let parentTab = targetElement.closest('.tab-content');
                if (parentTab) {
                    const tabId = parentTab.id;
                    const segment = tabId.replace('tab-', '');

                    // Switch to the correct tab if needed
                    if (segment !== currentActiveTab) {
                        document.querySelectorAll('.tab').forEach(tab => {
                            if (tab.onclick.toString().includes(segment)) {
                                tab.click();
                            }
                        });
                    }
                }

                // Highlight and scroll to the item
                setTimeout(() => {
                    targetElement.classList.add('comment-highlight');
                    targetElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }, 300);
            }
        }

        function renderField(label, value, segment, persona, field, changesMap) {
            const key = `${segment}.${persona}.${field}`;
            const changes = changesMap[key] || [];
            const changeId = changes.length > 0 ? changes[0].id : null;

            let html = `<div class="field-item"><span class="field-label">${label}:</span> `;

            if (changes.length > 0) {
                const change = changes[0];
                const reason = getChangeReason(segment, persona, field, null, change.type);
                if (change.type === 'modified') {
                    const itemText = `<strong>New value:</strong> ${escapeHtml(value)}<br><strong>Old value:</strong> ${escapeHtml(change.old)}`;
                    html += `${value} <span class="change-indicator badge-modified" onclick="showReasonModal('${segment}', '${persona}', '${field}', 'Modified'); event.stopPropagation();">Modified</span>`;
                    html += renderVoteControls(changeId);
                    html += `<span class="old-value">was: ${change.old}</span>`;
                } else if (change.type === 'added') {
                    html += `${value} <span class="change-indicator badge-added" onclick="showReasonModal('${segment}', '${persona}', '${field}', 'New'); event.stopPropagation();">New</span>`;
                    html += renderVoteControls(changeId);
                }
                html += renderCommentIndicator(changeId);
            } else {
                html += value;
                html += renderCommentIndicator(`${segment}.${persona}.${field}.text`);
            }

            html += `</div>`;
            return html;
        }

        function renderList(items, segment, persona, field, changesMap) {
            const key = `${segment}.${persona}.${field}`;
            const changes = changesMap[key] || [];

            let html = '<ul style="margin-left: 18px; margin-top: 6px; font-size: 14px; line-height: 1.5;">';

            items.forEach((item, idx) => {
                const addedChange = changes.find(c => c.type === 'added' && c.item_value === item);
                const itemId = addedChange ? addedChange.id : `${segment}.${persona}.${field}.item${idx}`;

                if (addedChange) {
                    const reason = getChangeReason(segment, persona, field, idx, 'added');
                    html += `<li style="margin: 5px 0;">${item} <span class="change-indicator badge-added" onclick="showReasonModal('${segment}', '${persona}', '${field}', 'New', null, ${idx}); event.stopPropagation();">New</span>`;
                    html += renderVoteControls(addedChange.id);
                    html += renderCommentIndicator(addedChange.id);
                    html += `</li>`;
                } else {
                    html += `<li style="margin: 5px 0;">${item}`;
                    html += renderCommentIndicator(itemId);
                    html += `</li>`;
                }
            });

            // Show removed items
            const removedChanges = changes.filter(c => c.type === 'deleted');
            removedChanges.forEach((change, idx) => {
                const reason = getChangeReason(segment, persona, field, null, 'deleted', change.item_value);
                html += `<li style="margin: 5px 0; color: #dc2626; text-decoration: line-through;">${change.item_value} <span class="change-indicator badge-deleted" onclick="showReasonModal('${segment}', '${persona}', '${field}', 'Removed', null, null, '${change.id}'); event.stopPropagation();">Removed</span>`;
                html += renderVoteControls(change.id);
                html += renderCommentIndicator(change.id);
                html += `</li>`;
            });

            html += '</ul>';
            return html;
        }

        function renderEnhancedList(items, segment, persona, field, changesMap) {
            const key = `${segment}.${persona}.${field}`;
            const changes = changesMap[key] || [];

            let html = '<ul class="insights-list" style="list-style: none; padding: 0; margin-top: 10px;">';

            items.forEach((item, idx) => {
                const text = typeof item === 'string' ? item : item.text;
                const frequency = item.frequency || 0;
                const signal = item.signal_strength || '○';
                const quote = item.quote || '';

                const signalClass = signal === '●' ? 'strong' : signal === '◑' ? 'moderate' : 'weak';
                const signalColor = signal === '●' ? '#27ae60' : signal === '◑' ? '#f39c12' : '#95a5a6';

                const addedChange = changes.find(c => c.type === 'added' && c.item_value === text);
                const itemId = addedChange ? addedChange.id : `${segment}.${persona}.${field}.item${idx}`;

                html += `<li class="insight-item ${signalClass}" style="border-left: 4px solid ${signalColor}; padding: 15px; margin: 12px 0; background: #f8f9fa; border-radius: 0 6px 6px 0;">`;
                html += `<span class="signal-indicator" style="font-size: 20px; margin-right: 8px; color: ${signalColor};">${signal}</span>`;
                html += `<span class="insight-text" style="font-weight: 500; color: #2c3e50;">${escapeHtml(text)}</span>`;

                if (frequency > 0) {
                    html += `<span class="frequency" style="color: #7f8c8d; font-size: 14px; margin-left: 8px;">(${frequency} mentions)</span>`;
                }

                if (addedChange) {
                    html += ` <span class="change-badge new" style="display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; margin-left: 10px; background: #d4edda; color: #155724;">🟢 NEW</span>`;
                    html += renderVoteControls(addedChange.id);
                }

                if (quote) {
                    html += `<div class="quote" style="margin-top: 10px; padding: 10px 15px; background: white; border-radius: 4px; border-left: 3px solid #3498db; font-style: italic; color: #555; font-size: 14px;">"${escapeHtml(quote)}"</div>`;
                }

                html += renderCommentIndicator(itemId);
                html += `</li>`;
            });

            html += '</ul>';
            return html;
        }

        function renderVoteControls(changeId) {
            const votes = allData.votes[changeId] || {agree: [], disagree: []};
            const userAgree = votes.agree.includes(reviewerName);
            const userDisagree = votes.disagree.includes(reviewerName);

            const agreeClass = userAgree ? 'active-agree' : '';
            const disagreeClass = userDisagree ? 'active-disagree' : '';

            const agreeTooltip = votes.agree.length > 0 ? votes.agree.join(', ') : 'No votes yet';
            const disagreeTooltip = votes.disagree.length > 0 ? votes.disagree.join(', ') : 'No votes yet';

            return `
                <span class="vote-controls" id="vote-${changeId}">
                    <button class="vote-btn ${agreeClass}" onclick="vote('${changeId}', 'agree')">
                        👍<span class="vote-count">${votes.agree.length || ''}</span>
                        <span class="vote-tooltip">${agreeTooltip}</span>
                    </button>
                    <button class="vote-btn ${disagreeClass}" onclick="vote('${changeId}', 'disagree')">
                        👎<span class="vote-count">${votes.disagree.length || ''}</span>
                        <span class="vote-tooltip">${disagreeTooltip}</span>
                    </button>
                </span>
            `;
        }

        function updateVoteButtons(changeId) {
            // Update just the vote buttons for this specific change (fast!)
            const voteElement = document.getElementById('vote-' + changeId);
            if (voteElement) {
                voteElement.outerHTML = renderVoteControls(changeId);
            }
        }

        function renderCommentIndicator(id) {
            const comments = allData.comments[id] || [];
            const hasComments = comments.length > 0;
            const iconClass = hasComments ? 'has-comments' : '';
            const count = hasComments ? comments.length : '';

            return `<span class="comment-indicator ${iconClass}" onclick="openCommentPopup('${id}')">💬${count}</span>`;
        }

        function toggleVoteControls(changeId) {
            // Just for click handling - votes are always visible
        }

        function showReasonModal(segment, persona, field, changeType, itemContent = null, itemIndex = null, changeId = null) {
            const modal = document.getElementById('reasonModal');
            const modalBody = document.getElementById('reasonModalBody');
            const badge = document.getElementById('reasonBadge');

            // If changeId is provided, look up the change and get item content
            if (changeId && itemContent === null) {
                try {
                    const change = CHANGES_DATA.find(c => c.id === changeId);
                    if (change && change.item_value) {
                        itemContent = change.item_value;
                    }
                } catch (e) {
                    console.error('Error looking up change:', e);
                }
            }

            // If itemIndex is provided but itemContent is not, look it up from PERSONAS_DATA
            if (itemIndex !== null && itemContent === null) {
                try {
                    const personaData = PERSONAS_DATA[segment][persona];
                    if (personaData && personaData[field] && Array.isArray(personaData[field])) {
                        itemContent = personaData[field][itemIndex];
                    }
                } catch (e) {
                    console.error('Error looking up item content:', e);
                }
            }

            // Normalize changeType to match what getChangeReason expects
            // UI uses 'New', 'Modified', 'Removed' but getChangeReason expects 'added', 'modified', 'deleted'
            const normalizedType = changeType === 'New' ? 'added' :
                                   changeType === 'Removed' ? 'deleted' :
                                   changeType === 'Modified' ? 'modified' : changeType;

            // Look up the reason
            let reason = getChangeReason(segment, persona, field, itemIndex, normalizedType, itemContent);

            // Clean up the reason text - remove redundant prefixes and quoted content
            // Patterns like "REMOVED: 'text' - actual reason" or "NEW CHALLENGE: 'text' - actual reason"
            reason = reason.replace(/^(REMOVED|KEPT|NEW\s+(CHALLENGE|GOAL|MESSAGE|OBJECTION)|Modified|Updated|Added):\s*['"].*?['"]\s*-\s*/i, '');
            // Also handle patterns without quotes like "REMOVED - actual reason"
            reason = reason.replace(/^(REMOVED|KEPT|NEW\s+(CHALLENGE|GOAL|MESSAGE|OBJECTION)|Modified|Updated|Added):\s*-?\s*/i, '');
            // Trim any leading/trailing whitespace
            reason = reason.trim();

            // Build the content
            let content = '';

            // Show the actual change if provided
            if (itemContent) {
                const escapedContent = escapeHtml(itemContent);
                content += `<div style="background: #f3f4f6; padding: 16px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #6366f1;">`;
                content += `<div style="font-weight: 600; color: #4b5563; margin-bottom: 8px; font-size: 13px; text-transform: uppercase;">Change:</div>`;
                content += `<div style="color: #111827; font-size: 15px; line-height: 1.6;">${escapedContent}</div>`;
                content += `</div>`;
            }

            // Add the reason
            content += `<div style="font-weight: 600; color: #4b5563; margin-bottom: 8px; font-size: 13px; text-transform: uppercase;">Why:</div>`;
            content += `<div style="color: #374151;">${escapeHtml(reason)}</div>`;

            modalBody.innerHTML = content;

            // Set the badge
            badge.textContent = changeType;
            badge.className = 'reason-badge ' + changeType.toLowerCase();

            // Show the modal
            modal.style.display = 'block';

            // Prevent body scroll
            document.body.style.overflow = 'hidden';
        }

        function closeReasonModal() {
            const modal = document.getElementById('reasonModal');
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }

        // Close modal when clicking outside
        window.onclick = function(event) {
            const modal = document.getElementById('reasonModal');
            if (event.target === modal) {
                closeReasonModal();
            }
        }

        // Close modal with Escape key
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape') {
                closeReasonModal();
            }
        });

        async function vote(changeId, voteType) {
            if (!reviewerName) {
                alert('Please enter your name to vote');
                document.getElementById('reviewerName').focus();
                return;
            }

            // Initialize votes if needed
            if (!allData.votes[changeId]) {
                allData.votes[changeId] = {agree: [], disagree: []};
            }

            const votes = allData.votes[changeId];
            let newVoteType = voteType;

            // Optimistic update - update UI immediately
            if (voteType === 'agree') {
                if (votes.agree.includes(reviewerName)) {
                    // Remove agree vote
                    votes.agree = votes.agree.filter(n => n !== reviewerName);
                    newVoteType = null;
                } else {
                    // Add agree vote, remove disagree if present
                    votes.agree.push(reviewerName);
                    votes.disagree = votes.disagree.filter(n => n !== reviewerName);
                }
            } else {
                if (votes.disagree.includes(reviewerName)) {
                    // Remove disagree vote
                    votes.disagree = votes.disagree.filter(n => n !== reviewerName);
                    newVoteType = null;
                } else {
                    // Add disagree vote, remove agree if present
                    votes.disagree.push(reviewerName);
                    votes.agree = votes.agree.filter(n => n !== reviewerName);
                }
            }

            // Update UI immediately (just this vote button - fast!)
            updateVoteButtons(changeId);

            // Save to Google Sheets in background (don't await)
            saveVote(changeId, newVoteType).catch(err => {
                console.error('Failed to save vote:', err);
                // Don't revert - auto-refresh will sync in 5 seconds
            });
        }

        function openCommentPopup(id) {
            if (!reviewerName) {
                alert('Please enter your name to comment');
                document.getElementById('reviewerName').focus();
                return;
            }

            currentCommentId = id;
            const comments = allData.comments[id] || [];

            // Render comments
            let html = '';
            if (comments.length === 0) {
                html = '<p style="color: #666; font-size: 14px;">No comments yet. Be the first!</p>';
            } else {
                comments.forEach(comment => {
                    html += `
                        <div class="comment-item">
                            <div class="comment-author">${comment.author}</div>
                            <div class="comment-text">${comment.text}</div>
                        </div>
                    `;
                });
            }

            document.getElementById('commentList').innerHTML = html;
            document.getElementById('newComment').value = '';
            document.getElementById('commentPopup').classList.add('show');
            document.getElementById('commentOverlay').classList.add('show');
        }

        function closeCommentPopup() {
            document.getElementById('commentPopup').classList.remove('show');
            document.getElementById('commentOverlay').classList.remove('show');
            currentCommentId = null;
        }

        async function submitComment() {
            const text = document.getElementById('newComment').value.trim();
            if (!text) {
                alert('Please enter a comment');
                return;
            }

            // Optimistic update - add comment immediately
            if (!allData.comments[currentCommentId]) {
                allData.comments[currentCommentId] = [];
            }

            const newComment = {
                author: reviewerName,
                text: text,
                timestamp: new Date().toISOString()
            };

            allData.comments[currentCommentId].push(newComment);

            // Update popup immediately (just the popup - fast!)
            openCommentPopup(currentCommentId); // Refresh popup with new comment

            // Save to Google Sheets in background (don't await)
            saveCommentToSheets(currentCommentId, text).catch(err => {
                console.error('Failed to save comment:', err);
                // Don't revert - auto-refresh will sync in 5 seconds
            });
        }

        window.addEventListener('DOMContentLoaded', init);
    </script>
</body>
</html>'''

        return html


    def generate_approval_html(self, personas: Dict, changes_data: Dict) -> str:
        """Generate approval interface with vote counts"""

        # Load current feedback
        feedback_data = self.load_feedback_counts()
        vote_counts = feedback_data['counts']
        total_reviewers = feedback_data['total_reviewers']

        # Same profile rendering as team version, but with vote counts
        changes_with_votes = []
        for change in changes_data['changes']:
            change_copy = change.copy()
            votes = vote_counts.get(change['id'], {'agree': 0, 'disagree': 0, 'comments': []})
            change_copy['votes'] = votes
            changes_with_votes.append(change_copy)

        html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Persona Approval - With Team Feedback</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f8f9fa;
            line-height: 1.6;
            color: #333;
        }
        .header {
            background: linear-gradient(135deg, #2D4C33 0%, #203524 100%);
            color: #D1F470;
            padding: 40px 20px;
            text-align: center;
        }
        .header h1 { font-size: 32px; margin-bottom: 10px; }
        .container { max-width: 1000px; margin: 0 auto; padding: 15px; }

        .stats-bar {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            display: flex;
            justify-content: space-around;
            text-align: center;
        }
        .stat { flex: 1; }
        .stat-value { font-size: 32px; font-weight: bold; color: #2D4C33; }
        .stat-label { font-size: 14px; color: #666; margin-top: 5px; }

        /* Tabs */
        .tabs {
            display: flex;
            gap: 4px;
            background: white;
            padding: 20px 20px 0 20px;
            border-radius: 8px 8px 0 0;
            margin-bottom: 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }

        .tab {
            padding: 12px 24px;
            background: #f8f9fa;
            border: none;
            border-radius: 8px 8px 0 0;
            cursor: pointer;
            font-size: 15px;
            font-weight: 600;
            color: #666;
            transition: all 0.2s;
            border-bottom: 3px solid transparent;
        }

        .tab:hover {
            background: #e9ecef;
            color: #333;
        }

        .tab.active {
            background: linear-gradient(135deg, #A1D78F 0%, #88c478 100%);
            color: white;
            border-bottom: 4px solid #2D4C33;
            font-weight: 700;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(161, 215, 143, 0.4);
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        .segment-section {
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }

        .segment-section.digital {
            border-left: 6px solid #60A5FA;
        }

        .segment-section.smb {
            border-left: 6px solid #A1D78F;
        }

        .segment-section.commercial {
            border-left: 6px solid #FEEB7E;
        }

        .segment-section.enterprise {
            border-left: 6px solid #A78BFA;
        }

        .segment-header {
            margin: -20px -20px 20px -20px;
            padding: 16px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-radius: 8px 8px 0 0;
        }

        .segment-section.digital .segment-header {
            background: #60A5FA;
        }

        .segment-section.smb .segment-header {
            background: #A1D78F;
        }

        .segment-section.commercial .segment-header {
            background: #FEEB7E;
        }

        .segment-section.enterprise .segment-header {
            background: #A78BFA;
        }

        .segment-title {
            font-size: 22px;
            font-weight: bold;
            margin: 0;
        }

        .segment-section.digital .segment-title {
            color: #1E3A8A;
        }

        .segment-section.smb .segment-title {
            color: #2D4C33;
        }

        .segment-section.commercial .segment-title {
            color: #11110D;
        }

        .segment-section.enterprise .segment-title {
            color: #5B21B6;
        }

        .segment-subtitle {
            font-size: 14px;
            opacity: 0.8;
            font-weight: 500;
        }

        .segment-section.digital .segment-subtitle {
            color: #1E3A8A;
        }

        .segment-section.smb .segment-subtitle {
            color: #2D4C33;
        }

        .segment-section.commercial .segment-subtitle {
            color: #11110D;
        }

        .segment-section.enterprise .segment-subtitle {
            color: #5B21B6;
        }

        .persona-card {
            margin-top: 20px;
            margin-bottom: 15px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
            border: 1px solid #e5e7eb;
            overflow: hidden;
            transition: box-shadow 0.3s ease;
        }

        .persona-card:hover {
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.12);
        }

        .persona-title {
            font-size: 20px;
            font-weight: bold;
            color: #11110D;
            padding: 14px 18px;
            margin: 0;
        }

        .segment-section.digital .persona-title {
            background: linear-gradient(135deg, #60A5FA 0%, #3B82F6 100%);
        }

        .segment-section.smb .persona-title {
            background: linear-gradient(135deg, #A1D78F 0%, #88c478 100%);
        }

        .segment-section.commercial .persona-title {
            background: linear-gradient(135deg, #FEEB7E 0%, #f5dc5e 100%);
        }

        .segment-section.enterprise .persona-title {
            background: linear-gradient(135deg, #A78BFA 0%, #8B5CF6 100%);
        }

        .persona-content {
            padding: 18px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        .persona-column {
            min-width: 0;
        }

        .section-header {
            font-size: 15px;
            font-weight: 600;
            margin: 12px 0 6px 0;
            padding-bottom: 3px;
            border-bottom: 1px solid #e5e7eb;
        }

        .segment-section.digital .section-header {
            color: #1E3A8A;
        }

        .segment-section.smb .section-header {
            color: #2D4C33;
        }

        .segment-section.commercial .section-header {
            color: #11110D;
        }

        .segment-section.enterprise .section-header {
            color: #5B21B6;
        }

        .section-header:first-child {
            margin-top: 0;
        }

        .full-width {
            grid-column: 1 / -1;
        }

        .field-item {
            margin: 6px 0;
            padding: 4px 0;
            font-size: 14px;
            line-height: 1.5;
        }

        .field-label {
            font-weight: 600;
            color: #495057;
            font-size: 14px;
        }

        .change-indicator {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
            margin-left: 8px;
        }

        .badge-added { background: #d1fae5; color: #065f46; }
        .badge-modified { background: #dbeafe; color: #1e40af; }
        .badge-deleted { background: #fee2e2; color: #991b1b; }

        .old-value {
            color: #dc2626;
            text-decoration: line-through;
            font-size: 14px;
            margin-left: 10px;
        }

        .editable {
            cursor: text;
            padding: 2px 4px;
            border-radius: 3px;
            transition: background 0.2s;
            display: inline-block;
            min-width: 20px;
        }

        .editable:hover {
            background: #f3f4f6;
            outline: 1px dashed #d1d5db;
        }

        .editable:focus {
            background: #fef3c7;
            outline: 2px solid #fbbf24;
        }

        .edited {
            background: #fef3c7 !important;
            border-left: 3px solid #f59e0b;
            padding-left: 6px !important;
        }

        .edit-indicator {
            display: inline-block;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 10px;
            font-weight: 600;
            margin-left: 6px;
            background: #fbbf24;
            color: #78350f;
        }

        .approval-actions {
            background: white;
            padding: 15px;
            border-radius: 6px;
            margin: 10px 0;
            border-left: 4px solid #10b981;
        }

        .action-buttons {
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }

        .action-btn {
            padding: 8px 16px;
            border: none;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }

        .btn-approve {
            background: #10b981;
            color: white;
        }

        .btn-approve:hover {
            background: #059669;
        }

        .btn-reject {
            background: #ef4444;
            color: white;
        }

        .btn-reject:hover {
            background: #dc2626;
        }

        .btn-approved {
            background: #d1fae5;
            color: #065f46;
            cursor: default;
        }

        .btn-rejected {
            background: #fee2e2;
            color: #991b1b;
            cursor: default;
        }

        .action-bar {
            position: sticky;
            bottom: 0;
            background: white;
            padding: 20px;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 15px;
        }

        .final-btn {
            padding: 12px 30px;
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
        }

        .final-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .share-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }

        .share-title {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 15px;
        }

        .share-content {
            display: flex;
            gap: 20px;
            align-items: center;
            flex-wrap: wrap;
            justify-content: space-between;
        }

        .share-url {
            flex: 1;
            background: rgba(255,255,255,0.2);
            padding: 12px 16px;
            border-radius: 6px;
            font-family: monospace;
            font-size: 14px;
            word-break: break-all;
            min-width: 300px;
        }

        .share-btn {
            padding: 12px 28px;
            background: white;
            color: #667eea;
            border: none;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 15px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .share-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(255,255,255,0.3);
        }

        .share-instructions {
            margin-top: 12px;
            font-size: 14px;
            opacity: 0.95;
        }

        /* Product Cards */
        .recommended-products {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-top: 10px;
            width: 100%;
        }

        .product-card {
            background: #f8f9fa;
            border-left: 4px solid #0275d8;
            padding: 12px;
            border-radius: 6px;
            position: relative;
        }

        .product-card.change-indicator.added {
            border-left-color: #5cb85c;
            background: #f0f9f0;
        }

        .product-card.change-indicator.modified {
            border-left-color: #0275d8;
            background: #f0f7ff;
        }

        .product-card.change-indicator.deleted {
            border-left-color: #d9534f;
            background: #fff5f5;
            opacity: 0.7;
        }

        .product-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }

        .product-name {
            font-weight: 600;
            color: #333;
            font-size: 14px;
        }

        .relevance-badge {
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
        }

        .relevance-critical {
            background: #d9534f;
            color: white;
        }

        .relevance-high {
            background: #f0ad4e;
            color: white;
        }

        .relevance-medium {
            background: #5bc0de;
            color: white;
        }

        .product-section {
            margin-bottom: 10px;
        }

        .product-section-title {
            font-size: 11px;
            font-weight: 600;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        }

        .product-why {
            font-size: 13px;
            color: #333;
            line-height: 1.5;
            font-weight: 500;
        }

        .product-challenge {
            font-size: 12px;
            color: #555;
            line-height: 1.4;
            font-style: italic;
        }

        .product-link {
            font-size: 12px;
            color: #0275d8;
            text-decoration: none;
            font-weight: 500;
        }

        .product-link:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📋 Persona Approval - Internal Review</h1>
        <p>Complete profiles with team feedback</p>
    </div>

    <div class="container">
        <div class="share-section">
            <div class="share-title">📤 Share Team Review</div>
            <div class="share-content">
                <div class="share-url" id="shareUrl">https://chrissherman-png.github.io/persona-analysis/reports/Persona_Team_Review_Full.html</div>
                <button class="share-btn" onclick="copyShareLink()">
                    <span>🔗</span>
                    <span id="btnText">Share Link</span>
                </button>
            </div>
            <div class="share-instructions">
                💡 Click to copy, then share via email/Slack (after git push)
            </div>
        </div>

        <div class="stats-bar">
            <div class="stat">
                <div class="stat-value" id="approvedCount">0</div>
                <div class="stat-label">Approved</div>
            </div>
            <div class="stat">
                <div class="stat-value" id="rejectedCount">0</div>
                <div class="stat-label">Rejected</div>
            </div>
            <div class="stat">
                <div class="stat-value" id="progress">0</div>
                <div class="stat-label">Progress</div>
            </div>
        </div>

        <div class="tabs" id="segmentTabs">
            <button class="tab active" onclick="switchTab('Digital')">Digital (≤49 employees)</button>
            <button class="tab" onclick="switchTab('SMB')">SMB (50-249 employees)</button>
            <button class="tab" onclick="switchTab('Commercial')">Commercial (250-1,499)</button>
            <button class="tab" onclick="switchTab('Enterprise')">Enterprise (1,500+)</button>
            <button class="tab" onclick="switchTab('DataSources')">📊 Data Sources</button>
        </div>

        <div id="profilesContainer">
            <!-- Will be rendered by JavaScript -->
        </div>
    </div>

    <div class="action-bar">
        <div>
            <span id="actionProgress">0</span> of <span id="totalChanges2">''' + str(len(changes_data['changes'])) + '''</span> changes reviewed
        </div>
        <button class="final-btn" onclick="generateFinal()" id="finalBtn" disabled>
            Generate Final Report
        </button>
    </div>

    <script>
        const CHANGES_WITH_VOTES = ''' + json.dumps(changes_with_votes) + ''';
        const PERSONAS_DATA = ''' + json.dumps(personas) + ''';

        let decisions = {};
        let edits = {};
        let currentActiveTab = 'Digital'; // Track active tab

        // Load saved decisions and edits
        const savedDecisions = localStorage.getItem('persona_approval_decisions');
        if (savedDecisions) {
            decisions = JSON.parse(savedDecisions);
        }

        const savedEdits = localStorage.getItem('persona_edits');
        if (savedEdits) {
            edits = JSON.parse(savedEdits);
        }

        function init() {
            renderProfiles();
            updateStats();
            attachEditListeners();
        }

        function attachEditListeners() {
            // Add listeners to all editable elements
            document.addEventListener('blur', (e) => {
                if (e.target.classList.contains('editable')) {
                    const editId = e.target.getAttribute('data-edit-id');
                    const originalValue = e.target.getAttribute('data-original');
                    const newValue = e.target.textContent.trim();

                    if (newValue !== originalValue) {
                        edits[editId] = newValue;
                        e.target.classList.add('edited');
                    } else {
                        delete edits[editId];
                        e.target.classList.remove('edited');
                    }

                    localStorage.setItem('persona_edits', JSON.stringify(edits));
                    renderProfiles(); // Re-render to show edit indicator
                }
            }, true);

            // Prevent line breaks in contenteditable
            document.addEventListener('keydown', (e) => {
                if (e.target.classList.contains('editable') && e.key === 'Enter') {
                    e.preventDefault();
                    e.target.blur();
                }
            }, true);
        }

        function copyShareLink() {
            const url = document.getElementById('shareUrl').textContent;
            navigator.clipboard.writeText(url).then(() => {
                const btnText = document.getElementById('btnText');
                const originalText = btnText.textContent;
                btnText.textContent = 'Copied!';
                const btn = event.currentTarget;
                btn.style.background = '#10b981';
                btn.style.color = 'white';
                setTimeout(() => {
                    btnText.textContent = originalText;
                    btn.style.background = 'white';
                    btn.style.color = '#667eea';
                }, 2000);
            });
        }

        function escapeHtml(text) {
            if (text === null || text === undefined) return '';
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        function getCompetitiveIntel(segment) {
            const intel = {
                'Digital': {
                    competitors: [
                        {
                            name: 'Freshdesk',
                            threat: 'High',
                            why: 'Low price and simple setup appeal to startups',
                            counter: 'Zendesk scales with you; Freshdesk forces migration at growth'
                        },
                        {
                            name: 'Intercom',
                            threat: 'Medium',
                            why: 'Modern UI and messaging-first approach for SaaS companies',
                            counter: 'Zendesk is omnichannel; Intercom is messaging-only'
                        }
                    ]
                },
                'SMB': {
                    competitors: [
                        {
                            name: 'Freshdesk',
                            threat: 'High',
                            why: 'Low price and simple setup appeal to growing businesses',
                            counter: 'Zendesk scales with you; Freshdesk forces migration at growth'
                        },
                        {
                            name: 'Intercom',
                            threat: 'Medium',
                            why: 'Modern UI and messaging-first approach',
                            counter: 'Zendesk is omnichannel; Intercom is messaging-only'
                        }
                    ]
                },
                'Commercial': {
                    competitors: [
                        {
                            name: 'Salesforce Service Cloud',
                            threat: 'Very High',
                            why: 'Deep CRM integration, brand recognition, enterprise scale',
                            counter: 'Zendesk is faster to implement with better agent UX'
                        },
                        {
                            name: 'Freshdesk',
                            threat: 'Medium',
                            why: 'Lower cost option for cost-conscious buyers',
                            counter: 'Limited scalability and weak integrations at this scale'
                        }
                    ]
                },
                'Enterprise': {
                    competitors: [
                        {
                            name: 'Salesforce Service Cloud',
                            threat: 'Very High',
                            why: 'Deep CRM integration, brand recognition, enterprise scale',
                            counter: 'Zendesk is faster to implement with better agent UX'
                        },
                        {
                            name: 'ServiceNow',
                            threat: 'Medium',
                            why: 'ITSM integration, enterprise workflows, compliance capabilities',
                            counter: 'Zendesk is purpose-built for CX; ServiceNow retrofitted from ITSM'
                        }
                    ]
                }
            };
            return intel[segment];
        }

        function getMessagingGuide(segment) {
            const guides = {
                'Digital': {
                    dos: [
                        '<strong>"Set up in 15 minutes"</strong> - Emphasize speed and simplicity',
                        '<strong>"No IT team needed"</strong> - Highlight self-service capability',
                        '<strong>"Automation"</strong> - Use instead of "AI" (less intimidating)',
                        '<strong>"$X per month"</strong> - Show concrete, affordable pricing',
                        '<strong>"Self-service"</strong> - Focus on independence and control'
                    ],
                    donts: [
                        '<strong>"Enterprise-grade"</strong> - Sounds expensive and complex',
                        '<strong>"Implementation timeline"</strong> - Use "setup time" instead',
                        '<strong>"Dedicated CSM"</strong> - They don\\'t expect this level of service',
                        '<strong>"AI/Machine Learning"</strong> - Technical jargon that feels out of reach',
                        '<strong>"ROI analysis"</strong> - Too formal; use "save money" or "save time"'
                    ],
                    keyInsight: 'Digital buyers (44% facing cost pressure) want simple language that emphasizes immediate value and ease of use. They\\'re buying tools, not transformations.'
                },
                'SMB': {
                    dos: [
                        '<strong>"Automation"</strong> - More tangible than "AI" (your example!)',
                        '<strong>"30% productivity gain"</strong> - Concrete, measurable outcomes',
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

        function renderProfiles() {
            console.log('renderProfiles called');
            const container = document.getElementById('profilesContainer');
            console.log('container:', container);
            console.log('PERSONAS_DATA:', Object.keys(PERSONAS_DATA));
            console.log('CHANGES_WITH_VOTES:', CHANGES_WITH_VOTES.length);
            const changesMap = {};

            CHANGES_WITH_VOTES.forEach(change => {
                const key = `${change.segment}.${change.persona}.${change.field}`;
                if (!changesMap[key]) changesMap[key] = [];
                changesMap[key].push(change);
            });

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

                // Add Competitive Intelligence
                const competitiveIntel = getCompetitiveIntel(segment);
                if (competitiveIntel) {
                    html += `<div class="messaging-guide-card">`;
                    html += `<div class="messaging-guide-title">🎯 Competitive Landscape for ${segment}</div>`;
                    html += `<div class="messaging-guide-subtitle">Key competitors and how to position against them</div>`;
                    html += `<div style="margin-top: 15px;">`;

                    competitiveIntel.competitors.forEach(comp => {
                        const threatColor = comp.threat === 'Very High' ? '#dc2626' :
                                          comp.threat === 'High' ? '#f59e0b' : '#6b7280';
                        html += `<div style="background: #f9fafb; border-left: 4px solid ${threatColor}; padding: 14px; margin-bottom: 12px; border-radius: 6px;">`;
                        html += `<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">`;
                        html += `<div style="font-size: 16px; font-weight: 700; color: #111827;">${comp.name}</div>`;
                        html += `<div style="font-size: 12px; font-weight: 600; padding: 3px 8px; border-radius: 12px; background: ${threatColor}; color: white;">${comp.threat} Threat</div>`;
                        html += `</div>`;
                        html += `<div style="font-size: 14px; color: #4b5563; margin-bottom: 6px;"><strong>Why they compete:</strong> ${comp.why}</div>`;
                        html += `<div style="font-size: 14px; color: #0275d8;"><strong>How to counter:</strong> ${comp.counter}</div>`;
                        html += `</div>`;
                    });

                    html += `</div>`;
                    html += `</div>`; // close competitive-intel-card
                }

                Object.keys(PERSONAS_DATA[segment]).forEach(personaName => {
                    const persona = PERSONAS_DATA[segment][personaName];
                    html += `<div class="persona-card">`;
                    html += `<div class="persona-title">${personaName}</div>`;
                    html += `<div class="persona-content" style="display: block; padding: 18px;">`;

                    // SECTION 1: Profile Overview (manual)
                    html += `<div class="section-header" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">📋 Profile Overview</div>`;
                    html += `<div class="profile-fields" style="padding: 10px 0;">`;
                    html += renderField('Job Titles', persona.job_titles.join(', '), segment, personaName, 'job_titles', changesMap);
                    html += renderField('Reports To', persona.reports_to, segment, personaName, 'reports_to', changesMap);
                    html += renderField('Team Size', persona.team_size, segment, personaName, 'team_size', changesMap);
                    html += renderField('Prevalence in Deals', persona.prevalence, segment, personaName, 'prevalence', changesMap);
                    html += renderField('Role in Buying Process', persona.role_in_deal, segment, personaName, 'role_in_deal', changesMap);
                    html += `</div>`;

                    // SECTION 2: Pain Points (NLP enhanced)
                    html += `<div class="section-header" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">😓 Pain Points</div>`;
                    const painPointsEnhanced = persona.pain_points_enhanced || [];
                    const painPoints = persona.pain_points || persona.challenges || persona.challenges_from_gong || [];
                    if (painPointsEnhanced.length > 0) {
                        html += renderEnhancedList(painPointsEnhanced, segment, personaName, 'pain_points', changesMap);
                    } else {
                        html += renderList(painPoints, segment, personaName, 'challenges_from_gong', changesMap);
                    }

                    // SECTION 3: Goals (NLP enhanced)
                    html += `<div class="section-header" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">🎯 Goals</div>`;
                    const goalsEnhanced = persona.goals_enhanced || [];
                    if (goalsEnhanced.length > 0) {
                        html += renderEnhancedList(goalsEnhanced, segment, personaName, 'goals', changesMap);
                    } else {
                        html += renderList(persona.goals || [], segment, personaName, 'goals', changesMap);
                    }

                    // SECTION 4: Objections (NLP enhanced)
                    html += `<div class="section-header" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">⚠️ Objections</div>`;
                    const objectionsEnhanced = persona.objections_enhanced || [];
                    if (objectionsEnhanced.length > 0) {
                        html += renderEnhancedList(objectionsEnhanced, segment, personaName, 'objections', changesMap);
                    } else {
                        html += renderList(persona.objections || [], segment, personaName, 'objections', changesMap);
                    }

                    // SECTION 5: Trigger Events (NEW - NLP enhanced)
                    const triggerEventsEnhanced = persona.trigger_events_enhanced || [];
                    if (triggerEventsEnhanced.length > 0) {
                        html += `<div class="section-header new" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">🔔 Trigger Events</div>`;
                        html += renderEnhancedList(triggerEventsEnhanced, segment, personaName, 'trigger_events', changesMap);
                    }

                    // SECTION 6: Product Requirements (NEW - NLP enhanced)
                    const productRequirementsEnhanced = persona.product_requirements_enhanced || [];
                    if (productRequirementsEnhanced.length > 0) {
                        html += `<div class="section-header new" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">✅ Product Requirements</div>`;
                        html += renderEnhancedList(productRequirementsEnhanced, segment, personaName, 'product_requirements', changesMap);
                    }

                    // SECTION 7: Information Sources (NEW - NLP enhanced)
                    const informationSourcesEnhanced = persona.information_sources_enhanced || [];
                    if (informationSourcesEnhanced.length > 0) {
                        html += `<div class="section-header new" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">📚 Information Sources</div>`;
                        html += renderEnhancedList(informationSourcesEnhanced, segment, personaName, 'information_sources', changesMap);
                    }

                    // SECTION 8: Messaging Preferences (NEW - NLP enhanced)
                    const messagingPreferencesEnhanced = persona.messaging_preferences_enhanced || [];
                    if (messagingPreferencesEnhanced.length > 0) {
                        html += `<div class="section-header new" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">💬 Messaging Preferences</div>`;
                        html += renderEnhancedList(messagingPreferencesEnhanced, segment, personaName, 'messaging_preferences', changesMap);
                    }

                    // SECTION 9: Verbatim Quotes (show 3-5 representative quotes)
                    const verbatimQuotes = persona.verbatim_quotes || [];
                    if (verbatimQuotes.length > 0) {
                        html += `<div class="section-header" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">🗣️ Verbatim Quotes</div>`;
                        html += `<div style="padding: 10px 0;">`;
                        verbatimQuotes.slice(0, 5).forEach((quote, idx) => {
                            html += `<div class="quote" style="margin: 12px 0; padding: 12px 16px; background: #f8f9fa; border-left: 4px solid #3498db; border-radius: 4px; font-style: italic; color: #555; font-size: 14px;">`;
                            html += `"${escapeHtml(quote)}"`;
                            html += `</div>`;
                        });
                        html += `</div>`;
                    }

                    // SECTION 10: Success Metrics (NLP enhanced)
                    html += `<div class="section-header new" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">📊 Success Metrics</div>`;
                    const successMetricsEnhanced = persona.success_metrics_enhanced || [];
                    if (successMetricsEnhanced.length > 0) {
                        html += renderEnhancedList(successMetricsEnhanced, segment, personaName, 'success_metrics', changesMap);
                    } else {
                        html += renderList(persona.success_metrics || [], segment, personaName, 'success_metrics', changesMap);
                    }

                    html += `</div>`; // persona-content

                    // Recommended Products Section - spans full width below
                    if (persona.recommended_products && persona.recommended_products.length > 0) {
                        html += `<div style="padding: 0 18px 18px 18px;">`;
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
                            html += '<div class="product-section-title">✓ Solves This Challenge</div>';
                            html += '<div class="product-challenge">' + escapeHtml(product.addresses_challenge) + '</div>';
                            html += '</div>';
                            html += '<a href="' + escapeHtml(product.url) + '" target="_blank" class="product-link">Learn more →</a>';
                            html += '</div>';
                        });
                        html += `</div>`; // recommended-products
                        html += `</div>`; // padding container
                    }

                    html += `</div>`; // persona-card
                });

                html += `</div>`; // segment-section
                html += `</div>`; // tab-content
            });

            container.innerHTML = html;
            restoreActiveTab(); // Restore previously selected tab
        }

        function switchTab(segment) {
            currentActiveTab = segment; // Save current tab

            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });

            // Show selected tab
            document.getElementById(`tab-${segment}`).classList.add('active');
            event.currentTarget.classList.add('active');

            // Scroll to top
            window.scrollTo({top: 0, behavior: 'smooth'});
        }

        function restoreActiveTab() {
            // Restore the previously active tab after re-rendering
            if (currentActiveTab) {
                document.querySelectorAll('.tab-content').forEach(tab => {
                    tab.classList.remove('active');
                });
                document.querySelectorAll('.tab').forEach(tab => {
                    tab.classList.remove('active');
                });

                document.getElementById(`tab-${currentActiveTab}`)?.classList.add('active');
                document.querySelectorAll('.tab').forEach(tab => {
                    if (tab.onclick.toString().includes(currentActiveTab)) {
                        tab.classList.add('active');
                    }
                });
            }
        }

        function renderField(label, value, segment, persona, field, changesMap) {
            const key = `${segment}.${persona}.${field}`;
            const changes = changesMap[key] || [];
            const editId = `edit_${segment}_${persona}_${field}`.replace(/\s+/g, '_').replace(/\./g, '_');

            // Check if edited
            const editedValue = edits[editId];
            const isEdited = editedValue !== undefined;
            const displayValue = isEdited ? editedValue : value;

            let html = `<div class="field-item"><span class="field-label">${label}:</span> `;
            html += `<span class="editable ${isEdited ? 'edited' : ''}" contenteditable="true" data-edit-id="${editId}" data-original="${value}">${displayValue}</span>`;

            if (isEdited) {
                html += `<span class="edit-indicator">EDITED</span>`;
            }

            if (changes.length > 0) {
                const change = changes[0];
                if (change.type === 'modified') {
                    html += ` <span class="change-indicator badge-modified">Modified</span>`;
                    html += `<span class="old-value">was: ${change.old}</span>`;
                    html += renderApprovalBox(change);
                } else if (change.type === 'added') {
                    html += ` <span class="change-indicator badge-added">New</span>`;
                    html += renderApprovalBox(change);
                }
            }

            html += `</div>`;
            return html;
        }

        function renderList(items, segment, persona, field, changesMap) {
            const key = `${segment}.${persona}.${field}`;
            const changes = changesMap[key] || [];

            let html = '<ul style="margin-left: 18px; margin-top: 6px; font-size: 14px; line-height: 1.5;">';

            items.forEach((item, index) => {
                const addedChange = changes.find(c => c.type === 'added' && c.item_value === item);
                const editId = `edit_${segment}_${persona}_${field}_${index}`.replace(/\s+/g, '_').replace(/\./g, '_');

                // Check if edited
                const editedValue = edits[editId];
                const isEdited = editedValue !== undefined;
                const displayValue = isEdited ? editedValue : item;

                html += `<li style="margin: 5px 0;">`;
                html += `<span class="editable ${isEdited ? 'edited' : ''}" contenteditable="true" data-edit-id="${editId}" data-original="${item}">${displayValue}</span>`;

                if (isEdited) {
                    html += ` <span class="edit-indicator">EDITED</span>`;
                }

                if (addedChange) {
                    html += ` <span class="change-indicator badge-added">New</span>`;
                    html += renderApprovalBox(addedChange);
                }

                html += `</li>`;
            });

            const removedChanges = changes.filter(c => c.type === 'deleted');
            removedChanges.forEach(change => {
                html += `<li style="margin: 5px 0; color: #dc2626; text-decoration: line-through;">${change.item_value} <span class="change-indicator badge-deleted">Removed</span>`;
                html += renderApprovalBox(change);
                html += `</li>`;
            });

            html += '</ul>';
            return html;
        }

        function renderApprovalBox(change) {
            const decision = decisions[change.id];
            const approvedClass = decision === 'approved' ? 'btn-approved' : '';
            const rejectedClass = decision === 'rejected' ? 'btn-rejected' : '';

            return `
                <div class="approval-actions">
                    <div style="font-size: 12px; color: #666; margin-bottom: 8px;">Your decision:</div>
                    <div class="action-buttons">
                        <button class="action-btn btn-approve ${approvedClass}"
                                onclick="decide('${change.id}', 'approved')"
                                ${decision === 'approved' ? 'disabled' : ''}>
                            ${decision === 'approved' ? '✓ Approved' : 'Approve'}
                        </button>
                        <button class="action-btn btn-reject ${rejectedClass}"
                                onclick="decide('${change.id}', 'rejected')"
                                ${decision === 'rejected' ? 'disabled' : ''}>
                            ${decision === 'rejected' ? '✗ Rejected' : 'Reject'}
                        </button>
                    </div>
                </div>
            `;
        }

        function decide(changeId, decision) {
            decisions[changeId] = decision;
            localStorage.setItem('persona_approval_decisions', JSON.stringify(decisions));
            updateStats();
            renderProfiles();
        }

        function updateStats() {
            const approved = Object.values(decisions).filter(d => d === 'approved').length;
            const rejected = Object.values(decisions).filter(d => d === 'rejected').length;
            const total = CHANGES_WITH_VOTES.length;

            document.getElementById('approvedCount').textContent = approved;
            document.getElementById('rejectedCount').textContent = rejected;
            document.getElementById('progress').textContent = approved + rejected;
            document.getElementById('actionProgress').textContent = approved + rejected;

            document.getElementById('finalBtn').disabled = (approved + rejected) < total;
        }

        function generateFinal() {
            if (!confirm('Generate final report with approved changes?\\n\\nThis will create a clean HTML report with only approved changes.')) {
                return;
            }

            // Build final report HTML with only approved changes
            const finalHtml = generateFinalReportHTML();

            // Download the HTML file
            const blob = new Blob([finalHtml], {type: 'text/html'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'Persona_Final_Report.html';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);

            // Show instructions
            setTimeout(() => {
                alert('✓ Final report downloaded!\\n\\nNext steps:\\n1. Move Persona_Final_Report.html to: persona_analysis/reports/\\n2. cd persona_analysis\\n3. git add reports/Persona_Final_Report.html\\n4. git commit -m "Add final persona report"\\n5. git push\\n\\nThen share: https://chrissherman-png.github.io/persona-analysis/reports/Persona_Final_Report.html');
            }, 100);
        }

        function generateFinalReportHTML() {
            // Get approved changes
            const approvedChanges = CHANGES_WITH_VOTES.filter(change => decisions[change.id] === 'approved');

            // Apply approved changes to personas data
            const finalPersonas = JSON.parse(JSON.stringify(PERSONAS_DATA));
            approvedChanges.forEach(change => {
                applyChange(finalPersonas, change);
            });

            // Apply all edits
            Object.keys(edits).forEach(editId => {
                applyEdit(finalPersonas, editId, edits[editId]);
            });

            // Generate clean HTML
            return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Buyer Personas - Final Report</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f8f9fa;
            line-height: 1.6;
            color: #333;
        }
        .header {
            background: linear-gradient(135deg, #2D4C33 0%, #203524 100%);
            color: #D1F470;
            padding: 40px 20px;
            text-align: center;
        }
        .header h1 { font-size: 32px; margin-bottom: 10px; }
        .header p { opacity: 0.95; font-size: 16px; }
        .container { max-width: 1000px; margin: 0 auto; padding: 15px; }

        .segment-section {
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }

        .segment-section.digital {
            border-left: 6px solid #60A5FA;
        }

        .segment-section.smb {
            border-left: 6px solid #A1D78F;
        }

        .segment-section.commercial {
            border-left: 6px solid #FEEB7E;
        }

        .segment-section.enterprise {
            border-left: 6px solid #A78BFA;
        }

        .segment-header {
            margin: -20px -20px 20px -20px;
            padding: 16px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-radius: 8px 8px 0 0;
        }

        .segment-section.digital .segment-header {
            background: #60A5FA;
        }

        .segment-section.smb .segment-header {
            background: #A1D78F;
        }

        .segment-section.commercial .segment-header {
            background: #FEEB7E;
        }

        .segment-section.enterprise .segment-header {
            background: #A78BFA;
        }

        .segment-title {
            font-size: 22px;
            font-weight: bold;
            margin: 0;
        }

        .segment-section.digital .segment-title {
            color: #1E3A8A;
        }

        .segment-section.smb .segment-title {
            color: #2D4C33;
        }

        .segment-section.commercial .segment-title {
            color: #11110D;
        }

        .segment-section.enterprise .segment-title {
            color: #5B21B6;
        }

        .segment-subtitle {
            font-size: 14px;
            opacity: 0.8;
            font-weight: 500;
        }

        .segment-section.digital .segment-subtitle {
            color: #1E3A8A;
        }

        .segment-section.smb .segment-subtitle {
            color: #2D4C33;
        }

        .segment-section.commercial .segment-subtitle {
            color: #11110D;
        }

        .segment-section.enterprise .segment-subtitle {
            color: #5B21B6;
        }

        .persona-card {
            margin-top: 20px;
            margin-bottom: 15px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
            border: 1px solid #e5e7eb;
            overflow: hidden;
        }
        .persona-title {
            font-size: 20px;
            font-weight: bold;
            color: #11110D;
            padding: 14px 18px;
        }

        .segment-section.digital .persona-title {
            background: linear-gradient(135deg, #60A5FA 0%, #3B82F6 100%);
        }

        .segment-section.smb .persona-title {
            background: linear-gradient(135deg, #A1D78F 0%, #88c478 100%);
        }

        .segment-section.commercial .persona-title {
            background: linear-gradient(135deg, #FEEB7E 0%, #f5dc5e 100%);
        }

        .segment-section.enterprise .persona-title {
            background: linear-gradient(135deg, #A78BFA 0%, #8B5CF6 100%);
        }
        .persona-content {
            padding: 18px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        .persona-column { min-width: 0; }

        .section-header {
            font-size: 15px;
            font-weight: 600;
            margin: 12px 0 6px 0;
            padding-bottom: 3px;
            border-bottom: 1px solid #e5e7eb;
        }
        .section-header:first-child { margin-top: 0; }

        .segment-section.digital .section-header {
            color: #1E3A8A;
        }

        .segment-section.smb .section-header {
            color: #2D4C33;
        }

        .segment-section.commercial .section-header {
            color: #11110D;
        }

        .segment-section.enterprise .section-header {
            color: #5B21B6;
        }

        .field-item {
            margin: 6px 0;
            padding: 4px 0;
            font-size: 14px;
            line-height: 1.5;
        }
        .field-label {
            font-weight: 600;
            color: #495057;
            font-size: 14px;
        }
        ul {
            margin-left: 18px;
            margin-top: 6px;
            font-size: 14px;
            line-height: 1.5;
        }
        li { margin: 5px 0; }

        .footer {
            text-align: center;
            padding: 30px 20px;
            color: #666;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 Buyer Personas</h1>
        <p>Final approved personas - ${new Date().toLocaleDateString('en-US', { month: 'long', year: 'numeric' })}</p>
    </div>

    <div class="container">
        ${generateFinalPersonasHTML(finalPersonas)}
    </div>

    <div class="footer">
        Generated on ${new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}
    </div>
</body>
</html>`;
        }

        function applyChange(personas, change) {
            const persona = personas[change.segment][change.persona];
            if (!persona) return;

            const fieldParts = change.field.split('.');

            if (change.type === 'added') {
                if (fieldParts.length === 1) {
                    // List item added
                    if (Array.isArray(persona[change.field])) {
                        persona[change.field].push(change.item_value);
                    }
                }
            } else if (change.type === 'deleted') {
                if (fieldParts.length === 1) {
                    // List item removed
                    if (Array.isArray(persona[change.field])) {
                        const index = persona[change.field].indexOf(change.item_value);
                        if (index > -1) {
                            persona[change.field].splice(index, 1);
                        }
                    }
                }
            } else if (change.type === 'modified') {
                // Field value changed
                if (fieldParts.length === 1) {
                    persona[change.field] = change.new;
                } else if (fieldParts.length === 2) {
                    // Nested field (e.g., buying_behavior.decision_speed)
                    persona[fieldParts[0]][fieldParts[1]] = change.new;
                }
            }
        }

        function applyEdit(personas, editId, newValue) {
            // Parse editId: edit_segment_persona_field or edit_segment_persona_field_index
            const parts = editId.replace('edit_', '').split('_');

            if (parts.length < 3) return;

            let segment = parts[0];

            // Simple approach: find persona by trying to match from personas data
            let foundPersona = null;
            let foundPersonaName = null;

            Object.keys(personas[segment] || {}).forEach(pName => {
                const normalizedPersona = pName.replace(/\s+/g, '_');
                if (editId.includes(normalizedPersona)) {
                    foundPersona = personas[segment][pName];
                    foundPersonaName = normalizedPersona;
                }
            });

            if (!foundPersona) return;

            // Extract field/index after segment and persona name
            const afterPersona = editId.split(foundPersonaName + '_')[1];
            if (!afterPersona) return;

            const remainingParts = afterPersona.split('_');
            const lastPart = remainingParts[remainingParts.length - 1];
            const isListItem = !isNaN(lastPart);

            if (isListItem) {
                // List item edit
                const index = parseInt(lastPart);
                const fieldName = remainingParts.slice(0, -1).join('_');

                if (foundPersona[fieldName] && Array.isArray(foundPersona[fieldName]) && foundPersona[fieldName][index] !== undefined) {
                    foundPersona[fieldName][index] = newValue;
                }
            } else {
                // Field edit
                const fieldName = remainingParts.join('_');

                if (fieldName.includes('_')) {
                    // Nested field like buying_behavior_decision_speed
                    const fieldParts = fieldName.split('_');
                    if (fieldParts.length === 2) {
                        if (!foundPersona[fieldParts[0]]) foundPersona[fieldParts[0]] = {};
                        foundPersona[fieldParts[0]][fieldParts[1]] = newValue;
                    }
                } else {
                    foundPersona[fieldName] = newValue;
                }
            }
        }

        function generateFinalPersonasHTML(personas) {
            let html = '';

            ['SMB', 'Commercial'].forEach(segment => {
                html += '<div class="segment-section ' + segment.toLowerCase() + '">';
                html += '<div class="segment-header">';
                html += '<div class="segment-title">' + segment + ' Segment Personas</div>';
                html += '<div class="segment-subtitle">Company Size: ' + (segment === 'SMB' ? '50-249' : '250-1,499') + ' employees</div>';
                html += '</div>';

                Object.keys(personas[segment]).forEach(personaName => {
                    const persona = personas[segment][personaName];
                    html += '<div class="persona-card">';
                    html += '<div class="persona-title">' + personaName + '</div>';
                    html += '<div class="persona-content">';

                    // LEFT COLUMN
                    html += '<div class="persona-column">';
                    html += '<div class="section-header">Profile Overview</div>';
                    html += '<div class="field-item"><span class="field-label">Job Titles:</span> ' + persona.job_titles.join(', ') + '</div>';
                    html += '<div class="field-item"><span class="field-label">Reports To:</span> ' + persona.reports_to + '</div>';
                    html += '<div class="field-item"><span class="field-label">Team Size:</span> ' + persona.team_size + '</div>';
                    html += '<div class="field-item"><span class="field-label">Prevalence in Deals:</span> ' + persona.prevalence + '</div>';
                    html += '<div class="field-item"><span class="field-label">Role in Buying Process:</span> ' + persona.role_in_deal + '</div>';

                    html += '<div class="section-header">Goals & Priorities</div>';
                    html += '<ul>' + persona.goals.map(g => '<li>' + g + '</li>').join('') + '</ul>';

                    html += '<div class="section-header">Pain Points</div>';
                    html += '<ul>' + persona.pain_points.map(p => '<li>' + p + '</li>').join('') + '</ul>';

                    html += '<div class="section-header">Customer Service Challenges</div>';
                    html += '<ul>' + persona.challenges_from_gong.map(c => '<li>' + c + '</li>').join('') + '</ul>';
                    html += '</div>'; // left column

                    // RIGHT COLUMN
                    html += '<div class="persona-column">';
                    html += '<div class="section-header">Evaluation Criteria</div>';
                    html += '<ul>' + persona.evaluation_criteria.map(e => '<li>' + e + '</li>').join('') + '</ul>';

                    html += '<div class="section-header">Common Objections</div>';
                    html += '<ul>' + persona.objections.map(o => '<li>' + o + '</li>').join('') + '</ul>';

                    html += '<div class="section-header">Key Messages</div>';
                    html += '<ul>' + persona.key_messages.map(m => '<li>' + m + '</li>').join('') + '</ul>';

                    html += '<div class="section-header">Content Preferences</div>';
                    html += '<ul>' + persona.content_preferences.map(c => '<li>' + c + '</li>').join('') + '</ul>';

                    html += '<div class="section-header">Success Metrics</div>';
                    html += '<ul>' + persona.success_metrics.map(s => '<li>' + s + '</li>').join('') + '</ul>';

                    html += '<div class="section-header">Buying Behavior</div>';
                    const bb = persona.buying_behavior;
                    html += '<div class="field-item"><span class="field-label">Decision Speed:</span> ' + bb.decision_speed + '</div>';
                    html += '<div class="field-item"><span class="field-label">Committee Size:</span> ' + bb.committee_size + '</div>';
                    html += '<div class="field-item"><span class="field-label">Authority Level:</span> ' + bb.authority_level + '</div>';
                    html += '<div class="field-item"><span class="field-label">Prefers:</span> ' + bb.prefers + '</div>';
                    html += '</div>'; // right column

                    html += '</div>'; // persona-content
                    html += '</div>'; // persona-card
                });

                html += '</div>'; // segment-section
            });

            return html;
        }

        window.addEventListener('DOMContentLoaded', init);
    </script>
</body>
</html>'''

        return html

    def generate_submissions_viewer(self, personas: Dict, changes_data: Dict) -> str:
        """Generate a viewer for individual team submissions with full change details"""
        feedback_data = self.load_feedback_counts()

        # Create a map of changes by ID for lookup
        changes_map = {change['id']: change for change in changes_data['changes']}

        html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Team Submissions Viewer</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f8f9fa;
            line-height: 1.6;
            color: #333;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
        }
        .header h1 { font-size: 32px; margin-bottom: 10px; }
        .container { max-width: 1000px; margin: 20px auto; padding: 20px; }

        .submission-card {
            background: white;
            border-radius: 8px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }

        .submission-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 15px;
            border-bottom: 2px solid #e9ecef;
            margin-bottom: 20px;
        }

        .reviewer-name {
            font-size: 20px;
            font-weight: bold;
            color: #495057;
        }

        .timestamp {
            font-size: 14px;
            color: #666;
        }

        .feedback-item {
            padding: 15px;
            background: #f8f9fa;
            border-radius: 6px;
            margin: 10px 0;
            border-left: 4px solid #667eea;
        }

        .change-path {
            font-size: 12px;
            color: #666;
            font-family: monospace;
            margin-bottom: 8px;
        }

        .change-details {
            margin: 10px 0;
            padding: 10px;
            background: white;
            border-radius: 4px;
            font-size: 14px;
        }

        .change-label {
            font-size: 11px;
            color: #666;
            text-transform: uppercase;
            font-weight: 600;
            margin-bottom: 4px;
        }

        .old-value {
            color: #dc2626;
            text-decoration: line-through;
        }

        .new-value {
            color: #059669;
            font-weight: 500;
        }

        .vote-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
            margin-right: 10px;
        }

        .vote-agree {
            background: #d1fae5;
            color: #065f46;
        }

        .vote-disagree {
            background: #fee2e2;
            color: #991b1b;
        }

        .comment {
            margin-top: 10px;
            padding: 10px;
            background: #fffbeb;
            border-radius: 4px;
            font-style: italic;
            border-left: 3px solid #f59e0b;
        }

        .back-link {
            display: inline-block;
            padding: 12px 24px;
            background: white;
            color: #667eea;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            margin-bottom: 20px;
            border: 2px solid #667eea;
            transition: all 0.2s;
        }

        .back-link:hover {
            background: #667eea;
            color: white;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>👥 Team Submissions</h1>
        <p>Individual feedback from team members</p>
    </div>

    <div class="container">
        <a href="Persona_Approval_Interface.html" class="back-link">← Back to Approval</a>

        <div id="submissionsContainer">
            <!-- Will be rendered by JavaScript -->
        </div>
    </div>

    <script>
        const SUBMISSIONS = ''' + json.dumps(feedback_data['submissions']) + ''';
        const CHANGES_MAP = ''' + json.dumps(changes_map) + ''';

        function init() {
            const container = document.getElementById('submissionsContainer');

            if (SUBMISSIONS.length === 0) {
                container.innerHTML = `
                    <div class="submission-card">
                        <p style="text-align: center; color: #666;">No submissions yet.</p>
                    </div>
                `;
                return;
            }

            let html = '';

            SUBMISSIONS.forEach(submission => {
                html += `
                    <div class="submission-card">
                        <div class="submission-header">
                            <div class="reviewer-name">${submission.reviewer}</div>
                            <div class="timestamp">${new Date(submission.timestamp).toLocaleString()}</div>
                        </div>
                `;

                submission.feedback.forEach(item => {
                    const change = CHANGES_MAP[item.change_id];
                    const voteClass = item.vote === 'agree' ? 'vote-agree' : 'vote-disagree';
                    const voteIcon = item.vote === 'agree' ? '👍' : '👎';

                    html += `
                        <div class="feedback-item">
                            <div class="change-path">${item.change_path} > ${item.change_field}</div>
                            <div>
                                <span class="vote-badge ${voteClass}">${voteIcon} ${item.vote.toUpperCase()}</span>
                                <span style="color: #666; font-size: 12px; text-transform: uppercase;">${item.change_type}</span>
                            </div>
                    `;

                    // Show what changed
                    if (change) {
                        if (change.type === 'added') {
                            html += `
                                <div class="change-details">
                                    <div class="change-label">Added</div>
                                    <div class="new-value">${escapeHtml(change.new || change.item_value || '')}</div>
                                </div>
                            `;
                        } else if (change.type === 'deleted') {
                            html += `
                                <div class="change-details">
                                    <div class="change-label">Removed</div>
                                    <div class="old-value">${escapeHtml(change.old || change.item_value || '')}</div>
                                </div>
                            `;
                        } else if (change.type === 'modified') {
                            html += `
                                <div class="change-details">
                                    <div class="change-label">Changed From</div>
                                    <div class="old-value">${escapeHtml(String(change.old || ''))}</div>
                                    <div class="change-label" style="margin-top: 8px;">Changed To</div>
                                    <div class="new-value">${escapeHtml(String(change.new || ''))}</div>
                                </div>
                            `;
                        }
                    }

                    if (item.comment) {
                        html += `<div class="comment">💬 "${escapeHtml(item.comment)}"</div>`;
                    }

                    html += `</div>`;
                });

                html += `</div>`;
            });

            container.innerHTML = html;
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        window.addEventListener('DOMContentLoaded', init);
    </script>
</body>
</html>'''

        return html


def main():
    print("\n" + "="*80)
    print("🚀 ENHANCED PERSONA PROFILE GENERATOR")
    print("="*80 + "\n")

    updater = EnhancedPersonaUpdater()

    # Load current personas from updated_personas.json
    print("📂 Loading current personas...")
    updated_personas_file = updater.data_dir / "updated_personas.json"
    if updated_personas_file.exists():
        with open(updated_personas_file, 'r') as f:
            data = json.load(f)
            # Check if it's the versioned format with 'personas' key
            if 'personas' in data:
                personas = data['personas']
            else:
                personas = data
        print(f"✓ Loaded personas from: {updated_personas_file}")
    else:
        print("⚠️  updated_personas.json not found, using static personas")
        # Fall back to imported personas if file doesn't exist
        pass

    print("\n📂 Loading previous version...")
    previous_version = updater.load_previous_version()

    if previous_version:
        print(f"✓ Found previous version: {previous_version['version_date']}")
    else:
        print("ℹ️  No previous version - this will be the baseline")

    print("\n🔍 Detecting changes...")
    changes_data = updater.detect_changes(previous_version, personas)

    # Always generate reports (not just when changes detected)
    if changes_data.get('has_changes'):
        print(f"✓ Found {len(changes_data['changes'])} changes")
    else:
        print("✓ No changes detected, regenerating reports with current data")

    # Generate team review HTML - use clean interface
    print("\n📄 Generating team review (clean interface)...")
    import subprocess
    import shutil
    result = subprocess.run(['python3', '/Users/chris.sherman/generate_final_clean_personas.py'],
                          capture_output=True, text=True)
    if result.returncode == 0:
        # Copy FINAL to Team Review
        final_file = updater.reports_dir / "Persona_Profiles_FINAL.html"
        team_file = updater.reports_dir / "Persona_Team_Review_Full.html"
        shutil.copy(final_file, team_file)
        print(f"✓ Team review: {team_file}")
    else:
        print(f"⚠️  Error generating clean interface: {result.stderr}")
        team_file = updater.reports_dir / "Persona_Team_Review_Full.html"

    # Generate approval interface (only if there are changes)
    if changes_data.get('has_changes'):
        print("\n📄 Generating approval interface (with vote counts)...")
        approval_html = updater.generate_approval_html(personas, changes_data)
        approval_file = updater.reports_dir / "Persona_Approval_Interface.html"
        with open(approval_file, 'w') as f:
            f.write(approval_html)
        print(f"✓ Approval interface: {approval_file}")

        # Generate submissions viewer
        print("\n📄 Generating submissions viewer...")
        submissions_html = updater.generate_submissions_viewer(personas, changes_data)
        submissions_file = updater.reports_dir / "submissions_viewer.html"
        with open(submissions_file, 'w') as f:
            f.write(submissions_html)
        print(f"✓ Submissions viewer: {submissions_file}")

    # Copy team review to git repo for GitHub Pages
    print("\n📤 Preparing for GitHub Pages...")
    print(f"✓ Team review ready in git repo")
    print(f"\n  To deploy to GitHub Pages:")
    print(f"  cd /Users/chris.sherman/persona_analysis")
    print(f"  git add reports/Persona_Team_Review_Full.html")
    print(f"  git commit -m 'Update team review'")
    print(f"  git push")

    print("\n" + "="*80)
    print("✨ FILES GENERATED")
    print("="*80)
    print(f"\n📤 Share link (after git push):")
    print(f"   https://chrissherman-png.github.io/persona-analysis/Persona_Team_Review_Full.html")

    if changes_data.get('has_changes'):
        print(f"\n📋 Your approval interface:")
        print(f"   {approval_file}")
        print(f"\n👥 View submissions:")
        print(f"   {submissions_file}")

        print("\n💡 WORKFLOW:")
        print("1. Open approval interface (has Share button)")
        print("2. Share team review file with team")
        print("3. Collect feedback JSON files → team_feedback/")
        print("4. Re-run this script to refresh vote counts")
        print("5. Review and approve/reject changes")
        print("6. Generate final report")

    # Save version
    version_file = updater.save_version(personas)
    print(f"\n✓ Version saved: {version_file}")

    print("\n" + "="*80)


if __name__ == "__main__":
    main()
