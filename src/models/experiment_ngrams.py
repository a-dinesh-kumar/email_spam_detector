import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix

from src.data.preprocess import clean_batch


# Load data
df = pd.read_csv("data/processed/emails.csv")

# Combine Subject + Body
df["subject"] = df["subject"].fillna("")
df["body"] = df["body"].fillna("")

df["text"] = df["subject"] + " " + df["body"]

# Train/Test split
X_train_text, X_test_text, y_train, y_test = train_test_split(
    df["text"],
    df["label"],
    test_size=0.2,
    random_state=42,
    stratify=df["label"]
)

# Clean
X_train_clean = clean_batch(
    X_train_text.astype(str)
)

X_test_clean = clean_batch(
    X_test_text.astype(str)
)


def run_experiment(name, ngram_range):

    vectorizer = CountVectorizer(
        max_features=5000,
        ngram_range=ngram_range
    )

    X_train = vectorizer.fit_transform(X_train_clean)
    X_test = vectorizer.transform(X_test_clean)

    model = MultinomialNB(alpha=1.0)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    report = classification_report(
        y_test,
        y_pred,
        output_dict=True
    )

    cm = confusion_matrix(y_test, y_pred)

    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    print("Feature matrix:")
    print("Training:", X_train.shape)
    print("Testing :", X_test.shape)

    print("\nSpam Precision :", round(report["spam"]["precision"], 4))
    print("Spam Recall    :", round(report["spam"]["recall"], 4))
    print("Spam F1        :", round(report["spam"]["f1-score"], 4))
    print("Accuracy       :", round(report["accuracy"], 4))

    print("\nConfusion Matrix:")
    print(cm)

    print("\nFP:", cm[0][1])
    print("FN:", cm[1][0])


# Experiment A
run_experiment(
    "CountVectorizer + Unigrams",
    (1, 1)
)

# Experiment B
run_experiment(
    "CountVectorizer + Unigrams + Bigrams",
    (1, 2)
)