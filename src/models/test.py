import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB


# Load cleaned data
df = pd.read_csv("data/processed/cleaned_emails.csv")

X_text = df["cleaned_body"].fillna("")
y = df["label"]


# Same split configuration used during training
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


# Train baseline model
model = MultinomialNB(alpha=1.0)
model.fit(X_train, y_train)


# Predict on unseen test data
y_pred = model.predict(X_test)


print("Testing completed.")
print("Predictions generated:", len(y_pred))