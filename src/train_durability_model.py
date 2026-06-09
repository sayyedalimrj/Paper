"""
train_durability_model.py  (Phase 4 — optional, with fallback)
==============================================================
Optional durability modelling (e.g., carbonation depth or chloride-related
indicators) IF a clean public dataset can be obtained.

Fallback policy (no fabricated data): if no suitable public durability dataset
is available, the passport records durability as "not assessed" and this module
documents the gap in ``outputs/progress_log.md`` rather than inventing values.

Phase-4 stub.
"""
from __future__ import annotations


def train(*args, **kwargs):  # pragma: no cover - stub
    raise NotImplementedError(
        "Durability model is optional; implemented in Phase 4 only if a public "
        "dataset is available. Otherwise durability is marked 'not assessed'."
    )
