# Commodity Intelligence Ontology

This ontology is designed for a commodities GraphRAG system that needs to answer four classes of questions:

1. Causal explanation
2. Supply chain propagation
3. Geospatial and trade flow analysis
4. Evidence-backed reasoning with time awareness

The design favors a small set of stable entity types, explicit causal mechanisms, and source-linked observations.

## Design principles

- Every time-sensitive fact should include `as_of`, `start_time`, or `end_time`.
- Every extracted or reported fact should carry `source_id`.
- Canonical entities use stable IDs so ingestion pipelines can upsert reliably.
- Documents and claims stay separate from inferred relationships.
- Mechanisms are first-class nodes so the system can explain market moves in analyst language.

## Node labels

### `Commodity`

Represents a tradable physical commodity or commodity specification.

Required properties:

- `id`
- `name`
- `category`
- `unit_standard`

Optional properties:

- `grade_spec`
- `hs_code`
- `description`

Examples:

- `COM:OIL_BRENT`
- `COM:COPPER_CATHODE`
- `COM:NICKEL_CLASS1`

### `Benchmark`

Represents a price identity or benchmark series.

Required properties:

- `id`
- `name`
- `symbol`
- `exchange`
- `currency`
- `unit`

Examples:

- `BM:ICE_BRENT`
- `BM:LME_CU_3M`

### `Indicator`

Represents a macro, financial, or activity series used to explain commodity moves.

Required properties:

- `id`
- `name`
- `indicator_type`
- `unit`

Optional properties:

- `frequency`
- `publisher`
- `description`

Recommended `indicator_type` values:

- `PolicyRate`
- `RealYield`
- `NominalYield`
- `Inflation`
- `DollarIndex`
- `PMI`
- `Activity`

### `Country`

Required properties:

- `id`
- `name`
- `iso_code`
- `region`

### `Company`

Required properties:

- `id`
- `name`
- `sector`

Optional properties:

- `ticker`

### `Organization`

Used for intergovernmental or market institutions.

Required properties:

- `id`
- `name`
- `org_type`

### `Industry`

Represents downstream demand sectors.

Required properties:

- `id`
- `name`

### `Product`

Represents intermediate or finished goods that consume commodities.

Required properties:

- `id`
- `name`

### `Asset`

Represents physical infrastructure or productive assets.

Required properties:

- `id`
- `name`
- `asset_type`

Optional properties:

- `capacity`
- `capacity_unit`
- `status`

Recommended `asset_type` values:

- `Mine`
- `OilField`
- `Refinery`
- `Smelter`
- `FarmRegion`
- `Port`
- `Pipeline`
- `Canal`
- `ShippingLane`

### `Event`

Represents a discrete occurrence that can affect markets.

Required properties:

- `id`
- `name`
- `event_type`
- `start_time`
- `summary`

Optional properties:

- `end_time`
- `severity`
- `confidence`

Recommended `event_type` values:

- `Geopolitical`
- `Weather`
- `Industrial`
- `Logistics`
- `Macroeconomic`
- `Regulatory`

### `Policy`

Subtype of `Event` for state or institutional actions.

Additional recommended properties:

- `policy_type`

Examples:

- `Sanction`
- `ExportRestriction`
- `Quota`
- `Tariff`
- `PriceCap`

### `Mechanism`

Represents the economic transmission channel connecting events to market effects.

Required properties:

- `id`
- `name`
- `mechanism_type`

Recommended `mechanism_type` values:

- `SupplyShock`
- `DemandShock`
- `LogisticsConstraint`
- `InventoryDraw`
- `RiskPremium`
- `FXPassThrough`

### `Observation`

Represents a time series point or reported metric.

Required properties:

- `id`
- `metric_type`
- `value`
- `unit`
- `as_of`
- `granularity`
- `source_id`

Optional properties:

- `currency`
- `change_value`
- `change_basis`

Recommended `metric_type` values:

- `Price`
- `Inventory`
- `Production`
- `Export`
- `Import`
- `FreightRate`
- `FX`
- `InterestRate`
- `PMI`

### `Document`

Represents a source record whose body is stored in a vector system or document store.

Required properties:

- `id`
- `doc_type`
- `title`
- `publisher`
- `published_at`

Optional properties:

- `url`
- `summary`

### `Claim`

Represents a structured assertion extracted from a document.

Required properties:

- `id`
- `claim_type`
- `text`
- `confidence`
- `source_id`

Optional properties:

- `start_time`
- `end_time`

Recommended `claim_type` values:

- `policy`
- `supply_change`
- `demand_change`
- `inventory_change`
- `shipment_delay`
- `price_explanation`

## Relationships

### Market structure

- `(:Benchmark)-[:BENCHMARK_FOR]->(:Commodity)`
- `(:Commodity)-[:SUBSTITUTE_OF {strength}]->(:Commodity)`
- `(:Commodity)-[:COMPLEMENT_OF]->(:Commodity)`

### Geography and actors

- `(:Company)-[:OPERATES_IN]->(:Country)`
- `(:Country)-[:MEMBER_OF]->(:Organization)`
- `(:Asset)-[:LOCATED_IN]->(:Country)`
- `(:Asset)-[:OWNED_BY]->(:Company)`

### Supply chain

