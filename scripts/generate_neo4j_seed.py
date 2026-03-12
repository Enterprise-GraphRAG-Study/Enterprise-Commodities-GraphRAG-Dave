from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

SUBTYPE_LABELS: dict[str, list[str]] = {
    "Policy": ["Policy", "Event"],
}

REQUIRED_NODE_FIELDS: dict[str, set[str]] = {
    "Commodity": {"id", "name", "category", "unit_standard"},
    "Benchmark": {"id", "name", "symbol", "exchange", "currency", "unit"},
    "Indicator": {"id", "name", "indicator_type", "unit"},
    "Country": {"id", "name", "iso_code", "region"},
    "Company": {"id", "name", "sector"},
    "Organization": {"id", "name", "org_type"},
    "Industry": {"id", "name"},
    "Product": {"id", "name"},
    "Asset": {"id", "name", "asset_type"},
    "Event": {"id", "name", "event_type", "start_time", "summary"},
    "Policy": {"id", "name", "event_type", "policy_type", "start_time", "summary"},
    "Mechanism": {"id", "name", "mechanism_type"},
    "Observation": {"id", "metric_type", "value", "unit", "as_of", "granularity", "source_id"},
    "Document": {"id", "doc_type", "title", "publisher", "published_at"},
    "Claim": {"id", "claim_type", "text", "confidence", "source_id"},
}


