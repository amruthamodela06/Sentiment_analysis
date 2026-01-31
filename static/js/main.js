document.addEventListener('DOMContentLoaded', () => {
    const inputField = document.getElementById('text-input');
    const analyzeBtn = document.getElementById('analyze-btn');
    const clearBtn = document.getElementById('clear-btn');
    const resultPreview = document.getElementById('result-preview');
    const moodDisplay = document.getElementById('mood-display');
    const moodDesc = document.getElementById('mood-desc');

    // --- State Management ---
    let currentAnalysis = null;

    // --- Actions ---
    analyzeBtn.addEventListener('click', async () => {
        const text = inputField.value.trim();
        if (!text) return;

        // UI Loading State (Optional: Add spinner)
        analyzeBtn.textContent = "Analyzing...";
        analyzeBtn.disabled = true;

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
            const data = await response.json();

            // Render Result
            showResult(data);

            // Save state for layout switching (if we implemented SPA)
            currentAnalysis = data;

        } catch (error) {
            console.error(error);
            alert("Something went wrong. Please try again.");
        } finally {
            analyzeBtn.textContent = "Analyze";
            analyzeBtn.disabled = false;
        }
    });

    clearBtn.addEventListener('click', () => {
        inputField.value = '';
        resultPreview.classList.remove('active');
        inputField.focus();
    });

    function showResult(data) {
        // Mocking 'Gentle Description' based on Mood
        const descriptions = {
            'Depression': "Your text reflects heavy emotions. It's okay to feel this way.",
            'Anxiety': "There seems to be some worry or tension in your words.",
            'Suicidal': "We hear deep pain here. Please remember you are not alone.",
            'Normal': "Your text appears to be balanced.",
            'Stress': "It sounds like things might be overwhelming right now.",
            'Bipolar': "Your text shows intense emotional variation.",
            'Personality Disorder': "We detect complex emotional patterns."
        };

        const desc = descriptions[data.mood] || "Analysis complete.";

        // Update DOM
        moodDisplay.textContent = `Mood: ${data.mood}`;
        moodDesc.textContent = desc;

        // Show Section
        resultPreview.classList.add('active');

        // Update link for Detailed View flow
        const detailLink = document.querySelector('.link-detailed');
        detailLink.onclick = (e) => {
            e.preventDefault();
            // Store text to reuse in Layout 2
            sessionStorage.setItem('analysisText', inputField.value);
            window.location.href = '/analyze';
        };

        // Scroll to result slightly
        resultPreview.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
});
