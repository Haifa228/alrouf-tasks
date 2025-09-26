# Task 1: RFQ → CRM Automation

## Setup (Using Zapier - No-Code)
1. Trigger: New Email in Gmail (filter for subject containing "RFQ").
2. Action 1: Use OpenAI (optional) or Zapier Parser to extract fields: Subject, Model, Qty, Location, Deadline, Contact Name, Phone, Email, Attachments.
3. Action 2: Add row to Google Sheets (columns: Date, Client, Model, Qty, etc.).
4. Action 3: Create Opportunity in Salesforce (mock: Write to JSON file).
5. Action 4: Upload attachments to Google Drive.
6. Action 5: Send auto-reply email (EN/AR based on lang detection - use googletrans for translation if needed).
7. Action 6: Post alert to Slack/Teams.

## Blueprints/Screenshots
- Upload screenshots of Zapier zap here (e.g., zap_screenshot1.png - add them to this folder).
- Sample Test Email: Processed the example provided.

## Deliverables
- Sample Sheet: See sample_sheet.csv (mock).
- Drive Folder: Mocked in drive_folder_mock.json.
- CRM Mock Log: crm_mock_log.json.
- Auto-Reply Samples: auto_reply_sample_en.txt and auto_reply_sample_ar.txt.
- Error Log: error_log.txt (example errors).

## How to Run Mock Locally
No code needed; just view files.
