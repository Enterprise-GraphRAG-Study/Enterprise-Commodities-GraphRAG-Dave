// Seed graph generated from ontology/model YAML.
// dataset_id: phase1-macro-commodities
// version: 2

// Asset nodes
MERGE (chl_escondida_mine:Asset {
    id: 'AS:CHL_ESCONDIDA_MINE',
    name: 'Escondida mine',
    asset_type: 'Mine',
    capacity: 1.1,
    capacity_unit: 'mtpa',
    status: 'Operating'
  })
MERGE (egy_suez_canal:Asset {
    id: 'AS:EGY_SUEZ_CANAL',
    name: 'Suez Canal',
    asset_type: 'Canal',
    status: 'Operating'
  })
MERGE (sau_crude_export_system:Asset {
    id: 'AS:SAU_CRUDE_EXPORT_SYSTEM',
    name: 'Saudi crude export system',
    asset_type: 'Port',
    status: 'Operating'
  })

// Benchmark nodes
MERGE (ice_brent:Benchmark {
    id: 'BM:ICE_BRENT',
    name: 'ICE Brent Front Month',
    symbol: 'BRN',
    exchange: 'ICE',
    currency: 'USD',
    unit: 'bbl'
  })
MERGE (lme_cu_3m:Benchmark {
    id: 'BM:LME_CU_3M',
    name: 'LME Copper 3M',
    symbol: 'LME_CU_3M',
    exchange: 'LME',
    currency: 'USD',
    unit: 'mt'
  })
MERGE (xag_spot:Benchmark {
    id: 'BM:XAG_SPOT',
    name: 'Silver spot',
    symbol: 'XAGUSD',
    exchange: 'OTC',
    currency: 'USD',
    unit: 'oz'
  })
MERGE (xau_spot:Benchmark {
    id: 'BM:XAU_SPOT',
    name: 'Gold spot',
    symbol: 'XAUUSD',
    exchange: 'OTC',
    currency: 'USD',
    unit: 'oz'
  })

// Claim nodes
MERGE (bls_2026_03_gold_yields:Claim {
    id: 'CLM:BLS-2026-03-GOLD-YIELDS',
    claim_type: 'price_explanation',
    text: 'Gold strengthened as softer CPI reduced upward pressure on real yields and the dollar.',
    confidence: 0.84,
    source_id: 'DOC:BLS-2026-03-CPI',
    start_time: datetime('2026-03-11T12:30:00Z')
  })
MERGE (chn_2026_03_copper_demand:Claim {
    id: 'CLM:CHN-2026-03-COPPER-DEMAND',
    claim_type: 'demand_change',
    text: 'Weaker China property activity reduced expected copper demand growth.',
    confidence: 0.79,
    source_id: 'DOC:CHN-2026-03-PROPERTY',
    start_time: datetime('2026-03-07T01:00:00Z')
  })
MERGE (fed_2026_03_realyield:Claim {
    id: 'CLM:FED-2026-03-REALYIELD',
    claim_type: 'policy',
    text: 'Restrictive Fed guidance kept real yields elevated, limiting upside for non-yielding metals.',
    confidence: 0.8,
    source_id: 'DOC:FED-2026-03-GUIDANCE',
    start_time: datetime('2026-03-18T18:00:00Z')
  })
MERGE (opec_2026_03_oil_supply:Claim {
    id: 'CLM:OPEC-2026-03-OIL-SUPPLY',
    claim_type: 'supply_change',
    text: 'Extended OPEC supply restraint tightened expected oil availability.',
    confidence: 0.83,
    source_id: 'DOC:OPEC-2026-03-SUPPLY',
    start_time: datetime('2026-03-05T10:00:00Z')
  })
MERGE (ops_2026_03_oil_freight:Claim {
    id: 'CLM:OPS-2026-03-OIL-FREIGHT',
    claim_type: 'shipment_delay',
    text: 'Red Sea shipping disruption increased freight risk for oil cargoes.',
    confidence: 0.78,
    source_id: 'DOC:OPS-2026-03-REDSEA',
    start_time: datetime('2026-03-04T06:00:00Z')
  })
