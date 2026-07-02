"""自訓模型推論層（D006）。模型檔不存在時回傳 None，讓 detect 降級。"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

_MODEL_PATH = Path(__file__).resolve().parents[1] / "model" / "scam_clf.joblib"


@lru_cache(maxsize=1)
def _model():
    if not _MODEL_PATH.exists():
        return None
    try:
        import joblib

        return joblib.load(_MODEL_PATH)
    except Exception as e:  # noqa: BLE001
        print(f"[model] load failed: {e}")
        return None


def model_available() -> bool:
    return _model() is not None


def predict_proba(text: str) -> float | None:
    """回傳 P(scam) ∈ [0,1]；模型不可用回 None。"""
    clf = _model()
    if clf is None:
        return None
    try:
        return float(clf.predict_proba([text])[0][1])
    except Exception as e:  # noqa: BLE001
        print(f"[model] predict failed: {e}")
        return None
