from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


ENTITY_ALIASES: dict[str, tuple[str, ...]] = {
    "COM:GOLD": ("gold", "bullion"),
    "COM:SILVER": ("silver",),
    "COM:OIL_BRENT": ("brent", "oil", "crude"),
    "COM:COPPER_CATHODE": ("copper",),
    "INDIC:US_10Y_REAL_YIELD": ("real yields", "real yield", "us 10y real yield"),
    "INDIC:FED_FUNDS_RATE": ("fed funds", "policy rate", "rates"),
    "INDIC:US_CPI_YOY": ("cpi", "inflation"),
    "INDIC:DXY": ("dxy", "dollar index", "usd", "dollar"),
    "INDIC:CHN_PROPERTY_ACTIVITY": ("china property", "property activity", "chinese property"),
    "ORG:FED": ("federal reserve", "fed"),
    "ORG:OPEC": ("opec", "opec+"),
    "ORG:IEA": ("iea", "international energy agency"),
    "IND:SOLAR": ("solar", "solar manufacturing"),
    "IND:CONSTRUCTION": ("construction", "property"),
    "AS:EGY_SUEZ_CANAL": ("suez", "suez canal", "red sea shipping"),
    "CTY:CHN": ("china", "chinese"),
    "CTY:SAU": ("saudi arabia", "saudi"),
}

CLAIM_RULES: tuple[tuple[str, str, float], ...] = (
    (r"\b(rate hike|rate hikes|holds? rates?|restrictive policy|policy guidance)\b", "policy", 0.78),
    (r"\b(reduced demand|weakened demand|demand slowed|slower .* demand)\b", "demand_change", 0.76),
    (r"\b(increased demand|stronger demand|demand rose|supports? .* demand)\b", "demand_change", 0.76),
    (r"\b(reduced supply|tightened .* supply|supply restraint|production cut|supply cut)\b", "supply_change", 0.8),
    (r"\b(delays?|shipping disruption|freight stress|rerouting)\b", "shipment_delay", 0.77),
    (r"\b(as|after|because|due to|amid|following|lifted by|pressured by|weighed on|supported by)\b", "price_explanation", 0.74),
)

SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


@dataclass(frozen=True)
class ExtractedClaim:
    payload: dict[str, Any]
    about_ids: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract graph-ready claims from curated commodity documents.")
    parser.add_argument(
        "--corpus",
        default="corpus/curated_docs.yaml",
        help="Path to the curated document corpus YAML.",
    )
    parser.add_argument(
        "--base",
        default="ontology/model/phase1.yaml",
        help="Base ontology YAML file to merge extracted records into.",
    )
    parser.add_argument(
        "--claims-output",
        default="ontology/model/extracted_claims.yaml",
        help="Path to write extracted Document/Claim YAML.",
    )
    parser.add_argument(
        "--merged-output",
        default="ontology/model/phase1_enriched.yaml",
        help="Path to write merged ontology YAML.",
    )
    return parser.parse_args()


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a top-level mapping.")
    return data


def split_sentences(body: str) -> list[str]:
    parts = [part.strip() for part in SENTENCE_SPLIT_RE.split(body.strip())]
    return [part for part in parts if part]


def find_entities(sentence: str) -> list[str]:
    found: list[str] = []
    lowered = sentence.lower()

    for entity_id, aliases in ENTITY_ALIASES.items():
        for alias in aliases:
            pattern = rf"(?<![A-Za-z0-9]){re.escape(alias.lower())}(?![A-Za-z0-9])"
            if re.search(pattern, lowered):
                found.append(entity_id)
                break

    return sorted(set(found))


def infer_claim(sentence: str) -> tuple[str, float] | None:
    lowered = sentence.lower()
    for pattern, claim_type, confidence in CLAIM_RULES:
        if re.search(pattern, lowered):
            return claim_type, confidence
    return None


def slugify(text: str) -> str:
    slug = re.sub(r"[^A-Z0-9]+", "_", text.upper()).strip("_")
    return slug[:48] or "CLAIM"


