#!/usr/bin/env python3
"""
Simple Flask Server for Team Review Inline Editing
Serves static files and provides API endpoints for editing personas
"""

import sys
from pathlib import Path

# Check Flask installation
try:
    from flask import Flask, request, jsonify, send_from_directory
    from flask_cors import CORS
except ImportError:
    print("\n❌ Flask is not installed")
    print("\nInstall required packages:")
    print("  pip install flask flask-cors")
    print("\nOr install all project dependencies:")
    print("  pip install -r requirements.txt")
    sys.exit(1)

import json
from datetime import datetime
import subprocess
import shutil

# Add parent directory to path for imports
sys.path.insert(0, '/Users/chris.sherman')

app = Flask(__name__)
CORS(app)  # Enable CORS for local development

# Configuration
BASE_DIR = Path("/Users/chris.sherman/persona_analysis")
REPORTS_DIR = BASE_DIR / "reports"
DATA_DIR = BASE_DIR / "data"
PENDING_DIR = BASE_DIR / "pending_changes"
UPDATED_PERSONAS_FILE = DATA_DIR / "updated_personas.json"

# Ensure directories exist
PENDING_DIR.mkdir(exist_ok=True)


def get_edits_file_path(run_quarter):
    """Get path to edits file for a specific run quarter"""
    filename = f"edits_{run_quarter.replace(' ', '_')}.json"
    return PENDING_DIR / filename


def load_edits(run_quarter):
    """Load edits file for the specified run quarter"""
    edits_file = get_edits_file_path(run_quarter)

    if not edits_file.exists():
        # Initialize new edits file
        return {
            'run_quarter': run_quarter,
            'last_edited': datetime.now().isoformat(),
            'edited_by': '',
            'edits': {}
        }

    with open(edits_file, 'r') as f:
        return json.load(f)


def save_edits(run_quarter, edits_data):
    """Save edits file for the specified run quarter"""
    edits_file = get_edits_file_path(run_quarter)
    edits_data['last_edited'] = datetime.now().isoformat()

    with open(edits_file, 'w') as f:
        json.dump(edits_data, f, indent=2)


# =============================================================================
# STATIC FILE SERVING
# =============================================================================

@app.route('/')
def index():
    """Serve index page"""
    return send_from_directory(REPORTS_DIR, 'Persona_Team_Review_Full.html')


@app.route('/<path:path>')
def serve_static(path):
    """Serve static files from reports directory"""
    try:
        return send_from_directory(REPORTS_DIR, path)
    except Exception as e:
        return jsonify({'error': str(e)}), 404


# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.route('/api/get_edits', methods=['GET'])
def get_edits():
    """Get current edits for a run quarter"""
    run_quarter = request.args.get('run_quarter')

    if not run_quarter:
        return jsonify({'error': 'run_quarter parameter required'}), 400

    try:
        edits_file = get_edits_file_path(run_quarter)

        # If file doesn't exist, return empty structure (not 404)
        if not edits_file.exists():
            return jsonify({
                'run_quarter': run_quarter,
                'last_edited': None,
                'edited_by': None,
                'edits': {}
            })

        edits_data = load_edits(run_quarter)
        return jsonify(edits_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/get_original', methods=['GET'])
def get_original():
    """Get original items for a section from updated_personas.json"""
    segment = request.args.get('segment')
    persona = request.args.get('persona')
    field = request.args.get('field')

    if not all([segment, persona, field]):
        return jsonify({'error': 'segment, persona, and field parameters required'}), 400

    try:
        # Load updated_personas.json
        with open(UPDATED_PERSONAS_FILE, 'r') as f:
            personas_data = json.load(f)

        # Navigate to the requested field
        if (segment not in personas_data or
            persona not in personas_data[segment] or
            field not in personas_data[segment][persona]):
            return jsonify({
                'segment': segment,
                'persona': persona,
                'field': field,
                'items': []
            })

        original_items = personas_data[segment][persona][field]

        return jsonify({
            'segment': segment,
            'persona': persona,
            'field': field,
            'items': original_items if isinstance(original_items, list) else []
        })

    except Exception as e:
        print(f"Error getting original: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/save_edit', methods=['POST'])
def save_edit():
    """Save an individual edit"""
    data = request.json

    # Validate required fields
    required = ['run_quarter', 'segment', 'persona', 'field', 'action']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    try:
        run_quarter = data['run_quarter']
        segment = data['segment']
        persona = data['persona']
        field = data['field']
        action = data['action']
        edited_by = data.get('edited_by', 'Unknown')

        # Load current edits
        edits_data = load_edits(run_quarter)

        # Update edited_by at root level
        edits_data['edited_by'] = edited_by

        # Ensure nested structure exists
        if segment not in edits_data['edits']:
            edits_data['edits'][segment] = {}
        if persona not in edits_data['edits'][segment]:
            edits_data['edits'][segment][persona] = {}
        if field not in edits_data['edits'][segment][persona]:
            # Initialize with original items from updated_personas.json
            with open(UPDATED_PERSONAS_FILE, 'r') as f:
                personas_data = json.load(f)

            original_items = []
            if (segment in personas_data and
                persona in personas_data[segment] and
                field in personas_data[segment][persona]):
                original_items = personas_data[segment][persona][field]

            edits_data['edits'][segment][persona][field] = {
                'items': original_items.copy() if isinstance(original_items, list) else [],
                'has_changes': False,
                'change_log': []
            }

        section = edits_data['edits'][segment][persona][field]

        # Apply the action
        if action == 'edit':
            index = data['index']
            new_value = data['new_value']
            original_value = data.get('original_value', '')

            # Ensure items list is long enough
            while len(section['items']) <= index:
                section['items'].append('')

            section['items'][index] = new_value
            section['has_changes'] = True

            # Add to change log
            section['change_log'].append({
                'action': 'edit',
                'index': index,
                'original_value': original_value,
                'new_value': new_value,
                'edited_by': edited_by,
                'timestamp': datetime.now().isoformat()
            })

        elif action == 'add':
            new_value = data['new_value']

            section['items'].append(new_value)
            section['has_changes'] = True

            # Add to change log
            section['change_log'].append({
                'action': 'add',
                'index': len(section['items']) - 1,
                'original_value': None,
                'new_value': new_value,
                'edited_by': edited_by,
                'timestamp': datetime.now().isoformat()
            })

        elif action == 'delete':
            index = data['index']
            original_value = data.get('original_value', '')

            if index < len(section['items']):
                # Store deleted value
                deleted_item = section['items'][index]

                # Check if this item was added (not in original)
                # If it was added, remove both the add and delete entries
                was_added = any(
                    log['action'] == 'add' and log['index'] == index
                    for log in section['change_log']
                )

                if was_added:
                    # Remove the add entry from change_log
                    section['change_log'] = [
                        log for log in section['change_log']
                        if not (log['action'] == 'add' and log['index'] == index)
                    ]
                    # Just remove the item, don't add a delete entry
                    section['items'].pop(index)
                else:
                    # This is an original item, so record the delete
                    # Remove item
                    section['items'].pop(index)

                    # If this item was previously edited, remove the edit entry
                    section['change_log'] = [
                        log for log in section['change_log']
                        if not (log['action'] == 'edit' and log['index'] == index)
                    ]

                    # Add to change log with actual deleted value
                    section['change_log'].append({
                        'action': 'delete',
                        'index': index,
                        'original_value': original_value or deleted_item,
                        'new_value': None,
                        'edited_by': edited_by,
                        'timestamp': datetime.now().isoformat()
                    })

                section['has_changes'] = True if section['change_log'] else False

        elif action == 'revert':
            index = data['index']
            original_value = data.get('original_value', '')

            # Restore original value
            if index < len(section['items']):
                section['items'][index] = original_value

                # Remove last change_log entry for this index if it exists
                section['change_log'] = [
                    entry for entry in section['change_log']
                    if not (entry['index'] == index and entry.get('timestamp') == section['change_log'][-1].get('timestamp'))
                ]

                # Check if any changes remain
                if len(section['change_log']) == 0:
                    section['has_changes'] = False

        # Save edits
        save_edits(run_quarter, edits_data)

        return jsonify({'success': True, 'message': 'Edit saved successfully'})

    except Exception as e:
        print(f"Error saving edit: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/apply_edits', methods=['POST'])
def apply_edits():
    """Apply all edits to updated_personas.json and regenerate Final page"""

    data = request.json
    run_quarter = data.get('run_quarter')

    if not run_quarter:
        return jsonify({'error': 'run_quarter parameter required'}), 400

    backup_file = None

    try:
        # Load edits
        edits_data = load_edits(run_quarter)

        # Count individual item-level changes (edited + added + deleted)
        changes_count = 0
        for segment in edits_data.get('edits', {}).values():
            for persona in segment.values():
                for field_data in persona.values():
                    if field_data.get('has_changes') and field_data.get('change_log'):
                        # Count each individual change in the change_log
                        changes_count += len(field_data['change_log'])

        # If no changes, return early
        if changes_count == 0:
            return jsonify({
                'success': False,
                'error': 'No pending changes to apply',
                'changes_applied': 0
            })

        # Create backup of updated_personas.json BEFORE any modifications
        backup_file = UPDATED_PERSONAS_FILE.parent / 'updated_personas.backup.json'
        shutil.copy2(UPDATED_PERSONAS_FILE, backup_file)

        # Load updated_personas.json
        with open(UPDATED_PERSONAS_FILE, 'r') as f:
            personas_data = json.load(f)

        # Apply edits to personas_data
        sections_modified = 0
        for segment, segment_data in edits_data['edits'].items():
            if segment not in personas_data:
                continue

            for persona, persona_data_edits in segment_data.items():
                if persona not in personas_data[segment]:
                    continue

                for field, field_data in persona_data_edits.items():
                    if field_data.get('has_changes'):
                        # Replace the field with edited items
                        personas_data[segment][persona][field] = field_data['items']
                        sections_modified += 1

        # Save updated personas (destructive step)
        with open(UPDATED_PERSONAS_FILE, 'w') as f:
            json.dump(personas_data, f, indent=2)

        # Regenerate Final page using subprocess
        script_path = BASE_DIR.parent / 'generate_final_clean_personas.py'
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout
        )

        if result.returncode != 0:
            # Subprocess failed - restore from backup
            shutil.copy2(backup_file, UPDATED_PERSONAS_FILE)
            error_msg = f"Final page regeneration failed. Restored from backup.\n\nError: {result.stderr}"
            print(error_msg)

            # Clean up backup
            if backup_file.exists():
                backup_file.unlink()

            return jsonify({
                'success': False,
                'error': error_msg,
                'changes_applied': 0,
                'restored_from_backup': True
            })

        # Success - log the apply action to pipeline metadata
        metadata_file = BASE_DIR / 'pipeline_run_metadata.json'
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)

                metadata['last_apply'] = {
                    'timestamp': datetime.now().isoformat(),
                    'changes_applied': changes_count,
                    'sections_modified': sections_modified,
                    'applied_by': edits_data.get('edited_by', 'Unknown')
                }

                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f, indent=2)
            except Exception as e:
                print(f"Warning: Could not update pipeline metadata: {e}")

        # Delete backup after successful apply
        if backup_file and backup_file.exists():
            backup_file.unlink()

        # Success - return output path
        output_path = "persona_analysis/reports/Persona_Profiles_FINAL.html"

        return jsonify({
            'success': True,
            'changes_applied': changes_count,
            'sections_modified': sections_modified,
            'output_path': output_path,
            'message': f'Applied {changes_count} changes across {sections_modified} sections and regenerated Final page'
        })

    except subprocess.TimeoutExpired:
        # Restore from backup on timeout
        if backup_file and backup_file.exists():
            shutil.copy2(backup_file, UPDATED_PERSONAS_FILE)
            backup_file.unlink()

        return jsonify({
            'success': False,
            'error': 'Final page regeneration timed out after 30 seconds. Restored from backup.',
            'restored_from_backup': True
        }), 500

    except Exception as e:
        # Restore from backup on any error
        if backup_file and backup_file.exists():
            try:
                shutil.copy2(backup_file, UPDATED_PERSONAS_FILE)
                backup_file.unlink()
                restored = True
            except:
                restored = False
        else:
            restored = False

        print(f"Error applying edits: {e}")
        import traceback
        traceback.print_exc()

        return jsonify({
            'success': False,
            'error': str(e),
            'restored_from_backup': restored
        }), 500


