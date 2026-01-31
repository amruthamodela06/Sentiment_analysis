# Sentra 🧠

> **Understand emotions in text. A private, non-judgmental sentiment analysis tool.**

Sentra is a mental health-focused chatbot and web application that helps users analyze the emotional tone of their writing. It provides a safe space for self-reflection with privacy-first journaling, calming mind games, and deep sentiment analysis.

![Sentra Banner](https://via.placeholder.com/1200x600/FAFAFA/5C7C7C?text=Sentra+Dashboard)

## ✨ Features

- **Mood Analysis**:
  - **Minimal View**: A gentle, safe interface for quick checks.
  - **Deep Analysis**: Detailed breakdown of emotional signals, confidence scores, and key phrase highlighting (Explainability).
  - *Powered by a Linear Support Vector Machine (SVM) with Lemmatization for robust accuracy.*

- **Private Journal** 🔒:
  - Write daily entries and track your mood.
  - **100% Privacy**: All journal data is stored locally in your browser (LocalStorage). Nothing is sent to our servers.
  - **Mood Trends**: Visual graph of your emotional journey over the last 7 days.

- **Mind Games** 🌿:
  - **4-7-8 Breathing**: A guided visual exercise to reduce anxiety.
  - **Calming Memory**: A soothing tile-matching game with nature symbols.

- **Support Resources**:
  - Dedicated pages for Privacy, Help, and Emergency Resources.

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **ML/AI**: Scikit-learn, NLTK, Pandas (LinearSVC, TF-IDF)
- **Frontend**: HTML5, Vanilla CSS (Custom Design System), JavaScript, Chart.js

## 🚀 Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/sentra.git
    cd sentra
    ```

2.  **Create a virtual environment**:
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Mac/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Download NLTK Data** (First run only):
    The app will automatically download necessary NLTK data (`wordnet`, `omw-1.4`, `stopwords`), but you can also ensure it's ready by running:
    ```bash
    python -c "import nltk; nltk.download('wordnet'); nltk.download('omw-1.4'); nltk.download('stopwords')"
    ```

## 🏃 Usage

1.  **Train the Model** (Optional, pre-trained model included):
    If you want to retrain the model on the dataset:
    ```bash
    python train_model.py
    ```

2.  **Run the Application**:
    ```bash
    python app.py
    ```
    Open your browser and visit `http://127.0.0.1:5000`.

## ⚠️ Disclaimer

**Sentra is not a medical tool.** It is designed for self-reflection and informational purposes only. The AI predictions are based on patterns in text and may not always be accurate.

**If you are in crisis or need immediate help, please contact emergency services or use the resources listed on the `/resources` page of the application.**

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
