# Implementation Guide

Complete phase-by-phase implementation of the Client Management System.

## Table of Contents

0. [Pre-Phase: Data Migration](#pre-phase-data-migration-week-0)
1. [Phase 1: SharePoint Foundation](#phase-1-sharepoint-foundation-week-1)
2. [Phase 2: Power Apps UI](#phase-2-power-apps-ui-week-2)
3. [Phase 3: Power Automate Workflows](#phase-3-power-automate-workflows-week-3)
4. [Phase 4: Advanced Integration](#phase-4-advanced-integration-week-4)

---

## Pre-Phase: Data Migration (Week 0)

Before setting up the new CRM system, you need to prepare and migrate existing client data.

### Step 0.1: Audit Current Data Sources

Identify where your client data currently lives:

```
Current Systems:
□ Salesforce (existing CRM)
□ Excel/CSV files (spreadsheets)
□ Azure AD (user accounts)
□ Email/Outlook contacts
□ Custom databases
□ Paper records
□ Other systems: _________________

Data to migrate:
□ Account/Company information
□ Contact details
□ Historical communications
□ Access levels/permissions
□ Contract dates
□ Custom fields
```

### Step 0.2: Assess Data Quality

Before migration, evaluate your data:

```
Data Quality Checklist:
□ Duplicate records: Are there duplicates? Run deduplication first.
□ Missing fields: What % of records have blank required fields?
□ Outdated contacts: When was data last updated?
□ Inconsistent formats: Email addresses, phone numbers, company names
□ Orphaned records: Contacts without accounts
□ Invalid data: Incorrect email formats, bad characters

Issues found:
- Issue 1: _______________  Severity: High/Medium/Low  Action: _______________
- Issue 2: _______________  Severity: High/Medium/Low  Action: _______________
- Issue 3: _______________  Severity: High/Medium/Low  Action: _______________
```

**Recommendation:** Clean data before migration (saves time later).

### Step 0.3: Choose Migration Strategy

#### **Option A: From Salesforce (Recommended if you have Salesforce)**

**Tools needed:**
- Salesforce Data Export
- Power Query (Excel)
- CSV upload to SharePoint

**Process:**
```
1. In Salesforce:
   ├─ Reports → Export Accounts → accounts.csv
   ├─ Reports → Export Contacts → contacts.csv
   └─ Save files locally

2. In Excel (Data Cleaning):
   ├─ Open accounts.csv
   ├─ Rename columns to match SharePoint:
   │  ├─ Account Name → Title
   │  ├─ Industry → Client_Segment (map manually)
   │  ├─ Annual Revenue → Tier (map manually)
   │  └─ Status → Status
   ├─ Remove unnecessary columns
   ├─ Check for duplicates
   └─ Save as cleaned-accounts.csv

3. Repeat for contacts.csv:
   ├─ Contact Name → Title
   ├─ Email → Email
   ├─ Account Name → Account (will link later)
   ├─ Title → Role (map Admin/User/Viewer)
   └─ Save as cleaned-contacts.csv

4. In SharePoint Lists:
   ├─ Go to Accounts list
   ├─ Click "Import" → Upload cleaned-accounts.csv
   ├─ Map columns
   ├─ Complete import
   └─ Verify: 10-100 accounts imported
```

**Mapping Example (Salesforce → SharePoint):**
```
Salesforce Field          → SharePoint Field
─────────────────────────────────────────
Account Name              → Title
Industry                  → Client_Segment
Annual Revenue            → Tier (map: <$1M=Startup, $1-10M=MidMarket, >$10M=Enterprise)
StageName (Opportunity)   → Status (map: Active/Inactive)
Contract Expiration Date  → Access_Expiry
Account Description       → Notes
```

#### **Option B: From Excel/CSV Files**

**Process:**
```
1. Gather all CSV files with client data
   ├─ accounts.csv
   ├─ contacts.csv
   └─ other_data.csv

2. In Excel, standardize format:
   ├─ Column headers must match SharePoint exactly
   ├─ Remove extra/unused columns
   ├─ Ensure all data types match (text, date, number)
   └─ Fix any special characters

3. Clean data:
   ├─ Remove duplicates (Data → Remove Duplicates)
   ├─ Trim whitespace (Find & Replace → Trim)
   ├─ Standardize date format (all as YYYY-MM-DD)
   └─ Verify no blank required fields

4. Upload to SharePoint:
   ├─ Go to List → Import
   ├─ Upload CSV file
   ├─ Map columns
   └─ Verify import
```

**Column mapping for CSV:**
```
CSV Column              → SharePoint Field
──────────────────────────────────────────
Company Name           → Title
Segment               → Client_Segment
Customer Type         → Tier
Is Active?            → Status
Contract Expires      → Access_Expiry
Notes                 → Notes
Contact Name          → Title (in Contacts)
Contact Email         → Email
Company (for Contact) → Account (Lookup)
```

#### **Option C: From Azure AD**

**Purpose:** Sync existing user accounts from Azure AD

**Process:**
```
1. In Azure AD:
   ├─ Groups → Export all groups containing "ClientGroup"
   └─ For each group:
      ├─ Export members list
      └─ Get: UserID, Email, DisplayName

2. Create contacts.csv from Azure AD data:
   ├─ Azure User ID → Azure_User_ID
   ├─ UserPrincipalName → Email
   ├─ DisplayName → Title
   ├─ Has Azure account → Set to "Yes" for all
   └─ Map to Account (manual or lookup)

3. Upload to SharePoint:
   ├─ Go to Contacts list
   ├─ Import contacts.csv
   ├─ Verify Azure_User_ID is populated
   └─ Set Has_Azure_Account = YES for all
```

#### **Option D: Hybrid (Multiple Sources)**

If data comes from multiple systems:

```
1. Export from each system:
   ├─ System A → accounts_a.csv
   ├─ System B → contacts_b.csv
   └─ System C → users_c.csv

2. Consolidate in Excel:
   ├─ Create master_accounts.csv
   │  ├─ Combine all accounts
   │  ├─ Deduplicate
   │  └─ Map to standard columns
   │
   ├─ Create master_contacts.csv
   │  ├─ Combine all contacts
   │  ├─ Deduplicate
   │  ├─ Add source field (which system)
   │  └─ Map to standard columns
   │
   └─ Reconcile discrepancies:
      ├─ Same account in System A and B?
      ├─ Different contact info?
      └─ Manual review and merge

3. Upload consolidated files to SharePoint
```

### Step 0.4: Data Validation & Cleanup

Before importing, validate your CSV files:

```
Validation Checklist:
☐ Column names match SharePoint exactly
☐ No duplicate records (remove with Find & Replace)
☐ Date fields are in YYYY-MM-DD format
☐ Email addresses are valid (basic check: contains @)
☐ Phone numbers are consistent format
☐ Required fields are populated (no blanks in critical fields)
☐ No special characters that break imports
☐ File is saved as UTF-8 (not Excel format)
☐ Row count is correct
☐ Sample spot-check: 5 random rows verified

Common issues to fix:
├─ Extra spaces at start/end of fields
│  └─ Solution: Find & Replace "  " → "" (remove spaces)
├─ Inconsistent company names (Acme Corp vs ACME CORP vs acme)
│  └─ Solution: Manual review or PROPER() function
├─ Multiple email addresses in one field
│  └─ Solution: Create separate contact records
├─ Dates in multiple formats (3/1/2026 vs 2026-03-01)
│  └─ Solution: Convert all to YYYY-MM-DD
└─ Text in number fields
   └─ Solution: Clean to numbers only
```

### Step 0.5: Create Migration Plan Document

Write down your specific migration plan:

```
MIGRATION PLAN

Data Sources:
□ Primary source: _________________ (Salesforce / Excel / Azure AD / Other)
□ Secondary source: _________________ (if applicable)
□ Tertiary source: _________________ (if applicable)

Timeline:
□ Data audit: __________ (date)
□ Data cleanup: __________ (date)
□ CSV preparation: __________ (date)
□ Test import: __________ (date)
□ Full production import: __________ (date)

Owner/Responsibility:
□ Data extraction: _______________
□ Data cleaning: _______________
□ Validation: _______________
□ Upload to SharePoint: _______________

Expected Results:
□ Accounts to migrate: __________ (number)
□ Contacts to migrate: __________ (number)
□ Campaigns to migrate: __________ (yes/no)
□ Interaction history: __________ (yes/no)

Rollback Plan:
□ If import fails: __________________________________
□ If data corruption: __________________________________
□ If < 90% successful: __________________________________
```

### Step 0.6: Perform Test Migration

**Do this BEFORE production:**

```
1. Create test SharePoint site:
   └─ /sites/client-management-test

2. Import sample data (10-20 records):
   ├─ accounts_sample.csv → Test Accounts list
   └─ contacts_sample.csv → Test Contacts list

3. Verify in SharePoint:
   ☐ All records imported
   ☐ All columns populated correctly
   ☐ Lookup fields working (Account link in Contacts)
   ☐ Dates formatted correctly
   ☐ No data corruption
   ☐ Can view and edit records

4. If issues found:
   ├─ Delete test data
   ├─ Fix CSV file
   ├─ Retry import
   └─ Repeat until successful

5. Document any issues:
   └─ Record what went wrong and how you fixed it
      (This helps with production import)
```

### Step 0.7: Production Data Import

Once test is successful:

```
1. Prepare production lists in SharePoint:
   ├─ Create all 4 lists (Accounts, Contacts, Campaigns, Interactions)
   ├─ Configure columns
   └─ Enable quick edit and attachments

2. Import Accounts:
   ├─ Go to Accounts list → Import
   ├─ Upload cleaned-accounts.csv
   ├─ Map columns carefully
   ├─ Preview before completing
   └─ Click "Import"
   └─ Verify: Count matches expected

3. Import Contacts:
   ├─ Go to Contacts list → Import
   ├─ Upload cleaned-contacts.csv
   ├─ Important: Map Account column as Lookup
   ├─ For each contact, system will find matching account
   ├─ Preview results
   └─ Click "Import"
   └─ Verify: All lookups resolved correctly

4. Verify all data:
   ├─ Total accounts: __________ ✓
   ├─ Total contacts: __________ ✓
   ├─ Account lookups working: Yes / No
   ├─ Contact lookups working: Yes / No
   ├─ No blank required fields: Yes / No
   └─ Data looks correct: Yes / No
```

### Step 0.8: Post-Migration Cleanup

After import:

```
1. Remove test records:
   ├─ Delete test SharePoint site (/sites/client-management-test)
   └─ Archive test CSV files

2. Archive source data:
   ├─ Back up original CSV files
   ├─ Store in: _________________ (OneDrive/SharePoint/GitHub)
   └─ Label with date and version

3. Document changes:
   ├─ Record final data counts
   ├─ Note any data quality issues found
   ├─ Document any field mappings that diverged from plan
   └─ Update README with migration notes

4. Notify stakeholders:
   ├─ Message Ryne Tudela (Salesforce owner)
   └─ Message Udit Gupta (Client dev manager)
      Subject: "Client data migrated to new CRM"
      Content: Summary of what was imported, any issues, next steps
```

### Deliverables for Pre-Phase
- ✅ Data audit completed
- ✅ Migration strategy chosen
- ✅ CSV files cleaned and validated
- ✅ Test migration successful
- ✅ Production data imported
- ✅ Migration documented

---

## Phase 1: SharePoint Foundation (Week 1)

### Step 1.1: Create SharePoint Site

**URL:** https://admin.microsoft.com → SharePoint Admin Center

```
1. Click "Create site"
2. Choose "Team site"
3. Enter:
   - Name: "Client Management"
   - Alias: "client-management"
4. Click "Next" → "Finish"
```

### Step 1.2: Create Data Lists

Once site is created, go to the site and create 4 lists.

**See docs/sharepoint-setup.md for detailed field definitions**

Quick reference:
```
List 1: Accounts (45 fields total)
List 2: Contacts (15 fields total)
List 3: Campaigns (10 fields total)
List 4: Interactions (8 fields total)
```

### Step 1.3: Configure List Settings

For each list:
```
1. Go to List → Settings
2. Enable "Quick Edit" (Edit in grid view)
3. Enable "Attachments"
4. Set default sort by creation date (newest first)
5. Hide columns you don't need
```

### Step 1.4: Add Sample Data

Use provided CSV files:
- examples/sample-accounts.csv (10 accounts)
- examples/sample-contacts.csv (50 contacts)
- examples/sample-campaigns.csv (5 campaigns)

**How to import:**
```
1. Go to Accounts list
2. Click "Import"
3. Upload sample-accounts.csv
4. Map columns
5. Complete
```

**Verify:**
- ✅ 10 accounts in Accounts list
- ✅ 50 contacts in Contacts list
- ✅ 5 campaigns in Campaigns list

---

## Phase 2: Power Apps UI (Week 2)

### Step 2.1: Create Canvas App

**URL:** https://make.powerapps.com

```
1. Click "+ Create"
2. Select "Canvas app from blank"
3. Name: "ClientManager"
4. Format: "Tablet"
5. Click "Create"
```

### Step 2.2: Build Dashboard Screen

**Screen 1: Home/Dashboard**

Layout:
```
┌──────────────────────────────────┐
│  CLIENT MANAGEMENT DASHBOARD     │
├──────────────────────────────────┤
│  📊 Quick Stats                  │
│  ├─ Total Clients: 45            │
│  ├─ Total Contacts: 320          │
│  ├─ With Azure AD: 280           │
│  └─ Campaigns This Month: 5      │
│                                   │
│  📈 By Segment                   │
│  ├─ Enterprise-T1: 15            │
│  ├─ Enterprise-T2: 12            │
│  ├─ MidMarket-T1: 10             │
│  └─ Startup: 8                   │
│                                   │
│  🔘 [View Accounts] [Contacts]  │
│  🔘 [New Campaign] [Azure Sync]  │
└──────────────────────────────────┘
```

**Components:**
1. Insert → Gallery → Blank vertical (for statistics)
2. Add text labels for each metric
3. Add buttons for navigation

### Step 2.3: Build Accounts Screen

**Screen 2: Accounts List**

```
Gallery showing:
- Company Name (Title)
- Segment
- Tier
- Status
- Buttons: [Edit] [Delete]
```

**Implementation:**
```
1. Insert → Gallery → Vertical (Accounts data source)
2. Fields: Title, Client_Segment, Tier, Status
3. Add Edit/Delete buttons
4. Add search/filter controls
```

### Step 2.4: Build Account Details Screen

**Screen 3: Account Edit Form**

```
Form with fields:
□ Company Name (Text)
□ Client Segment (Dropdown)
□ Tier (Dropdown)
□ Status (Dropdown)
□ Resources Assigned (Multi-select)
□ Access Expiry (Date picker)

Embedded gallery: Related Contacts
├─ Name
├─ Email
├─ Role
└─ Buttons: [Edit] [Delete]

Buttons: [Save] [Cancel] [Add Contact]
```

### Step 2.5: Build Contacts Screen

**Screen 4: Contacts List**

Similar to Accounts screen:
```
Gallery showing:
- Name
- Email
- Account (company)
- Has_Azure_Account (yes/no icon)
- Buttons: [Edit] [Delete]

Filters: [By Account] [With Azure] [Without Azure]
```

### Step 2.6: Build Contact Details Screen

**Screen 5: Contact Edit Form**

```
Form with fields:
□ Contact Name
□ Email
□ Account (lookup dropdown)
□ Role
□ Has_Azure_Account (toggle)
□ Azure User ID (disabled if no account)
□ Contact Type
□ Phone

Buttons: [Save] [Cancel]
```

### Step 2.7: Build Campaign Screen

**Screen 6: Campaign Manager**

```
Campaign creator form:
□ Campaign Name (auto-generated: Month-Segment-Year)
□ Campaign Segment (dropdown)
□ Email Subject
□ Email Body (rich text)
□ Send Date (date picker)
□ Recipient Count (auto, read-only)
□ Status (Draft/Scheduled/Sent)

Preview section: HTML email preview

Buttons: [Preview] [Schedule] [Send Now] [Cancel]
```

### Deliverables for Phase 2
- ✅ Power App with 6 screens
- ✅ All lists connected
- ✅ Form validation working
- ✅ Navigation between screens

---

## Phase 3: Power Automate Workflows (Week 3)

### Step 3.1: Monthly Email Campaign Workflow

**URL:** https://flow.microsoft.com

```
Workflow name: Monthly Email Campaign - Auto
Trigger: Recurrence (1st of month at 8:00 AM)

Actions:
1. Get items (Campaigns list)
   - Filter: Send_Date = today, Status = "Scheduled"

2. For each campaign:
   a. Get items (Contacts list)
      - Filter: Account.Client_Segment = campaign.Campaign_Segment

   b. For each contact:
      i. Send email (Outlook)
         - To: contact.Email
         - Subject: campaign.Email_Subject
         - Body: campaign.Email_Body
         - From: noreply@company.com (shared mailbox)

      ii. Create item (Interactions list)
          - Contact: this contact
          - Campaign: this campaign
          - Type: "Email"
          - Status: "Sent"
          - Timestamp: utcNow()

   c. Update item (Campaigns list)
      - Status: "Sent"
      - Sent_Date: today()
      - Recipients_Count: count of emails sent

3. Send email (to admin)
   - Subject: "Campaign Completed"
   - Body: "X emails sent for campaign Y"
```

### Step 3.2: Azure AD Sync Workflow

```
Workflow name: Azure AD Sync - Manual
Trigger: Manual button (or schedule weekly)

Actions:
1. HTTP action → Get Azure AD groups
   - URL: https://graph.microsoft.com/v1.0/groups
   - Filter: displayName contains 'ClientGroup'
   - Headers: Authorization Bearer token

2. For each group:
   a. Get group members

   b. For each member:
      i. Check if contact exists (Contacts list)
         - Filter by email

      ii. If NOT exists:
          - Create new Contact
          - Email: from Azure AD
          - Azure_User_ID: from Azure AD
          - Has_Azure_Account: YES
          - Active: YES

      iii. If EXISTS:
           - Update Contact
           - Azure_User_ID: (if blank)
           - Has_Azure_Account: YES
           - Last_Sync: now()

3. Send summary email
   - Created: X contacts
   - Updated: Y contacts
   - Deactivated: Z contacts
```

### Step 3.3: Manual Send Workflow

```
Workflow name: Send Campaign - Manual
Trigger: Button (in Power App)

Actions:
1. Get campaign details (from Power App input)

2. Get all contacts for segment
   - Filter: Account.Client_Segment = campaign segment
   - Filter: Active = YES

3. For each contact:
   a. Send email via Outlook
   b. Create Interaction record
   c. Increment counter

4. Update campaign status to "Sent"

5. Notify: Success message to Power App
```

### Step 3.4: Access Expiry Notification

```
Workflow name: Access Expiry Reminder - Auto
Trigger: Daily at 8:00 AM

Actions:
1. Get items (Accounts list)
   - Filter: Access_Expiry = TODAY + 7 days
   - Filter: Status = "Active"

2. For each account:
   a. Send email to account owner
      Subject: "Access expires in 7 days"

   b. Log notification in Interactions
```

### Deliverables for Phase 3
- ✅ Monthly email workflow (automated)
- ✅ Azure AD sync workflow (manual trigger)
- ✅ Manual campaign send (from Power App)
- ✅ Access expiry notifications
- ✅ All workflows tested with sample data

---

## Phase 4: Advanced Integration (Week 4)

### Step 4.1: Excel Dashboard

Create Excel workbook with live data:

**Sheet 1: Summary**
```
Metrics:
- Total Clients: =COUNTA(Accounts)
- Active Clients: =COUNTIF(Accounts[Status], "Active")
- Total Contacts: =COUNTA(Contacts)
- With Azure: =COUNTIF(Contacts[Has_Azure_Account], TRUE)
- Last Sync: =MAX(Contacts[Last_Sync])
```

**Sheet 2: By Segment**
```
Segment | Count | Active | Azure | % Azure
─────────────────────────────────────────
Enterprise-T1 | 15 | 15 | 14 | 93%
Enterprise-T2 | 12 | 11 | 10 | 91%
MidMarket-T1 | 10 | 10 | 8 | 80%
...
```

**Sheet 3: Campaign Performance**
```
Campaign | Sent | Opened | Clicked | Open%
──────────────────────────────────────────
Feb-Enterprise-T1 | 200 | 45 | 12 | 22.5%
Feb-MidMarket-T1 | 100 | 18 | 4 | 18%
...
```

### Step 4.2: Embed Excel in Power App

1. Go to Power App
2. Insert → Excel Online
3. Connect to workbook
4. Select specific sheet/table
5. Configure refresh interval

### Step 4.3: Set Up Access Control

**Define who can edit what:**

SharePoint List Permissions:
```
Accounts list:
- Owners: Can edit all
- Members: Can edit own records
- Visitors: Read-only

Contacts list:
- Owners: Can edit all
- Members: Can edit + create
- Visitors: Read-only

Campaigns list:
- Owners: Can edit all
- Members: Can read only
- Visitors: No access
```

### Step 4.4: Configure Security Groups

**Create Azure AD groups:**
```
CRM-Admins
├─ Can: Create campaigns, manage all data, view reports
├─ Members: PM, Marketing lead

CRM-Users
├─ Can: View/edit own contacts, send campaigns
├─ Members: Team members

CRM-Viewers
├─ Can: View-only dashboard
├─ Members: Executives
```

### Step 4.5: Setup Monitoring

Create Power Automate flow for alerts:
```
Trigger: Weekly check (Sunday 6 AM)

Actions:
1. Check sync status (last 7 days)
2. Check email delivery rate
3. Check access expiry approaching
4. Send admin summary email
```

### Deliverables for Phase 4
- ✅ Excel dashboard created
- ✅ Dashboard embedded in Power App
- ✅ SharePoint permissions configured
- ✅ Azure AD security groups set up
- ✅ Monitoring workflows active

---

## Post-Implementation

### Ongoing Operations

**Daily:**
- Monitor Power Automate runs
- Check for sync errors

**Weekly:**
- Review contact quality
- Update segments as needed
- Check campaign opens

**Monthly:**
- Send automated campaigns
- Review performance metrics
- Plan next month's content

### Maintenance Tasks

**Monthly:**
- Check access expiry dates
- Audit inactive contacts
- Review engagement trends

**Quarterly:**
- Full data audit
- Email template updates
- Process improvements

### Troubleshooting

See docs/troubleshooting.md for:
- Common errors
- Connection issues
- Data sync problems
- Email failures

---

## Success Metrics

✅ Phase 1 Complete: SharePoint lists created and populated
✅ Phase 2 Complete: Power App fully functional
✅ Phase 3 Complete: Automated workflows running
✅ Phase 4 Complete: Dashboard and security configured

**Go-Live Criteria:**
- All workflows tested with production data
- Team trained on system
- Backup/disaster recovery plan in place
- Support process documented
- First monthly campaign successfully sent

---

## Timeline

```
Week 1: SharePoint lists + sample data
Week 2: Power Apps screens + testing
Week 3: Power Automate workflows
Week 4: Excel dashboard + security + go-live prep

Optional Week 5: Fine-tuning and optimization
```

Estimated effort: 40-60 hours (1-1.5 weeks full-time)
