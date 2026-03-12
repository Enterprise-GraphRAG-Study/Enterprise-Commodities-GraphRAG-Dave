# Ontology Model Format

This directory defines a YAML authoring format for the commodity intelligence graph.

The goal is to keep ontology content editable as structured data and generate database-specific artifacts from it later.

## Files

- `format.md`: authoring contract for nodes and relationships
- `phase1.yaml`: initial dataset aligned with the Neo4j seed graph

## Format summary

Top-level sections:

- `metadata`: dataset metadata
- `nodes`: entities grouped by label
- `relationships`: typed edges with optional properties

Each node must include:

- `id`
- label-specific required properties from `ontology/commodity_ontology.md`

Each relationship must include:

- `type`
- `from`
- `to`

Optional relationship fields:

- `properties`

## Intended workflow

1. Author entities and links in YAML.
2. Validate IDs and required properties.
3. Generate Cypher, JSONL, or API payloads for the target graph store.

This keeps the ontology source-of-truth portable across Neo4j and future backends.

The current starter dataset is intentionally centered on a macro-linked commodity network:

- commodities: gold, silver, Brent crude, copper
- indicators: US real yields, Fed funds, CPI, DXY, China property activity
- institutions: Federal Reserve, OPEC
- sectors: solar, EV batteries, construction
- events: Fed decisions, OPEC supply actions, shipping disruptions, China demand slowdowns

That scope is small enough to manage while still supporting causal GraphRAG questions.
