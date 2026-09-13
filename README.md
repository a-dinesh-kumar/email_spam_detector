# EmailGuard --- Email Spam Detection System

An end-to-end **NLP-based Email Spam Detection system** built with
Python, spaCy, scikit-learn, FastAPI, and a web dashboard.

The system classifies emails as **HAM (legitimate)** or **SPAM**,
isolates spam messages in quarantine, and provides a web interface for
classification and review.

**Live application:** https://email-spam-detector-vlxv.onrender.com\
**GitHub:** https://github.com/a-dinesh-kumar

------------------------------------------------------------------------

## Project Overview

``` text
Incoming Email
      |
      v
Subject + Body
      |
      v
Email-aware preprocessing
      |
      v
CountVectorizer
      |
      v
Multinomial Naive Bayes
      |
      v
+-----------+-----------+
|                       |
HAM                     SPAM
|                       |
v                       v
Inbox               Quarantine
```

The project follows an end-to-end machine-learning lifecycle:

1.  Business Understanding
2.  Data Collection
3.  Data Understanding
4.  Data Preparation
5.  Model Building
6.  Model Training
7.  Model Testing
8.  Model Evaluation
9.  Model Optimization
10. Model Deployment
11. CI/CD

------------------------------------------------------------------------

## Key Features

-   HAM/SPAM email classification
-   Subject + body based classification
-   Email-aware preprocessing
-   URL and HTML removal
-   Technical email-header filtering
-   Stopword removal and lemmatization
-   Bag-of-Words using `CountVectorizer`
-   Multinomial Naive Bayes classification
-   CountVectorizer vs TF-IDF comparison
-   Multiple classifier comparison
-   Class-imbalance experiment using RandomOverSampler
-   Inbox and spam/quarantine workflow
-   Release quarantined emails
-   `.eml` upload and parsing
-   FastAPI REST API
-   Interactive web dashboard
-   GitHub Actions CI
-   Render cloud deployment

------------------------------------------------------------------------

## Dataset

The primary dataset is the **SpamAssassin Public Corpus**, using:

-   `easy_ham`
-   `hard_ham`
-   `spam`

### Dataset statistics

  Category        Records
  ----------- -----------
  Easy Ham          2,551
  Hard Ham            250
  Spam                501
  **Total**     **3,302**

Class distribution:

-   HAM: 2,801 --- 84.83%
-   SPAM: 501 --- 15.17%

Raw email files are kept separate from processed data.

------------------------------------------------------------------------

## Data Pipeline

``` text
SpamAssassin raw emails
        |
        v
Email parser
        |
        v
Subject + Body + Label
        |
        v
Processed dataset
        |
        v
Preprocessing
        |
        v
Vectorization
        |
        v
Model training
```

The ingestion layer handles multipart emails, text/plain content,
text/html content, subjects, bodies, and parsing failures.

------------------------------------------------------------------------

## Text Preprocessing

The baseline preprocessing was implemented first and then improved
through measured experiments.

The final preprocessing includes:

1.  Remove technical email headers
2.  Convert text to lowercase
3.  Remove URLs
4.  Remove HTML tags
5.  Remove non-alphabetic characters
6.  Normalize whitespace
7.  Remove stopwords
8.  Lemmatize tokens

Email-specific cleaning was evaluated experimentally rather than added
without measurement.

------------------------------------------------------------------------

## Feature Engineering

The final feature pipeline is:

``` text
Subject + Body
      |
      v
Preprocessing
      |
      v
CountVectorizer
max_features = 5000
ngram_range = (1, 2)
      |
      v
Feature matrix
```

CountVectorizer was retained because it performed better than TF-IDF in
the tested configuration. Bigrams were retained because combinations of
words can provide useful spam-related context.

------------------------------------------------------------------------

## Model

The final classifier is:

**Multinomial Naive Bayes**

``` text
CountVectorizer
       |
       v
MultinomialNB(alpha=1.0)
```

It was selected empirically after comparing multiple vectorizer/model
combinations.

------------------------------------------------------------------------

# Model Experiments

The project deliberately follows:

> **Build a baseline → measure it → change one thing → measure again →
> keep only improvements.**

### Train/Test split

``` text
80% Training
20% Testing

random_state = 42
stratify = y
```

The test set remained separate from training and optimization.

## Vectorizer comparison

### CountVectorizer + MultinomialNB

| Metric | Result |
| :--- | ---: |
| **Accuracy** | 97.28% |
| **Spam Precision** | 91.84% |
| **Spam Recall** | 90.00% |
| **Spam F1** | 90.91% |
| **False Positives** | 8 |
| **False Negatives** | 10 |

### TF-IDF + MultinomialNB

| Metric | Result |
| :--- | ---: |
| **Accuracy** | 90.92% |
| **Spam Precision** | 67.86% |
| **Spam Recall** | 76.00% |
| **Spam F1** | 71.70% |


CountVectorizer clearly outperformed TF-IDF for this dataset/model
combination.

------------------------------------------------------------------------

## Model comparison

