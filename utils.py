from __future__ import annotations

import re
from typing import Iterable

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


THEME_KEYWORDS: dict[str, list[str]] = {
    "Payment": [
        r"\bpayment\b", r"\bpay\b", r"\bcharged\b", r"\brefund\b", r"\binvoice\b",
        r"\btransaction\b", r"\bgateway\b", r"\bupi\b", r"\bcard\b", r"\bsubscription\b"
    ],
    "Support": [
        r"\bsupport\b", r"\bcustomer care\b", r"\bhelpline\b", r"\bresponse\b",
        r"\bresponding\b", r"\bcallback\b", r"\bticket\b", r"\bagent\b"
    ],
    "Lead Quality": [
        r"\blead(s)?\b", r"\benquir(y|ies)\b", r"\bwrong buyer\b", r"\birrelevant\b",
        r"\bspam\b", r"\bfake buyer\b", r"\bnot interested\b"
    ],
    "Onboarding": [
        r"\bonboarding\b", r"\bsign ?up\b", r"\bregister\b", r"\bverification\b",
        r"\bkyc\b", r"\bgetting started\b", r"\bfirst time\b"
    ],
    "App & Technical Bugs": [
        r"\bapp\b", r"\bcrash\b", r"\bbug\b", r"\berror\b", r"\bslow\b",
        r"\bloading\b", r"\blogin\b", r"\bnot working\b", r"\bglitch\b", r"\bfreeze\b"
    ],
    "Pricing & Subscription": [
        r"\bprice\b", r"\bpricing\b", r"\bexpensive\b", r"\bplan\b", r"\bpremium\b",
        r"\brenew(al)?\b", r"\bsubscription\b", r"\bvalue for money\b"
    ],
    "Delivery & Fulfillment": [
        r"\bdelivery\b", r"\bdelivered\b", r"\bshipment\b", r"\bshipping\b",
        r"\bdispatch\b", r"\bdelay\b", r"\breturn\b"
    ],
    "Search & Discovery": [
        r"\bsearch\b", r"\bfind\b", r"\bfilter\b", r"\bdiscover\b",
        r"\bresult(s)?\b", r"\bvisibility\b", r"\bdiscoverability\b"
    ],
    "Account & Profile": [
        r"\bprofile\b", r"\baccount\b", r"\bpassword\b", r"\bmobile number\b",
        r"\bemail\b", r"\bedit details\b", r"\bdeactivate\b"
    ],
}

POSITIVE_HINTS = {"great", "easy", "helpful", "reliable", "smooth", "excellent", "love", "fast", "useful"}
NEGATIVE_HINTS = {"not working", "worst", "poor", "bad", "fraud", "fake", "irrelevant", "slow", "failed", "refund"}

_analyzer = SentimentIntensityAnalyzer()


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Accept common CSV column aliases while retaining the original data."""
    df = df.copy()
    normalized_lookup = {str(c).strip().lower().replace(" ", "_"): c for c in df.columns}
    aliases = {
        "feedback": ["feedback", "review", "comment", "message", "text", "feedback_text"],
        "date": ["date", "created_at", "created_date", "submitted_at"],
        "rating": ["rating", "score", "stars", "star_rating"],
        "user_type": ["user_type", "customer_type", "persona", "segment", "user_segment"],
        "feedback_id": ["feedback_id", "id", "review_id", "ticket_id"],
    }

    rename_map: dict[str, str] = {}
    for canonical, candidates in aliases.items():
        if canonical in df.columns:
            continue
        for candidate in candidates:
            if candidate in normalized_lookup:
                rename_map[normalized_lookup[candidate]] = canonical
                break

    return df.rename(columns=rename_map)


def validate_input(df: pd.DataFrame) -> tuple[bool, str]:
    if "feedback" not in df.columns:
        return False, "Your CSV needs a `feedback` column (or an alias such as `review`, `comment`, or `message`)."
    if df.empty:
        return False, "The uploaded CSV is empty."
    return True, ""


def classify_sentiment(text: object) -> tuple[str, float]:
    """Return a VADER-based label and confidence score, with lightweight product-feedback safeguards."""
    clean_text = str(text or "").strip()
    if not clean_text:
        return "Neutral", 0.0

    text_lower = clean_text.lower()
    compound = _analyzer.polarity_scores(clean_text)["compound"]

    # Product reviews often contain phrases VADER understates; gently correct those cases.
    if any(hint in text_lower for hint in NEGATIVE_HINTS) and compound > -0.25:
        compound -= 0.30
    if any(hint in text_lower for hint in POSITIVE_HINTS) and compound < 0.25:
        compound += 0.20

    compound = max(-1.0, min(1.0, compound))
    if compound >= 0.20:
        return "Positive", round(compound, 3)
    if compound <= -0.20:
        return "Negative", round(compound, 3)
    return "Neutral", round(compound, 3)


def detect_themes(text: object) -> list[str]:
    clean_text = str(text or "").lower()
    matches: list[str] = []

    for theme, patterns in THEME_KEYWORDS.items():
        if any(re.search(pattern, clean_text, flags=re.IGNORECASE) for pattern in patterns):
            matches.append(theme)

    return matches or ["Other"]


def prepare_feedback(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize, enrich, and prepare feedback for dashboard analysis."""
    df = normalize_columns(df)
    valid, message = validate_input(df)
    if not valid:
        raise ValueError(message)

    df = df.copy()
    df["feedback"] = df["feedback"].fillna("").astype(str).str.strip()
    df = df[df["feedback"].ne("")].copy()

    if "feedback_id" not in df.columns:
        df["feedback_id"] = [f"FB-{i:04d}" for i in range(1, len(df) + 1)]
    else:
        df["feedback_id"] = df["feedback_id"].fillna("").astype(str)

    if "date" not in df.columns:
        df["date"] = pd.NaT
    else:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    if "rating" not in df.columns:
        df["rating"] = pd.NA
    else:
        df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

    if "user_type" not in df.columns:
        df["user_type"] = "Unknown"
    else:
        df["user_type"] = df["user_type"].fillna("Unknown").astype(str).str.strip()

    sentiment = df["feedback"].apply(classify_sentiment)
    df["sentiment"] = sentiment.apply(lambda item: item[0])
    df["sentiment_score"] = sentiment.apply(lambda item: item[1])
    df["themes_list"] = df["feedback"].apply(detect_themes)
    df["themes"] = df["themes_list"].apply(", ".join)
    df["feedback_length"] = df["feedback"].str.len()
    return df.reset_index(drop=True)


