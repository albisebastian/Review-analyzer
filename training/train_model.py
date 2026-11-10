"""Train the CNN review classifier locally (same pipeline as the Colab notebook).

    python training/train_model.py reviews1.csv reviews2.csv

Each CSV needs a review-text column and a sentiment/rating column; the column is
detected automatically (e.g. reviews.text + reviews.rating, review + sentiment).
Ratings 1-2 -> negative, 3 -> neutral, 4-5 -> positive.

Output (default: backend/models/, which the web app watches):
    customer_review_analyzer.keras   the model, text pre-processing included
    sentiment_classes.json           class order used by the model

Needs:  pip install -r requirements-train.txt
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import numpy as np
import pandas as pd

SEED = 42
CLASS_NAMES = ["negative", "neutral", "positive"]
TEXT_CANDIDATES = ["reviews.text", "review_text", "review", "reviews", "text", "content",
                   "comment", "customer_review"]
LABEL_CANDIDATES = ["reviews.rating", "sentiment", "label", "rating", "score", "stars",
                    "class", "polarity"]
DEFAULT_OUT = Path(__file__).resolve().parent.parent / "backend" / "models"


def load_csv(path: str) -> pd.DataFrame:
    for sep, engine in ((",", "python"), (None, "python")):
        for enc in ("utf-8-sig", "cp1252", "latin1"):
            try:
                df = pd.read_csv(path, encoding=enc, sep=sep, engine=engine, on_bad_lines="warn")
                if len(df.columns) > 1:
                    return df
            except Exception:  # noqa: BLE001
                continue
    raise ValueError(f"Could not read {path}")


def find_col(df: pd.DataFrame, candidates: list[str]):
    cols = {str(c).strip().lower(): c for c in df.columns}
    return next((cols[x] for x in candidates if x in cols), None)


def to_sentiment(v):
    if pd.isna(v):
        return None
    s = str(v).strip().lower()
    try:
        n = float(s)
        if 1 <= n <= 2:
            return "negative"
        if n == 3:
            return "neutral"
        if 4 <= n <= 5:
            return "positive"
    except ValueError:
        pass
    s = re.sub(r"[^a-z]", "", s)
    return {"positive": "positive", "pos": "positive", "good": "positive",
            "negative": "negative", "neg": "negative", "bad": "negative",
            "neutral": "neutral", "neu": "neutral", "mixed": "neutral"}.get(s)


def build_dataset(paths: list[str]) -> pd.DataFrame:
    parts = []
    for path in paths:
        df = load_csv(path)
        tc, lc = find_col(df, TEXT_CANDIDATES), find_col(df, LABEL_CANDIDATES)
        print(f"{path}: {len(df)} rows | review column: {tc} | sentiment column: {lc}")
        if tc is None or lc is None:
            print("  skipped: could not find a review-text and a sentiment/rating column")
            continue
        p = df[[tc, lc]].copy()
        p.columns = ["review", "raw_label"]
        p["review"] = p["review"].fillna("").astype(str).str.strip()
        p["sentiment"] = p["raw_label"].apply(to_sentiment)
        parts.append(p[(p.review.str.len() > 0) & p.sentiment.notna()][["review", "sentiment"]])
    if not parts:
        sys.exit("No usable review/label columns found in the given files.")
    data = pd.concat(parts, ignore_index=True).drop_duplicates(["review", "sentiment"])
    print("\nUsable reviews:", len(data))
    print(data.sentiment.value_counts().to_string())
    if set(data.sentiment.unique()) != set(CLASS_NAMES):
        sys.exit("Need all three classes (negative, neutral, positive) in the data.")
    if data.sentiment.value_counts().min() < 2:
        sys.exit("Each class needs at least 2 reviews.")
    return data


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv", nargs="+", help="one or more CSV files")
    ap.add_argument("--out-dir", default=str(DEFAULT_OUT), help="where to save the model")
    ap.add_argument("--name", default="customer_review_analyzer.keras")
    ap.add_argument("--epochs", type=int, default=10)
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--max-tokens", type=int, default=20000)
    ap.add_argument("--seq-len", type=int, default=120)
    args = ap.parse_args()

    import tensorflow as tf
    from sklearn.metrics import classification_report
    from sklearn.model_selection import train_test_split

    np.random.seed(SEED)
    tf.random.set_seed(SEED)

    data = build_dataset(args.csv)
    label_map = {v: i for i, v in enumerate(CLASS_NAMES)}
    X = data.review.astype(str).to_numpy(dtype=str)
    y = np.array([label_map[v] for v in data.sentiment])
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=SEED, stratify=y)
    X_fit, X_val, y_fit, y_val = train_test_split(
        X_train, y_train, test_size=0.15, random_state=SEED, stratify=y_train)

    def as_dataset(texts, labels, shuffle=False):
        # tf.data is the reliable way to feed strings to Keras 3 (numpy str arrays are rejected)
        ds = tf.data.Dataset.from_tensor_slices((tf.constant(texts.tolist(), dtype=tf.string), labels))
        if shuffle:
            ds = ds.shuffle(len(texts), seed=SEED)
        return ds.batch(args.batch_size).prefetch(tf.data.AUTOTUNE)

    vectorizer = tf.keras.layers.TextVectorization(
        max_tokens=args.max_tokens, output_mode="int", output_sequence_length=args.seq_len,
        standardize="lower_and_strip_punctuation")
    vectorizer.adapt(tf.data.Dataset.from_tensor_slices(X_train).batch(256))

    inputs = tf.keras.Input(shape=(), dtype=tf.string, name="review")
    x = vectorizer(inputs)
    x = tf.keras.layers.Embedding(args.max_tokens, 128)(x)
    x = tf.keras.layers.Conv1D(128, 5, activation="relu", padding="same")(x)
    x = tf.keras.layers.GlobalMaxPooling1D()(x)
    x = tf.keras.layers.Dropout(0.35)(x)
    x = tf.keras.layers.Dense(64, activation="relu")(x)
    x = tf.keras.layers.Dropout(0.25)(x)
    outputs = tf.keras.layers.Dense(3, activation="softmax")(x)
    model = tf.keras.Model(inputs, outputs)
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

    stop = tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=2, restore_best_weights=True)
    model.fit(as_dataset(X_fit, y_fit, shuffle=True), validation_data=as_dataset(X_val, y_val),
              epochs=args.epochs, callbacks=[stop])

    test_ds = as_dataset(X_test, y_test)
    _, acc = model.evaluate(test_ds, verbose=0)
    print(f"\nTest accuracy: {acc:.4f}")
    pred = np.argmax(model.predict(test_ds.map(lambda t, _: t), verbose=0), axis=1)
    print(classification_report(y_test, pred, labels=[0, 1, 2], target_names=CLASS_NAMES, zero_division=0))

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    model.save(out / args.name)
    (out / "sentiment_classes.json").write_text(json.dumps(CLASS_NAMES), encoding="utf-8")
    print(f"Saved {out / args.name}\nSaved {out / 'sentiment_classes.json'}")
    print("Restart the app or click 'Reload model' in the engine panel to use it.")


if __name__ == "__main__":
    main()