| Vectorizer | Model | Spam F1 |
| :--- | :--- | ---: |
| CountVectorizer | MultinomialNB | **90.91%** |
| CountVectorizer | LogisticRegression | 90.82% |
| CountVectorizer | LinearSVC | 88.12% |
| TF-IDF | MultinomialNB | 71.70% |
| TF-IDF | LogisticRegression | 82.22% |
| TF-IDF | LinearSVC | 90.45% |


The best baseline was **CountVectorizer + MultinomialNB**.

------------------------------------------------------------------------

# Optimization Experiments

## Random Oversampling

The training split was oversampled only during training:

``` text
Before:
HAM   2240
SPAM   401

After:
HAM   2240
SPAM  2240
```

Spam F1 decreased to approximately 90.45%.

**Decision: rejected.**

## HTML-aware preprocessing

HTML-specific cleaning was evaluated.

**Result:** no measurable improvement over the baseline.

**Decision: rejected as a separate optimization.**

## Header-aware preprocessing

Removing technical email headers improved the result:

| Metric | Result |
| :--- | ---: |
| **Accuracy** | 97.43% |
| **Spam Precision** | 92.78% |
| **Spam Recall** | 90.00% |
| **Spam F1** | 91.37% |
| **False Positives** | 7 |
| **False Negatives** | 10 |


**Decision: kept.**

## Subject + Body

Including the subject produced the strongest tested configuration:

| Metric | Result |
| :--- | ---: |
| **Accuracy** | **97.58%** |
| **Spam Precision** | **92.86%** |
| **Spam Recall** | **91.00%** |
| **Spam F1** | **91.92%** |
| **False Positives** | **7** |
| **False Negatives** | **9** |


**Decision: champion configuration.**

## Alpha tuning

`MultinomialNB(alpha=1.0)` was the best tested smoothing value.

## Unigrams vs unigrams + bigrams

| Configuration | Accuracy | Spam Precision | Spam Recall | Spam F1 | FP | FN |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| Unigrams | 97.58% | 94.68% | 89.00% | 91.75% | 5 | 11 |
| Unigrams + Bigrams | 97.58% | 92.86% | 91.00% | **91.92%** | 7 | 9 |


Unigrams + bigrams were retained because spam recall and F1 were more
important for this use case.

------------------------------------------------------------------------

# Final Model

``` text
Subject + Body
      |
      v
Email Header Removal
      |
      v
URL + HTML + Character Cleaning
      |
      v
Stopword Removal
      |
      v
Lemmatization
      |
      v
CountVectorizer
max_features = 5000
ngram_range = (1,2)
      |
      v
MultinomialNB
alpha = 1.0
      |
      v
HAM / SPAM
```

### Final validation result

**97.58% accuracy**\
**91.92% spam F1**

Confusion matrix:

``` text
              Predicted
              HAM   SPAM

Actual HAM     554    7
Actual SPAM      9   91
```

The production artifacts were subsequently retrained on the complete
labeled dataset and saved for deployment.

------------------------------------------------------------------------

# Project Structure

``` text
email_spam_detector/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── data/
│   ├── raw/
│   │   ├── easy_ham/
│   │   ├── hard_ham/
│   │   └── spam/
│   ├── processed/
│   ├── inbox/
│   └── quarantine/
│
├── models/
│   ├── count_vectorizer.pkl
│   └── spam_model.pkl
│
├── notebooks/
│
├── src/
│   ├── api/
│   │   ├── predict.py
│   │   ├── management.py
│   │   └── overview.py
│   ├── data/
│   │   ├── load_data.py
│   │   ├── email_parser.py
│   │   ├── preprocess.py
│   │   └── prepare_data.py
│   ├── inbox/
│   │   └── inbox.py
│   ├── quarantine/
│   │   └── quarantine.py
│   ├── models/
│   │   ├── build_baseline.py
│   │   ├── train.py
│   │   └── train_final.py
│   └── utils/
│       └── classifier.py
│
├── static/
├── templates/
│   └── index.html
├── main.py
├── requirements.txt
├── .python-version
└── README.md
```

------------------------------------------------------------------------

# FastAPI API

| Endpoint | Purpose |
| :--- | :--- |
| `POST /predict` | Classify subject + body JSON |
| `POST /predict-file` | Classify an `.eml` file |
| `GET /inbox` | View delivered emails |
| `GET /quarantine` | View quarantined emails |
| `POST /quarantine/{email_id}/release` | Release a quarantined email |
| `GET /overview` | Dashboard statistics |
| `GET /docs` | Swagger API documentation |


### Example request

``` json
{
  "subject": "Action Required: Your account has been temporarily suspended!",
  "body": "Dear Customer,We detected some unusual sign-in activity on your account from a device located in a different country. For your security, we have temporarily restricted access to your profile and payment methods.To restore your account, you must verify your identity within 24 hours. Failure to do so will result in the permanent deletion of your data.👉 [Verify Your Account & Update Information Now]Please do not reply to this email, as this inbox is not monitored.Thank you,Customer Support Team"
}
```

### Example response

``` json
{
  "prediction": "SPAM",
  "status": "quarantined"
}
```

