# Standards

The open standards Ontolox adopts, by adoption level:

- **Core** — foundational; the platform is built on these.
- **Recommended** — adopt where the capability is in scope.
- **Watch** — track; adopt on demand.

Related docs: [storage.md](./storage.md) (where data lives) · [runtime-architecture.md](./runtime-architecture.md) (how it runs) · [buildtime-architecture.md](./buildtime-architecture.md) (how the model is built).

## Standards by area

| Area | Standard | Level | Purpose |
|---|---|---|---|
| Ontology model | **RDF 1.1 / RDFS** (W3C) | Core | Base graph model; classes, properties, stable IRIs. |
| Ontology model | **OWL 2** (W3C, RL profile) | Core | Rich semantics and tractable reasoning. |
| Ontology model | **SHACL** (W3C) | Core | Machine-checkable rules and data validation. |
| Ontology model | **PROV-O** (W3C) | Core | Provenance of every proposal, mapping, and approval. |
| Ontology model | **SKOS** (W3C) | Recommended | Glossaries and taxonomies (stages, categories, severities). |
| Ontology authoring | **LinkML** | Recommended | YAML-authored models that agents and SME experts can read; compiles to OWL, SHACL, JSON Schema, SQL, Pydantic. |
| Serialisation | **Turtle**, **JSON-LD 1.1** | Core | Turtle for review/diff; JSON-LD for APIs and LLM context. |
| Query | **SPARQL 1.1** (W3C) | Core | Query, update, and federation over the ontology graph. |
| Query | **SQL** (ISO) | Core | Federation and push-down to relational sources. |
| Query | **GraphQL**, **GQL** (ISO) | Recommended | Developer API surface; property-graph querying if a projection is added. |
| Catalogue & lineage | **DCAT v3** (W3C) | Recommended | Standard, exportable source/dataset catalogue. |
| Catalogue & lineage | **OpenLineage** | Recommended | Run-level pipeline lineage, complementing PROV-O. |
| Integration | **OpenAPI 3.x**, **JSON Schema** | Core | Describe REST sources and our own APIs; validate payloads and action contracts. |
| Integration | **JDBC / ODBC**, **S3 API** | Core | Relational/warehouse and object-storage connectivity. |
| Integration | **AsyncAPI**, **CloudEvents** | Watch | Event-stream sources and CDC (Phase 2). |
| Security | **OAuth 2.1 / OIDC**, **TLS 1.3 / JWK** | Core | Authentication, delegated authorisation, transport, credentials. |
| Security | **SCIM 2.0**, policy-as-code (OPA / Cedar) | Recommended | Identity provisioning; versioned access and action policies. |
| AI interop | **MCP** | Core | Expose ontology read/query/action tools to external copilots and agents. |
| Operations | **SemVer**, **RFC 3339**, **OpenTelemetry** | Core / Rec. | Versioned releases, consistent timestamps, observability. |
| Vocabularies | schema.org, FOAF / Org, Time Ontology | Recommended | Reuse for people, orgs, and temporal concepts before inventing terms. |

## How we apply them

1. **RDF/OWL is the guaranteed interchange model, not necessarily the runtime.** Every ontology exports as OWL + SHACL + PROV-O regardless of the store — this is the no-lock-in guarantee that matters to Nordic SME clients.
2. **Author simply, export formally.** LinkML-style YAML is the candidate authoring layer; W3C standards are compile targets (see [storage.md](./storage.md)).
3. **Every ontology object gets a stable IRI**; identifier discipline makes lineage, versioning, and federation work.
4. **Agents emit standards-conformant artefacts** (RDF/SHACL fragments with PROV-O provenance) so review, diff, and audit share one representation.
5. **Validate at the boundary:** JSON Schema for API payloads, SHACL for graph data, both enforced before anything reaches the persistent layer.
