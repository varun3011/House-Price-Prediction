# 🏡 House Price Prediction — friendly demo

Welcome! This is a small Flask web app that predicts approximate house prices (Bangalore-focused) using a saved ML model. The UI is simple and playful — enter area, pick a location and type, and get a quick estimate.

Badges
- Python | Flask | Machine Learning | Web UI

Why this repo exists
- Quickly demo an ML model behind a lightweight web UI.
- Provide a place to experiment with forms, templates and embedding dashboards.

Quick contract (what I changed/tested)
- Inputs: total_sqft (integer), location (string from `artifacts/columns.json`), Type (radio: apartment/villa)
- Output: an estimated price printed on the page and a category label (Lakhs/Crore/Crores)
- Error modes: missing artifacts or model file -> app raises an exception on startup; missing MongoDB -> comment route will fail when used

Getting started (copy-paste)

Prerequisites
- Python 3.8+ (recommended)
- Git (optional)
- Optional: MongoDB running locally for comment persistence

Install & run

```bash
# create and activate venv
python3 -m venv .venv
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt

# verify artifacts exist: ./artifacts/columns.json and the pickled model
# start the app (default: 0.0.0.0:80)
python server.py

# OR run Flask on port 5000 for local dev
export FLASK_APP=server.py
python -m flask run --host=0.0.0.0 --port=5000
```

Open http://localhost:5000 and try the form.

What to expect on the UI
- Left panel: enter Area (sq ft), pick Location, choose Apartment or Villa, then Submit.
- Right panel: estimated price and category. If you select a location, the map attempts to center on its coordinates (Google Maps key must be added in `templates/index1.html`).

Important files
- `server.py` — Flask app and routes (`/`, `/submit-comment`, `/dashboard_`).
- `util.py` — loads `artifacts/columns.json` and the pickled model `banglore_home_prices_model_random.pickle`; exposes `get_estimated_price`, `get_location_names`, `load_saved_artifacts`, `type_price`.
- `form.py` — Flask-WTF form definition.
- `templates/index1.html` and `templates/dashboard.html` — user-facing templates.
- `artifacts/` — must contain the model and columns metadata.

Developer notes & gotchas
- `util.type_price` contains oddly-named parameters and some obfuscated computation; it currently returns a numeric value. If you refactor it, keep inputs/outputs identical.
- `util.load_saved_artifacts()` expects `artifacts/columns.json` with `data_columns`; the location list is taken from items after the first three columns.
- `server.py` uses a hard-coded `SECRET_KEY` and connects to MongoDB at `mongodb://localhost:27017/`. For production, move these to environment variables.
- Google Maps API key in `templates/index1.html` is blank — add your key to enable map rendering.

Edge cases to watch
- Missing artifact files -> startup failure when `util.load_saved_artifacts()` is called.
- Locations not found in `data_columns` -> `get_estimated_price` treats them as unknown (model input will have no one-hot feature for that location).
- Very small or invalid `total_sqft` values -> client-side validators require a minimum (see `form.py`), but server code casts to int directly; unexpected values can cause exceptions.

Quick improvements I can implement next (pick one)
1. Cleanup `util.type_price` (remove obfuscation + clearer logic). Small, low risk.
2. Add a Dockerfile + docker-compose with a MongoDB service for one-command local runs.
3. Add a minimal pytest unit test around `util.load_saved_artifacts()` using temporary files / mocks.

If you want a creative touch: I can add a small CSS animation to the estimated price or a playful emoji-based output depending on price range.

License
- No license file is included. Add one if you plan to open-source.

Thanks — tell me which of the quick improvements you'd like and I'll make it happen! 🎯
