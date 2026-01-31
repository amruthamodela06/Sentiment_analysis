from flask import Flask, request, jsonify, send_from_directory, render_template
import pickle
import re
import os
import nltk
from nltk.stem import WordNetLemmatizer

# Ensure resources are downloaded (lite check)
try:
    nltk.data.find('corpora/wordnet.zip')
except LookupError:
    nltk.download('wordnet')
try:
    nltk.data.find('corpora/omw-1.4.zip')
except LookupError:
    nltk.download('omw-1.4')

app = Flask(__name__, static_folder="static")

# === Load the model and vectorizer ===
MODEL_PATH = os.path.join("backend", "model.pkl")
VECTORIZER_PATH = os.path.join("backend", "vectorizer.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(VECTORIZER_PATH, "rb") as f:
    vectorizer = pickle.load(f)

# === Text cleaning function ===
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = re.sub(r"http\S+|www\S+|https\S+", '', str(text))
    text = re.sub(r'\@\w+|\#', '', text)
    text = re.sub(r'[^A-Za-z0-9 ]+', '', text)
    text = text.lower().strip()
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return " ".join(tokens)

# === Serve frontend ===
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze")
def analyze_view():
    return render_template("analyze_view.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/resources")
def resources():
    return render_template("resources.html")

@app.route("/help")
def help():
    return render_template("help.html")

@app.route("/games")
def games():
    return render_template("games.html")

@app.route("/journal")
def journal():
    return render_template("journal.html")


# === API Route for Mood Prediction ===
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    user_input = data.get("message")

    if not user_input:
        return jsonify({"error": "Please send a message."}), 400

    cleaned = clean_text(user_input)
    vec = vectorizer.transform([cleaned])
    
    # Get prediction
    prediction = model.predict(vec)[0]
    
    # Get confidence
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(vec)[0]
        conf = round(proba[list(model.classes_).index(prediction)] * 100, 2)
    else:
        conf = 100.0
        
    # Explainability: Get top contributing words (rudimentary)
    # Note: SVM coefficients are global, but we can check input words x coefficients
    highlighted = []
    try:
        if hasattr(model, "calibrated_classifiers_"):
            # For CalibratedClassifierCV, get the base estimator (LinearSVC)
            # We average coefficients from all folds or just pick the first one
            base_model = model.calibrated_classifiers_[0].estimator
        else:
            base_model = model
            
        feature_names = vectorizer.get_feature_names_out()
        coefs = base_model.coef_
        
        # Get index of predicted class
        class_idx = list(model.classes_).index(prediction)
        
        # If binary, coefs is (1, n_features), if multi-class, (n_classes, n_features)
        if coefs.shape[0] == 1:
            class_coefs = coefs[0] if class_idx == 1 else -coefs[0]
        else:
            class_coefs = coefs[class_idx]
            
        # Check which words in input are important
        input_tokens = cleaned.split()
        for token in set(input_tokens): # Unique tokens
            if token in vectorizer.vocabulary_:
                idx = vectorizer.vocabulary_[token]
                score = class_coefs[idx]
                if score > 0.5: # Threshold for "important" positive contributor
                    highlighted.append(token)
                    
    except Exception as e:
        print(f"Explainability error: {e}")

    return jsonify({
        "mood": prediction,
        "confidence": f"{conf}%",
        "highlighted_phrases": highlighted
    })

if __name__ == "__main__":
    app.run(debug=True)
