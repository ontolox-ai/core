# Standards

The open standards Ontolox adopts, by adoption level:

- **Core** — required by the MVP architecture or its portable release artefacts.
- **Recommended** — adopt where the capability is in scope.
- **Watch** — track; adopt on demand.

Related docs: [artifact-management.md](./artifact-management.md) (source and build artefacts) · [storage.md](./storage.md) (where data lives) · [runtime-architecture.md](./runtime-architecture.md) (how it runs) · [buildtime-architecture.md](./buildtime-architecture.md) (how the model is built).

## Standards by area

| Area | Standard | Level | Purpose |
| --- | --- | --- | --- |
| Ontology authoring | **LinkML** | Core | Canonical, reviewable YAML model for the MVP; restricted to an explicitly tested generator profile. |
| Ontology interchange | **RDF 1.1 / RDFS** (W3C) | Core | Portable graph representation, classes, properties, and stable IRIs. |
| Ontology interchange | **SHACL** (W3C) | Core | Generated graph constraints and release-conformance tests. |
| Ontology interchange | **PROV-O** (W3C) | Core | Portable representation of proposal, mapping, approval, and release provenance. |
| Ontology reasoning | **OWL 2** (W3C; RL target) | Recommended | Export richer semantics when they fit the supported profile; live reasoning is not an MVP dependency. |
| Ontology model | **SKOS** (W3C) | Recommended | Glossaries and taxonomies (stages, categories, severities). |
| Serialisation | **Turtle**, **JSON-LD 1.1** | Core | Generated RDF review/export and linked-data interchange. |
| Query | **SQL** (ISO) | Core | MVP materialised read model, identity registry, lineage, and operational state. |
| Query | **SPARQL 1.1** (W3C) | Recommended | Query RDF exports or a future semantic graph runtime; not SQL/API source federation. |
| API query | **GraphQL** | Watch | Optional developer API after REST requirements are stable. |
| Property-graph query | **GQL** (ISO/IEC 39075) | Watch | Query a future property-graph projection; distinct from GraphQL. |
| Catalogue & lineage | **DCAT v3** (W3C) | Recommended | Standard, exportable source/dataset catalogue. |
| Catalogue & lineage | **OpenLineage** | Watch | Future run-level interoperability; MVP records equivalent identifiers in PostgreSQL. |
| Integration | **OpenAPI 3.1**, **JSON Schema 2020-12** | Core | Describe REST sources and services; validate proposal payloads and action contracts. |
| Integration | **JDBC / ODBC**, **S3 API** | Core | Relational/warehouse and object-storage connectivity. |
| Integration | **AsyncAPI**, **CloudEvents** | Watch | Event-stream sources and CDC (Phase 2). |
| Security | **OAuth 2.0 + RFC 9700**, **OpenID Connect**, **TLS 1.3**, **JWK** | Core | Current authentication/security baseline, transport, and key representation. |
| Security | **OAuth 2.1** | Watch | Track the active IETF draft; adopt after publication and provider support. |
| Security | **SCIM 2.0** | Recommended | Identity provisioning when enterprise tenant requirements need it. |
| Security | Policy-as-code (**OPA** or **Cedar**) | Recommended | Add one engine when RBAC/resource tags no longer express tested policies; do not deploy both. |
| AI interop | **MCP** | Recommended | Optional thin tools over the same query/action service contracts. |
| Version control | **Git** | Core | Canonical ontology/integration source, reviewable changes, protected release tags. |
| Artefact distribution | **OCI Image and Distribution specifications** | Core | Content-addressed connector images and generated release bundles. |
| Software supply chain | **SPDX** or **CycloneDX**; **SLSA provenance** | Recommended | SBOM and verifiable build provenance linked to release digests. |
| Operations | **SemVer**, **RFC 3339** | Core | Versioned releases and unambiguous timestamps. |
| Operations | **OpenTelemetry** | Recommended | Traces, metrics, and logs across services and connectors. |
| Vocabularies | schema.org, FOAF / Org, Time Ontology | Recommended | Reuse for people, orgs, and temporal concepts before inventing terms. |

## How we apply them

1. **One canonical source.** Reviewed ontology, integration code, mappings, contracts, migrations, and tests in a Git monorepo define the desired MVP release. PostgreSQL holds active runtime projections/state; generated formats and images are not edited independently.
2. **Generate, verify, and address by digest.** Every release exports RDF/OWL, SHACL, JSON-LD, and PROV-O and builds connector/action images. CI must prove that used LinkML features survive generation and publish outputs as immutable OCI artefacts. Unsupported, lossy, or non-reproducible output blocks release.
3. **Stable identity is contractual.** Every canonical object receives a stable IRI, and every source mapping declares the exact key and construction rule that produces it.
4. **Agents propose; deterministic code emits.** Agents return JSON-Schema-constrained proposals and LinkML patches with evidence. Trusted compilers and validators generate release artefacts.
5. **Standards do not imply a runtime product.** SPARQL, GraphQL, GQL, MCP, OpenLineage, OPA, and Cedar are adopted only when a tested capability needs them.

## Validation boundaries

“Validate before persistence” is too broad: raw evidence, rejected proposals, and failed action attempts must be retained precisely because they are not trusted. Validation instead occurs before promotion across a trust boundary.

| Artefact | Validation before it becomes trusted |
| --- | --- |
| Agent proposal | JSON Schema, LinkML syntax/profile, evidence references, policy classification |
| Product release | Source/code checks, generated-artifact parsing, LinkML↔SHACL conformance examples, connector/migration tests, stable-IRI/mapping checks, golden query/action tests, OCI digest/SBOM checks |
| API or action request | OpenAPI/JSON Schema, authentication, authorisation, expected model/source version |
| Materialised instance | Operational-contract transforms, relational constraints, identity resolution, quality checks; SHACL before an RDF projection is published |
| Raw evidence or failed attempt | Malware/type/size checks, classification, access and retention controls; never promoted directly |
