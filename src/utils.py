"""
utils.py
========
Shared helper utilities: reproducibility, logging, I/O, metrics, and a small
progress-log appender so every phase leaves a durable, restartable trail.
"""
from __future__ import annotations

import json
import logging
import os
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable

import numpy as np

try:
    from src import config
except ImportError:  # when executed as a script from within src/
    import config  # type: ignore


# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------
def get_logger(name: str = "cpp") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        fmt = logging.Formatter("[%(asctime)s] %(levelname)s %(name)s: %(message)s")
        handler.setFormatter(fmt)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


LOG = get_logger()


# -----------------------------------------------------------------------------
# Reproducibility
# -----------------------------------------------------------------------------
def set_seed(seed: int = config.RANDOM_SEED) -> None:
    """Seed all relevant RNGs for reproducible runs."""
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    LOG.info("Random seed set to %d", seed)


# -----------------------------------------------------------------------------
# I/O helpers
# -----------------------------------------------------------------------------
def save_json(obj: Any, path: Path | str, indent: int = 2) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=indent, default=_json_default)
    LOG.info("Saved JSON -> %s", path)
    return path


def load_json(path: Path | str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _json_default(o: Any):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.ndarray,)):
        return o.tolist()
    if isinstance(o, (datetime,)):
        return o.isoformat()
    return str(o)


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# -----------------------------------------------------------------------------
# Regression metrics (no hard sklearn dependency for the formulas themselves)
# -----------------------------------------------------------------------------
def regression_metrics(y_true: Iterable[float], y_pred: Iterable[float]) -> Dict[str, float]:
    y_true = np.asarray(list(y_true), dtype=float)
    y_pred = np.asarray(list(y_pred), dtype=float)
    err = y_true - y_pred
    mae = float(np.mean(np.abs(err)))
    rmse = float(np.sqrt(np.mean(err ** 2)))
    ss_res = float(np.sum(err ** 2))
    ss_tot = float(np.sum((y_true - y_true.mean()) ** 2))
    r2 = float(1.0 - ss_res / ss_tot) if ss_tot > 0 else float("nan")
    # Mean absolute percentage error, guarding against divide-by-zero.
    nz = y_true != 0
    mape = float(np.mean(np.abs(err[nz] / y_true[nz])) * 100.0) if nz.any() else float("nan")
    return {"mae": mae, "rmse": rmse, "r2": r2, "mape": mape}


# -----------------------------------------------------------------------------
# Progress log appender
# -----------------------------------------------------------------------------
def append_progress(
    phase: str,
    completed: Iterable[str] | None = None,
    files: Iterable[str] | None = None,
    decisions: Iterable[str] | None = None,
    problems: Iterable[str] | None = None,
    next_actions: Iterable[str] | None = None,
    log_path: Path | str = config.PROGRESS_LOG,
) -> None:
    """Append a structured, timestamped entry to outputs/progress_log.md."""
    log_path = Path(log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    def _block(title: str, items: Iterable[str] | None) -> str:
        items = list(items or [])
        if not items:
            return ""
        body = "\n".join(f"  - {i}" for i in items)
        return f"- **{title}:**\n{body}\n"

    entry = [f"\n### {utc_timestamp()} — {phase}\n"]
    entry.append(_block("Completed", completed))
    entry.append(_block("Files created/modified", files))
    entry.append(_block("Key decisions", decisions))
    entry.append(_block("Problems encountered", problems))
    entry.append(_block("Next actions", next_actions))
    text = "".join(entry)

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(text)
    LOG.info("Appended progress entry for phase: %s", phase)
