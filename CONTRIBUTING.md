# Contributing

## Scope

This repository is for ontology design, curated corpus authoring, extraction logic, and generated Neo4j graph assets for `Enterprise-Commodities-GraphRAG-Dave`.

Changes should improve one of these areas:

- ontology coverage and schema quality
- curated commodity and macro document quality
- extraction reliability and graph correctness
- generation and validation workflow

## Workflow

1. Create a branch from `main`.
2. Make focused changes.
3. Regenerate derived artifacts if you changed source YAML or extraction logic.
4. Open a pull request using the repository template.

## Local Validation

Run these commands before opening a pull request:

```powershell
python scripts\extract_graph_claims.py
python scripts\generate_neo4j_seed.py
python scripts\generate_neo4j_seed.py --input ontology\model\phase1_enriched.yaml --output ontology\neo4j\seed_enriched.cypher
```

If you use the local virtual environment:

```powershell
.\venv\Scripts\python.exe scripts\extract_graph_claims.py
.\venv\Scripts\python.exe scripts\generate_neo4j_seed.py
.\venv\Scripts\python.exe scripts\generate_neo4j_seed.py --input ontology\model\phase1_enriched.yaml --output ontology\neo4j\seed_enriched.cypher
```

## Contribution Guidelines

- Keep IDs stable and uppercase ASCII.
- Do not introduce new node labels or relationship types casually; update the ontology and schema first.
- Prefer small, inspectable corpus additions with clear causal language over large noisy dumps.
- Keep generated assets synchronized with their source files.
- Update `README.md` when workflow or expected outputs change.

## Data Quality Expectations

- Documents should contain explanatory market language, not only raw tables.
- Claims should preserve source linkage through `source_id`.
- Event, observation, and policy records should remain time-aware.
- Relationship endpoints must resolve to valid canonical node IDs.

## Pull Requests

Pull requests should include:

- a short explanation of what changed
- validation notes
- any ontology or data-model implications
- known limitations or follow-up work

Code owner review is configured through `.github/CODEOWNERS`.
