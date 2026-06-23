# Google Sheets API Setup for Team Feedback

This guide shows you how to set up service account credentials for reading feedback from Google Sheets.

**Note:** The `aggregate_team_feedback.py` script is not included in this repository. This guide is provided for reference if you want to implement Google Sheets integration for feedback collection.

## Prerequisites

- Google Cloud project (free tier is sufficient)
- Access to the Google Sheet with team feedback

## Step 1: Create Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project or create a new one:
   - Click the project dropdown at the top
   - Click **New Project**
   - Name: `Persona Feedback`
   - Click **Create**

3. Enable Google Sheets API:
   - Go to **APIs & Services** → **Library**
   - Search for "Google Sheets API"
   - Click on it and click **Enable**

4. Create Service Account:
   - Go to **IAM & Admin** → **Service Accounts**
   - Click **Create Service Account**
   - Service account name: `persona-feedback-reader`
   - Service account description: `Reads team feedback from Google Sheets`
   - Click **Create and Continue**
   - Skip granting roles (click **Continue**)
   - Click **Done**

## Step 2: Create and Download Key

1. In the Service Accounts list, click on **persona-feedback-reader**
2. Go to the **Keys** tab
3. Click **Add Key** → **Create new key**
4. Choose **JSON** format
5. Click **Create**
6. The key file downloads automatically (looks like `projectname-abc123.json`)
7. **Rename the file** to `google_service_account.json`
8. **Move it** to: `<repo_root>/google_service_account.json`

## Step 3: Share Google Sheet with Service Account

1. Open the JSON file you just downloaded
2. Find the `client_email` field - it looks like:
   ```
   "client_email": "persona-feedback-reader@projectname-abc123.iam.gserviceaccount.com"
   ```
3. Copy the email address

4. Open your Google Sheet:
   - ID: `1S4ePwUL3wCA84frDlO7G0sGLSwY64YIrKJJAA6G9ok0`
   - URL: https://docs.google.com/spreadsheets/d/1S4ePwUL3wCA84frDlO7G0sGLSwY64YIrKJJAA6G9ok0

5. Click the **Share** button (top right)
6. Paste the service account email
7. Change permission to **Viewer**
8. **Uncheck** "Notify people"
9. Click **Share**

## Step 4: Install Python Libraries

```bash
pip install gspread google-auth
```

## Step 5: Test the Connection

```bash
python3 aggregate_team_feedback.py --run-quarter "Q2 2026"
```

You should see:
```
✓ Connected to Google Sheets
✓ Found N feedback rows
```

## Troubleshooting

### Error: "Service account credentials not found"
- Make sure the file is saved to the exact path: `<repo_root>/google_service_account.json`
- Check the filename is exactly `google_service_account.json`

### Error: "The caller does not have permission"
- Make sure you shared the Google Sheet with the service account email
- Double-check the email in the JSON file matches what you shared

### Error: "gspread library not available"
- Install the required libraries: `pip install gspread google-auth`

## Security Notes

- **Never commit** `google_service_account.json` to git
- It's already in `.gitignore`
- The service account only has read access to the shared sheet
- You can revoke access anytime by removing the service account from the Share settings

## File Locations

- Service account key: `<repo_root>/google_service_account.json`
- Aggregated output: `<repo_root>/team_feedback/aggregated_feedback_Q2_2026.json`
