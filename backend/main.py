from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd

# app = Flask(__name__)
import os
from flask import Flask, render_template, request, jsonify

# This automatically finds the absolute directory path where main.py sits
current_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(current_dir, 'templates'),
    static_folder=os.path.join(current_dir, 'static')
)


with open('pipe.pkl', 'rb') as f:
    pipe = pickle.load(f)

@app.route('/')
def home():
    # Renders the main HTML page
    return render_template('index.html')



@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data sent from the JavaScript frontend
        data = request.json
        
        # Extract features from the JSON request
        batting_team = data.get('batting_team')
        bowling_team = data.get('bowling_team')
        city = data.get('city')
        runs_left = int(data.get('runs_left'))
        balls_left = int(data.get('balls_left'))
        wickets = int(data.get('wickets'))
        total_runs_x = int(data.get('total_runs_x'))
        crr = float(data.get('crr'))
        rrr = float(data.get('rrr'))

        # Create the DataFrame required by your pipeline
        input_df = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'city': [city],
            'runs_left': [runs_left],
            'balls_left': [balls_left],
            'wickets': [wickets],
            'total_runs_x': [total_runs_x],
            'crr': [crr],
            'rrr': [rrr]
        })

        # Predict probability
        prob = pipe.predict_proba(input_df)[0]
        
        win_prob = round(prob[1] * 100, 2)
        lose_prob = round(prob[0] * 100, 2)

        # Return the response as JSON
        return jsonify({
            "status": "success",
            "batting_team": batting_team,
            "bowling_team": bowling_team,
            "win_probability": win_prob,
            "lose_probability": lose_prob
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
