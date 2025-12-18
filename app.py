import pandas as pd

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

if __name__ == "__main__":
    data = load_data()

    # Applying sentiment classification
    data["sentiment"] = data["rating"].apply(classify_sentiment)

    # Applying issue categorization
    data["issue_category"] = data["feedback_text"].apply(categorize_issue)

    # Sentiment distribution
    sentiment_counts = data["sentiment"].value_counts()
    print("\nSentiment Distribution:")
    print(sentiment_counts)

    # Issue category distribution
    issue_counts = data["issue_category"].value_counts()
    print("\nIssue Category Distribution:")
    print(issue_counts)

    # Department-wise issue analysis
    dept_issue_counts = pd.crosstab(
        data["department"], data["issue_category"]
    )
    print("\nDepartment-wise Issue Breakdown:")
    print(dept_issue_counts)

    # getting results
    print(data[["department", "rating", "sentiment", "issue_category"]].head())


 