def extract_claims(corpus: dict[str, Any]) -> dict[str, Any]:
    documents = corpus.get("documents")
    if not isinstance(documents, list):
        raise ValueError("Corpus YAML must contain a `documents` list.")

    output: dict[str, Any] = {
        "metadata": {
            "dataset_id": corpus.get("metadata", {}).get("corpus_id", "curated-claims"),
            "version": corpus.get("metadata", {}).get("version", 1),
            "generated_from": "corpus/curated_docs.yaml",
        },
        "nodes": {"Document": [], "Claim": []},
        "relationships": [],
    }

    seen_claim_ids: set[str] = set()

    for document in documents:
        if not isinstance(document, dict):
            raise ValueError("Each corpus document must be a mapping.")

        body = str(document.get("body", "")).strip()
        if not body:
            continue

        doc_payload = {
            "id": document["id"],
            "doc_type": document["doc_type"],
            "title": document["title"],
            "publisher": document["publisher"],
            "published_at": document["published_at"],
        }
        for optional_field in ("url", "summary"):
            if optional_field in document:
                doc_payload[optional_field] = document[optional_field]
        output["nodes"]["Document"].append(doc_payload)

        for index, sentence in enumerate(split_sentences(body), start=1):
            inferred = infer_claim(sentence)
            if inferred is None:
                continue

            about_ids = find_entities(sentence)
            if not about_ids:
                continue

            claim_type, confidence = inferred
            claim_id = f"CLM:{document['id'].split(':', 1)[1]}-{index:02d}-{slugify(sentence)}"
            while claim_id in seen_claim_ids:
                claim_id = f"{claim_id}_X"
            seen_claim_ids.add(claim_id)

            claim_payload = {
                "id": claim_id,
                "claim_type": claim_type,
                "text": sentence,
                "confidence": confidence,
                "source_id": document["id"],
                "start_time": document["published_at"],
            }
            output["nodes"]["Claim"].append(claim_payload)
            output["relationships"].append({"type": "SUPPORTS", "from": document["id"], "to": claim_id})

            for about_id in about_ids:
                output["relationships"].append({"type": "ABOUT", "from": claim_id, "to": about_id})

    return output


def merge_graphs(base: dict[str, Any], extracted: dict[str, Any]) -> dict[str, Any]:
    merged = {
        "metadata": dict(base.get("metadata", {})),
        "nodes": {label: [dict(item) for item in entries] for label, entries in base.get("nodes", {}).items()},
        "relationships": [dict(item) for item in base.get("relationships", [])],
    }

    merged["metadata"]["derived_claim_pack"] = extracted.get("metadata", {}).get("dataset_id", "unknown")

    existing_ids = {
        str(node["id"])
        for entries in merged["nodes"].values()
        for node in entries
        if isinstance(node, dict) and "id" in node
    }

    for label, entries in extracted.get("nodes", {}).items():
        target = merged["nodes"].setdefault(label, [])
        for entry in entries:
            node_id = str(entry["id"])
            if node_id in existing_ids:
                raise ValueError(f"Duplicate node id during merge: {node_id}")
            target.append(dict(entry))
            existing_ids.add(node_id)

    existing_relationships = {relationship_key(rel) for rel in merged["relationships"]}
    for rel in extracted.get("relationships", []):
        key = relationship_key(rel)
        if key not in existing_relationships:
            merged["relationships"].append(dict(rel))
            existing_relationships.add(key)

    return merged


def relationship_key(rel: dict[str, Any]) -> tuple[Any, ...]:
    props = rel.get("properties")
    if isinstance(props, dict):
        prop_items = tuple(sorted(props.items()))
    else:
        prop_items = ()
    return (rel.get("type"), rel.get("from"), rel.get("to"), prop_items)


def write_yaml(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(payload, handle, sort_keys=False, allow_unicode=False)


def main() -> int:
    args = parse_args()
    corpus = load_yaml(Path(args.corpus))
    base = load_yaml(Path(args.base))

    extracted = extract_claims(corpus)
    merged = merge_graphs(base, extracted)

    write_yaml(Path(args.claims_output), extracted)
    write_yaml(Path(args.merged_output), merged)

    claim_count = len(extracted.get("nodes", {}).get("Claim", []))
    doc_count = len(extracted.get("nodes", {}).get("Document", []))
    print(f"Extracted {claim_count} claims from {doc_count} documents.")
    print(f"Wrote claim pack to {args.claims_output}")
    print(f"Wrote merged dataset to {args.merged_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