MERGE (solar_2026_03_silver_demand:Claim {
    id: 'CLM:SOLAR-2026-03-SILVER-DEMAND',
    claim_type: 'demand_change',
    text: 'Solar manufacturing growth increased structural silver demand.',
    confidence: 0.76,
    source_id: 'DOC:SOLAR-2026-03-SILVER',
    start_time: datetime('2026-03-06T14:00:00Z')
  })

// Commodity nodes
MERGE (copper_cathode:Commodity {
    id: 'COM:COPPER_CATHODE',
    name: 'Copper cathode',
    category: 'Metals',
    unit_standard: 'USD/mt',
    description: 'Industrial metal strongly tied to construction, electrification, and China activity.'
  })
MERGE (gold:Commodity {
    id: 'COM:GOLD',
    name: 'Gold',
    category: 'Precious Metals',
    unit_standard: 'USD/oz',
    description: 'Monetary and defensive precious metal sensitive to yields, USD, and inflation expectations.'
  })
MERGE (oil_brent:Commodity {
    id: 'COM:OIL_BRENT',
    name: 'Brent crude oil',
    category: 'Energy',
    unit_standard: 'USD/bbl',
    description: 'Global seaborne crude benchmark sensitive to supply disruption and shipping risk.'
  })
MERGE (silver:Commodity {
    id: 'COM:SILVER',
    name: 'Silver',
    category: 'Precious Metals',
    unit_standard: 'USD/oz',
    description: 'Precious and industrial metal with sensitivity to macro conditions and solar demand.'
  })

// Company nodes
MERGE (bhp:Company {
    id: 'CO:BHP',
    name: 'BHP',
    sector: 'Mining'
  })
MERGE (saudi_aramco:Company {
    id: 'CO:SAUDI_ARAMCO',
    name: 'Saudi Aramco',
    sector: 'Energy'
  })

// Country nodes
MERGE (chl:Country {
    id: 'CTY:CHL',
    name: 'Chile',
    iso_code: 'CHL',
    region: 'South America'
  })
MERGE (chn:Country {
    id: 'CTY:CHN',
    name: 'China',
    iso_code: 'CHN',
    region: 'Asia'
  })
MERGE (egy:Country {
    id: 'CTY:EGY',
    name: 'Egypt',
    iso_code: 'EGY',
    region: 'Middle East/Africa'
  })
MERGE (rus:Country {
    id: 'CTY:RUS',
    name: 'Russia',
    iso_code: 'RUS',
    region: 'Europe/Asia'
  })
MERGE (sau:Country {
    id: 'CTY:SAU',
    name: 'Saudi Arabia',
    iso_code: 'SAU',
    region: 'Middle East'
  })
MERGE (usa:Country {
    id: 'CTY:USA',
    name: 'United States',
    iso_code: 'USA',
    region: 'North America'
  })

// Document nodes
MERGE (bls_2026_03_cpi:Document {
    id: 'DOC:BLS-2026-03-CPI',
    doc_type: 'release',
    title: 'US CPI release points to softer inflation',
    publisher: 'BLS summary',
    published_at: datetime('2026-03-11T12:30:00Z'),
    url: 'internal://bls/2026-03-cpi',
    summary: 'Inflation release used to link CPI, real yields, USD, and precious metals.'
  })
MERGE (chn_2026_03_property:Document {
    id: 'DOC:CHN-2026-03-PROPERTY',
    doc_type: 'report',
    title: 'China property slowdown pressures industrial metals',
    publisher: 'Internal Macro Desk',
    published_at: datetime('2026-03-07T01:00:00Z'),
    url: 'internal://macro/2026-03-china-property',
    summary: 'China activity note connecting weaker property demand to copper expectations.'
  })
