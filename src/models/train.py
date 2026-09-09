import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB


# Load cleaned data
df = pd.read_csv("data/processed/cleaned_emails.csv")

X_text = df["cleaned_body"].fillna("")
y = df["label"]


# Split into training and testing sets
X_train_text, X_test_text, y_train, y_test = train_test_split(
    X_text,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Build and fit vectorizer ONLY on training data
vectorizer = CountVectorizer(
    max_features=5000,
    ngram_range=(1, 2)
)

X_train = vectorizer.fit_transform(X_train_text)

# Transform test data using the SAME vectorizer
X_test = vectorizer.transform(X_test_text)


# Build and train baseline model
model = MultinomialNB(alpha=1.0)

model.fit(X_train, y_train)


print("Total records       :", len(df))
print("Training records    :", len(X_train_text))
print("Testing records     :", len(X_test_text))
print("Training features   :", X_train.shape)
print("Testing features    :", X_test.shape)

print("\nTraining label distribution:")
print(y_train.value_counts())

print("\nTesting label distribution:")
print(y_test.value_counts())

print("\nModel trained successfully.")