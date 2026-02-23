# System Architecture

## Overview

The Client Management System is built on Microsoft Power Platform with Azure AD integration, designed for <1000 clients with monthly segmented communications.

## Technology Stack

```
Data Layer:
├─ SharePoint Lists (accounts, contacts, campaigns, interactions)
└─ Azure AD (identity, groups, users)

Application Layer:
├─ Power Apps (Canvas App UI)
└─ Power Automate (Workflow orchestration)

Communication Layer:
├─ Outlook/Exchange (Email delivery)
└─ Microsoft Graph API (Azure AD integration)

Analytics Layer:
├─ Excel Online (dashboards)
└─ SharePoint List views (reports)
```

## Data Flow

### 1. Client Onboarding Flow

```
New Client → Create Account in SharePoint
             ├─ Name, Segment, Tier
             ├─ Assign Azure AD group
             └─ Set access expiry

             → Add Contacts
             ├─ Email addresses
             ├─ Link to Account
             └─ Set roles (Admin/User/Viewer)

             → Azure AD Sync (automatic)
             ├─ Pull from ClientGroup-Enterprise-T1
             ├─ Create/update Contacts
             └─ Set Has_Azure_Account flag
```

### 2. Monthly Campaign Flow

```
Day 1: Admin creates Campaign
├─ Select segment (Enterprise-T1)
├─ Write email subject/body
├─ Schedule for send date
└─ Status: Draft

Day 1, 8 AM: Power Automate triggers
├─ Get Campaign where Status = "Scheduled"
├─ Get all Contacts for that segment
├─ For each Contact:
│  ├─ Send email via Outlook
│  ├─ Create Interaction record
│  └─ Track: Sent, Open, Click
└─ Update Campaign Status to "Sent"

Post-send: Tracking
├─ Monitor opens/clicks (manual)
├─ Update Interaction records
└─ Analyze performance
```

### 3. Access Control Flow

```
Client Company → Account record in SharePoint
                 ├─ Tier: Enterprise-T1
                 ├─ Resources_Assigned: Dashboards, Files, Website
                 └─ Azure_AD_Group: ClientGroup-Enterprise-Tier1

                 ↓

Azure AD Group (ClientGroup-Enterprise-Tier1)
├─ Contains all users from this client
├─ Assigned RBAC roles:
│  ├─ Reader (Power BI dashboards)
│  ├─ Storage Blob Data Reader (File share)
│  └─ Website Admin (custom portal)
└─ Auto-expires at Account.Access_Expiry date

                 ↓

Client Users → Can access:
├─ Power BI dashboards (via RBAC)
├─ Azure File Share (via RBAC)
└─ Custom portal (via Azure App Service)
```

## Data Model

### Accounts List
```
{
  id: GUID,
  Title: "Acme Corp",
  Client_Segment: "Enterprise-T1",
  Azure_AD_Group: "ClientGroup-Enterprise-Tier1",
  Tier: "Enterprise",
  Status: "Active" | "Inactive" | "Trial",
  Resources_Assigned: ["Dashboards", "Files", "Website"],
  Access_Expiry: Date,
  Contact_Count: Integer (calculated),
  Last_Sync: DateTime,
  Notes: RichText
}
```

### Contacts List
```
{
  id: GUID,
  Title: "John Smith",
  Email: "john@acmecorp.com",
  Account: LookupRef (to Accounts),
  Role: "Admin" | "User" | "Viewer",
  Azure_User_ID: "a1b2c3d4-...",
  Has_Azure_Account: Boolean,
  Contact_Type: "Employee" | "Contractor" | "Partner" | "Other",
  Can_Access_Portal: Boolean,
  Last_Contacted: Date,
  Active: Boolean,
  Preferred_Language: "EN" | "ES" | "FR",
  Phone: String
}
```

### Campaigns List
```
{
  id: GUID,
  Title: "Feb-2026-Enterprise-T1",
  Campaign_Segment: "Enterprise-T1",
  Email_Subject: "Your February Insights",
  Email_Body: HtmlContent,
  Send_Date: Date,
  Status: "Draft" | "Scheduled" | "Sent" | "Completed",
  Recipients_Count: Integer,
  Sent_Date: DateTime,
  Opened_Count: Integer,
  Clicked_Count: Integer,
  Created_By: String,
  Notes: String
}
```

### Interactions List
```
{
  id: GUID,
  Title: "Email-2026-02-01",
  Contact: LookupRef (to Contacts),
  Campaign: LookupRef (to Campaigns),
  Type: "Email" | "Call" | "Meeting" | "Note",
  Status: "Sent" | "Opened" | "Clicked" | "No Action",
  Timestamp: DateTime,
  Notes: String,
  Created_Date: DateTime
}
```

## Integration Points

### 1. Azure AD Integration

**Direction:** Azure AD → SharePoint

```
Sync Frequency: Weekly (manual trigger or scheduled)
Endpoint: Microsoft Graph API
├─ GET /groups (filter: ClientGroup-*)
├─ GET /groups/{id}/members
└─ POST/PATCH /contacts

On Sync:
├─ New contacts in Azure AD → Create in SharePoint
├─ Existing contacts updated → Update in SharePoint
├─ Removed from Azure AD → Deactivate in SharePoint
└─ Log all changes in Interactions list
```

### 2. Email Delivery

