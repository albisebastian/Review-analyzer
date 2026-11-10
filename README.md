# ReviewLens: Customer Review Analyzer

Paste a customer review and get its **sentiment and confidence percentage**: just the winning
sentiment, e.g. *Positive 94.2%*. The result also shows which words drove it (highlighted) and
which topics (delivery, quality, price...) the customer is happy or unhappy about.

It works **out of the box** with a built-in engine, and switches automatically to **your own
Keras model** when you drop the file into `backend/models/`.

## Run it

**Windows:** double-click `run_windows.bat`
**Mac / Linux:** `./run.sh`

Or manually:

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows   (Mac/Linux: source .venv/bin/activate)
pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:8000>. API docs are at `/api/docs`.

## Use your own Keras model (the large `.keras` file)

1. Copy the file into **`backend/models/`**:
   ```
   backend/models/customer_review_analyzer.keras
   backend/models/sentiment_classes.json      (optional)
   ```
   Any `*.keras` filename works. `customer_review_analyzer.keras` and `sentiment_model.keras` are checked first.
2. Install TensorFlow once: `pip install -r requirements-keras.txt`
3. Restart, **or** click the engine pill (top right) → **Reload model**. No restart needed.

The pill shows which engine is active and tells you plainly if something is wrong
(missing TensorFlow, corrupt file, wrong number of classes). The app falls back to the
built-in engine instead of breaking.

Requirements for the model: it accepts a **raw review string** and outputs class
probabilities (the `TextVectorization` layer is saved inside the model, which is what the Colab
notebook and `training/train_model.py` produce). Class order defaults to
`negative, neutral, positive`; override it with `sentiment_classes.json`.
You can also point at a file elsewhere with the `MODEL_PATH` environment variable.

## Train a model from your CSVs

This is the notebook's pipeline as a local script:

```bash
pip install -r requirements-train.txt
python training/train_model.py data1.csv data2.csv
```

It auto-detects the review and rating/sentiment columns (1-2 negative, 3 neutral, 4-5 positive),
trains the same CNN, prints accuracy, and writes the model + `sentiment_classes.json` straight into
`backend/models/`. The original notebook is kept in `training/` for Colab use.

## How the analysis works

| | Built-in engine | Keras model |
|---|---|---|
| Verdict + % | Rule-based: negation (*"not good"*), intensity (*"extremely"*, caps, `!`), contrast (*"nice **but** it broke"*), idioms (*"waste of money"*), star mentions (*"2/5"*), emoji | Your trained CNN's softmax output |
| Highlights + topics + summary | Yes | Yes (always from the built-in engine, so the explanation looks the same either way) |

Set `LEXICON_BLEND=0.3` (0-1) to mix the rule-based verdict into the Keras score, which can help
with negation and mixed reviews. The default `0` uses the model's output unchanged.

The built-in engine is a transparent heuristic, not a trained model. It is a sensible default and
fallback, but a model trained on your own data will be more accurate for your domain.

## Project layout

```
app.py                  start the app
backend/
  main.py               FastAPI: /api/analyze, /api/status, /api/reload + serves the UI
  analyzer.py           combines engines, builds the response
  keras_engine.py       drop-in Keras model loading
  lexicon_engine.py     built-in engine
  lexicon_data.py       word lists (plain data, easy to extend)
  models/               <- put your .keras file here
frontend/               index.html, style.css, app.js (no build step)
training/               train_model.py + original notebook
tests/test_engine.py    sanity checks:  python tests/test_engine.py
```

## Customising

- **Colours:** edit the tokens at the top of `frontend/style.css`. Positive = teal, neutral = blue, negative = near-black.
- **Port / host:** `PORT=9000 python app.py` (default `127.0.0.1:8000`, local only).
- **Topics / vocabulary:** edit `backend/lexicon_data.py`.

## Notes

- English only. Reviews are processed in memory and not stored; recent items live in your browser only.
- The percentage is the model's confidence, not a guarantee of correctness. The display is capped at 99.9%.
- `*.keras` files are git-ignored because of their size.
