import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


# Load cleaned data
df = pd.read_csv("data/processed/cleaned_emails.csv")

X_text = df["cleaned_body"].fillna("")
y = df["label"]


# Bag-of-Words vectorization
vectorizer = CountVectorizer(
    max_features=5000,
    ngram_range=(1, 2)
)

X = vectorizer.fit_transform(X_text)


# Baseline model
model = MultinomialNB(alpha=1.0)


print("Total emails        :", len(df))
print("Feature matrix      :", X.shape)
print("Vocabulary size     :", len(vectorizer.vocabulary_))
print("Model               :", model)