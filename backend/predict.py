
import pickle
import pandas as pd

# Load trained pipeline
pipe = pickle.load(open('pipe.pkl', 'rb'))

def predict_win_probability(
    batting_team,
    bowling_team,
    city,
    runs_left,
    balls_left,
    wickets,
    total_runs_x,
    crr,
    rrr
):
    
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

    prob = pipe.predict_proba(input_df)[0]

    return {
        # "lose_probability": round(prob[0] * 100, 2),
        "win_probability": round(prob[1] * 100, 2)
    }


# if __name__ == "__main__": result = predict_win_probability( batting_team="Mumbai Indians", bowling_team="Chennai Super Kings", city="Mumbai", runs_left=45, balls_left=30, wickets=6, total_runs_x=180, crr=9.0, rrr=9.0 )
# print(result)
