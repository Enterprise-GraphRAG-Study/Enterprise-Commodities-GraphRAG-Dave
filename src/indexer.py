"""Index-building utilities for commodity GraphRAG retrieval experiments."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

TOKEN_RE = re.compile(r"[A-Za-z0-9_]+")


@dataclass(frozen=True)
class IndexBundle:
    """Container for generated index artifacts."""

    graph_summary: dict[str, Any]
    node_index: dict[str, dict[str, Any]]
    entity_to_evidence: dict[str, dict[str, list[str]]]
    keyword_inverted_index: dict[str, list[str]]
    temporal_index: list[dict[str, str]]


def build_indices(dataset: dict[str, Any]) -> IndexBundle:
    """Build a minimal set of retrieval-oriented indices from the graph dataset."""
    nodes_section = dataset.get("nodes", {})
    relationships = dataset.get("relationships", [])

    node_index = build_node_index(nodes_section)
    entity_to_evidence = build_entity_to_evidence_index(relationships, node_index)
    keyword_inverted_index = build_keyword_inverted_index(node_index)
    temporal_index = build_temporal_index(node_index)
    graph_summary = build_graph_summary(nodes_section, relationships)

    return IndexBundle(
        graph_summary=graph_summary,
        node_index=node_index,
        entity_to_evidence=entity_to_evidence,
        keyword_inverted_index=keyword_inverted_index,
        temporal_index=temporal_index,
    )


def build_node_index(nodes_section: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Build a canonical node lookup keyed by graph ID."""
    node_index: dict[str, dict[str, Any]] = {}

    for label, entries in nodes_section.items():
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if not isinstance(entry, dict) or "id" not in entry:
                continue
            node_id = str(entry["id"])
            node_index[node_id] = {
                "label": label,
                "name": str(entry.get("name", entry.get("title", node_id))),
                "properties": serialize_value(entry),
            }

    return node_index


def build_entity_to_evidence_index(
    relationships: list[dict[str, Any]],
    node_index: dict[str, dict[str, Any]],
) -> dict[str, dict[str, list[str]]]:
    """Map entity IDs to related claim, document, observation, and event evidence."""
    claim_to_document: dict[str, str] = {}
    claim_to_entities: dict[str, list[str]] = defaultdict(list)
    claim_to_events: dict[str, list[str]] = defaultdict(list)
    entity_to_observations: dict[str, list[str]] = defaultdict(list)

    for rel in relationships:
        rel_type = str(rel.get("type", ""))
        src = str(rel.get("from", ""))
        dst = str(rel.get("to", ""))
        if rel_type == "SUPPORTS" and src.startswith("DOC:") and dst.startswith("CLM:"):
            claim_to_document[dst] = src
        elif rel_type == "ABOUT" and src.startswith("CLM:"):
            claim_to_entities[src].append(dst)
            if dst.startswith("EV:"):
                claim_to_events[src].append(dst)
        elif rel_type == "OF" and src.startswith("OBS:"):
            entity_to_observations[dst].append(src)

    entity_to_evidence: dict[str, dict[str, list[str]]] = {}
    for node_id in node_index:
        entity_to_evidence[node_id] = {
            "claims": [],
            "documents": [],
            "observations": sorted(set(entity_to_observations.get(node_id, []))),
            "events": [],
        }

    for claim_id, entity_ids in claim_to_entities.items():
        for entity_id in entity_ids:
            if entity_id not in entity_to_evidence:
                continue
            entity_to_evidence[entity_id]["claims"].append(claim_id)
            if claim_id in claim_to_document:
                entity_to_evidence[entity_id]["documents"].append(claim_to_document[claim_id])
            entity_to_evidence[entity_id]["events"].extend(claim_to_events.get(claim_id, []))

    for payload in entity_to_evidence.values():
        payload["claims"] = sorted(set(payload["claims"]))
        payload["documents"] = sorted(set(payload["documents"]))
        payload["events"] = sorted(set(payload["events"]))

    return entity_to_evidence


def build_keyword_inverted_index(node_index: dict[str, dict[str, Any]]) -> dict[str, list[str]]:
    """Create a simple lexical inverted index over names, titles, summaries, and texts."""
    postings: dict[str, set[str]] = defaultdict(set)

    for node_id, payload in node_index.items():
        properties = payload.get("properties", {})
        text_parts: list[str] = []
        for field in ("name", "title", "summary", "text", "description"):
            if field in properties and isinstance(properties[field], str):
                text_parts.append(properties[field])

        for token in tokenize(" ".join(text_parts)):
            postings[token].add(node_id)

    return {token: sorted(node_ids) for token, node_ids in sorted(postings.items())}


def build_temporal_index(node_index: dict[str, dict[str, Any]]) -> list[dict[str, str]]:
    """Create a time-sorted index across events, documents, claims, and observations."""
    temporal_entries: list[dict[str, str]] = []

    for node_id, payload in node_index.items():
        properties = payload.get("properties", {})
        timestamp = (
            properties.get("published_at")
            or properties.get("start_time")
            or properties.get("as_of")
            or properties.get("end_time")
        )
        if not isinstance(timestamp, str):
            continue

        temporal_entries.append(
            {
                "id": node_id,
                "label": str(payload["label"]),
                "name": str(payload["name"]),
                "timestamp": timestamp,
            }
        )

    return sorted(temporal_entries, key=lambda item: item["timestamp"], reverse=True)


def build_graph_summary(nodes_section: dict[str, Any], relationships: list[dict[str, Any]]) -> dict[str, Any]:
    """Summarize node counts and relationship counts for quick inspection."""
    node_counts = {
        label: len(entries)
        for label, entries in sorted(nodes_section.items())
        if isinstance(entries, list)
    }
    relationship_counts: dict[str, int] = defaultdict(int)
    for rel in relationships:
        relationship_counts[str(rel.get("type", "UNKNOWN"))] += 1

    return {
        "node_counts": node_counts,
        "relationship_count": len(relationships),
        "relationship_counts": dict(sorted(relationship_counts.items())),
    }


def tokenize(text: str) -> list[str]:
    """Tokenize text into lowercase alphanumeric terms."""
    return [token.lower() for token in TOKEN_RE.findall(text)]


def serialize_value(value: Any) -> Any:
    """Convert runtime values into JSON-safe scalar structures."""
    if isinstance(value, datetime):
        return value.isoformat().replace("+00:00", "Z")
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: serialize_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [serialize_value(item) for item in value]
    return value


def write_index_bundle(bundle: IndexBundle, output_dir: str | Path) -> None:
    """Persist each generated index artifact as an individual JSON file."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    files = {
        "graph_summary.json": bundle.graph_summary,
        "node_index.json": bundle.node_index,
        "entity_to_evidence.json": bundle.entity_to_evidence,
        "keyword_inverted_index.json": bundle.keyword_inverted_index,
        "temporal_index.json": bundle.temporal_index,
    }

    for filename, payload in files.items():
        (output_path / filename).write_text(json.dumps(payload, indent=2), encoding="utf-8")
