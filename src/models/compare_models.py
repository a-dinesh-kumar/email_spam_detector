import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split

from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


# --------------------------------------------------
# 1. Load data
# --------------------------------------------------

df = pd.read_csv("data/processed/cleaned_emails.csv")

X_text = df["cleaned_body"].fillna("")
y = df["label"]


# --------------------------------------------------
# 2. Same train/test split
# --------------------------------------------------

X_train_text, X_test_text, y_train, y_test = train_test_split(
    X_text,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# --------------------------------------------------
# 3. CountVectorizer
# --------------------------------------------------

vectorizers = {
    "CountVectorizer": CountVectorizer(
        max_features=5000,
        ngram_range=(1, 2)
    ),

    "TfidfVectorizer": TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2)
    )
}


# --------------------------------------------------
# 4. Define models
# --------------------------------------------------

models = {
    "MultinomialNB": MultinomialNB(
        alpha=1.0
    ),

    "LogisticRegression": LogisticRegression(
        max_iter=1000,
        random_state=42
    ),

    "LinearSVC": LinearSVC(
        random_state=42
    )
}


# --------------------------------------------------
# 5. Run experiments
# --------------------------------------------------

results = []

for vectorizer_name, vectorizer in vectorizers.items():

    X_train = vectorizer.fit_transform(X_train_text)
    X_test = vectorizer.transform(X_test_text)

    for model_name, model in models.items():

        print("\n" + "=" * 60)
        print(f"Vectorizer: {vectorizer_name}")
        print(f"Model     : {model_name}")
        print("=" * 60)

        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)

        spam_precision = precision_score(
            y_test,
            y_pred,
            pos_label="spam"
        )

        spam_recall = recall_score(
            y_test,
            y_pred,
            pos_label="spam"
        )

        spam_f1 = f1_score(
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

        print(f"Accuracy          : {accuracy:.4f}")
        print(f"Spam Precision    : {spam_precision:.4f}")
        print(f"Spam Recall       : {spam_recall:.4f}")
        print(f"Spam F1           : {spam_f1:.4f}")

        print("\nConfusion Matrix:")
        print(cm)

        print(f"\nFalse Positives   : {fp}")
        print(f"False Negatives   : {fn}")

        results.append({
            "Vectorizer": vectorizer_name,
            "Model": model_name,
            "Accuracy": accuracy,
            "Spam Precision": spam_precision,
            "Spam Recall": spam_recall,
            "Spam F1": spam_f1,
            "False Positives": fp,
            "False Negatives": fn
        })


# --------------------------------------------------
# 6. Comparison table
# --------------------------------------------------

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="Spam F1",
    ascending=False
)

print("\n\n" + "=" * 60)
print("VECTORISER + MODEL COMPARISON")
print("=" * 60)

print(results_df.to_string(index=False))