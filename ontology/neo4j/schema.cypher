// Commodity intelligence ontology schema for Neo4j 5.x
// Run this before loading seed or ingestion data.

CREATE CONSTRAINT commodity_id_unique IF NOT EXISTS
FOR (n:Commodity)
REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT benchmark_id_unique IF NOT EXISTS
FOR (n:Benchmark)
REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT indicator_id_unique IF NOT EXISTS
FOR (n:Indicator)
REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT country_id_unique IF NOT EXISTS
FOR (n:Country)
REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT company_id_unique IF NOT EXISTS
FOR (n:Company)
REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT organization_id_unique IF NOT EXISTS
FOR (n:Organization)
REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT industry_id_unique IF NOT EXISTS
FOR (n:Industry)
REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT product_id_unique IF NOT EXISTS
FOR (n:Product)
REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT asset_id_unique IF NOT EXISTS
FOR (n:Asset)
REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT event_id_unique IF NOT EXISTS
FOR (n:Event)
REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT policy_id_unique IF NOT EXISTS
FOR (n:Policy)
REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT mechanism_id_unique IF NOT EXISTS
FOR (n:Mechanism)
REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT observation_id_unique IF NOT EXISTS
FOR (n:Observation)
REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT document_id_unique IF NOT EXISTS
FOR (n:Document)
REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT claim_id_unique IF NOT EXISTS
FOR (n:Claim)
REQUIRE n.id IS UNIQUE;

CREATE INDEX commodity_name_idx IF NOT EXISTS
FOR (n:Commodity)
ON (n.name);

CREATE INDEX benchmark_name_idx IF NOT EXISTS
FOR (n:Benchmark)
ON (n.name);

CREATE INDEX indicator_name_idx IF NOT EXISTS
FOR (n:Indicator)
ON (n.name);

CREATE INDEX country_name_idx IF NOT EXISTS
FOR (n:Country)
ON (n.name);

CREATE INDEX asset_type_idx IF NOT EXISTS
FOR (n:Asset)
ON (n.asset_type);

CREATE INDEX event_type_idx IF NOT EXISTS
FOR (n:Event)
ON (n.event_type);

CREATE INDEX policy_type_idx IF NOT EXISTS
FOR (n:Policy)
ON (n.policy_type);

CREATE INDEX mechanism_type_idx IF NOT EXISTS
FOR (n:Mechanism)
ON (n.mechanism_type);

CREATE INDEX indicator_type_idx IF NOT EXISTS
FOR (n:Indicator)
ON (n.indicator_type);

CREATE INDEX observation_metric_idx IF NOT EXISTS
FOR (n:Observation)
ON (n.metric_type, n.as_of);

CREATE INDEX document_published_idx IF NOT EXISTS
FOR (n:Document)
ON (n.published_at);

CREATE INDEX claim_type_idx IF NOT EXISTS
FOR (n:Claim)
ON (n.claim_type);
