document.addEventListener('DOMContentLoaded', () => {
    const moodBtns = document.querySelectorAll('.mood-btn');
    const moodLabel = document.getElementById('selected-mood-label');
    const saveBtn = document.getElementById('save-entry-btn');
    const input = document.getElementById('journal-input');
    const entriesList = document.getElementById('entries-list');
    const saveStatus = document.getElementById('save-status');

    let selectedMood = null;

    // === Mood Selection ===
    moodBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Reset others
            moodBtns.forEach(b => b.style.opacity = '0.5');
            moodBtns.forEach(b => b.style.transform = 'scale(1)');

            // Highlight selected
            btn.style.opacity = '1';
            btn.style.transform = 'scale(1.2)';
            selectedMood = parseInt(btn.dataset.mood);
            moodLabel.textContent = btn.dataset.label;
        });
    });

    // === Load Data ===
    loadEntries();
    renderChart();

    // === Save Entry ===
    saveBtn.addEventListener('click', () => {
        const text = input.value.trim();
        if (!text && !selectedMood) {
            alert("Please write something or select a mood.");
            return;
        }

        const entry = {
            id: Date.now(),
            date: new Date().toLocaleDateString(),
            timestamp: new Date().toISOString(),
            text: text,
            mood: selectedMood
        };

        saveEntryToLocal(entry);

        // Reset UI
        input.value = '';
        selectedMood = null;
        moodBtns.forEach(b => { b.style.opacity = '1'; b.style.transform = 'scale(1)'; });
        moodLabel.textContent = '';

        // Feedback
        saveStatus.style.opacity = '1';
        setTimeout(() => saveStatus.style.opacity = '0', 2000);

        // Reload
        loadEntries();
        renderChart();
    });

    // === LocalStorage Logic ===
    function saveEntryToLocal(entry) {
        let entries = JSON.parse(localStorage.getItem('sentra_journal')) || [];
        entries.unshift(entry); // Add to top
        localStorage.setItem('sentra_journal', JSON.stringify(entries));
    }

    function loadEntries() {
        const entries = JSON.parse(localStorage.getItem('sentra_journal')) || [];

        if (entries.length === 0) {
            entriesList.innerHTML = '<p style="color: #999;">No entries yet.</p>';
            return;
        }

        entriesList.innerHTML = entries.map(entry => `
            <div class="entry-card" style="background: white; padding: 20px; border-radius: 12px; margin-bottom: 16px; box-shadow: 0 4px 10px rgba(0,0,0,0.02);">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="font-weight: 500; font-size: 0.9rem; color: #666;">${entry.date}</span>
                    <span style="font-size: 1.2rem;">${getMoodEmoji(entry.mood)}</span>
                </div>
                <p style="color: #333; white-space: pre-wrap;">${entry.text}</p>
            </div>
        `).join('');
    }

    function getMoodEmoji(score) {
        if (!score) return '';
        const map = { 5: '🌟', 4: '🙂', 3: '😐', 2: '😔', 1: '😣' };
        return map[score] || '';
    }

    // === Chart Logic ===
    function renderChart() {
        const ctx = document.getElementById('moodChart').getContext('2d');
        const entries = JSON.parse(localStorage.getItem('sentra_journal')) || [];

        // Group by Date (Take average mood per day or just last entry)
        // For simplicity: Take last 7 entries reverse chronological -> chronological
        const dataPoints = entries.slice(0, 7).reverse();

        const labels = dataPoints.map(e => e.date.slice(0, 5)); // Just Month/Day
        const data = dataPoints.map(e => e.mood || null);

        if (window.myChart) {
            window.myChart.destroy();
        }

        window.myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Mood Score',
                    data: data,
                    borderColor: '#5C7C7C',
                    backgroundColor: 'rgba(92, 124, 124, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: '#E89B85'
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        min: 0,
                        max: 6,
                        ticks: { stepSize: 1, callback: (v) => getMoodEmoji(v) }
                    }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }
});