**Direction:** Power Automate → Outlook

```
Service: Microsoft Outlook
From: noreply@company.com (shared mailbox)
To: Contact.Email
Method: Power Automate "Send an email (V2)" action

Tracking:
├─ Sent: Logged in Interactions.Status = "Sent"
├─ Opened: Manual tracking via pixel/link clicks
├─ Clicked: Manual tracking via utm parameters
└─ Bounced: Review undeliverable receipts
```

### 3. Reporting & Analytics

**Direction:** SharePoint → Excel → Power App

```
Data Source: SharePoint Lists
Transform: Excel formulas
Display: Power App + Excel Online

Key Reports:
├─ Accounts by segment (gallery)
├─ Contact engagement (interactions)
├─ Campaign performance (metrics)
├─ Access expiry timeline (alerts)
└─ Segment health (dashboards)
```

## Security Architecture

### Access Control Layers

**Layer 1: Azure AD Groups**
```
ClientGroup-Enterprise-Tier1
├─ Contains: All users from Enterprise-Tier1 accounts
├─ RBAC: Reader on /subscriptions/*/resourceGroups/*
└─ Resources: Power BI dashboards, File shares
```

**Layer 2: SharePoint List Permissions**
```
Accounts List:
├─ Owners (CRM-Admins): Edit all
├─ Members (CRM-Users): Edit own segment
└─ Visitors (CRM-Viewers): Read-only

Contacts List:
├─ Owners: Edit all
├─ Members: Edit, create, delete
└─ Visitors: Read-only

Campaigns List:
├─ Owners: Create, edit, send
├─ Members: Create, edit own
└─ Visitors: No access

Interactions List:
├─ Owners: Edit all
└─ Members: View own, create
```

**Layer 3: Power App Security**

```
Dashboard Screen: All authenticated users
Accounts Screen: CRM-Users or higher
Contacts Screen: CRM-Users or higher
Campaigns Screen: CRM-Admins only
```

## Deployment Architecture

```
Development:
└─ SharePoint site: /sites/client-management-dev
   ├─ Lists (dev versions)
   ├─ Power App (dev version)
   └─ Power Automate (test flows)

Staging:
└─ SharePoint site: /sites/client-management-test
   ├─ Copy of production data (sanitized)
   ├─ Power App (test version)
   └─ Power Automate (staging flows)

Production:
└─ SharePoint site: /sites/client-management
   ├─ Live lists
   ├─ Power App (published)
   └─ Power Automate (active workflows)
```

## Scalability Considerations

### Current Setup (<1000 clients)
- ✅ SharePoint Lists: Fast (queries <100ms)
- ✅ Power Apps: Responsive (<2s load)
- ✅ Power Automate: 600 runs/day limit (sufficient)
- ✅ Excel: <10,000 rows (no issues)

### Future Scaling (>5000 clients)
- 📌 Consider: Azure SQL Database instead of SharePoint
- 📌 Consider: Dataverse instead of lists
- 📌 Consider: Dynamics 365 Sales (enterprise option)
- 📌 Archive: Historical campaigns to separate list

## Disaster Recovery

### Data Backup
```
Frequency: Daily (automatic via SharePoint versioning)
Method: SharePoint List backups + Excel snapshots
Retention: 30 days (SharePoint default)
Recovery: Restore from version history
```

### Workflow Backup
```
Frequency: Before major changes
Method: Export Power Automate flows as .zip
Storage: GitHub repo
Version: git-tagged releases
```

### Testing Recovery
```
Quarterly:
├─ Restore test data to dev site
├─ Verify all workflows run correctly
├─ Validate data integrity
└─ Document any issues
```

## Monitoring & Alerts

### Key Metrics
```
Real-time:
├─ Power Automate run success rate
├─ Average run duration
├─ Failed runs count

Daily:
├─ Azure AD sync completion
├─ Email delivery rate
├─ New contacts added

Weekly:
├─ Campaign open rate
├─ Click-through rate
├─ Contact engagement score

Monthly:
├─ Access expiry approaching
├─ Inactive contacts
├─ Segment health score
```

### Alert Triggers
```
Critical:
├─ Workflow failed 3+ times
├─ Sync not completed in 24h
└─ Email bounces >5%

Warning:
├─ Workflow ran slow (>5min)
├─ Campaign open rate <15%
└─ Contacts with missing data
```

## Cost Optimization

```
Current Stack (<1000 users):
├─ SharePoint: Included in M365
├─ Power Apps: $15-20/user/month
├─ Power Automate: $5-15/month
├─ Outlook: Included
└─ Total: $20-35/user/month

Optimization Options:
├─ Consolidate to fewer admin accounts
├─ Use free tier (Power Apps, limited)
├─ Archive old campaigns (reduce list size)
└─ Compress email storage (delete old content)
```

## Compliance & Governance

### Data Residency
- All data in Microsoft 365 (tenant-specified region)
- No third-party data transfers
- GDPR compliant (with DPA)

### Audit Trail
- SharePoint list versioning (automatic)
- Power Automate run history (30 days)
- Azure AD sign-in logs (30 days)
- Contact modification tracking (list auditing)

### Access Revocation
- Automatic: Account.Access_Expiry date triggers removal
- Manual: Remove from Azure AD group
- System: Disable Contact.Active flag
- Verification: Weekly audit report