@dataclass(frozen=True)
class NodeRecord:
    label: str
    payload: dict[str, Any]

    @property
    def node_id(self) -> str:
        return str(self.payload["id"])

    @property
    def labels(self) -> list[str]:
        return SUBTYPE_LABELS.get(self.label, [self.label])


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for seed generation."""
    parser = argparse.ArgumentParser(description="Generate Neo4j seed Cypher from ontology YAML.")
    parser.add_argument(
        "--input",
        default="ontology/model/phase1.yaml",
        help="Path to the ontology YAML file.",
    )
    parser.add_argument(
        "--output",
        default="ontology/neo4j/seed.cypher",
        help="Path to write the generated Cypher file.",
    )
    return parser.parse_args()


def load_yaml(path: Path) -> dict[str, Any]:
    """Load a YAML file and validate that the top level is a mapping."""
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError("Top-level YAML document must be a mapping.")
    return data


def validate_document(data: dict[str, Any]) -> tuple[list[NodeRecord], list[dict[str, Any]]]:
    """Validate ontology data and return normalized node and relationship records."""
    nodes_section = data.get("nodes")
    relationships = data.get("relationships")

    if not isinstance(nodes_section, dict):
        raise ValueError("`nodes` must be a mapping of labels to node arrays.")
    if not isinstance(relationships, list):
        raise ValueError("`relationships` must be a list.")

    records: list[NodeRecord] = []
    seen_ids: dict[str, str] = {}

    for label, entries in nodes_section.items():
        if label not in REQUIRED_NODE_FIELDS:
            raise ValueError(f"Unknown node label `{label}`.")
        if not isinstance(entries, list):
            raise ValueError(f"`nodes.{label}` must be a list.")

        for entry in entries:
            if not isinstance(entry, dict):
                raise ValueError(f"Node entry under `{label}` must be a mapping.")
            missing = REQUIRED_NODE_FIELDS[label] - set(entry)
            if missing:
                raise ValueError(
                    f"Node `{entry.get('id', '<missing id>')}` is missing required fields for `{label}`: "
                    + ", ".join(sorted(missing))
                )
            node_id = str(entry["id"])
            if node_id in seen_ids:
                raise ValueError(f"Duplicate node id `{node_id}` found in `{label}` and `{seen_ids[node_id]}`.")
            seen_ids[node_id] = label
            records.append(NodeRecord(label=label, payload=entry))

    node_ids = set(seen_ids)
    document_ids = {record.node_id for record in records if "Document" in record.labels}
    policy_ids = {record.node_id for record in records if record.label == "Policy"}

    for relationship in relationships:
        if not isinstance(relationship, dict):
            raise ValueError("Each relationship entry must be a mapping.")
        for field in ("type", "from", "to"):
            if field not in relationship:
                raise ValueError(f"Relationship is missing required field `{field}`.")
        if relationship["from"] not in node_ids:
            raise ValueError(f"Relationship source `{relationship['from']}` does not exist.")
        if relationship["to"] not in node_ids:
            raise ValueError(f"Relationship target `{relationship['to']}` does not exist.")

    for record in records:
        if record.label == "Observation":
            source_id = str(record.payload["source_id"])
            if not (source_id in document_ids or ":" in source_id):
                raise ValueError(f"Observation `{record.node_id}` has invalid source_id `{source_id}`.")
        if record.label == "Claim":
            source_id = str(record.payload["source_id"])
            if source_id not in document_ids:
                raise ValueError(f"Claim `{record.node_id}` has source_id `{source_id}` not present as a Document.")
        if record.label == "Policy" and record.node_id in policy_ids:
            missing_event_fields = REQUIRED_NODE_FIELDS["Event"] - set(record.payload)
            if missing_event_fields:
                raise ValueError(
                    f"Policy `{record.node_id}` is missing Event fields: " + ", ".join(sorted(missing_event_fields))
                )

    return records, relationships


def quote_string(value: str) -> str:
    """Escape a string for safe Cypher output."""
    escaped = value.replace("\\", "\\\\").replace("'", "\\'")
    return f"'{escaped}'"


def render_scalar(value: Any) -> str:
    """Render a Python scalar value as a Cypher literal."""
    if isinstance(value, datetime):
        return f"datetime({quote_string(value.isoformat().replace('+00:00', 'Z'))})"
    if isinstance(value, date):
        return quote_string(value.isoformat())
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return repr(value)
    if value is None:
        return "null"

    text = str(value)
    if looks_like_datetime(text):
        return f"datetime({quote_string(text)})"
    return quote_string(text)


def looks_like_datetime(value: str) -> bool:
    """Return whether a string matches the narrow ISO-8601 format emitted into Cypher."""
    if len(value) < 20:
        return False
    if not (value[:4].isdigit() and value[5:7].isdigit() and value[8:10].isdigit()):
        return False
    if value[4] != "-" or value[7] != "-" or value[10] != "T":
        return False
    return value.endswith("Z")


def render_map(payload: dict[str, Any], indent: int = 0) -> str:
    """Render a flat property mapping as a Cypher map."""
    pad = " " * indent
    inner_pad = " " * (indent + 2)
    items = list(payload.items())
    if not items:
        return "{}"
    if len(items) == 1:
        key, value = items[0]
        return f"{{{key}: {render_scalar(value)}}}"

    lines = ["{"]
    for index, (key, value) in enumerate(items):
        suffix = "," if index < len(items) - 1 else ""
        lines.append(f"{inner_pad}{key}: {render_scalar(value)}{suffix}")
    lines.append(f"{pad}}}")
    return "\n".join(lines)


def render_node(record: NodeRecord) -> str:
    """Render a validated node record as a Cypher MERGE statement."""
    labels = ":".join(record.labels)
    alias = alias_for(record.node_id)
    body = render_map(record.payload, indent=2)
    return f"MERGE ({alias}:{labels} {body})"


def render_relationship(rel: dict[str, Any]) -> str:
    """Render a validated relationship record as a Cypher MERGE statement."""
    src_alias = alias_for(str(rel["from"]))
    dst_alias = alias_for(str(rel["to"]))
    rel_type = str(rel["type"])
    properties = rel.get("properties")
    if properties is None:
        return f"MERGE ({src_alias})-[:{rel_type}]->({dst_alias})"
    if not isinstance(properties, dict):
        raise ValueError(f"Relationship `{rel_type}` properties must be a mapping.")
    body = render_map(properties, indent=2)
    return f"MERGE ({src_alias})-[:{rel_type} {body}]->({dst_alias})"


def alias_for(node_id: str) -> str:
    """Convert a canonical node ID into a safe Cypher variable alias."""
    base = node_id.split(":", 1)[1] if ":" in node_id else node_id
    chars: list[str] = []
    for char in base.lower():
        if char.isalnum():
            chars.append(char)
        else:
            chars.append("_")
    alias = "".join(chars).strip("_")
    if not alias:
        alias = "node"
    if alias[0].isdigit():
        alias = f"n_{alias}"
    return alias


def render_document(metadata: dict[str, Any], records: list[NodeRecord], relationships: list[dict[str, Any]]) -> str:
    """Render the full ontology payload into a deterministic Cypher document."""
    lines: list[str] = [
        "// Seed graph generated from ontology/model YAML.",
        f"// dataset_id: {metadata.get('dataset_id', 'unknown')}",
        f"// version: {metadata.get('version', 'unknown')}",
        "",
    ]

    current_label: str | None = None
    ordered_records = sorted(records, key=lambda record: (record.label, record.node_id))
    for record in ordered_records:
        if record.label != current_label:
            if current_label is not None:
                lines.append("")
            lines.append(f"// {record.label} nodes")
            current_label = record.label
        lines.append(render_node(record))

    lines.append("")
    lines.append("// Relationships")
    for relationship in relationships:
        lines.append(render_relationship(relationship))

    if lines[-1]:
        lines[-1] = lines[-1] + ";"
    return "\n".join(lines) + "\n"


def main() -> int:
    """Generate the Cypher seed file from the ontology YAML input."""
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    data = load_yaml(input_path)
    records, relationships = validate_document(data)
    cypher = render_document(data.get("metadata", {}), records, relationships)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(cypher, encoding="utf-8")

    print(f"Generated {output_path} from {input_path}")
    print(f"Nodes: {len(records)}")
    print(f"Relationships: {len(relationships)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