MERGE (fed_2026_03_guidance:Document {
    id: 'DOC:FED-2026-03-GUIDANCE',
    doc_type: 'statement',
    title: 'Fed guidance keeps policy restrictive',
    publisher: 'Federal Reserve',
    published_at: datetime('2026-03-18T18:00:00Z'),
    url: 'internal://fed/2026-03-guidance',
    summary: 'Policy statement framing rates as restrictive for longer.'
  })
MERGE (opec_2026_03_supply:Document {
    id: 'DOC:OPEC-2026-03-SUPPLY',
    doc_type: 'report',
    title: 'OPEC supply discipline remains in place',
    publisher: 'OPEC monitor',
    published_at: datetime('2026-03-05T10:00:00Z'),
    url: 'internal://opec/2026-03-supply',
    summary: 'Note on extended supply restraint and tighter crude balances.'
  })
MERGE (ops_2026_03_redsea:Document {
    id: 'DOC:OPS-2026-03-REDSEA',
    doc_type: 'report',
    title: 'Red Sea disruptions lift freight stress',
    publisher: 'Internal Ops Desk',
    published_at: datetime('2026-03-04T08:30:00Z'),
    url: 'internal://ops/2026-03-redsea',
    summary: 'Freight and routing update on shipping disruptions affecting energy cargoes.'
  })
MERGE (solar_2026_03_silver:Document {
    id: 'DOC:SOLAR-2026-03-SILVER',
    doc_type: 'note',
    title: 'Solar manufacturing supports silver demand',
    publisher: 'Internal Metals Desk',
    published_at: datetime('2026-03-06T14:00:00Z'),
    url: 'internal://metals/2026-03-solar-silver',
    summary: 'Demand note linking solar manufacturing growth to silver usage.'
  })

// Event nodes
MERGE (n_2026_03_china_property_weakness:Event {
    id: 'EV:2026-03-CHINA-PROPERTY-WEAKNESS',
    name: 'China property activity weakens',
    event_type: 'Macroeconomic',
    start_time: datetime('2026-03-07T01:00:00Z'),
    severity: 0.61,
    confidence: 0.79,
    summary: 'Slower Chinese property activity weighed on copper demand expectations.'
  })
MERGE (n_2026_03_opec_cut_extension:Event {
    id: 'EV:2026-03-OPEC-CUT-EXTENSION',
    name: 'OPEC extends supply restraint',
    event_type: 'Regulatory',
    start_time: datetime('2026-03-05T10:00:00Z'),
    severity: 0.66,
    confidence: 0.83,
    summary: 'OPEC maintained production discipline, tightening expectations for near-term oil balances.'
  })
MERGE (n_2026_03_red_sea_disruption:Event {
    id: 'EV:2026-03-RED-SEA-DISRUPTION',
    name: 'Red Sea shipping disruption',
    event_type: 'Logistics',
    start_time: datetime('2026-03-04T06:00:00Z'),
    severity: 0.63,
    confidence: 0.78,
    summary: 'Shipping delays increased voyage risk and freight costs for crude cargoes.'
  })
MERGE (n_2026_03_us_cooler_cpi:Event {
    id: 'EV:2026-03-US-COOLER-CPI',
    name: 'US inflation cools',
    event_type: 'Macroeconomic',
    start_time: datetime('2026-03-11T12:30:00Z'),
    severity: 0.52,
    confidence: 0.84,
    summary: 'Softer CPI data reduced real-yield pressure and supported precious metals sentiment.'
  })

// Indicator nodes
MERGE (chn_property_activity:Indicator {
    id: 'INDIC:CHN_PROPERTY_ACTIVITY',
    name: 'China property activity index',
    indicator_type: 'Activity',
    unit: 'index',
    frequency: 'monthly',
    publisher: 'Internal composite'
  })
MERGE (dxy:Indicator {
    id: 'INDIC:DXY',
    name: 'US dollar index',
    indicator_type: 'DollarIndex',
    unit: 'index',
    frequency: 'daily',
    publisher: 'ICE'
  })
