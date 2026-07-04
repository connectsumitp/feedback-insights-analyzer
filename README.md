# Feedback Insights Analyzer

> A product-feedback intelligence dashboard that turns unstructured customer feedback into sentiment trends, recurring issue themes, priority scores, and recommended product actions.

**Live app:** [analyzer-feedback.streamlit.app](https://analyzer-feedback.streamlit.app/)  
**Repository:** [connectsumitp/feedback-insights-analyzer](https://github.com/connectsumitp/feedback-insights-analyzer)  
**Built with:** Python · Streamlit · Pandas · Plotly · VADER Sentiment

---

## Overview

Customer feedback is often spread across app reviews, surveys, support tickets, CRM notes, sales calls, and NPS responses. The volume is valuable, but it is difficult for Product, Support, and Customer Success teams to turn hundreds of comments into clear decisions.

**Feedback Insights Analyzer** is a lightweight dashboard designed to make that workflow easier. It accepts feedback data in CSV format, classifies sentiment, detects recurring issue themes, highlights the most urgent themes, and surfaces representative customer comments for investigation.

The project is built as a product-thinking portfolio MVP: it combines customer discovery, prioritisation, analytics, and an interactive internal-tool experience.

> The bundled sample dataset is synthetic and fictional. It does not include real IndiaMART or customer data.

---

## Problem Statement

Teams often prioritise customer issues through manual spreadsheet review, isolated escalations, or the loudest complaint. This approach creates a few predictable gaps:

- Important themes stay hidden inside large volumes of unstructured feedback.
- Product decisions can be driven by anecdotes instead of patterns.
- Support, Product, and Sales teams may each see only part of the customer problem.
- PMs spend excessive time manually tagging and summarising comments.
- Emerging problems are detected after they have already become widespread.
- Leadership lacks a concise, evidence-backed Voice of Customer view.

### Product Opportunity

Create a transparent, easy-to-use feedback-analysis workflow that helps teams move from:

```text
Raw customer comments
        ↓
Sentiment and theme detection
        ↓
Prioritised problem areas
        ↓
Representative verbatims
        ↓
Product investigation and action
```

---

## Target Users

| User | Primary Job To Be Done | How the Product Helps |
|---|---|---|
| Product Manager | Identify customer pain points and decide what to investigate first | Ranks themes by volume and negative sentiment; enables verbatim drill-down |
| Support Lead | Understand recurring contact reasons and operational gaps | Highlights support-related complaint patterns and potential SLA issues |
| Customer Success Team | Monitor dissatisfaction across customer segments | Filters feedback by user type, sentiment, theme, and date |
| Growth / Retention Team | Find friction affecting activation, conversion, and retention | Surfaces onboarding, pricing, payment, search, and product-experience issues |
| Leadership | Understand customer health without reading hundreds of comments | Provides a concise overview of sentiment, top issues, and recommended actions |

---

## Key Features

### 1. CSV Upload and Built-in Sample Dataset

Users can either explore the included synthetic marketplace dataset or upload their own feedback CSV.

The only required input column is:

```text
feedback
```

Recommended optional columns:

```text
feedback_id
date
user_type
rating
```

This makes the app useful for feedback exported from app reviews, CSAT forms, support tools, CRM systems, survey platforms, or spreadsheets.

---

### 2. Sentiment Classification

Each feedback item is classified into:

- **Positive**
- **Neutral**
- **Negative**

The MVP uses VADER sentiment analysis with lightweight safeguards for common product-feedback phrases such as:

```text
payment failed
support not responding
not working
irrelevant leads
easy to use
great experience
```

This gives teams a quick read of overall customer sentiment and helps them identify whether complaint volume is changing over time.

---

### 3. Product Theme Detection

Each feedback item is tagged with one or more product themes using a transparent, rule-based taxonomy.

Current themes include:

```text
Payment
Support
Lead Quality
Onboarding
App & Technical Bugs
Pricing & Subscription
Delivery & Fulfillment
Search & Discovery
Account & Profile
Other
```

A single comment can map to multiple themes.

For example:

> “My payment failed and customer support has not responded for two days.”

is tagged as:

```text
Payment
Support
```

---

### 4. Executive Dashboard

The dashboard provides a quick snapshot of feedback health:

- Total feedback volume
- Negative-feedback rate
- Average rating
- Highest-priority issue theme

This helps a PM start with the key question:

> What is the most important customer problem to investigate right now?

---

### 5. Sentiment and Trend Analysis

The dashboard visualises:

- Overall sentiment split
- Weekly feedback trends
- Changes in feedback by sentiment
- Issue-level feedback volume
- Negative sentiment by issue theme

This can help teams identify whether an issue is isolated, stable, improving, or worsening after a release.

---

### 6. Issue Priority Score

Each product theme receives a priority score based on two signals:

```text
Priority Score =
45% Relative Feedback Volume
+
55% Negative Feedback Rate
```

A higher score indicates an issue that is both commonly reported and strongly negative.

This is a **triage mechanism**, not an automatic roadmap decision. A production-ready prioritisation model should also consider:

- Customer segment and customer value
- Revenue at risk
- Churn correlation
- Complaint severity
- Frequency of repeat contacts
- Support-contact rate
- Strategic importance
- Confidence in the data
- Engineering effort and feasibility

---

### 7. Action Recommendations

For the highest-priority themes, the product suggests a practical next step for investigation.

| Theme | Recommended Next Action |
|---|---|
| Payment | Review payment-failure codes, retry flows, alternate payment methods, and refund-status communication |
| Support | Audit first-response SLA, backlog ageing, escalation paths, and self-service help content |
| Lead Quality | Review matching logic, lead-source quality, buyer qualification, and seller feedback loops |
| Onboarding | Instrument onboarding steps and investigate the highest-drop-off point |
| App & Technical Bugs | Segment issues by app version, device, OS, error code, and reproducibility |
| Search & Discovery | Review search relevance, zero-result queries, filtering behaviour, and catalogue completeness |
| Pricing & Subscription | Test clearer plan comparison, value communication, renewal messaging, and cancellation reasons |

The product intentionally frames recommendations as a starting point for discovery—not as a substitute for validating root cause.

---

### 8. Feedback Drill-Down

Dashboards should not replace customer context. The drill-down view allows users to read the actual feedback behind each theme and filter by:

- User type
- Sentiment
- Issue theme
- Date range

This helps Product Managers review representative verbatims before creating a problem statement, writing a PRD, or escalating an issue.

---

### 9. Exportable Insights

Users can download their filtered feedback with generated insights as CSV.

The export includes:

```text
Original feedback
Sentiment label
Sentiment score
Detected themes
Rating
User type
Date
```

This allows teams to continue analysing data in Excel, Google Sheets, Power BI, Tableau, SQL, or their existing reporting workflow.

---

## Example Product Questions

The dashboard can help answer questions such as:

- Which issue has the highest combination of volume and negative sentiment?
- Are payment complaints increasing week over week?
- Do buyers and sellers report different types of friction?
- Are support complaints about slow response, unresolved cases, or a specific workflow?
- Is poor lead quality a matching issue, a targeting issue, or an expectation-setting issue?
- Which customer comments should a PM read before defining a problem statement?
- Which product issue should be discussed in the next product-review meeting?

---

## Example PM Use Case

### Scenario

A marketplace Product Manager sees that paid sellers are repeatedly complaining about irrelevant leads.

The dashboard shows:

```text
Theme: Lead Quality
Feedback Volume: High
Negative Feedback Rate: High
Priority Score: High
```

### Recommended Investigation Flow

1. Read representative seller feedback to understand the exact complaint language.
2. Segment feedback by:
   - Product category
   - Geography
   - Membership plan
   - Lead source
   - Lead age
   - Seller tenure
3. Compare complaints with operational and product metrics:
   - Lead-contact rate
   - Seller response rate
   - Buyer intent signals
   - Conversion from enquiry to order
   - Seller renewal rate
   - Paid seller retention
4. Form hypotheses:
   - Buyer requirements are low intent.
   - Category matching is too broad.
   - The lead-qualification flow is weak.
   - Sellers lack filtering or quality-control options.
5. Run experiments:
   - Add buyer-intent questions before enquiry submission.
   - Improve category and location matching.
   - Add seller-side lead filters.
   - Introduce a “not relevant” feedback reason.
6. Measure impact:
   - Relevant-lead rate
   - Seller response rate
   - Seller satisfaction
   - Renewal rate
   - Retention of paid sellers

---

## Metrics Framework

### Adoption Metrics

- Number of feedback files analysed per week
- Weekly active internal users
- Number of Product, Support, or CX teams using the tool
- Number of CSV exports
- Number of recurring Voice of Customer reports generated

### Analysis Quality Metrics

- Sentiment-classification precision on a manually reviewed sample
- Theme-classification precision and recall
- Percentage of feedback grouped as `Other`
- Percentage of comments successfully tagged with more than one valid theme
- Time required to produce a weekly Voice of Customer report

### Product and Business Impact Metrics

- Reduction in manual feedback-review time
- Reduction in time to identify emerging issues
- Improvement in support-contact rate
- Improvement in negative-feedback rate after a release
- Change in CSAT or NPS
- Reduction in churn related to recurring friction points
- Resolution rate for high-priority customer problems

---

## Technical Architecture

```text
CSV Upload / Sample Dataset
            ↓
Input Validation and Column Normalisation
            ↓
Sentiment Classification (VADER + product-feedback safeguards)
            ↓
Rule-Based Theme Detection
            ↓
Theme-Level Aggregation
            ↓
Priority Scoring and Recommendations
            ↓
Interactive Streamlit Dashboard and CSV Export
```

---

## Technology Stack

| Layer | Technology |
|---|---|
| Programming Language | Python |
| Dashboard Framework | Streamlit |
| Data Processing | Pandas |
| Visualisation | Plotly |
| Sentiment Analysis | VADER Sentiment |
| Theme Detection | Regex-based rule taxonomy |
| Testing | Python smoke tests |
| Deployment | Streamlit Community Cloud |

---

## Project Structure

```text
feedback-insights-analyzer/
│
├── app.py
│   └── Main Streamlit dashboard application
│
├── utils.py
│   └── Sentiment classification, theme detection, input validation,
│       issue scoring, and recommendation logic
│
├── requirements.txt
│   └── Python dependencies
│
├── README.md
│   └── Product overview, setup instructions, and product case study
│
├── .gitignore
│   └── Prevents virtual environments, secrets, and temporary files from being uploaded
│
├── data/
│   └── sample_marketplace_feedback.csv
│
├── docs/
│   └── product-case-study.md
│
└── tests/
    └── test_utils.py
```

---

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/connectsumitp/feedback-insights-analyzer.git
cd feedback-insights-analyzer
```

### 2. Create a virtual environment

```bash
py -m venv .venv
```

### 3. Activate the environment

**Windows PowerShell**

```bash
.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
py -m pip install -r requirements.txt
```

### 5. Start the app

```bash
py -m streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

## Input CSV Format

### Minimum Required Format

```csv
feedback
"Payment failed and I could not renew my subscription"
"Support responded quickly and solved my profile issue"
"Search results are not relevant for my product category"
```

### Recommended Format

```csv
feedback_id,date,user_type,rating,feedback
1,2026-06-01,Seller,1,"I cannot complete payment for my premium plan"
2,2026-06-01,Buyer,5,"Easy to find reliable suppliers"
3,2026-06-02,Seller,2,"Leads are irrelevant and support is not responding"
```

---

## Product Decisions and Trade-Offs

### Rule-Based Themes vs. LLM-Based Theme Discovery

The MVP uses a rule-based taxonomy because it is:

- Transparent and easy to explain
- Fast and low-cost
- Easy to test and debug
- Suitable for a portfolio MVP
- Easier for Product and Support teams to validate

A more advanced version could use an LLM to:

- Detect emerging themes automatically
- Cluster semantically similar feedback
- Summarise long ticket threads
- Generate weekly Voice of Customer reports
- Identify themes not covered by the current taxonomy
- Suggest root-cause hypotheses and experiment ideas

### CSV Upload vs. Direct Integrations

CSV upload was selected for the MVP because it is simple to test with existing exports.

Potential future integrations include:

```text
Zendesk
Intercom
Freshdesk
HubSpot
Google Play Store reviews
Apple App Store reviews
Salesforce
Google Forms
Typeform
WhatsApp Business exports
```

### Priority Score vs. True Business Impact

The current score combines feedback volume and negative sentiment. It is useful for early triage but should not make product decisions on its own.

A more mature scoring model would include:

```text
Revenue impact
Customer segment
Customer lifetime value
Churn risk
Issue severity
Frequency
Strategic importance
Engineering effort
Confidence level
```

---

## Roadmap

### Phase 1 — Improve Analysis Quality

- Configurable theme taxonomy
- Custom keyword lists by business domain
- User correction of sentiment and theme labels
- Sentiment-confidence review queue
- Hindi and multilingual feedback support
- Duplicate feedback detection

### Phase 2 — Add AI Capabilities

- LLM-powered feedback summarisation
- Automated weekly Voice of Customer report
- Emerging-theme detection
- Root-cause hypothesis generation
- Suggested experiment ideas
- PRD starter drafts for high-priority issues

### Phase 3 — Add Integrations

- Zendesk and Intercom integrations
- Google Play Store and App Store review ingestion
- HubSpot CRM feedback ingestion
- Slack alerts for complaint spikes
- Jira ticket creation for high-priority issues

### Phase 4 — Build Team Workflows

- Assign issue owners
- Track investigation and resolution status
- Add comments and evidence
- Measure sentiment before and after a product release
- Generate leadership-ready weekly reports

---

## Limitations

This is an MVP and should not be treated as a production-grade customer intelligence platform.

Current limitations include:

- Sentiment analysis can misclassify sarcasm, mixed sentiment, or niche industry language.
- Theme detection is dependent on predefined keywords.
- Root cause is not detected automatically.
- Priority scores do not include revenue impact or customer value.
- The dashboard does not include authentication or role-based access control.
- The app does not yet redact PII or enforce data-retention policies.
- Quantitative patterns should be validated with customer research and operational data before roadmap decisions are made.

---

## Privacy and Responsible Use

Do not upload sensitive customer data unless you have the right permissions and safeguards.

A production implementation should include:

- PII detection and redaction
- Authentication and role-based access control
- Encryption at rest and in transit
- Data-retention policies
- Audit logs
- Consent and data-processing compliance
- Secure secret management
- Restricted access to support-ticket data

The included sample data is synthetic and intended only for demonstration and testing.

---

## Why This Project Matters

This project demonstrates the ability to:

- Translate a business problem into a usable product workflow
- Define users and jobs-to-be-done
- Build an MVP around measurable user value
- Use customer feedback as a product-discovery input
- Think in prioritisation, metrics, trade-offs, and experimentation
- Combine Product Management thinking with Python, analytics, and AI-adjacent tooling
- Design a practical internal tool for Product, Support, and Growth teams

---

## Author

**Sumit Pandey**  
Product Manager — AI, Growth, Marketplace, and Customer Experience Products

[GitHub](https://github.com/connectsumitp)

---

## License

This project is licensed under the [MIT License](LICENSE).
