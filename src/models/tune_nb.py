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


# Load data
df = pd.read_csv("data/processed/emails.csv")

df["subject"] = df["subject"].fillna("")
df["body"] = df["body"].fillna("")


# Subject + Body
X_text = (
    df["subject"].astype(str)
    + " "
    + df["body"].astype(str)
)

y = df["label"]


# Same split
X_train_text, X_test_text, y_train, y_test = train_test_split(
    X_text,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Same preprocessing
print("Cleaning training data...")
X_train_clean = clean_batch(X_train_text)

print("Cleaning testing data...")
X_test_clean = clean_batch(X_test_text)


# Same vectorizer
vectorizer = CountVectorizer(
    max_features=5000,
    ngram_range=(1, 2)
)

X_train = vectorizer.fit_transform(X_train_clean)
X_test = vectorizer.transform(X_test_clean)


# Alpha values to test
alpha_values = [
    0.01,
    0.1,
    0.5,
    1.0,
    2.0,
    5.0,
    10.0
]


results = []


for alpha in alpha_values:

    model = MultinomialNB(alpha=alpha)

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

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

    results.append({
        "alpha": alpha,
        "accuracy": accuracy,
        "spam_precision": precision,
        "spam_recall": recall,
        "spam_f1": f1,
        "FP": fp,
        "FN": fn
    })


# Display results
results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="spam_f1",
    ascending=False
)


print("\n" + "=" * 80)
print("MultinomialNB Alpha Tuning")
print("=" * 80)

print(
    results_df.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}"
    )
)