MERGE (fed_funds_rate:Indicator {
    id: 'INDIC:FED_FUNDS_RATE',
    name: 'Fed funds target upper bound',
    indicator_type: 'PolicyRate',
    unit: 'percent',
    frequency: 'event',
    publisher: 'Federal Reserve'
  })
MERGE (us_10y_real_yield:Indicator {
    id: 'INDIC:US_10Y_REAL_YIELD',
    name: 'US 10Y real yield',
    indicator_type: 'RealYield',
    unit: 'percent',
    frequency: 'daily',
    publisher: 'US Treasury derived',
    description: 'Real yield proxy used to explain precious metals performance.'
  })
MERGE (us_cpi_yoy:Indicator {
    id: 'INDIC:US_CPI_YOY',
    name: 'US CPI year over year',
    indicator_type: 'Inflation',
    unit: 'percent',
    frequency: 'monthly',
    publisher: 'BLS'
  })

// Industry nodes
MERGE (construction:Industry {
    id: 'IND:CONSTRUCTION',
    name: 'Construction'
  })
MERGE (ev_batteries:Industry {
    id: 'IND:EV_BATTERIES',
    name: 'EV batteries'
  })
MERGE (solar:Industry {
    id: 'IND:SOLAR',
    name: 'Solar manufacturing'
  })

// Mechanism nodes
MERGE (china_demand_slowdown:Mechanism {
    id: 'MECH:CHINA_DEMAND_SLOWDOWN',
    name: 'China demand slowdown',
    mechanism_type: 'DemandShock'
  })
MERGE (dollar_pressure:Mechanism {
    id: 'MECH:DOLLAR_PRESSURE',
    name: 'Dollar pressure',
    mechanism_type: 'FXPassThrough'
  })
MERGE (inflation_hedge_demand:Mechanism {
    id: 'MECH:INFLATION_HEDGE_DEMAND',
    name: 'Inflation hedge demand',
    mechanism_type: 'DemandShock'
  })
MERGE (logistics_constraint:Mechanism {
    id: 'MECH:LOGISTICS_CONSTRAINT',
    name: 'Logistics constraint',
    mechanism_type: 'LogisticsConstraint'
  })
MERGE (rate_sensitivity:Mechanism {
    id: 'MECH:RATE_SENSITIVITY',
    name: 'Rate sensitivity',
    mechanism_type: 'DemandShock'
  })
MERGE (supply_shock:Mechanism {
    id: 'MECH:SUPPLY_SHOCK',
    name: 'Supply shock',
    mechanism_type: 'SupplyShock'
  })

// Observation nodes
MERGE (freight_2026_03_04_redsea:Observation {
    id: 'OBS:FREIGHT-2026-03-04-REDSEA',
    metric_type: 'FreightRate',
    value: 1.19,
    unit: 'index_ratio',
    as_of: datetime('2026-03-04T00:00:00Z'),
    granularity: 'daily',
    source_id: 'DOC:OPS-2026-03-REDSEA'
  })
MERGE (indic_2026_03_07_chn_property:Observation {
    id: 'OBS:INDIC-2026-03-07-CHN_PROPERTY',
    metric_type: 'PMI',
    value: 47.8,
    unit: 'index',
    as_of: datetime('2026-03-07T00:00:00Z'),
    granularity: 'monthly',
    source_id: 'DOC:CHN-2026-03-PROPERTY'
  })
MERGE (indic_2026_03_11_dxy:Observation {
    id: 'OBS:INDIC-2026-03-11-DXY',
    metric_type: 'FX',
    value: 103.4,
    unit: 'index',
    as_of: datetime('2026-03-11T00:00:00Z'),
    granularity: 'daily',
    source_id: 'DOC:BLS-2026-03-CPI'
  })
MERGE (indic_2026_03_11_us_10y_real_yield:Observation {
    id: 'OBS:INDIC-2026-03-11-US_10Y_REAL_YIELD',
    metric_type: 'RealYield',
    value: 1.62,
    unit: 'percent',
    as_of: datetime('2026-03-11T00:00:00Z'),
    granularity: 'daily',
    source_id: 'DOC:BLS-2026-03-CPI'
  })
