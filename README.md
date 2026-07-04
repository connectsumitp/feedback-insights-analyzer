# Feedback Insights Analyzer

A product-feedback analytics dashboard that turns unstructured customer reviews into sentiment trends, issue themes, priority scores, and recommended product actions.

**Live demo:** Add your Streamlit deployment link here  
**Built with:** Python, Streamlit, Pandas, Plotly, and VADER sentiment analysis

## Why I built this

Product, support, and customer-success teams receive feedback across app reviews, tickets, surveys, and calls—but manual reading does not scale. This MVP helps teams identify where customers are struggling, quantify recurring themes, and decide which problem to investigate first.

The included CSV is **synthetic marketplace feedback**. It does not contain real customer or company data.

## What it does

- Upload a feedback CSV or explore the included sample data
- Classify feedback as **Positive, Neutral, or Negative**
- Detect themes such as payment, support, lead quality, onboarding, bugs, pricing, search, and account issues
- Show sentiment trends over time
- Rank issue themes using a transparent **priority score**
- Surface feedback verbatims for each theme
- Generate practical product-investigation recommendations
- Download enriched feedback data as CSV

## Product lens

### Target users
- Product Managers
- Customer Experience / Support leads
- Growth and Operations teams
- Research teams reviewing Voice of Customer signals

### Example questions it answers
- Which friction point has both high complaint volume and high negative sentiment?
- Are payment complaints increasing week over week?
- Do sellers and buyers complain about different things?
- Which feedback samples should a PM read before writing a problem statement?

### Priority score
The dashboard scores each theme on a 0–100 scale:

```text
Priority score = 45% relative feedback volume + 55% negative-feedback rate
```

This is meant for first-pass triage. A production version should also use customer segment, revenue impact, support-contact rate, severity, and confidence.

## CSV format

Only `feedback` is required. The app accepts common aliases such as `review`, `comment`, and `message`.

```csv
feedback_id,date,user_type,rating,feedback
1,2026-06-01,Seller,1,"I cannot complete payment for my premium plan"
2,2026-06-01,Buyer,5,"Easy to find reliable suppliers"
3,2026-06-02,Seller,2,"Leads are irrelevant and support is not responding"
```

Optional columns:
- `feedback_id`
- `date`
- `user_type`
- `rating`

## Local setup

```bash
git clone https://github.com/YOUR_USERNAME/feedback-insights-analyzer.git
cd feedback-insights-analyzer

python -m venv .venv
```

Activate the environment:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

Install dependencies and run the app:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Project structure

```text
feedback-insights-analyzer/
├── app.py
├── utils.py
├── requirements.txt
├── data/
│   └── sample_marketplace_feedback.csv
├── docs/
│   └── product-case-study.md
└── tests/
    └── test_utils.py
```

## Roadmap

- Add an LLM-powered weekly Voice of Customer summary
- Detect new or emerging themes over time
- Support multilingual feedback
- Connect Zendesk, Intercom, Google Play reviews, or a CRM export
- Add team/owner assignment and Jira ticket creation
- Track issue resolution and measure whether negative-feedback rate improves after a release

## Privacy and responsible use

Do not upload sensitive customer data without appropriate permission and access controls. This MVP runs locally when you use Streamlit locally. For production, add authentication, data-retention policies, PII redaction, audit logs, and role-based access.

## License

MIT
