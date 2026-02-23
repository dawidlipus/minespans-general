# Client Management System

A lightweight CRM system for managing <1000 clients with segmented communication capabilities, built entirely on Microsoft Power Platform and Azure AD.

## Overview

This project provides a complete client management solution using:
- **SharePoint Lists** for data storage
- **Power Apps** for user interface
- **Power Automate** for workflow automation
- **Azure AD** for identity and access management
- **Outlook** for email communications

## Key Features

✅ **Account Management** - Track client companies and their details
✅ **Contact Management** - Store contacts with/without Azure AD accounts
✅ **Segmentation** - Organize clients into 10 customizable segments
✅ **Monthly Campaigns** - Send segmented emails to different client groups
✅ **Azure AD Sync** - Auto-sync contacts from Azure AD groups
✅ **Access Control** - Manage who can access dashboards, files, and website
✅ **Email Tracking** - Log all communications and interactions
✅ **Dashboard** - View metrics and campaign performance

## Architecture

```
Azure AD (Identity)
    ↓
SharePoint Lists (Data Storage)
    ├─ Accounts
    ├─ Contacts
    ├─ Campaigns
    └─ Interactions
    ↓
Power Apps (UI)
    ├─ Dashboard
    ├─ Account Manager
    ├─ Contact Manager
    └─ Campaign Creator
    ↓
Power Automate (Workflows)
    ├─ Monthly Email Campaign
    ├─ Azure AD Sync
    └─ Manual Send
    ↓
Outlook (Email)
```

## Quick Start

See [QUICKSTART.md](./QUICKSTART.md) for 15-minute setup guide.

## Full Documentation

- [QUICKSTART.md](./QUICKSTART.md) - 15-minute getting started
- [IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md) - Detailed phase-by-phase setup
- [ARCHITECTURE.md](./docs/architecture.md) - System design and data flow
- [SHAREPOINT_SETUP.md](./docs/sharepoint-setup.md) - List configuration
- [POWER_APPS_GUIDE.md](./docs/power-apps-guide.md) - UI/App setup
- [POWER_AUTOMATE_GUIDE.md](./docs/power-automate-guide.md) - Workflow setup
- [EXCEL_DASHBOARD.md](./docs/excel-dashboard.md) - Reporting and dashboards

## Project Structure

```
client-management/
├── README.md
├── QUICKSTART.md
├── IMPLEMENTATION_GUIDE.md
├── docs/
│   ├── architecture.md
│   ├── sharepoint-setup.md
│   ├── power-apps-guide.md
│   ├── power-automate-guide.md
│   └── excel-dashboard.md
├── templates/
│   ├── sharepoint-lists-schema.md
│   ├── power-app-screens.md
│   ├── power-automate-workflows.md
│   └── email-templates.html
├── scripts/
│   ├── setup.ps1
│   └── azure-ad-sync.py
└── examples/
    ├── sample-accounts.csv
    ├── sample-contacts.csv
    └── sample-campaigns.csv
```

## Cost

**Monthly:** ~$15-25/user/month
**Annual:** ~$180-300/user (vs $1,000+ for Dynamics 365)

Includes: Power Apps, Power Automate, SharePoint, Azure AD, Outlook

## System Requirements

- Microsoft 365 subscription (Office 365)
- Azure AD tenant
- SharePoint Online
- Power Apps licenses (or free tier)
- Power Automate (included or $5-15/month)

## Use Cases

**Enterprise:** Multi-tier clients, premium features, full portal access
**Mid-Market:** Standard clients, core features, limited portal
**Startup:** Trial clients, onboarding content, no portal
**Trial:** New clients, preview content, time-limited access
**VIP:** Premium clients, white-glove service, custom resources

## Implementation Timeline

- **Phase 1:** SharePoint setup (1 week)
- **Phase 2:** Power Apps UI (1 week)
- **Phase 3:** Power Automate workflows (1 week)
- **Phase 4:** Email & Reporting (1 week)

**Total:** 4 weeks to full production

## Monitoring & Maintenance

**Weekly:**
- Review campaign performance
- Monitor sync status
- Check for inactive contacts

**Monthly:**
- Run monthly email campaigns (automated)
- Review access expiry dates
- Update client segments as needed

**Quarterly:**
- Audit contact data quality
- Review email templates
- Analyze engagement trends

## Support & Troubleshooting

See [IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md) for common issues and solutions.

## License

Private - Internal Use Only

## Author

Created for MineSpans Client Management
Generated with Claude Code
