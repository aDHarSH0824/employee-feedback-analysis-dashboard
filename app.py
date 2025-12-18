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

    # getting results
    print(data[["department", "rating", "sentiment", "issue_category"]].head())


 