MERGE (indic_2026_03_11_us_cpi_yoy:Observation {
    id: 'OBS:INDIC-2026-03-11-US_CPI_YOY',
    metric_type: 'Inflation',
    value: 2.9,
    unit: 'percent',
    as_of: datetime('2026-03-11T00:00:00Z'),
    granularity: 'monthly',
    source_id: 'DOC:BLS-2026-03-CPI'
  })
MERGE (indic_2026_03_18_fed_funds:Observation {
    id: 'OBS:INDIC-2026-03-18-FED_FUNDS',
    metric_type: 'InterestRate',
    value: 5.5,
    unit: 'percent',
    as_of: datetime('2026-03-18T00:00:00Z'),
    granularity: 'event',
    source_id: 'DOC:FED-2026-03-GUIDANCE'
  })
MERGE (price_2026_03_05_ice_brent:Observation {
    id: 'OBS:PRICE-2026-03-05-ICE_BRENT',
    metric_type: 'Price',
    value: 84.9,
    unit: 'USD/bbl',
    currency: 'USD',
    as_of: datetime('2026-03-05T00:00:00Z'),
    granularity: 'daily',
    source_id: 'DOC:OPEC-2026-03-SUPPLY'
  })
MERGE (price_2026_03_07_lme_cu_3m:Observation {
    id: 'OBS:PRICE-2026-03-07-LME_CU_3M',
    metric_type: 'Price',
    value: 8715.0,
    unit: 'USD/mt',
    currency: 'USD',
    as_of: datetime('2026-03-07T00:00:00Z'),
    granularity: 'daily',
    source_id: 'DOC:CHN-2026-03-PROPERTY'
  })
MERGE (price_2026_03_11_xag:Observation {
    id: 'OBS:PRICE-2026-03-11-XAG',
    metric_type: 'Price',
    value: 24.6,
    unit: 'USD/oz',
    currency: 'USD',
    as_of: datetime('2026-03-11T00:00:00Z'),
    granularity: 'daily',
    source_id: 'DOC:SOLAR-2026-03-SILVER'
  })
MERGE (price_2026_03_11_xau:Observation {
    id: 'OBS:PRICE-2026-03-11-XAU',
    metric_type: 'Price',
    value: 2184.0,
    unit: 'USD/oz',
    currency: 'USD',
    as_of: datetime('2026-03-11T00:00:00Z'),
    granularity: 'daily',
    source_id: 'DOC:BLS-2026-03-CPI'
  })

// Organization nodes
MERGE (fed:Organization {
    id: 'ORG:FED',
    name: 'Federal Reserve',
    org_type: 'CentralBank'
  })
MERGE (iea:Organization {
    id: 'ORG:IEA',
    name: 'International Energy Agency',
    org_type: 'Intergovernmental'
  })
MERGE (opec:Organization {
    id: 'ORG:OPEC',
    name: 'OPEC',
    org_type: 'ProducerGroup'
  })

// Policy nodes
MERGE (n_2026_03_fed_hold:Policy:Event {
    id: 'EV:2026-03-FED-HOLD',
    name: 'Federal Reserve holds policy rate',
    event_type: 'Regulatory',
    policy_type: 'RateDecision',
    start_time: datetime('2026-03-18T18:00:00Z'),
    severity: 0.44,
    confidence: 0.8,
    summary: 'Federal Reserve maintained restrictive policy guidance, keeping real yields elevated.'
  })

// Relationships
MERGE (ice_brent)-[:BENCHMARK_FOR]->(oil_brent)
MERGE (lme_cu_3m)-[:BENCHMARK_FOR]->(copper_cathode)
MERGE (xau_spot)-[:BENCHMARK_FOR]->(gold)
MERGE (xag_spot)-[:BENCHMARK_FOR]->(silver)
MERGE (copper_cathode)-[:INPUT_TO {
    share: 0.71,
    criticality: 'high'
  }]->(construction)
