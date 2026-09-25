# Fake Internship Detection System — Django + React build

Same decision-support system as the original Flask+HTML implementation —
NLP analysis of advertisement text combined with structured employer
credibility indicators, producing a prediction, confidence, uncertainty,
and an explanation — rebuilt with a **Django REST API backend** and a
**React (Vite) frontend**. The `ml/` research pipeline is unchanged.

Trained and tested on your real EMSCAD dataset (17,880 postings, 4.8%
fraudulent) — see `docs/dataset_documentation.md`.

**This tool predicts, it does not verify.** Every result is presented as a
model output, never as confirmed fact.

## Project layout

```
config/         Django project settings, root urls
apps/
  accounts/     Custom User model, register/login (DRF token auth)
  advertisements/  Advertisement model + endpoints
  detection/    Credibility/Prediction/Explanation models, services.py (wraps ml/), views.py
ml/             Research layer: preprocessing, models, uncertainty, XAI, evaluation (unchanged)
frontend/       React (Vite) single-page app
models/         Saved model artefacts
tests/          pytest-django API tests
docs/           Architecture, dataset, API, model, implementation docs
```

## Setup

### 1. Backend (Django)

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env

python manage.py migrate
python -m ml.train_baseline    # trains E2 on ml/data/raw/emscad_research_ready.csv
python manage.py createsuperuser   # optional, for /admin/

python manage.py runserver     # → http://localhost:8000
```

Your prepared dataset is already at
`ml/data/raw/emscad_research_ready.csv` (44 columns, duplicate-aware
train/validation/test split already applied) — no need to regenerate it.

### 2. Frontend (React / Vite)

In a **second terminal**, from the project root:

```bash
cd frontend
npm install
cp .env.example .env    # VITE_API_BASE=http://localhost:8000/api by default
npm run dev             # → http://localhost:5173
```

Open `http://localhost:5173`, register an account, and submit an
advertisement via **Analyse**.

## Run the tests

```bash
pytest              # 8 Django API tests
cd frontend && npm run build   # confirms the frontend compiles cleanly
```

## Key documents

- [`docs/system_architecture.md`](docs/system_architecture.md) — processing flow, app layering, auth model
- [`docs/dataset_documentation.md`](docs/dataset_documentation.md) — your dataset, schema, leakage safeguards
- [`docs/api_documentation.md`](docs/api_documentation.md) — every endpoint, request/response shapes
- [`docs/model_documentation.md`](docs/model_documentation.md) — model registry, currently active model
- [`docs/implementation_notes.md`](docs/implementation_notes.md) — what's verified, what to tighten before deploying (especially authorization)

## Before any shared or deployed use

Read `docs/implementation_notes.md` §3 — in particular, every API view is
currently `AllowAny` rather than enforcing authentication/ownership. Fine
for local development and demoing; tighten before exposing this beyond
your own machine.