------------------------------------------------------------------------

# Web Dashboard

The EmailGuard dashboard provides:

-   Overview statistics
-   Email classifier
-   Subject and body input
-   `.eml` upload
-   Inbox view
-   Spam/quarantine view
-   Quarantine release
-   Refresh functionality
-   Pagination
-   GitHub and LinkedIn navigation
-   Responsive UI

------------------------------------------------------------------------

# Running Locally

## Clone

``` bash
git clone https://github.com/a-dinesh-kumar/email_spam_detector.git
cd email_spam_detector
```

## Create environment

Windows:

``` bash
python -m venv .venv
.venv\Scripts ctivate
```

Linux/macOS:

``` bash
python -m venv .venv
source .venv/bin/activate
```

## Install dependencies

``` bash
pip install -r requirements.txt
```

## Install spaCy model

``` bash
python -m spacy download en_core_web_sm
```

## Start FastAPI

``` bash
uvicorn main:app --reload
```

Open:

``` text
http://127.0.0.1:8000
```

Swagger:

``` text
http://127.0.0.1:8000/docs
```

------------------------------------------------------------------------

# Deployment

The application is deployed as a Python FastAPI Web Service on
**Render**.

### Build command

``` bash
pip install -r requirements.txt && python -m spacy download en_core_web_sm
```

### Start command

``` bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Python is pinned using `.python-version`:

``` text
3.13.15
```

The service deploys from the `main` branch.

**Live application:** https://email-spam-detector-vlxv.onrender.com

------------------------------------------------------------------------

# CI/CD

GitHub Actions validates important project components automatically.

``` text
Developer
   |
   v
Git commit
   |
   v
GitHub push
   |
   v
GitHub Actions
   |
   +---- Tests pass ----+
   |                    |
   v                    v
Validation          Render deployment
```

This provides a basic continuous-integration and continuous-deployment
workflow for the project.

------------------------------------------------------------------------

# Important Design Decisions

### Why CountVectorizer?

It was the primary approach from the project guide and also performed
substantially better than TF-IDF in the measured experiments.

### Why Multinomial Naive Bayes?

It is efficient for word-count based text classification and achieved
the best result among the tested model/vectorizer combinations.

### Why Subject + Body?

Email subjects can contain useful spam signals that are absent from the
body.

### Why spam F1 instead of accuracy alone?

The dataset is imbalanced. Accuracy alone can hide poor spam detection.

The project therefore focuses on:

-   Spam precision
-   Spam recall
-   Spam F1
-   False positives
-   False negatives
-   Confusion matrix

### Why reject oversampling?

It was tested empirically and reduced spam F1 in the current
configuration.

------------------------------------------------------------------------

# Limitations

This is a portfolio and learning project, not a production email
gateway.

Current limitations:

-   Classical NLP rather than transformer-based classification
-   Relatively small training corpus
-   CSV-based inbox/quarantine storage
-   No authentication
-   No real mail-server integration
-   No attachment malware analysis
-   No continuous retraining
-   No model registry
-   No production-grade monitoring

### Render storage

The deployed demo uses local CSV files for inbox and quarantine records.

Render's free service uses ephemeral filesystem storage, so
runtime-generated CSV changes can be lost after service restarts or
redeployments.

For a production implementation, the storage layer should be migrated to
persistent storage such as PostgreSQL.

------------------------------------------------------------------------

# Future Improvements

1.  PostgreSQL-backed inbox and quarantine
2.  Server-side pagination
3.  Search and filtering
4.  Authentication and role-based access
5.  Model confidence scores
6.  More email-specific feature engineering
7.  Character n-gram experiments
8.  Transformer-based models
9.  Continuous model monitoring
10. Automated retraining
11. Model versioning
12. Production email-server integration
13. Attachment and phishing detection
14. Explainable AI

------------------------------------------------------------------------

# Learning Outcomes

This project was built as a hands-on transition from QA/automation
engineering toward AI/ML engineering.

Concepts practiced include:

-   NLP preprocessing
-   Bag-of-Words
-   TF-IDF
-   Naive Bayes
-   Logistic Regression
-   Linear SVM
-   Train/test splitting
-   Stratification
-   Class imbalance
-   Oversampling
-   Hyperparameter tuning
-   Precision, recall and F1
-   Confusion matrices
-   Model serialization
-   FastAPI
-   REST APIs
-   `.eml` parsing
-   Frontend/API integration
-   CI/CD
-   Cloud deployment

------------------------------------------------------------------------

### 👨‍💻 Author

**Dinesh Kumar Alagarsamy**  
*Software Quality Engineer / SDET*
-   GitHub: https://github.com/a-dinesh-kumar
-   LinkedIn: https://www.linkedin.com/in/dinesh-kumar-alagarsamy

#### Areas of Interest:
* Quality Engineering
* Test Automation
* API Testing
* Artificial Intelligence
* Machine Learning
* AI-powered Testing
* Software Architecture

------------------------------------------------------------------------

## License

This project is intended for educational, portfolio, and demonstration
purposes.
