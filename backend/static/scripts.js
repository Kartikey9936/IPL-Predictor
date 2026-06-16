document.getElementById('predictionForm').addEventListener('submit', async function(e) {
    e.preventDefault(); // Stop page refresh

    // Gather input data from the form
    const formData = {
        batting_team: document.getElementById('batting_team').value,
        bowling_team: document.getElementById('bowling_team').value,
        city: document.getElementById('city').value,
        total_runs_x: document.getElementById('total_runs_x').value,
        runs_left: document.getElementById('runs_left').value,
        balls_left: document.getElementById('balls_left').value,
        wickets: document.getElementById('wickets').value,
        crr: document.getElementById('crr').value,
        rrr: document.getElementById('rrr').value
    };

    // Edge check: Prevent predicting matching teams against each other
    if (formData.batting_team === formData.bowling_team) {
        alert("Batting and Bowling teams cannot be the same!");
        return;
    }

    try {
        // Send data to Flask backend
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();

        if (result.status === 'success') {
            // Unhide result display
            const resultCard = document.getElementById('resultCard');
            resultCard.classList.remove('hidden');

            // Animate probability bar graph
            const winBar = document.getElementById('winBar');
            winBar.style.width = `${result.win_probability}%`;

            // Display descriptive results text
            document.getElementById('resultText').innerHTML = `
                ${result.batting_team}: <span style="color:#22c55e">${result.win_probability}%</span> Chance<br>
                ${result.bowling_team}: <span style="color:#ef4444">${result.lose_probability}%</span> Chance
            `;
        } else {
            alert("Error in prediction: " + result.message);
        }

    } catch (error) {
        console.error("Error connecting to server:", error);
        alert("Failed to connect to the backend server.");
    }
});