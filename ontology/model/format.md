# YAML Authoring Contract

This format is the portable source-of-truth for ontology instances.

## Structure

```yaml
metadata:
  dataset_id: phase1-demo
  version: 1
  as_of: 2026-03-04

nodes:
  Commodity:
    - id: COM:OIL_BRENT
      name: Brent crude oil
      category: Energy
      unit_standard: USD/bbl
  Country:
    - id: CTY:IDN
      name: Indonesia
      iso_code: IDN
      region: Asia
  Indicator:
    - id: INDIC:US_10Y_REAL_YIELD
      name: US 10Y real yield
      indicator_type: RealYield
      unit: percent

relationships:
  - type: EXPORTS
    from: CTY:IDN
    to: COM:NICKEL_CLASS1
    properties:
      share: 0.38
      as_of: 2026-02-28T00:00:00Z
      source_id: DOC:REUTERS-2026-03-IDN-NICKEL
```

## Rules

### `metadata`

Recommended fields:

- `dataset_id`
- `version`
- `as_of`
- `description`

### `nodes`

- Keys are node labels.
- Values are arrays of node objects.
- Each node must have a unique `id`.
- Labels should match the ontology labels exactly.
- Node properties should remain flat unless there is a strong reason to nest them.

### `relationships`

- `type` must match the canonical edge name.
- `from` and `to` reference canonical node IDs.
- `properties` is optional.
- Relationship direction is explicit and should match the ontology spec.

## Temporal values

Use ISO 8601 strings for:

- `as_of`
- `start_time`
- `end_time`
- `published_at`

## Numeric values

Keep numeric measures as numbers, not strings:

- `value`
- `share`
- `severity`
- `confidence`
- `strength`

## Recommended validation checks

- every node `id` is unique across the file
- every relationship endpoint exists
- every `Observation.source_id` points to a `Document.id` or external source namespace
- every `Claim.source_id` points to a `Document.id`
- every `Policy` record is also valid as an `Event`
- every `Indicator` uses a stable canonical ID and unit

## Notes on subtypes

For Neo4j, subtype labels such as `Policy` can also be emitted with multiple labels, for example `:Policy:Event`.

In YAML, keep subtype instances under their most specific label:

```yaml
nodes:
  Policy:
    - id: EV:2026-03-IDN-NICKEL-EXPORT_RESTRICTION
      name: Indonesia nickel export restriction
      event_type: Regulatory
      policy_type: ExportRestriction
      start_time: 2026-03-01T00:00:00Z
      summary: Indonesia tightened nickel export rules.
```

The generator can then attach the broader `Event` label as needed.