MERGE (copper_cathode)-[:INPUT_TO {
    share: 0.44,
    criticality: 'medium'
  }]->(ev_batteries)
MERGE (silver)-[:INPUT_TO {
    share: 0.36,
    criticality: 'high'
  }]->(solar)
MERGE (gold)-[:SUBSTITUTE_OF {strength: 0.29}]->(silver)
MERGE (silver)-[:SUBSTITUTE_OF {strength: 0.29}]->(gold)
MERGE (bhp)-[:OPERATES_IN]->(chl)
MERGE (saudi_aramco)-[:OPERATES_IN]->(sau)
MERGE (sau)-[:MEMBER_OF]->(opec)
MERGE (fed)-[:SETS]->(fed_funds_rate)
MERGE (n_2026_03_fed_hold)-[:ISSUED_BY]->(fed)
MERGE (chl_escondida_mine)-[:LOCATED_IN]->(chl)
MERGE (chl_escondida_mine)-[:OWNED_BY]->(bhp)
MERGE (chl_escondida_mine)-[:PRODUCES]->(copper_cathode)
MERGE (egy_suez_canal)-[:LOCATED_IN]->(egy)
MERGE (sau_crude_export_system)-[:LOCATED_IN]->(sau)
MERGE (sau_crude_export_system)-[:OWNED_BY]->(saudi_aramco)
MERGE (sau_crude_export_system)-[:PRODUCES]->(oil_brent)
MERGE (oil_brent)-[:TRANSPORTED_VIA]->(egy_suez_canal)
MERGE (oil_brent)-[:DEPENDS_ON {
    channel: 'supply',
    criticality: 'high'
  }]->(sau)
MERGE (copper_cathode)-[:DEPENDS_ON {
    channel: 'demand',
    criticality: 'high'
  }]->(chn)
MERGE (sau)-[:EXPORTS {
    share: 0.17,
    as_of: datetime('2026-03-05T00:00:00Z'),
    source_id: 'DOC:OPEC-2026-03-SUPPLY'
  }]->(oil_brent)
MERGE (chl)-[:EXPORTS {
    share: 0.24,
    as_of: datetime('2026-03-07T00:00:00Z'),
    source_id: 'DOC:CHN-2026-03-PROPERTY'
  }]->(copper_cathode)
MERGE (chn)-[:IMPORTS {
    share: 0.15,
    as_of: datetime('2026-03-05T00:00:00Z'),
    source_id: 'DOC:OPEC-2026-03-SUPPLY'
  }]->(oil_brent)
MERGE (us_10y_real_yield)-[:AFFECTS {
    direction: 'negative',
    horizon: 'short_term'
  }]->(gold)
MERGE (us_10y_real_yield)-[:AFFECTS {
    direction: 'negative',
    horizon: 'short_term'
  }]->(silver)
MERGE (dxy)-[:AFFECTS {
    direction: 'negative',
    horizon: 'short_term'
  }]->(gold)
MERGE (dxy)-[:AFFECTS {
    direction: 'negative',
    horizon: 'short_term'
  }]->(oil_brent)
MERGE (chn_property_activity)-[:AFFECTS {
    direction: 'positive',
    horizon: 'medium_term'
  }]->(copper_cathode)
MERGE (us_cpi_yoy)-[:AFFECTS {
    direction: 'positive',
    horizon: 'medium_term'
  }]->(gold)
MERGE (gold)-[:RESPONDS_TO {
    direction: 'inverse',
    horizon: 'short_term'
  }]->(us_10y_real_yield)
MERGE (gold)-[:RESPONDS_TO {
    direction: 'inverse',
    horizon: 'short_term'
  }]->(dxy)
MERGE (copper_cathode)-[:RESPONDS_TO {
    direction: 'positive',
    horizon: 'medium_term'
  }]->(chn_property_activity)
MERGE (gold)-[:CORRELATED_WITH {
    sign: 'positive',
    window: 'medium_term'
  }]->(us_cpi_yoy)
