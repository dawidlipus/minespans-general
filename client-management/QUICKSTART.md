# Quick Start Guide (15 minutes)

Get a basic client management system running in 15 minutes.

## Prerequisites

- ✅ Microsoft 365 subscription
- ✅ Azure AD tenant
- ✅ SharePoint Online access
- ✅ Power Apps/Power Automate access

## Step 1: Create SharePoint Site (3 minutes)

1. Go to **SharePoint Online**
2. Click **+ Create Site**
3. Enter:
   - **Site name:** "Client Management"
   - **Site address:** client-management
   - **Description:** CRM for client accounts and contacts
4. Click **Create**

## Step 2: Create SharePoint Lists (5 minutes)

Go to your new SharePoint site and create 4 lists:

### List 1: Accounts
```
Click + New → List
Name: Accounts

Columns to add:
- Title (default, rename to "Company Name")
- Client_Segment (Choice: Enterprise-T1, Enterprise-T2, MidMarket-T1, Startup, Trial)
- Tier (Choice: Enterprise, MidMarket, Startup, Trial)
- Status (Choice: Active, Inactive, Trial)
- Access_Expiry (Date)
```

### List 2: Contacts
```
Click + New → List
Name: Contacts

Columns to add:
- Title (default, rename to "Contact Name")
- Email (Text)
- Account (Lookup → Accounts)
- Has_Azure_Account (Yes/No)
- Role (Choice: Admin, User, Viewer)
- Contact_Type (Choice: Employee, Contractor, Partner, Other)
```

### List 3: Campaigns
```
Click + New → List
Name: Campaigns

Columns to add:
- Title (default, rename to "Campaign Name")
- Campaign_Segment (Choice: Enterprise-T1, Enterprise-T2, MidMarket-T1, Startup, Trial)
- Email_Subject (Text)
- Email_Body (Rich Text)
- Send_Date (Date)
- Status (Choice: Draft, Scheduled, Sent)
```

### List 4: Interactions
```
Click + New → List
Name: Interactions

Columns to add:
- Title (default, rename to "Description")
- Contact (Lookup → Contacts)
- Campaign (Lookup → Campaigns)
- Type (Choice: Email, Call, Meeting, Note)
- Status (Choice: Sent, Opened, Clicked, No Action)
- Timestamp (DateTime)
```

## Step 3: Add Sample Data (3 minutes)

### Add sample account
- Go to **Accounts** list
- Click **+ New**
- **Company Name:** Acme Corp
- **Client_Segment:** Enterprise-T1
- **Tier:** Enterprise
- **Status:** Active
- **Access_Expiry:** 2026-12-31
- Click **Save**

### Add sample contact
- Go to **Contacts** list
- Click **+ New**
- **Contact Name:** John Smith
- **Email:** john@acmecorp.com
- **Account:** Acme Corp
- **Has_Azure_Account:** Yes
- **Role:** Admin
- **Contact_Type:** Employee
- Click **Save**

## Step 4: Create Power App (3 minutes)

1. Go to **Power Apps** (powerapps.microsoft.com)
2. Click **+ Create**
3. Select **Canvas App from Blank**
4. **App name:** ClientManager
5. **Format:** Tablet
6. Click **Create**

### Add accounts screen
```
Screen layout:
┌─────────────────────┐
│ Accounts            │
├─────────────────────┤
│ [Gallery showing    │
│  company names,     │
│  segments, status]  │
│                     │
│ [+ New Account]     │
└─────────────────────┘
```

**Quick setup:**
1. Insert → Gallery → Blank vertical
2. Set data source: Accounts list
3. Add fields: Title, Client_Segment, Status
4. Add button for new account

## Step 5: Test Email Flow (Bonus - 5 minutes if quick)

1. Go to **Power Automate** (flow.microsoft.com)
2. Click **+ Create** → **Cloud flow** → **Automated**
3. **Flow name:** Test Email
4. **Trigger:** Manual button
5. Add action: **Send an email (V2)**
6. Set to your email
7. Test by clicking button

---

## What's Next?

✅ Now you have:
- Basic data structure (4 lists)
- Sample data loaded
- Power App UI started
- Email capability tested

🎯 Next steps (see IMPLEMENTATION_GUIDE.md):
- Finish Power App screens
- Create Power Automate workflows
- Set up Azure AD sync
- Build dashboard

---

## Troubleshooting

**"Can't create list"**
- Check SharePoint permissions
- Ensure you have Editor role

**"Power Apps won't load"**
- Clear browser cache
- Try different browser
- Check Power Apps license

**"Email test failed"**
- Verify Outlook email address
- Check Power Automate connector is authorized
- Try "Send Email" action instead

---

## Next: Full Implementation

Read [IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md) for complete setup including:
- Power App screens (dashboard, forms, views)
- Power Automate workflows (monthly emails, Azure sync)
- Excel dashboards
- Full integration with Azure AD

**Estimated time:** 4 weeks for production ready system
