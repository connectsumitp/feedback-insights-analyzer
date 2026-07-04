# Product Case Study: Feedback Insights Analyzer

## Problem

Teams collect feedback from reviews, support tickets, NPS comments, and sales conversations. The information is rich but unstructured: a PM cannot reliably tell which complaint is most widespread, most negative, or growing fastest without spending hours in spreadsheets.

## Goal

Build a lightweight, transparent feedback-analysis MVP that helps a product team move from raw comments to a prioritized investigation queue.

## Users

- **Product Manager:** identifies product friction and frames the next discovery question.
- **Support Lead:** finds recurring contact reasons and backlog drivers.
- **Customer Success / Sales:** spots segment-specific pain points to escalate.
- **Leadership:** gets a concise Voice of Customer view instead of anecdotal updates.

## Core flow

1. User uploads a CSV of feedback.
2. The app normalizes standard columns.
3. VADER-assisted sentiment labels each response.
4. A rule-based taxonomy tags one or more product themes.
5. The dashboard calculates theme volume, negative rate, and a priority score.
6. The user reads top verbatims and recommended investigation actions.

## MVP metrics

### Product adoption
- Number of feedback files analyzed per week
- Weekly active internal users
- Percentage of users exporting insights

### Quality
- Sentiment-label precision on a manually reviewed sample
- Theme-label precision and recall
- Percentage of feedback assigned to a useful theme instead of `Other`

### Product impact
- Time required to produce a weekly Voice of Customer report
- Time to identify a newly emerging issue
- Change in support contact rate or negative-feedback rate after intervention

## Key trade-offs

- **Rule-based themes vs. LLM categorization:** Rules are transparent, cheap, and easy to debug, but need ongoing taxonomy maintenance. An LLM version could discover richer themes, with a human-review loop and privacy safeguards.
- **Priority score vs. business impact:** Complaint volume and sentiment are useful triage signals, but not a complete severity model. A future version should include customer value, revenue at risk, segment, recurrence, and operational cost.
- **CSV first vs. integrations:** CSV makes the MVP easy to test. API integrations should follow only after data quality, taxonomy, and user workflow are validated.

## First experiments

1. **Support SLA hypothesis:** If long first-response times drive negative support feedback, then improving first response for high-volume contact reasons will reduce support-related negativity.
2. **Payment recovery hypothesis:** If failed payments are caused by retry friction, adding clearer retry states and alternate payment methods will lower payment-related negative feedback.
3. **Lead-quality hypothesis:** If sellers receive poor-fit leads, improving matching or giving sellers better qualification controls will improve lead-quality sentiment and paid-seller retention.
