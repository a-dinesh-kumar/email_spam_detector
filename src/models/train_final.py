import joblib

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix

from src.data.load_data import load_data
from src.data.preprocess import clean_batch


INPUT_FILE = "data/processed/emails.csv"

MODEL_FILE = "models/spam_model.pkl"
VECTORIZER_FILE = "models/count_vectorizer.pkl"


def main():

    # ---------------------------------------------
    # 1. Load data
    # ---------------------------------------------

    df = load_data(INPUT_FILE)

    df["subject"] = df["subject"].fillna("")
    df["body"] = df["body"].fillna("")

    df["text"] = df["subject"] + " " + df["body"]

    print("Total emails:", len(df))


    # ---------------------------------------------
    # 2. Train/Test split
    # ---------------------------------------------

    X_train_text, X_test_text, y_train, y_test = train_test_split(
        df["text"],
        df["label"],
        test_size=0.2,
        random_state=42,
        stratify=df["label"]
    )


    # ---------------------------------------------
    # 3. Clean text
    # ---------------------------------------------

    print("\nCleaning training data...")
    X_train_clean = clean_batch(
        X_train_text.astype(str)
    )

    print("Cleaning testing data...")
    X_test_clean = clean_batch(
        X_test_text.astype(str)
    )


    # ---------------------------------------------
    # 4. Vectorization
    # ---------------------------------------------

    vectorizer = CountVectorizer(
        max_features=5000,
        ngram_range=(1, 2)
    )

    X_train = vectorizer.fit_transform(X_train_clean)
    X_test = vectorizer.transform(X_test_clean)

    print("\nTraining features:", X_train.shape)
    print("Testing features :", X_test.shape)


    # ---------------------------------------------
    # 5. Train selected model
    # ---------------------------------------------

    model = MultinomialNB(alpha=1.0)

    model.fit(X_train, y_train)


    # ---------------------------------------------
    # 6. Evaluate holdout test set
    # ---------------------------------------------

    predictions = model.predict(X_test)

    print("\n" + "=" * 60)
    print("FINAL HOLDOUT EVALUATION")
    print("=" * 60)

    print(classification_report(y_test, predictions))

    cm = confusion_matrix(
        y_test,
        predictions,
        labels=["ham", "spam"]
    )

    print("Confusion Matrix:")
    print(cm)


    # ---------------------------------------------
    # 7. Retrain on complete dataset
    # ---------------------------------------------

    print("\nRetraining final production model on all data...")

    all_clean = clean_batch(
        df["text"].astype(str)
    )

    final_vectorizer = CountVectorizer(
        max_features=5000,
        ngram_range=(1, 2)
    )

    X_all = final_vectorizer.fit_transform(all_clean)

    final_model = MultinomialNB(alpha=1.0)

    final_model.fit(
        X_all,
        df["label"]
    )


    # ---------------------------------------------
    # 8. Save production artifacts
    # ---------------------------------------------

    joblib.dump(
        final_vectorizer,
        VECTORIZER_FILE
    )

    joblib.dump(
        final_model,
        MODEL_FILE
    )

    print("\nProduction artifacts saved:")
    print(VECTORIZER_FILE)
    print(MODEL_FILE)


if __name__ == "__main__":
    main()