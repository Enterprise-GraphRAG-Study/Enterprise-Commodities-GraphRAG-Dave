"""Dataset loading helpers for local ontology files and Hugging Face datasets."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

DEFAULT_HF_DATASET_ID = "aaronmat1905/global-commodity-shocks-analysis-data"


def load_yaml_document(path: str | Path) -> dict[str, Any]:
    """Load a YAML document and enforce a mapping top level."""
    resolved_path = Path(path)
    with resolved_path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)

    if not isinstance(data, dict):
        raise ValueError(f"{resolved_path} must contain a top-level mapping.")
    return data


def load_local_graph_dataset(path: str | Path = "ontology/model/phase1.yaml") -> dict[str, Any]:
    """Load the repository's local ontology dataset."""
    return load_yaml_document(path)


def load_huggingface_dataset(dataset_id: str = DEFAULT_HF_DATASET_ID, split: str = "train") -> Any:
    """Load a Hugging Face dataset split on demand.

    The dependency is imported lazily so local graph generation can still run
    without the `datasets` package in minimal environments.
    """
    try:
        from datasets import load_dataset
    except ImportError as exc:
        raise RuntimeError(
            "The `datasets` package is required to load Hugging Face datasets. "
            "Install project dependencies first."
        ) from exc

    return load_dataset(dataset_id, split=split)
