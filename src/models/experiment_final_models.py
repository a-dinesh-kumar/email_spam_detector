import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

from src.data.preprocess import clean_batch


# --------------------------------------------------
# 1. Load data
# --------------------------------------------------

df = pd.read_csv("data/processed/emails.csv")

df["subject"] = df["subject"].fillna("")
df["body"] = df["body"].fillna("")

# Subject + Body
df["text"] = df["subject"] + " " + df["body"]


# --------------------------------------------------
# 2. Train/Test split
# --------------------------------------------------

X_train_text, X_test_text, y_train, y_test = train_test_split(
    df["text"],
    df["label"],
    test_size=0.2,
    random_state=42,
    stratify=df["label"]
)


# --------------------------------------------------
# 3. Preprocess
# --------------------------------------------------

print("Cleaning training data...")
X_train_clean = clean_batch(
    X_train_text.astype(str)
)

print("Cleaning testing data...")
X_test_clean = clean_batch(
    X_test_text.astype(str)
)


# --------------------------------------------------
# 4. Vectorization
# --------------------------------------------------

vectorizer = CountVectorizer(
    max_features=5000,
    ngram_range=(1, 2)
)

X_train = vectorizer.fit_transform(X_train_clean)
X_test = vectorizer.transform(X_test_clean)

print("\nFeature matrix:")
print("Training:", X_train.shape)
print("Testing :", X_test.shape)


# --------------------------------------------------
# 5. Define models
# --------------------------------------------------

models = {
    "MultinomialNB": MultinomialNB(alpha=1.0),

    "LogisticRegression": LogisticRegression(
        max_iter=1000,
        random_state=42
    )
}


# --------------------------------------------------
# 6. Train and evaluate
# --------------------------------------------------

for name, model in models.items():

    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    report = classification_report(
        y_test,
        y_pred,
        output_dict=True
    )

    cm = confusion_matrix(y_test, y_pred)

    print("Accuracy       :", round(report["accuracy"], 4))
    print("Spam Precision :", round(report["spam"]["precision"], 4))
    print("Spam Recall    :", round(report["spam"]["recall"], 4))
    print("Spam F1        :", round(report["spam"]["f1-score"], 4))

    print("\nConfusion Matrix:")
    print(cm)

    print("\nFP:", cm[0][1])
    print("FN:", cm[1][0])