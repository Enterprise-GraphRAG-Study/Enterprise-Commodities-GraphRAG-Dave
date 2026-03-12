# 2주차 과제 정리

## 1. 도메인셋 분석하기

현재 저장소의 도메인셋은 크게 4개 층으로 구성된다.

### 1) 구조화된 온톨로지 계층

- 파일: `ontology/commodity_ontology.md`
- 역할: 어떤 노드와 관계를 그래프에 넣을지 정의
- 장점:
  - `Commodity`, `Indicator`, `Event`, `Policy`, `Claim`, `Observation` 같은 핵심 타입이 이미 정리되어 있음
  - 시간 정보(`as_of`, `start_time`, `published_at`)와 출처(`source_id`)를 분리해서 관리함
  - GraphRAG에서 중요한 인과 관계와 설명 가능성을 고려한 구조임
- 한계:
  - 아직 실제 대규모 외부 데이터셋과 자동 정합되는 단계는 아님
  - 관계 타입이 많아질수록 추출 규칙과 인덱스 설계가 같이 보강되어야 함

### 2) 수작업 그래프 데이터 계층

- 파일: `ontology/model/phase1.yaml`
- 역할: 현재 시스템의 기준 데이터셋
- 포함 범위:
  - 상품: 금, 은, 브렌트유, 구리
  - 지표: 미국 실질금리, Fed funds, CPI, DXY, 중국 부동산 활동
  - 기관: Fed, OPEC, IEA
  - 사건: 인플레이션 둔화, OPEC 감산 유지, 홍해/수에즈 물류 차질, 중국 부동산 둔화
- 장점:
  - 그래프 구조가 작고 explainable 해서 실험용으로 적절함
  - 인과관계 질문을 만들기 쉬움
- 한계:
  - 현재는 student-scale seed data라서 coverage가 좁음
  - 실제 뉴스/리포트 분포를 대표하지는 못함

### 3) 설명형 텍스트 코퍼스 계층

- 파일: `corpus/curated_docs.yaml`
- 역할: 문서에서 claim을 뽑아 그래프로 연결하는 원천 텍스트
- 장점:
  - 문장이 관계를 직접 드러냄
  - `Gold gained after CPI eased`, `OPEC maintained supply restraint` 같은 causal sentence 중심이라 GraphRAG에 적합함
- 한계:
  - 문서 수가 매우 적음
  - 아직은 curated sample이며 실제 production corpus가 아님

### 4) 파생 데이터 계층

- 파일:
  - `ontology/model/extracted_claims.yaml`
  - `ontology/model/phase1_enriched.yaml`
  - `ontology/neo4j/seed_enriched.cypher`
- 역할: 추출된 claim과 그래프 시드 결과물
- 장점:
  - 수작업 seed + 추출 결과를 합쳐서 end-to-end 검증 가능
- 한계:
  - 규칙 기반 추출이라 recall이 낮음
  - 의미적으로 복잡한 문장은 아직 잘 못 다룸

## 2. 인덱싱 방법 구상하기

이 도메인에서는 단일 인덱스보다 **다층 인덱싱 구조**가 적합하다.

### 제안하는 인덱싱 구조

#### A. 그래프 구조 인덱스

- 대상: `Node ID`, `Label`, `Relationship`
- 목적:
  - 특정 상품과 연결된 이벤트/기관/지표를 빠르게 추적
  - causal path 탐색
- 구현 위치:
  - Neo4j 제약조건 및 인덱스
  - `ontology/neo4j/schema.cypher`

#### B. 엔티티-증거 인덱스

- 대상: Entity -> Claim / Document / Observation
- 목적:
  - "금과 관련된 근거 문서 보여줘"
  - "구리에 대한 claim과 observation 묶어서 보여줘"
- 구현:
  - `artifacts/index/entity_to_evidence.json`

#### C. 키워드 역색인

- 대상: 문서 제목, claim text, 요약, 설명
- 목적:
  - lexical retrieval
  - 초기 candidate recall 확보
- 구현:
  - `artifacts/index/keyword_inverted_index.json`

#### D. 시간 인덱스

- 대상: `published_at`, `start_time`, `as_of`
- 목적:
  - 최근 이벤트/관측치 우선 조회
  - 특정 기간 필터링
- 구현:
  - `artifacts/index/temporal_index.json`

#### E. 향후 벡터 인덱스

- 현재 repo에는 아직 없음
- 향후 추가 목적:
  - 의미 기반 유사 문서/claim 검색
  - 질의 표현이 exact keyword와 다를 때 recall 보완

### 왜 이렇게 나누는가

상품 도메인은 단순 문서 검색이 아니라:

- 인과 관계
- 시계열 변화
- 이벤트 전파
- 출처 기반 설명

이 동시에 필요하다. 따라서:

- 그래프 인덱스는 연결 탐색
- 키워드 인덱스는 빠른 후보 검색
- 시간 인덱스는 recent filtering
- 벡터 인덱스는 semantic recall

역할을 분리하는 것이 적합하다.

## 2.5 시스템 목표 정하기

### 목표 시스템

**상품 시장 이벤트 기반 분석 보조 시스템**

### 한 줄 설명

거시경제 이벤트, 공급 충격, 물류 차질, 정책 변화가 상품 가격과 수요/공급에 어떻게 전파되는지를 설명형으로 찾아주는 GraphRAG 시스템.

### 사용자가 기대하는 질문 예시

- 왜 금 가격이 올랐는가?
- 최근 유가 상승의 원인은 무엇인가?
- 중국 부동산 둔화가 구리에 어떤 영향을 주는가?
- OPEC 정책과 브렌트유 가격은 어떤 경로로 연결되는가?
- 금, 실질금리, 달러지수 사이의 관계를 근거와 함께 설명해줘

### 시스템 출력 목표

- 관련 문서/claim/observation 회수
- causal path 요약
- 시간 정보 포함
- source-aware explanation 제공

## 3. 시간되면 인덱싱 해보기

이번 저장소에서는 간단한 인덱싱 프로토타입까지 구현했다.

### 구현 파일

- `src/indexer.py`
- `scripts/build_indices.py`

### 생성 결과물

- `artifacts/index/graph_summary.json`
- `artifacts/index/node_index.json`
- `artifacts/index/entity_to_evidence.json`
- `artifacts/index/keyword_inverted_index.json`
- `artifacts/index/temporal_index.json`

### 현재 프로토타입이 하는 일

1. 그래프 노드를 ID 기준으로 정리
2. 엔티티별 근거 claim / document / observation 연결
3. 키워드 역색인 생성
4. 시간순 정렬 인덱스 생성
5. 전체 그래프 요약 통계 생성

### 한계

- 아직 벡터 인덱스는 없음
- 랭킹 모델이 없음
- Neo4j + lexical index + vector index를 결합한 hybrid retrieval은 다음 단계

### 다음 단계 제안

1. `claim` 단위 embedding 생성
2. Neo4j path retrieval + vector retrieval 결합
3. 시간 가중치와 출처 신뢰도를 scoring에 반영
4. 질의 유형별 검색 전략 분리
   - 원인 분석형
   - 최근 이슈형
   - 비교형
   - 영향 전파형
