## Summary

Describe the change and why it is needed for `Enterprise-Commodities-GraphRAG-Dave`.

## Checklist

- [ ] I updated the ontology, model, or scripts only where necessary for this change.
- [ ] I regenerated derived graph artifacts if source YAML or extraction logic changed.
- [ ] I ran the local validation flow:
      `python scripts/extract_graph_claims.py`
      `python scripts/generate_neo4j_seed.py`
      `python scripts/generate_neo4j_seed.py --input ontology/model/phase1_enriched.yaml --output ontology/neo4j/seed_enriched.cypher`
- [ ] I verified that generated YAML/Cypher files are consistent with the ontology.
- [ ] I updated documentation if workflow, schema, or corpus format changed.
- [ ] I confirmed this change does not introduce unsupported node labels, edge types, or invalid IDs.

## Changes

- 

## Validation Notes

- 

## Risks

- 

## Repo

- Repository: `Enterprise-GraphRAG-Study/Enterprise-Commodities-GraphRAG-Dave`