@app.route('/api/rollback_edits', methods=['POST'])
def rollback_edits():
    """Rollback the last applied edits using change_log"""
    data = request.json
    run_quarter = data.get('run_quarter')

    if not run_quarter:
        return jsonify({'error': 'run_quarter parameter required'}), 400

    try:
        # Load edits
        edits_data = load_edits(run_quarter)

        # Load updated_personas.json
        with open(UPDATED_PERSONAS_FILE, 'r') as f:
            personas_data = json.load(f)

        # Rollback edits using change_log
        rollback_count = 0
        for segment, segment_data in edits_data['edits'].items():
            if segment not in personas_data:
                continue

            for persona, persona_data_edits in segment_data.items():
                if persona not in personas_data[segment]:
                    continue

                for field, field_data in persona_data_edits.items():
                    if field_data.get('has_changes') and field_data.get('change_log'):
                        # Reconstruct original by reversing change_log
                        # This is complex - for now, just clear the edits
                        # TODO: Implement proper rollback from original values

                        # For now, remove the applied changes by clearing has_changes flag
                        # User will need to re-run pipeline for true rollback
                        field_data['has_changes'] = False
                        rollback_count += 1

        # Save edits (with has_changes cleared)
        save_edits(run_quarter, edits_data)

        # Note: A full rollback would require storing pre-edit state
        # For now, this marks edits as not applied

        return jsonify({
            'success': True,
            'message': f'Rolled back {rollback_count} section changes. Note: Full rollback requires re-running the pipeline.',
            'rollback_count': rollback_count
        })

    except Exception as e:
        print(f"Error rolling back edits: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# =============================================================================
# SERVER STARTUP
# =============================================================================

if __name__ == '__main__':
    print("\n" + "="*80)
    print("🚀 Team Review Server Starting")
    print("="*80)
    print(f"\n📍 Serving from: {REPORTS_DIR}")
    print(f"📊 Data directory: {DATA_DIR}")
    print(f"✏️  Edits directory: {PENDING_DIR}")
    print("\n🌐 Server running at: http://localhost:8080")
    print("   Open: http://localhost:8080/Persona_Team_Review_Full.html")
    print("\n💡 Press Ctrl+C to stop the server")
    print("="*80 + "\n")

    app.run(host='0.0.0.0', port=8080, debug=True)
