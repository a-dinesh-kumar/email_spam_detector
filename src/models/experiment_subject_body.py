import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

from src.data.preprocess import clean_batch


# Load original processed emails
df = pd.read_csv("data/processed/emails.csv")

# Combine subject + body
df["subject"] = df["subject"].fillna("")
df["body"] = df["body"].fillna("")

X_text = (
    df["subject"].astype(str)
    + " "
    + df["body"].astype(str)
)

y = df["label"]


# Same train-test split
X_train_text, X_test_text, y_train, y_test = train_test_split(
    X_text,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Same header-aware preprocessing
X_train_clean = clean_batch(X_train_text)
X_test_clean = clean_batch(X_test_text)


# Same vectorizer
vectorizer = CountVectorizer(
    max_features=5000,
    ngram_range=(1, 2)
)

X_train = vectorizer.fit_transform(X_train_clean)
X_test = vectorizer.transform(X_test_clean)


# Same model
model = MultinomialNB(alpha=1.0)

model.fit(X_train, y_train)


# Prediction
y_pred = model.predict(X_test)


# Evaluation
accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    pos_label="spam"
)

recall = recall_score(
    y_test,
    y_pred,
    pos_label="spam"
)

f1 = f1_score(
    y_test,
    y_pred,
    pos_label="spam"
)

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=["ham", "spam"]
)

tn, fp, fn, tp = cm.ravel()


print("=" * 60)
print("Subject + Body Experiment")
print("=" * 60)

print(f"Accuracy        : {accuracy:.4f}")
print(f"Spam Precision  : {precision:.4f}")
print(f"Spam Recall     : {recall:.4f}")
print(f"Spam F1         : {f1:.4f}")

print("\nConfusion Matrix:")
print(cm)

print(f"\nFalse Positives  : {fp}")
print(f"False Negatives  : {fn}")