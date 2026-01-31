# predict_mood.py

import pickle
import re
import nltk
from nltk.stem import WordNetLemmatizer

# Ensure resources are downloaded
try:
    nltk.data.find('corpora/wordnet.zip')
except LookupError:
    nltk.download('wordnet')
try:
    nltk.data.find('corpora/omw-1.4.zip')
except LookupError:
    nltk.download('omw-1.4')

# === 1. Load Model and Vectorizer ===
with open("backend/model.pkl", "rb") as f:
    model = pickle.load(f)

with open("backend/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

lemmatizer = WordNetLemmatizer()

# === 2. Clean Text ===
def clean_text(text):
    text = re.sub(r"http\S+|www\S+|https\S+", '', str(text), flags=re.MULTILINE)
    text = re.sub(r'\@\w+|\#', '', text)
    text = re.sub(r'[^A-Za-z0-9 ]+', '', text)
    text = text.lower().strip()
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return " ".join(tokens)

# === 3. Predict Function ===
def predict_mood(user_input):
    cleaned = clean_text(user_input)
    vectorized = vectorizer.transform([cleaned])
    
    pred = model.predict(vectorized)[0]
    
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(vectorized)[0]
        label_idx = list(model.classes_).index(pred)
        confidence = proba[label_idx]
    else:
        confidence = 1.0  # fallback if model doesn't support proba

    return pred, round(confidence * 100, 2)

# === 4. CLI Loop ===
if __name__ == "__main__":
    print("🧠 Mood Predictor with Confidence Scores\n")
    while True:
        user_input = input("Enter a statement (or 'q' to quit): ")
        if user_input.lower() in ["q", "quit", "exit"]:
            break

        mood, confidence = predict_mood(user_input)
        print(f"💬 Mood: {mood} ({confidence}% confidence)\n")
        