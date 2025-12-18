import pandas as pd
import streamlit as st
import plotly.express as px

def load_data():
    df = pd.read_csv("data/employee_feedback.csv")
    return df

def classify_sentiment(rating):
    if rating >= 4:
        return "Positive"
    elif rating == 3:
        return "Neutral"
    else:
        return "Negative"

def categorize_issue(feedback_text):
    text = feedback_text.lower()

    if any(word in text for word in ["workload", "pressure", "deadline", "hours"]):
        return "Workload"
    elif any(word in text for word in ["management", "expectations"]):
        return "Management"
    elif any(word in text for word in ["tools", "process", "manual"]):
        return "Tools & Process"
    elif any(word in text for word in ["culture", "environment", "cooperation"]):
        return "Culture"
    elif any(word in text for word in ["growth", "training"]):
        return "Growth"
    else:
        return "Other"

st.set_page_config(
    page_title="Employee Feedback Dashboard",
    layout="wide"
)

st.title("Employee Feedback Analysis & Action Recommendation Dashboard")

st.markdown(
    "This dashboard analyzes employee feedback to highlight sentiment trends, key issue areas, "
    "and department-level insights for leadership decision-making."
)


data = load_data()

data["sentiment"] = data["rating"].apply(classify_sentiment)

data["issue_category"] = data["feedback_text"].apply(categorize_issue)

st.subheader("Raw Feedback Data (Preview)")
st.dataframe(data.head())

st.subheader("Key Insights")

sentiment_counts = data["sentiment"].value_counts()
st.write("### Sentiment Distribution")

sentiment_df = sentiment_counts.reset_index()
sentiment_df.columns = ["Sentiment", "Count"]

st.dataframe(
    sentiment_df,
    use_container_width=True,
    hide_index=True
)

issue_counts = data["issue_category"].value_counts()
st.write("### Issue Category Distribution")

issue_df = issue_counts.reset_index()
issue_df.columns = ["Issue Category", "Count"]

st.dataframe(
    issue_df,
    use_container_width=True,
    hide_index=True
)

dept_issue_counts = pd.crosstab(
    data["department"], data["issue_category"]
)

st.write("### Department-wise Issue Breakdown")
st.dataframe(dept_issue_counts)

st.write("### Sentiment Distribution Chart")

sentiment_fig = px.bar(
    sentiment_df,
    x="Sentiment",
    y="Count",
    text="Count",
    title="Employee Sentiment Overview"
)

sentiment_fig.update_traces(textposition="outside")
sentiment_fig.update_layout(
    xaxis_title="Sentiment",
    yaxis_title="Number of Responses",
    uniformtext_minsize=10,
    uniformtext_mode="hide"
)

st.plotly_chart(sentiment_fig, use_container_width=True)

st.write("### Issue Category Distribution Chart")

issue_fig = px.bar(
    issue_df,
    x="Issue Category",
    y="Count",
    text="Count",
    title="Frequency of Reported Issues"
)

issue_fig.update_traces(textposition="outside")
issue_fig.update_layout(
    xaxis_title="Issue Category",
    yaxis_title="Number of Responses",
    uniformtext_minsize=10,
    uniformtext_mode="hide"
)

st.plotly_chart(issue_fig, use_container_width=True)

st.subheader("Action-Oriented Recommendations")

if issue_counts.get("Workload", 0) >= 3:
    st.write("- **Workload Management:** High frequency of workload-related feedback suggests a need to review deadlines, staffing levels, and task allocation.")

if issue_counts.get("Tools & Process", 0) >= 2:
    st.write("- **Process Improvement:** Feedback indicates inefficiencies in tools or workflows. Consider upgrading systems or automating repetitive tasks.")

if sentiment_counts.get("Negative", 0) >= sentiment_counts.get("Positive", 0):
    st.write("- **Employee Engagement:** A relatively high number of negative responses suggests the need for targeted engagement initiatives and follow-up surveys.")


 
