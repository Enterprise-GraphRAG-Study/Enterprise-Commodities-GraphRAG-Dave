# Enterprise Commodities GraphRAG

This repository starts with the ontology and graph bootstrap assets for a commodities intelligence system.

The first implementation target is Neo4j because it gives the fastest path to:

- causal graph traversal
- source-aware market intelligence
- GraphRAG retrieval over structured entities and relationships

## Contents

- `ontology/commodity_ontology.md`: ontology specification
- `ontology/model/phase1.yaml`: editable ontology instance data
- `ontology/neo4j/schema.cypher`: constraints and indexes
- `ontology/neo4j/seed.cypher`: generated demo graph for oil, copper, and nickel
- `scripts/generate_neo4j_seed.py`: YAML to Neo4j seed generator

## Initial scope

Phase 1 focuses on a macro-linked commodity graph:

- commodities: gold, silver, Brent crude, copper
- indicators: US real yields, Fed funds, CPI, DXY, China property activity
- institutions: Federal Reserve, OPEC, IEA
- countries: United States, China, Saudi Arabia, Chile, Egypt
- industries: solar, EV batteries, construction
- event mechanisms: rate sensitivity, inflation hedge demand, dollar pressure, supply shock, logistics constraint
- observations: prices, inflation, yields, policy rate, freight stress, China activity

## Usage

Generate the seed data from YAML, then load the schema and seed data.

```powershell
.\venv\Scripts\python.exe scripts\generate_neo4j_seed.py
```

```cypher
:source ontology/neo4j/schema.cypher
:source ontology/neo4j/seed.cypher
```

The seed data is intentionally small and explainable. It is meant to validate ontology shape and causal reasoning before ingesting larger document corpora and time series.

## Claim Extraction Pipeline

A minimal rule-based extraction pipeline is included for curated narrative text.

```powershell
.\venv\Scripts\python.exe scripts\extract_graph_claims.py
.\venv\Scripts\python.exe scripts\generate_neo4j_seed.py --input ontology/model/phase1_enriched.yaml --output ontology/neo4j/seed_enriched.cypher
```

Inputs and outputs:

- `corpus/curated_docs.yaml`: curated narrative documents
- `ontology/model/extracted_claims.yaml`: generated `Document` and `Claim` nodes plus `SUPPORTS` and `ABOUT` edges
- `ontology/model/phase1_enriched.yaml`: merged graph dataset ready for Neo4j seed generation

The extractor is intentionally simple and deterministic. It is a starter ingestion path for relationship-bearing text, not a substitute for a full LLM extraction pipeline.
