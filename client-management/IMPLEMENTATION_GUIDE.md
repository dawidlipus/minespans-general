# Implementation Guide

Complete phase-by-phase implementation of the Client Management System.

## Table of Contents

1. [Phase 1: SharePoint Foundation](#phase-1-sharepoint-foundation-week-1)
2. [Phase 2: Power Apps UI](#phase-2-power-apps-ui-week-2)
3. [Phase 3: Power Automate Workflows](#phase-3-power-automate-workflows-week-3)
4. [Phase 4: Advanced Integration](#phase-4-advanced-integration-week-4)

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