def explode_themes(df: pd.DataFrame) -> pd.DataFrame:
    """Return one row per feedback-theme association for theme-level analysis."""
    if df.empty:
        return df.copy()
    return df.explode("themes_list").rename(columns={"themes_list": "theme"})


def theme_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate volume, negative rate, average rating, and a 0-100 priority score."""
    theme_df = explode_themes(df)
    if theme_df.empty:
        return pd.DataFrame(columns=[
            "theme", "feedback_volume", "negative_rate", "avg_rating", "priority_score"
        ])

    summary = (
        theme_df.groupby("theme", as_index=False)
        .agg(
            feedback_volume=("feedback_id", "count"),
            negative_rate=("sentiment", lambda values: round((values == "Negative").mean() * 100, 1)),
            avg_rating=("rating", "mean"),
        )
    )
    summary["avg_rating"] = summary["avg_rating"].round(2)
    max_volume = max(summary["feedback_volume"].max(), 1)
    summary["priority_score"] = (
        (summary["feedback_volume"] / max_volume) * 45
        + (summary["negative_rate"] / 100) * 55
    ).round(1)
    return summary.sort_values(["priority_score", "feedback_volume"], ascending=[False, False]).reset_index(drop=True)


def recommendation_for_theme(row: pd.Series) -> str:
    theme = str(row["theme"])
    volume = int(row["feedback_volume"])
    negative_rate = float(row["negative_rate"])

    actions = {
        "Payment": "Review payment-failure codes, retry flows, and refund status communication.",
        "Support": "Audit first-response SLA, backlog ageing, and self-serve resolution for the top contact reasons.",
        "Lead Quality": "Review lead-source quality, matching logic, filters, and the seller feedback loop for invalid leads.",
        "Onboarding": "Instrument each onboarding step and simplify the highest-drop-off verification or profile-completion stage.",
        "App & Technical Bugs": "Cluster by app version, device, OS, and error code; triage reproducible issues with engineering.",
        "Pricing & Subscription": "Test plan comparison clarity, renewal messaging, and value communication before changing price.",
        "Delivery & Fulfillment": "Break down delays by fulfillment stage and add proactive shipment-status notifications.",
        "Search & Discovery": "Check search relevance, ranking, zero-result queries, and filters used by high-intent users.",
        "Account & Profile": "Review login recovery, edit-profile friction, and account verification journeys.",
        "Other": "Read the top verbatims manually and create a new theme only after the pattern is recurring.",
    }
    urgency = "High priority" if negative_rate >= 60 or (negative_rate >= 40 and volume >= 5) else "Monitor"
    return f"{urgency}: {actions.get(theme, actions['Other'])}"


def build_recommendations(summary: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    if summary.empty:
        return pd.DataFrame(columns=["theme", "priority_score", "recommendation"])

    output = summary.head(top_n).copy()
    output["recommendation"] = output.apply(recommendation_for_theme, axis=1)
    return output[["theme", "feedback_volume", "negative_rate", "priority_score", "recommendation"]]
