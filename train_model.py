import pandas as pd
import re
import os
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

# === Ensure NLTK data is available ===
try:
    nltk.data.find('corpora/wordnet.zip')
except LookupError:
    nltk.download('wordnet')

try:
    nltk.data.find('corpora/omw-1.4.zip')
except LookupError:
    nltk.download('omw-1.4')
    
try:
    nltk.data.find('corpora/stopwords.zip')
except LookupError:
    nltk.download('stopwords')

lemmatizer = WordNetLemmatizer()

# === 1. Load Data ===
print("Loading data...")
df = pd.read_csv("data/Combined Data.csv")

# === 2. Clean Text ===
def clean_text(text):
    text = re.sub(r"http\S+|www\S+|https\S+", '', str(text))
    text = re.sub(r'\@\w+|\#', '', text)
    text = re.sub(r'[^A-Za-z0-9 ]+', '', text)
    text = text.lower().strip()
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return " ".join(tokens)

print("Cleaning text...")
df['status'] = df['status'].str.strip().str.title()
df['cleaned'] = df['statement'].apply(clean_text)

# Filter classes with < 2 samples
label_counts = df['status'].value_counts()
valid_labels = label_counts[label_counts >= 2].index
df = df[df['status'].isin(valid_labels)]

X = df['cleaned']
y = df['status']

# === 3. Train-Test Split ===
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# === 4. Build Pipeline ===
# Use LinearSVC for better text classification performance
# Wrap in CalibratedClassifierCV to get probability estimates
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=5000, stop_words='english')),
    ('clf', CalibratedClassifierCV(LinearSVC(class_weight='balanced', dual=False, random_state=42)))
])

# === 5. Hyperparameter Tuning ===
# Tune ngram_range for Tfidf
params = {
    'tfidf__ngram_range': [(1, 1), (1, 2)]
}

print("Training model (GridSearch)...")
grid = GridSearchCV(pipeline, params, cv=3, scoring='accuracy', n_jobs=1)
grid.fit(X_train, y_train)

print(f"Best parameters: {grid.best_params_}")

# === 6. Evaluate ===
y_pred = grid.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print("\n\U0001F4CB Classification Report:\n")
print(classification_report(y_test, y_pred))
print(f"\nOverall Accuracy: {acc}")

# === 7. Save Artifacts ===
os.makedirs("backend", exist_ok=True)

best_model = grid.best_estimator_
vectorizer = best_model.named_steps['tfidf']
clf = best_model.named_steps['clf']

# Save components separately for compatibility with app.py
with open("backend/model.pkl", "wb") as f:
    pickle.dump(clf, f)

with open("backend/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)
    
print("\n✅ New SVM model and vectorizer saved to 'backend/'")
