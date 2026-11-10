"""Drop-in Keras model support.

Put your trained model in ``backend/models/`` and it is picked up automatically:

    backend/models/customer_review_analyzer.keras     <- from the training notebook
    backend/models/sentiment_classes.json             <- optional, class order

Nothing else needs to change. If the file is missing, TensorFlow is not installed,
or the model can't be loaded, the app falls back to the built-in engine and shows
the reason in the "engine" panel.
"""

from __future__ import annotations

import json
import os
import threading
from pathlib import Path

import numpy as np

MODELS_DIR = Path(os.environ.get("MODELS_DIR", Path(__file__).parent / "models"))
DEFAULT_CLASSES = ["negative", "neutral", "positive"]  # same order as the training notebook
PREFERRED_NAMES = ("customer_review_analyzer.keras", "sentiment_model.keras")
VALID_LABELS = {"negative", "neutral", "positive"}


class KerasEngine:
    def __init__(self, models_dir: Path = MODELS_DIR):
        self.models_dir = Path(models_dir)
        self._model = None
        self._lock = threading.RLock()  # re-entrant: load() warms up via predict()
        self.model_path: Path | None = None
        self.classes: list[str] = list(DEFAULT_CLASSES)
        self.error: str | None = None
        self.tensorflow_installed: bool | None = None

    # ---- discovery -------------------------------------------------------
    def find_model_file(self) -> Path | None:
        explicit = os.environ.get("MODEL_PATH")
        if explicit:
            p = Path(explicit).expanduser()
            return p if p.is_file() else None
        for name in PREFERRED_NAMES:
            p = self.models_dir / name
            if p.is_file():
                return p
        if self.models_dir.is_dir():
            found = sorted(self.models_dir.glob("*.keras"))
            if found:
                return found[0]
        return None

    def _load_classes(self, model_path: Path) -> list[str]:
        for candidate in (model_path.with_name("sentiment_classes.json"),
                          model_path.with_suffix(".classes.json")):
            if candidate.is_file():
                data = json.loads(candidate.read_text(encoding="utf-8"))
                classes = [str(c).strip().lower() for c in data]
                if not classes or not set(classes) <= VALID_LABELS:
                    raise ValueError(
                        f"{candidate.name} must list class names from "
                        f"{sorted(VALID_LABELS)} in the model's output order."
                    )
                return classes
        return list(DEFAULT_CLASSES)

    # ---- lifecycle -------------------------------------------------------
    @property
    def ready(self) -> bool:
        return self._model is not None

    def load(self) -> bool:
        """(Re)load the model from disk. Never raises; sets ``self.error`` instead."""
        with self._lock:
            self._model, self.error, self.model_path = None, None, None
            path = self.find_model_file()
            if path is None:
                return False  # not an error: simply no model supplied yet
            self.model_path = path
            try:
                os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
                import tensorflow as tf  # imported lazily: TensorFlow is optional

                self.tensorflow_installed = True
            except ImportError:
                self.tensorflow_installed = False
                self.error = ("A model file was found but TensorFlow is not installed. "
                              "Run: pip install -r requirements-keras.txt")
                return False
            try:
                self.classes = self._load_classes(path)
                self._model = tf.keras.models.load_model(path, compile=False, safe_mode=True)
                self._tf = tf
                self._warm_up()
                return True
            except Exception as exc:  # noqa: BLE001 - surface any load problem to the UI
                self._model = None
                detail = str(exc)
                if "File not found" in detail or "zip" in detail.lower():
                    detail = ("the file is not a valid .keras archive (was the upload or "
                              "download interrupted?)")
                self.error = f"Could not load {path.name}: {detail}"
                return False

    def _warm_up(self) -> None:
        self.predict("warm up")  # fails early if the model isn't text-in / probabilities-out

    # ---- inference -------------------------------------------------------
    def predict(self, text: str) -> dict[str, float]:
        if self._model is None:
            raise RuntimeError("Keras model is not loaded")
        batch = self._tf.constant([text], dtype=self._tf.string)
        with self._lock:
            raw = self._model(batch, training=False)
        values = np.asarray(raw, dtype="float64").reshape(-1)
        return self._to_scores(values)

    def _to_scores(self, values: np.ndarray) -> dict[str, float]:
        classes = self.classes
        if values.size == 1 and len(classes) != 1:  # sigmoid head -> P(positive)
            p = float(np.clip(values[0], 0, 1))
            values, classes = np.array([1 - p, p]), ["negative", "positive"]
        if values.size != len(classes):
            raise ValueError(
                f"Model returned {values.size} scores but {len(classes)} classes are configured "
                f"({classes}). Fix sentiment_classes.json or retrain."
            )
        if np.any(values < 0) or not np.isclose(values.sum(), 1.0, atol=0.03):
            e = np.exp(values - values.max())  # logits -> probabilities
            values = e / e.sum()
        values = np.clip(values, 0, 1)
        values = values / values.sum()
        scores = {label: 0.0 for label in ("negative", "neutral", "positive")}
        for label, p in zip(classes, values):
            scores[label] += float(p)
        return scores

    # ---- status ----------------------------------------------------------
    def status(self) -> dict:
        return {
            "loaded": self.ready,
            "file": self.model_path.name if self.model_path else None,
            "classes": self.classes if self.ready else None,
            "error": self.error,
            "tensorflow_installed": self.tensorflow_installed,
            "models_dir": str(self.models_dir),
        }
