from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from utils import build_recommendations, prepare_feedback, theme_summary


st.set_page_config(
    page_title="Feedback Insights Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_PATH = Path(__file__).parent / "data" / "sample_marketplace_feedback.csv"


@st.cache_data
def load_and_prepare(data: pd.DataFrame) -> pd.DataFrame:
    return prepare_feedback(data)


def load_sample_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def show_header() -> None:
    st.title("💬 Feedback Insights Analyzer")
    st.caption(
        "Turn unstructured customer feedback into sentiment trends, issue priorities, and product actions."
    )


def filter_feedback(df: pd.DataFrame) -> pd.DataFrame:
    with st.sidebar:
        st.header("Filters")

        user_types = sorted(df["user_type"].dropna().unique().tolist())
        selected_user_types = st.multiselect("User type", user_types, default=user_types)

        sentiment_options = ["Positive", "Neutral", "Negative"]
        selected_sentiments = st.multiselect("Sentiment", sentiment_options, default=sentiment_options)

        all_themes = sorted({theme for values in df["themes_list"] for theme in values})
        selected_themes = st.multiselect("Issue theme", all_themes, default=all_themes)

        dated = df["date"].dropna()
        selected_dates = None
        if not dated.empty:
            selected_dates = st.date_input(
                "Feedback date",
                value=(dated.min().date(), dated.max().date()),
                min_value=dated.min().date(),
                max_value=dated.max().date(),
            )

    filtered = df[
        df["user_type"].isin(selected_user_types)
        & df["sentiment"].isin(selected_sentiments)
    ].copy()

    filtered = filtered[
        filtered["themes_list"].apply(lambda values: any(theme in selected_themes for theme in values))
    ].copy()

    if selected_dates and len(selected_dates) == 2:
        start_date, end_date = pd.to_datetime(selected_dates[0]), pd.to_datetime(selected_dates[1])
        filtered = filtered[
            filtered["date"].isna()
            | ((filtered["date"] >= start_date) & (filtered["date"] <= end_date))
        ].copy()

    return filtered


def summary_metrics(df: pd.DataFrame, summary: pd.DataFrame) -> None:
    total_feedback = len(df)
    negative_rate = (df["sentiment"].eq("Negative").mean() * 100) if total_feedback else 0
    avg_rating = df["rating"].mean()
    top_issue = summary.iloc[0]["theme"] if not summary.empty else "—"

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total feedback", f"{total_feedback:,}")
    col2.metric("Negative feedback", f"{negative_rate:.1f}%")
    col3.metric("Average rating", f"{avg_rating:.1f}/5" if pd.notna(avg_rating) else "Not available")
    col4.metric("Top issue", top_issue)


def sentiment_and_trend_charts(df: pd.DataFrame) -> None:
    left, right = st.columns([1, 2])

    with left:
        sentiment_counts = (
            df["sentiment"].value_counts()
            .reindex(["Positive", "Neutral", "Negative"], fill_value=0)
            .reset_index()
        )
        sentiment_counts.columns = ["sentiment", "feedback_count"]
        fig = px.pie(
            sentiment_counts,
            names="sentiment",
            values="feedback_count",
            hole=0.55,
            title="Sentiment split",
        )
        fig.update_layout(margin=dict(t=55, b=10, l=10, r=10), legend_title_text="")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        trend_data = df.dropna(subset=["date"]).copy()
        if trend_data.empty:
            st.info("Add a `date` column to see sentiment trends.")
        else:
            trend_data["week"] = trend_data["date"].dt.to_period("W").apply(lambda value: value.start_time)
            trend = (
                trend_data.groupby(["week", "sentiment"], as_index=False)
                .size()
                .rename(columns={"size": "feedback_count"})
            )
            fig = px.line(
                trend,
                x="week",
                y="feedback_count",
                color="sentiment",
                markers=True,
                title="Weekly feedback trend",
            )
            fig.update_layout(margin=dict(t=55, b=10, l=10, r=10), legend_title_text="")
            st.plotly_chart(fig, use_container_width=True)


def issue_analysis(summary: pd.DataFrame) -> None:
    st.subheader("Issue analysis")
    if summary.empty:
        st.info("No feedback matches the current filters.")
        return

    left, right = st.columns([1.25, 1])

    with left:
        fig = px.bar(
            summary.sort_values("priority_score"),
            x="priority_score",
            y="theme",
            orientation="h",
            hover_data=["feedback_volume", "negative_rate", "avg_rating"],
            title="Issue priority score",
            labels={"priority_score": "Priority score (0–100)", "theme": ""},
        )
        fig.update_layout(margin=dict(t=55, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)

    with right:
        fig = px.scatter(
            summary,
            x="feedback_volume",
            y="negative_rate",
            size="priority_score",
            hover_name="theme",
            hover_data=["avg_rating", "priority_score"],
            title="Volume vs. negative sentiment",
            labels={"feedback_volume": "Feedback volume", "negative_rate": "Negative feedback (%)"},
        )
        fig.update_layout(margin=dict(t=55, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)

    display = summary.copy()
    display["negative_rate"] = display["negative_rate"].map(lambda value: f"{value:.1f}%")
    display["priority_score"] = display["priority_score"].map(lambda value: f"{value:.1f}")
    display["avg_rating"] = display["avg_rating"].map(
        lambda value: f"{value:.2f}" if pd.notna(value) else "—"
    )
    st.dataframe(
        display.rename(
            columns={
                "theme": "Theme",
                "feedback_volume": "Feedback volume",
                "negative_rate": "Negative rate",
                "avg_rating": "Avg. rating",
                "priority_score": "Priority score",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )


def recommendations(summary: pd.DataFrame) -> None:
    st.subheader("Recommended product actions")
    recommendations_df = build_recommendations(summary)

    if recommendations_df.empty:
        st.info("No recommendations are available for the current filters.")
        return

    for _, row in recommendations_df.iterrows():
        st.markdown(
            f"**{row['theme']}** · priority `{row['priority_score']:.1f}` · "
            f"{int(row['feedback_volume'])} feedback items · {row['negative_rate']:.1f}% negative  \n"
            f"{row['recommendation']}"
        )


def feedback_drilldown(df: pd.DataFrame) -> None:
    st.subheader("Feedback drill-down")
    available_themes = sorted({theme for values in df["themes_list"] for theme in values})
    selected_theme = st.selectbox("Show feedback for theme", ["All themes"] + available_themes)

    drilldown = df.copy()
    if selected_theme != "All themes":
        drilldown = drilldown[
            drilldown["themes_list"].apply(lambda values: selected_theme in values)
        ].copy()

    columns = ["feedback_id", "date", "user_type", "rating", "sentiment", "themes", "feedback"]
    st.dataframe(
        drilldown[columns].sort_values("date", ascending=False, na_position="last"),
        use_container_width=True,
        hide_index=True,
        column_config={
            "feedback": st.column_config.TextColumn("Feedback", width="large"),
            "date": st.column_config.DateColumn("Date", format="DD MMM YYYY"),
            "rating": st.column_config.NumberColumn("Rating", format="%.1f"),
        },
    )

    download_data = drilldown.drop(columns=["themes_list"], errors="ignore").to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download filtered feedback with insights",
        data=download_data,
        file_name="feedback_insights_export.csv",
        mime="text/csv",
    )


def main() -> None:
    show_header()

    with st.sidebar:
        st.header("Data source")
        use_sample = st.toggle("Use sample marketplace feedback", value=True)
        uploaded_file = st.file_uploader("Upload your feedback CSV", type=["csv"])
        st.caption("Required: `feedback`. Optional: `date`, `rating`, `user_type`, `feedback_id`.")

    try:
        if uploaded_file is not None and not use_sample:
            raw_df = pd.read_csv(uploaded_file)
        else:
            raw_df = load_sample_data()

        feedback_df = load_and_prepare(raw_df)
    except Exception as error:
        st.error(f"Could not process this file: {error}")
        st.stop()

    filtered_df = filter_feedback(feedback_df)
    summary = theme_summary(filtered_df)

    summary_metrics(filtered_df, summary)
    st.divider()
    sentiment_and_trend_charts(filtered_df)
    st.divider()
    issue_analysis(summary)
    st.divider()
    recommendations(summary)
    st.divider()
    feedback_drilldown(filtered_df)

    with st.expander("How the priority score works"):
        st.write(
            "Priority blends issue volume (45%) and negative-feedback rate (55%). "
            "It is a triage signal, not a substitute for impact, revenue, or customer-segment analysis."
        )

    with st.expander("Important limitations"):
        st.write(
            "Sentiment and theme detection are rule-based/VADER-assisted for a transparent MVP. "
            "Before using this for production decisions, validate the labels on a reviewed sample and "
            "add domain-specific taxonomy, ticket metadata, and impact metrics."
        )


if __name__ == "__main__":
    main()