- `(:Asset)-[:PRODUCES]->(:Commodity)`
- `(:Country)-[:EXPORTS {share, as_of, source_id}]->(:Commodity)`
- `(:Country)-[:IMPORTS {share, as_of, source_id}]->(:Commodity)`
- `(:Commodity)-[:TRANSPORTED_VIA]->(:Asset)`
- `(:Commodity)-[:INPUT_TO {share, criticality}]->(:Industry)`
- `(:Commodity)-[:INPUT_TO {share, criticality}]->(:Product)`
- `(:Product)-[:USED_IN]->(:Industry)`
- `(:Company)-[:CONSUMES]->(:Commodity)`
- `(:Industry)-[:INCREASES_DEMAND_FOR]->(:Commodity)`

### Events and causal reasoning

- `(:Event)-[:AFFECTS {mode, severity}]->(:Commodity)`
- `(:Event)-[:AFFECTS {mode, severity}]->(:Asset)`
- `(:Event)-[:AFFECTS {mode, severity}]->(:Indicator)`
- `(:Policy)-[:ISSUED_BY]->(:Country)`
- `(:Policy)-[:ISSUED_BY]->(:Organization)`
- `(:Policy)-[:TARGETS]->(:Commodity)`
- `(:Policy)-[:TARGETS]->(:Country)`
- `(:Policy)-[:TARGETS]->(:Company)`
- `(:Organization)-[:SETS]->(:Indicator)`
- `(:Event)-[:TRIGGERS]->(:Mechanism)`
- `(:Mechanism)-[:AFFECTS]->(:Commodity)`
- `(:Mechanism)-[:AFFECTS]->(:Benchmark)`
- `(:Mechanism)-[:AFFECTS]->(:Indicator)`
- `(:Mechanism)-[:EVIDENCED_BY]->(:Observation)`
- `(:Mechanism)-[:EVIDENCED_BY]->(:Claim)`
- `(:Indicator)-[:AFFECTS {direction, horizon}]->(:Commodity)`
- `(:Indicator)-[:AFFECTS {direction, horizon}]->(:Indicator)`
- `(:Commodity)-[:RESPONDS_TO {direction, horizon}]->(:Indicator)`
- `(:Commodity)-[:DEPENDS_ON {channel, criticality}]->(:Country)`
- `(:Commodity)-[:CORRELATED_WITH {sign, window}]->(:Indicator)`

### Evidence and provenance

- `(:Document)-[:SUPPORTS]->(:Claim)`
- `(:Claim)-[:ABOUT]->(:Commodity)`
- `(:Claim)-[:ABOUT]->(:Country)`
- `(:Claim)-[:ABOUT]->(:Company)`
- `(:Claim)-[:ABOUT]->(:Asset)`
- `(:Claim)-[:ABOUT]->(:Benchmark)`
- `(:Claim)-[:ABOUT]->(:Event)`
- `(:Claim)-[:ABOUT]->(:Policy)`
- `(:Claim)-[:CAUSES {strength}]->(:Claim)`

### Time series

- `(:Observation)-[:OF]->(:Benchmark)`
- `(:Observation)-[:OF]->(:Commodity)`
- `(:Observation)-[:OF]->(:Country)`
- `(:Observation)-[:OF]->(:Asset)`
- `(:Observation)-[:OF]->(:Indicator)`

## Canonical ID convention

- Commodity: `COM:<NAME>`
- Benchmark: `BM:<NAME>`
- Indicator: `INDIC:<NAME>`
- Country: `CTY:<ISO3>`
- Company: `CO:<NAME>`
- Organization: `ORG:<NAME>`
- Industry: `IND:<NAME>`
- Product: `PRD:<NAME>`
- Asset: `AS:<NAME>`
- Event: `EV:<YYYY-MM>-<SHORT_NAME>`
- Mechanism: `MECH:<NAME>`
- Observation: `OBS:<DOMAIN>-<DATE>-<NAME>`
- Document: `DOC:<SOURCE>-<DATE>-<NAME>`
- Claim: `CLM:<SOURCE>-<DATE>-<NAME>`

Use uppercase ASCII IDs with underscores. Keep labels stable even if display names change.

## Time and provenance rules

- Static reference entities such as `Country` or `Industry` do not require `as_of`.
- Relationship properties should carry `as_of` when they represent dynamic facts like export share.
- `Observation.source_id` must resolve to a `Document.id` or an external dataset identifier.
- Extracted `Claim` nodes should not be merged into direct graph facts without preserving the originating `Document`.

## Recommended ingestion order

1. Reference entities: commodities, benchmarks, countries, industries, assets
2. Structural edges: `BENCHMARK_FOR`, `INPUT_TO`, `LOCATED_IN`, `PRODUCES`
3. Documents and claims
4. Events and policies
5. Observations
6. Mechanism links and inferred causal edges

## Phase 1 scope

The starter graph should cover:

- commodities: gold, silver, Brent oil, copper cathode
- indicators: US real yields, Fed funds, CPI, DXY, China property activity
- countries: United States, China, Saudi Arabia, Russia
- organizations: Federal Reserve, OPEC
- industries: solar, EV batteries, construction
- assets: Suez Canal, a major Saudi oil export system, a Chilean copper mine
- mechanisms: supply shock, logistics constraint, dollar pressure, rate sensitivity, inflation hedge demand

This is sufficient to answer:

- why did gold move after inflation or yield changes
- how do Fed decisions propagate into metals
- how do OPEC or shipping disruptions affect oil
- how does weaker China activity affect copper