MERGE (gold)-[:CORRELATED_WITH {
    sign: 'negative',
    window: 'short_term'
  }]->(us_10y_real_yield)
MERGE (rate_sensitivity)-[:AFFECTS]->(gold)
MERGE (rate_sensitivity)-[:AFFECTS]->(silver)
MERGE (rate_sensitivity)-[:AFFECTS]->(us_10y_real_yield)
MERGE (inflation_hedge_demand)-[:AFFECTS]->(gold)
MERGE (inflation_hedge_demand)-[:AFFECTS]->(silver)
MERGE (dollar_pressure)-[:AFFECTS]->(gold)
MERGE (dollar_pressure)-[:AFFECTS]->(oil_brent)
MERGE (dollar_pressure)-[:AFFECTS]->(dxy)
MERGE (supply_shock)-[:AFFECTS]->(oil_brent)
MERGE (logistics_constraint)-[:AFFECTS]->(oil_brent)
MERGE (china_demand_slowdown)-[:AFFECTS]->(copper_cathode)
MERGE (china_demand_slowdown)-[:AFFECTS]->(chn_property_activity)
MERGE (n_2026_03_fed_hold)-[:TARGETS]->(fed_funds_rate)
MERGE (n_2026_03_fed_hold)-[:AFFECTS {
    mode: 'policy',
    severity: 0.44
  }]->(fed_funds_rate)
MERGE (n_2026_03_fed_hold)-[:AFFECTS {
    mode: 'macro',
    severity: 0.46
  }]->(us_10y_real_yield)
MERGE (n_2026_03_fed_hold)-[:TRIGGERS]->(rate_sensitivity)
MERGE (n_2026_03_fed_hold)-[:TRIGGERS]->(dollar_pressure)
MERGE (n_2026_03_us_cooler_cpi)-[:AFFECTS {
    mode: 'macro',
    severity: 0.52
  }]->(us_cpi_yoy)
MERGE (n_2026_03_us_cooler_cpi)-[:AFFECTS {
    mode: 'macro',
    severity: 0.48
  }]->(us_10y_real_yield)
MERGE (n_2026_03_us_cooler_cpi)-[:AFFECTS {
    mode: 'sentiment',
    severity: 0.51
  }]->(gold)
MERGE (n_2026_03_us_cooler_cpi)-[:TRIGGERS]->(inflation_hedge_demand)
MERGE (n_2026_03_opec_cut_extension)-[:AFFECTS {
    mode: 'supply',
    severity: 0.66
  }]->(oil_brent)
MERGE (n_2026_03_opec_cut_extension)-[:AFFECTS {
    mode: 'supply',
    severity: 0.59
  }]->(sau_crude_export_system)
MERGE (n_2026_03_opec_cut_extension)-[:TRIGGERS]->(supply_shock)
MERGE (n_2026_03_red_sea_disruption)-[:AFFECTS {
    mode: 'logistics',
    severity: 0.63
  }]->(egy_suez_canal)
MERGE (n_2026_03_red_sea_disruption)-[:AFFECTS {
    mode: 'logistics',
    severity: 0.57
  }]->(oil_brent)
MERGE (n_2026_03_red_sea_disruption)-[:TRIGGERS]->(logistics_constraint)
MERGE (n_2026_03_china_property_weakness)-[:AFFECTS {
    mode: 'macro',
    severity: 0.61
  }]->(chn_property_activity)
MERGE (n_2026_03_china_property_weakness)-[:AFFECTS {
    mode: 'demand',
    severity: 0.58
  }]->(copper_cathode)
