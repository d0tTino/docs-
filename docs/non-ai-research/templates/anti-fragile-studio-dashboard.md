---
title: "Anti-Fragile Studio Dashboard Template"
tags:
  - template
  - workflow
  - studio-management
project: docs-hub
updated: 2025-10-02
---

# Anti-Fragile Studio Dashboard Template

Use this board to externalise your commission pipeline and keep weekly maintenance lightweight. The structure below mirrors the workflow described in the playbook and can be recreated in any kanban-capable tool.

## Quick Import or Recreation

- **Notion:** Create a new board database, copy the tables below, and paste them into Notion. It will convert the first table into database groups (columns) and the property tables into database properties. Duplicate the sample cards as templates.
- **Trello:** Create a new board, add the lists in the order shown, and copy the sample cards into each list. Apply labels, due dates, and checklists to match the property guide.
- **Other tools:** Recreate each column name, limit, and property, then copy the sample card titles and checklists as defaults for new cards.

## Column Blueprint

| Column | Purpose | Suggested WIP Limit | Default Checklists & Automations | Sample Card Title |
| --- | --- | --- | --- | --- |
| **Intake Queue** | Capture new inquiries created automatically from forms or emails before you triage them. | Unlimited (inbox) | Checklist: `Qualify lead → Send intake confirmation → Schedule discovery call`. Auto-archive cards older than 30 days with no response. | `Inquire: Indie Game NPC Portraits` |
| **Simmering** | High-potential leads awaiting confirmation, deposit, or scheduling. | 5 | Checklist: `Send proposal → Follow up on deposit → Prep kickoff doc`. Reminder 48 hours before deposit due. | `Proposal: Liminal Tarot Cover` |
| **Active Focus** | The single project receiving deep work time right now. | 1 | Checklist: `Current milestone → Next visible step → Client update scheduled`. Block focus sessions on calendar when card enters column. | `Production: Album Art Variant` |
| **Client Reply Needed** | Work paused because you are waiting on client feedback, approvals, or assets. | 3 | Checklist: `Log request date → Send follow-up reminder (48h) → Escalate if no response`. Auto-remind clients via email integration. | `Awaiting: Revision Notes for Stream Overlay` |
| **Cooling Down** | Project delivered and pending final invoice, testimonial request, or archival tasks. | 3 | Checklist: `Send wrap-up email → Issue final invoice → Request testimonial → Archive files`. Trigger thank-you email template. | `Delivery: Merch Line Illustrations` |
| **Archive & Reference** | Closed projects stored for historical context, testimonials, and reuse. | Unlimited | Checklist: `Tag with lessons learned → Store assets link → Note cognitive load score`. Export key data quarterly for portfolio updates. | `Archive: Convention Poster Series` |

## Card Property Guide

| Property | Type / Format | Usage |
| --- | --- | --- |
| **Energy Rating** | Select (1 = Low, 2 = Medium, 3 = High) | Schedule high-energy cards during peak cognitive windows. |
| **Next Visible Step** | Text | Write the single action required to move the card forward. |
| **Status Note** | Text or comment | Log date-stamped communications or blockers. |
| **Risk Flags** | Multi-select labels (`scope risk`, `payment risk`, `RSD trigger`) | Flag cards that need boundary scripts or pricing adjustments. |
| **Due / Follow-up Date** | Date | Drives calendar blocks and automated reminders. |
| **Cognitive Load Multiplier** | Number | Reference the pricing calculator to track actual vs. projected load. |
| **Assets & Links** | Files / URLs | Store briefs, mood boards, and delivery folders for fast retrieval. |

## Sample Card Templates

- **Focus Project Template (Active Focus)**
  - Title: `Production: [Project Name]`
  - Energy Rating: 3
  - Next Visible Step: `Render lighting pass`
  - Checklist: `Prep workspace → Execute milestone task → Log progress → Draft client update`
  - Labels: `scope risk` if the client is prone to scope creep
- **Waiting on Client Template (Client Reply Needed)**
  - Title: `Awaiting: [Feedback/Asset]`
  - Energy Rating: 1
  - Status Note: `Sent reminder on {{date}}`
  - Checklist: `Log request → Follow up in 2 days → Escalate in 5 days`
- **Wrap-Up Template (Cooling Down)**
  - Title: `Delivery: [Project Name]`
  - Energy Rating: 2
  - Checklist: `Send final files → Issue invoice → Request testimonial → Archive assets`
  - Due Date: Final invoice date

## Weekly Maintenance Blocks

Use two recurring sessions to keep the dashboard trustworthy:

### Monday Weekly Review (45 minutes)
1. Process the **Intake Queue** and move viable leads into **Simmering** with clear next steps.
2. Re-assess energy ratings and ensure only one card sits in **Active Focus**.
3. Update due dates, follow-up reminders, and risk flags so the week’s commitments are visible.
4. Plan focus blocks in your calendar that match the `Next Visible Step` field for each active card.

### Friday Admin Sweep (30 minutes)
1. Advance completed work into **Cooling Down** and trigger wrap-up checklists.
2. Reconcile invoices, deposits, and expense receipts tied to cards finishing this week.
3. Send or schedule client update emails summarising progress and outstanding needs.
4. Archive cards that are fully closed and note any cognitive load lessons learned in the card properties.

Keep these blocks booked on your calendar as non-negotiable maintenance appointments so the board remains a reliable control centre.
