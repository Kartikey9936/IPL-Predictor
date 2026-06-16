# 🏏 IPL Win Predictor

> **Real-time IPL match win probability prediction powered by Machine Learning**

![Build](https://img.shields.io/badge/build-passing-brightgreen) ![License](https://img.shields.io/badge/license-MIT-blue) ![Version](https://img.shields.io/badge/version-1.0.0-orange) ![Python](https://img.shields.io/badge/python-3.10%2B-yellow) ![Flask](https://img.shields.io/badge/flask-3.0%2B-lightgrey)



## 📋 Table of Contents

- [Problem Statement](#-problem-statement)
- [Solution Overview](#-solution-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [System Architecture](#-system-architecture)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Workflow](#-workflow)
- [Problems Faced During Building](#-problems-faced-during-building)
- [Future Improvements](#-future-improvements)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact & Acknowledgements](#-contact--acknowledgements)


---

## 🎯 Problem Statement

### What real problem does this solve?
During an IPL match, fans, commentators, and fantasy sports players constantly try to gauge which team has the upper hand — but this judgment is purely based on gut feeling. There's no accessible, data-driven tool that tells you **exactly** how likely a team is to win at any point in the second innings.

### Who faces this problem?
- 🧑‍💻 **Fantasy sports players** who need to make last-minute substitution decisions
- 📺 **Broadcast commentators** who want data to support live commentary
- 🏟️ **Cricket fans** who want more than just scorecards
- 📊 **Sports analysts** building dashboards and insights tools

### Why are existing solutions not enough?
- Most cricket apps show only raw stats — no win probability in real time
- Existing probability models (like those used in broadcasts) are proprietary, black-box, and unavailable for public use
- There is no simple, open-source, deployable tool that does this with a clean UI

---

## 💡 Solution Overview

### How does this project solve the problem?
IPL Win Predictor takes the **current match situation** as input — batting team, bowling team, city, target, current score, overs, and wickets — and outputs a live **win probability** for both teams. It uses a pre-trained Scikit-Learn ML pipeline trained on historical IPL match data.

### Key insight
Rather than predicting from static pre-match features, the model uses **derived in-game features** like runs left, balls left, current run rate (CRR), and required run rate (RRR), which are the true drivers of second-innings outcomes. This makes the prediction dynamic and meaningful at any point in a match.

---



## 🛠️ Tech Stack

### Frontend
| Technology | Purpose | Why Chosen |
|---|---|---|
| **HTML5** | Page structure | Lightweight, no build step needed |
| **CSS3** | Styling & animations | Custom cricket-themed design with variables |
| **Vanilla JS (ES6+)** | Async API calls & DOM updates | No framework overhead; Fetch API is sufficient |

### Backend
| Technology | Purpose | Why Chosen |
|---|---|---|
| **Python 3.10+** | Core language | Industry standard for ML projects |
| **Flask 3.0** | Web server & API routing | Minimal, unopinionated, easy to learn |
| **Flask-CORS** | Cross-origin request handling | Allows frontend & backend on different ports |
| **Scikit-Learn** | ML model pipeline | Robust, well-documented, battle-tested |
| **Pandas** | DataFrame creation for model input | Required by the trained pipeline |
| **Pickle** | Model serialisation | Native Python, zero dependencies |

### DevOps / Tooling
| Technology | Purpose |
|---|---|
| **pip + venv** | Dependency isolation |
| **Render / Railway** | Cloud deployment target |
| **Git + GitHub** | Version control |

---

## 🏗️ System Architecture

```
                        ┌──────────────────────────────────┐
                        │           USER BROWSER            │
                        │   HTML + CSS + Vanilla JS UI      │
                        │  (index.html, style.css, main.js) │
                        └─────────────┬────────────────────┘
                                      │  POST /predict
                                      │  JSON payload
                                      ▼
                        ┌──────────────────────────────────┐
                        │         FLASK BACKEND             │
                        │           app.py                  │
                        │                                   │
                        │  1. Receive & validate request    │
                        │  2. Derive features:              │
                        │     • runs_left = target - score  │
                        │     • balls_left = 120 - (ov×6)   │
                        │     • crr = score / overs         │
                        │     • rrr = runs_left / balls × 6 │
                        │  3. Build Pandas DataFrame        │
                        └─────────────┬────────────────────┘
                                      │
                                      ▼
                        ┌──────────────────────────────────┐
                        │       SCIKIT-LEARN PIPELINE       │
                        │           pipe.pkl                │
                        │                                   │
                        │  • OneHotEncoder (teams, city)    │
                        │  • Feature scaling (if any)       │
                        │  • Classifier (LogReg / RFC / XGB)│
                        │  • predict_proba() → [lose, win]  │
                        └─────────────┬────────────────────┘
                                      │
                                      ▼
                        ┌──────────────────────────────────┐
                        │        JSON RESPONSE              │
                        │  {                                │
                        │    batting_win_probability: 67.4  │
                        │    bowling_win_probability: 32.6  │
                        │    runs_left: 45                  │
                        │    balls_left: 30                 │
                        │    crr: 9.0, rrr: 9.0             │
                        │  }                                │
                        └──────────────────────────────────┘
```

### Data Flow — Input to Output

```
User fills form
     ↓
JS validates locally (empty fields, same team, score ≥ target)
     ↓
POST /predict → Flask receives JSON
     ↓
Flask derives [runs_left, balls_left, wickets, crr, rrr]
     ↓
Pandas DataFrame built with 9 features
     ↓
pipe.pkl → predict_proba() called
     ↓
Win probabilities returned as JSON
     ↓
JS renders animated bar, winner callout, stat chips
```

---

## 📁 Project Structure

```
football-prediction/              # Root project directory
│
├── myenv/                        # Python virtual environment (local dev, not committed)
├── requirements.txt              # Pinned production dependencies
│
└── backend/                      # Main application package
    ├── app.py                    # Flask server: routes, feature engineering, API
    ├── pipe.pkl                  # Serialised Scikit-Learn pipeline (trained model)
    ├── predict.py                # Standalone prediction sandbox for quick testing
    │
    ├── templates/
    │   └── index.html            # Jinja2 template: cricket-themed interactive UI
    │
    └── static/
        ├── css/
        │   └── style.css         # Full UI styling: tokens, layout, animations
        └── js/
            └── main.js           # Fetch API calls, form validation, result rendering
```

### Key File Responsibilities

| File | Role |
|---|---|
| `app.py` | Entry point; defines `/` and `/predict` routes; all feature derivation logic lives here |
| `pipe.pkl` | The trained ML pipeline; loaded once at startup via `pickle.load` |
| `predict.py` | Offline testing — call `predict_win_probability()` directly without starting the server |
| `index.html` | Jinja2 template; receives `teams` and `cities` lists from Flask at render time |
| `style.css` | Cricket-green dark theme with CSS custom properties for easy theming |
| `main.js` | All client-side logic: validation, async fetch, animated result rendering |

---

## ⚙️ Prerequisites

Make sure the following are installed before setup:

| Software | Minimum Version | Check Command |
|---|---|---|
| Python | 3.10 | `python --version` |
| pip | 23.0 | `pip --version` |
| Git | 2.x | `git --version` |

> ⚠️ **Windows users:** Use `python` and `pip`. On Linux/macOS, use `python3` and `pip3`.

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ipl-win-predictor.git
cd ipl-win-predictor
```

### 2. Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv myenv

# Activate — Windows
myenv\Scripts\activate

# Activate — macOS / Linux
source myenv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify the Model File

Make sure `pipe.pkl` is present in the `backend/` directory. This file is the trained ML pipeline and **must not be deleted**.

```bash
ls backend/pipe.pkl   # Should output the path without error
```

### 5. Run the Flask Server

```bash
cd backend
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### 6. Open the App

Navigate to **[http://localhost:5000](http://localhost:5000)** in your browser.

---

## 🔧 Configuration

The app works out of the box with no `.env` file required for local development. For production deployment, consider these environment variables:

| Variable | Default | Description |
|---|---|---|
| `FLASK_ENV` | `development` | Set to `production` on hosting platforms |
| `FLASK_DEBUG` | `True` | Set to `False` in production |
| `PORT` | `5000` | Port Flask listens on (Render sets this automatically) |
| `SECRET_KEY` | *(none)* | Add if you extend the app with sessions or auth |

### Example `.env` file (for production)

```env
FLASK_ENV=production
FLASK_DEBUG=False
PORT=10000
SECRET_KEY=your-random-secret-key-here
```

---

## 📖 Usage

### Running the App

```bash
# Activate venv first
source myenv/bin/activate   # or myenv\Scripts\activate on Windows

cd backend
python app.py
# Open http://localhost:5000
```

### API Endpoints

#### `GET /`
Returns the rendered HTML frontend.

---

#### `POST /predict`

Predict win probability for the current match situation.

**Request:**
```http
POST /predict
Content-Type: application/json
```

```json
{
  "batting_team": "Mumbai Indians",
  "bowling_team": "Chennai Super Kings",
  "city": "Mumbai",
  "target": 180,
  "current_score": 100,
  "overs_done": 12.3,
  "wickets_fallen": 3
}
```

**Success Response `200`:**
```json
{
  "batting_team": "Mumbai Indians",
  "bowling_team": "Chennai Super Kings",
  "batting_win_probability": 67.42,
  "bowling_win_probability": 32.58,
  "runs_left": 80,
  "balls_left": 45,
  "crr": 8.0,
  "rrr": 10.67
}
```

**Error Response `400`:**
```json
{
  "error": "Batting and bowling teams must be different."
}
```

### Supported Teams

| # | Team |
|---|---|
| 1 | Mumbai Indians |
| 2 | Chennai Super Kings |
| 3 | Royal Challengers Bangalore |
| 4 | Kolkata Knight Riders |
| 5 | Delhi Capitals |
| 6 | Punjab Kings |
| 7 | Rajasthan Royals |
| 8 | Sunrisers Hyderabad |
| 9 | Gujarat Titans |
| 10 | Lucknow Super Giants |

---

## 🔄 Workflow

Here's exactly what happens from the moment a user submits the form:

```
Step 1 — User fills the form
         Teams, city, target, current score, overs, wickets fallen

Step 2 — Client-side validation (main.js)
         ├── All fields filled?
         ├── Batting ≠ Bowling team?
         ├── Current score < Target?
         └── Overs < 20?

Step 3 — POST /predict sent via Fetch API
         JSON body constructed and sent asynchronously

Step 4 — Flask receives request (app.py)
         ├── Parses JSON body
         ├── Derives features:
         │     runs_left  = target - current_score
         │     balls_left = 120 - (overs_done × 6)
         │     wickets    = 10 - wickets_fallen
         │     crr        = current_score / overs_done
         │     rrr        = (runs_left / balls_left) × 6
         └── Validates edge cases (balls_left > 0, etc.)

Step 5 — ML prediction (pipe.pkl)
         ├── Pandas DataFrame constructed with 9 features
         ├── Pipeline applies preprocessing (encoding, scaling)
         └── predict_proba() returns [P(loss), P(win)]

Step 6 — JSON response sent back
         Win probabilities, derived stats returned

Step 7 — Frontend renders result (main.js)
         ├── Animated probability bar fills left (batting) & right (bowling)
         ├── Winner callout displayed
         └── Stat chips show runs left, balls left, CRR, RRR
```

---

## 🐛 Problems Faced During Building

### Problem 1 — Feature Mismatch Between Training and Inference

❌ **Problem:** The model was trained with specific column names and order, but the inference DataFrame had columns in a different order, causing silent wrong predictions.

🔍 **Cause:** Pandas DataFrames passed to Scikit-Learn pipelines are order-sensitive when using `ColumnTransformer` without explicit column selection.

✅ **Fix:** Explicitly defined the column order in `predict_win_probability()` to exactly match the training feature order.

📖 **Learning:** Always document and enforce feature column order in ML pipelines. Add an assertion check during inference.

---

### Problem 2 — `predict_proba` Returns Reversed Class Order

❌ **Problem:** The model was outputting `prob[0]` as win probability, which gave inverted results (teams that should be losing showed high win chances).

🔍 **Cause:** Scikit-Learn's `predict_proba()` returns probabilities ordered by `clf.classes_`, which may not always be `[0=loss, 1=win]` depending on how labels were encoded during training.

✅ **Fix:** Inspected `pipe.named_steps['classifier'].classes_` to confirm class order, then correctly used `prob[1]` for win probability.

📖 **Learning:** Always verify `clf.classes_` before indexing `predict_proba()` output.

---

### Problem 3 — CORS Error When Calling API from Frontend

❌ **Problem:** Browser blocked the `POST /predict` request from the frontend with a CORS policy error.

🔍 **Cause:** Flask doesn't allow cross-origin requests by default. During development, the frontend was served from a different port than the API.

✅ **Fix:** Added `flask-cors` and called `CORS(app)` in `app.py`.

📖 **Learning:** Always add CORS handling early in Flask projects that serve a separate frontend.

---

### Problem 4 — Division by Zero When Overs = 0

❌ **Problem:** App crashed with `ZeroDivisionError` when `overs_done` was set to 0.

🔍 **Cause:** CRR calculation `current_score / overs_done` fails when no overs have been bowled yet.

✅ **Fix:** Added a guard: `crr = current_score / overs_done if overs_done > 0 else 0`

📖 **Learning:** Always guard against zero-division in derived feature calculations; never trust user input.

---

### Problem 5 — Pickle File Not Found on Render Deployment

❌ **Problem:** App worked locally but crashed on Render with `FileNotFoundError: pipe.pkl`.

🔍 **Cause:** `pickle.load(open('pipe.pkl', 'rb'))` uses a relative path, which resolves to the working directory — which differs between local dev and Render's deployment environment.

✅ **Fix:** Changed to an absolute path using `os.path`:
```python
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
pipe = pickle.load(open(os.path.join(BASE_DIR, 'pipe.pkl'), 'rb'))
```

📖 **Learning:** Always use `__file__`-relative absolute paths for loading model files in production.

---

## 🚀 Future Improvements

### What I'd add with more time

- 📈 **Ball-by-ball probability chart** — A live Recharts/Chart.js line graph showing how win probability evolved over the innings
- 🔄 **Live match integration** — Connect to a cricket data API (Cricbuzz / CricAPI) for real-time score ingestion
- 🏆 **Tournament bracket view** — Full IPL 2025 schedule with predicted outcomes for upcoming matches
- 🤖 **Model comparison dashboard** — Show predictions from Logistic Regression vs Random Forest vs XGBoost side by side


### Known Limitations

- The model is only accurate for **second innings predictions** — it's not designed for first innings forecasting
- City encoding in the model only covers venues where IPL matches historically took place; new venues will fail
- The model does not account for **player-level features** (e.g., key batsman at crease, bowler on strike)

### Roadmap

| Milestone | Status |
|---|---|
| v1.0 — Core prediction with Flask + HTML UI | ✅ Done |
| v1.1 — Improved UI with animated result card | ✅ Done |
| v1.2 — Deploy to Render with absolute path fix | 🚧 In Progress |
| v2.0 — Live match data integration | 📅 Planned |
| v2.1 — Ball-by-ball chart | 📅 Planned |

---


### Acknowledgements & References

- 📊 **IPL Dataset** — [Kaggle IPL Ball-by-Ball Dataset](https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020)
- 🤖 **Scikit-Learn** — [scikit-learn.org](https://scikit-learn.org)
- 🌐 **Flask Documentation** — [flask.palletsprojects.com](https://flask.palletsprojects.com)
- 🎨 **Design Inspiration** — ESPN Cricinfo & ICC live match interfaces


---

<div align="center">

**Built with ❤️ and 🏏 for cricket fans everywhere**

⭐ Star this repo if you found it useful!

</div>