MERGE (n_2026_03_china_property_weakness)-[:TRIGGERS]->(china_demand_slowdown)
MERGE (bls_2026_03_cpi)-[:SUPPORTS]->(bls_2026_03_gold_yields)
MERGE (fed_2026_03_guidance)-[:SUPPORTS]->(fed_2026_03_realyield)
MERGE (opec_2026_03_supply)-[:SUPPORTS]->(opec_2026_03_oil_supply)
MERGE (ops_2026_03_redsea)-[:SUPPORTS]->(ops_2026_03_oil_freight)
MERGE (chn_2026_03_property)-[:SUPPORTS]->(chn_2026_03_copper_demand)
MERGE (solar_2026_03_silver)-[:SUPPORTS]->(solar_2026_03_silver_demand)
MERGE (bls_2026_03_gold_yields)-[:ABOUT]->(gold)
MERGE (bls_2026_03_gold_yields)-[:ABOUT]->(us_10y_real_yield)
MERGE (bls_2026_03_gold_yields)-[:ABOUT]->(dxy)
MERGE (fed_2026_03_realyield)-[:ABOUT]->(fed)
MERGE (fed_2026_03_realyield)-[:ABOUT]->(us_10y_real_yield)
MERGE (fed_2026_03_realyield)-[:ABOUT]->(gold)
MERGE (opec_2026_03_oil_supply)-[:ABOUT]->(opec)
MERGE (opec_2026_03_oil_supply)-[:ABOUT]->(oil_brent)
MERGE (ops_2026_03_oil_freight)-[:ABOUT]->(oil_brent)
MERGE (ops_2026_03_oil_freight)-[:ABOUT]->(egy_suez_canal)
MERGE (chn_2026_03_copper_demand)-[:ABOUT]->(copper_cathode)
MERGE (chn_2026_03_copper_demand)-[:ABOUT]->(chn_property_activity)
MERGE (solar_2026_03_silver_demand)-[:ABOUT]->(silver)
MERGE (solar_2026_03_silver_demand)-[:ABOUT]->(solar)
MERGE (price_2026_03_11_xau)-[:OF]->(xau_spot)
MERGE (price_2026_03_11_xag)-[:OF]->(xag_spot)
MERGE (price_2026_03_05_ice_brent)-[:OF]->(ice_brent)
MERGE (price_2026_03_07_lme_cu_3m)-[:OF]->(lme_cu_3m)
MERGE (indic_2026_03_11_us_cpi_yoy)-[:OF]->(us_cpi_yoy)
MERGE (indic_2026_03_11_us_10y_real_yield)-[:OF]->(us_10y_real_yield)
MERGE (indic_2026_03_11_dxy)-[:OF]->(dxy)
MERGE (indic_2026_03_18_fed_funds)-[:OF]->(fed_funds_rate)
MERGE (indic_2026_03_07_chn_property)-[:OF]->(chn_property_activity)
MERGE (freight_2026_03_04_redsea)-[:OF]->(egy_suez_canal)
MERGE (rate_sensitivity)-[:EVIDENCED_BY]->(fed_2026_03_realyield)
MERGE (rate_sensitivity)-[:EVIDENCED_BY]->(indic_2026_03_11_us_10y_real_yield)
MERGE (inflation_hedge_demand)-[:EVIDENCED_BY]->(bls_2026_03_gold_yields)
MERGE (inflation_hedge_demand)-[:EVIDENCED_BY]->(indic_2026_03_11_us_cpi_yoy)
MERGE (dollar_pressure)-[:EVIDENCED_BY]->(bls_2026_03_gold_yields)
MERGE (dollar_pressure)-[:EVIDENCED_BY]->(indic_2026_03_11_dxy)
MERGE (supply_shock)-[:EVIDENCED_BY]->(opec_2026_03_oil_supply)
MERGE (supply_shock)-[:EVIDENCED_BY]->(price_2026_03_05_ice_brent)
MERGE (logistics_constraint)-[:EVIDENCED_BY]->(ops_2026_03_oil_freight)
MERGE (logistics_constraint)-[:EVIDENCED_BY]->(freight_2026_03_04_redsea)
MERGE (china_demand_slowdown)-[:EVIDENCED_BY]->(chn_2026_03_copper_demand)
MERGE (china_demand_slowdown)-[:EVIDENCED_BY]->(indic_2026_03_07_chn_property);
