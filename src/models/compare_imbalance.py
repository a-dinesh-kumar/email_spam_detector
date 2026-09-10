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

from imblearn.over_sampling import RandomOverSampler


# Load data
df = pd.read_csv("data/processed/cleaned_emails.csv")

X_text = df["cleaned_body"].fillna("")
y = df["label"]


# Train-test split
X_train_text, X_test_text, y_train, y_test = train_test_split(
    X_text,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Vectorization
vectorizer = CountVectorizer(
    max_features=5000,
    ngram_range=(1, 2)
)

X_train = vectorizer.fit_transform(X_train_text)
X_test = vectorizer.transform(X_test_text)


print("=" * 60)
print("Before Oversampling")
print("=" * 60)

print(y_train.value_counts())


# Random oversampling
ros = RandomOverSampler(random_state=42)

X_train_resampled, y_train_resampled = ros.fit_resample(
    X_train,
    y_train
)


print("\n" + "=" * 60)
print("After Oversampling")
print("=" * 60)

print(y_train_resampled.value_counts())


# Train model
model = MultinomialNB(alpha=1.0)

model.fit(
    X_train_resampled,
    y_train_resampled
)


# Predict on ORIGINAL test set
y_pred = model.predict(X_test)


# Evaluation
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, pos_label="spam")
recall = recall_score(y_test, y_pred, pos_label="spam")
f1 = f1_score(y_test, y_pred, pos_label="spam")

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=["ham", "spam"]
)

tn, fp, fn, tp = cm.ravel()


print("\n" + "=" * 60)
print("Random Oversampling Results")
print("=" * 60)

print(f"Accuracy        : {accuracy:.4f}")
print(f"Spam Precision  : {precision:.4f}")
print(f"Spam Recall     : {recall:.4f}")
print(f"Spam F1         : {f1:.4f}")

print("\nConfusion Matrix:")
print(cm)

print(f"\nFalse Positives  : {fp}")
print(f"False Negatives  : {fn}")