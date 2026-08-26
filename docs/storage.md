# Storage

What Ontolox persists and where. Constraint: **mature open-source technologies** (OSI licence, years of production history, active community); commercial engines only as upgrade paths.

Related docs: [standards.md](./standards.md) · [runtime-architecture.md](./runtime-architecture.md) · [buildtime-architecture.md](./buildtime-architecture.md).

## What we store, and where

| Category | Contents | First-version store |
|---|---|---|
| Ontology model | Classes, relationships, rules (SHACL), mappings | **Apache Jena Fuseki** (RDF, named graphs) + Turtle in git |
| Ontology instances | Materialised business objects | Federated by default; Fuseki or Postgres when materialised |
| Metadata catalogue | Sources, schemas, profiling, contracts | **PostgreSQL** |
| Provenance & lineage | Evidence trails, agent activity, run events | Fuseki (PROV-O) + Postgres (OpenLineage events) |
| Evidence & documents | Samples, schema snapshots, docs | **MinIO** (S3-compatible) |
| Vector indexes | Embeddings for retrieval | **pgvector**; Qdrant if volume demands |
| Operational state | Agent runs, proposals, approvals, audit | **PostgreSQL** (append-only audit) |
| Credentials | Connector secrets, keys | **OpenBao** (open-source Vault fork) |
| Cache | Federated query results, TTL-bound | **Valkey** or Postgres materialised views |

MVP footprint: **Fuseki, one PostgreSQL (with pgvector), MinIO, OpenBao** — all mature open source.

## The ontology graph store

**Recommendation: Apache Jena Fuseki as a containerised black box.** Apache 2.0, ~20 years mature, and the only open-source server covering the full standards commitment natively: SPARQL 1.1 + SHACL + RDFS/OWL RL inference. It is JVM software, but it is consumed only over the standard SPARQL HTTP protocol — application and agent code stays in Python (**RDFLib**, **pySHACL**, **owlrl**) or .NET (**dotNetRDF**), and the store is swappable.

**Alternatives:**

- **Mature open source:** Eclipse RDF4J (JVM), Virtuoso OSE (C, dated operationally).
- **Modern, non-JVM (watch):** **QLever** (C++, fastest SPARQL engine in independent benchmarks — a query accelerator, no reasoning), **Oxigraph** (Rust, best Python bindings, optimiser still immature), **MillenniumDB** (C++, dual RDF + property-graph model), **OxiRS** (Rust, drop-in Fuseki replacement, first production release mid-2026, unproven).
- **Property-graph projection** (only if traversal workloads demand it): Apache AGE first (Cypher inside Postgres, no new infra), then JanusGraph or Neo4j Community (GPLv3; clustering/RBAC are enterprise-only). These have no native OWL/SHACL — projection only, never the system of record.

### Alternative architecture: standards at the boundary

Because the platform serves **Nordic SME clients** (no ontologists, cost-sensitive per-tenant footprint, strongly lock-in-averse), a simpler variant stays open: author and operate in **LinkML** YAML compiled to Pydantic/SQL, run on **Postgres only** (+ AGE, pgvector), and guarantee OWL + SHACL + JSON-LD as export targets rather than the runtime. Gains: agent and SME authoring velocity, cheap tenants, plain-YAML client templates. Gives up: live OWL reasoning and SPARQL federation. The no-lock-in guarantee ("your ontology exports as standard OWL") holds in both architectures.

## Federation versus materialisation

Instance data is *not* copied by default. Per mapping, recorded in the ontology's operational contract:

| Mode | When | Storage |
|---|---|---|
| **Federated** | Source queryable with acceptable latency; sensitive or fast-changing data | No copy; push-down at read time |
| **Cached** | Repeated reads, tolerable staleness | TTL-bound entries in cache layer |
| **Materialised** | Cross-source joins too slow, or source can't take load | Governed pipeline into graph/Postgres, with lineage and refresh |

## Versioning

- Named graphs per release in the triple store, tagged with SemVer.
- Turtle (or LinkML YAML) committed to git as the review/diff surface; approval merges proposals.
- Proposals are first-class Postgres records referencing the fragments they apply, with confidence, evidence, and review state.

## Decision points after MVP

1. **Whether Jena still fits** — re-evaluate against Oxigraph/OxiRS maturity; add QLever as a read-optimised query tier if raw SPARQL speed over materialised data becomes the bottleneck.
2. **Property-graph projection** — trigger: traversal queries the triple store or federation can't serve in latency targets.
3. **Vectors out of Postgres** — trigger: beyond pgvector comfort; Qdrant is the open-source target.
4. **CDC / event streaming** — MVP polls for freshness; Kafka + CloudEvents in Phase 2.
