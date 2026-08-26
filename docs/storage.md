# Storage

What Ontolox persists and where. The first implementation favours a small operational footprint, explicit contracts, and standards-compliant exports over a live semantic-graph dependency.

Related docs: [artifact-management.md](./artifact-management.md) (authoritative artefact systems) · [standards.md](./standards.md) · [runtime-architecture.md](./runtime-architecture.md) · [buildtime-architecture.md](./buildtime-architecture.md).

## Accepted MVP storage profile

The MVP uses **one Git monorepo for canonical ontology, integration, mapping, contract, migration, and test source**, an **OCI-compatible registry for generated release bundles and connector images**, and **PostgreSQL for operational state**. Release automation generates RDF/OWL, SHACL, JSON-LD, JSON Schema, provenance, and runtime artefacts from a deliberately constrained LinkML profile. Generated artefacts are tested and versioned with the source but are not edited as competing Git sources of truth.

This profile is chosen because the 99x proof needs understandable review, deterministic cross-system joins, lineage, and one safe write-back—not live OWL inference or arbitrary SPARQL. A semantic graph service remains a later, evidence-triggered option.

## What we store, and where

| Category | Contents | MVP system of record |
| --- | --- | --- |
| Canonical ontology model | LinkML classes, relationships, constraints, stable IRIs | **Git** (reviewed YAML, immutable release tags) |
| Integration source | Connector/action-adapter code, transforms, templates, tests | **Git**; built images in **OCI registry** |
| Mapping and operational contracts | Source fields, transforms, identity keys, access mode, freshness, owner, quality expectations | **Git** with release; active projection in **PostgreSQL** |
| Action contracts | JSON Schema input, target adapter, policy, approval mode, idempotency and concurrency rules | **Git** with release; active projection in **PostgreSQL** |
| Generated release artefacts | RDF/OWL, SHACL, JSON-LD, JSON Schema, provenance, reports, SBOM/build provenance | Immutable bundle in **OCI registry** |
| Release registry | Verified manifest, publication state, active pointer, activation/rollback history | **PostgreSQL**; manifest's immutable bundle copy in **OCI registry** |
| Environment bindings | Endpoints, tenant, schedules, enabled fields, secret references | **PostgreSQL** |
| Connector runtime state | Checkpoints, watermarks, leases, retry/reconciliation and quarantine state | **PostgreSQL** |
| Identity registry | Canonical IRI ↔ source-system keys, match status, merge/split history | **PostgreSQL** |
| Materialised business objects | The approved MVP read model and source-version metadata | **PostgreSQL** |
| Metadata catalogue | Sources, schemas, profiles, classifications, deployed connector/image versions | **PostgreSQL** |
| Proposals and approvals | Proposed patch, confidence, rationale, evidence links, decisions, release linkage | **PostgreSQL** |
| Runtime lineage and audit | Extraction runs, field lineage, queries, action attempts/outcomes, model version | **PostgreSQL** (append-only permissions and integrity controls) |
| Evidence and documents | Samples, schema snapshots, source documents | **S3-compatible object storage** when required; content-addressed and retention-bound |
| Credentials | Connector secrets and keys | **Deployment-provided secret manager**; records contain secret references only |

The minimum runtime footprint is the Ontolox services plus **one PostgreSQL instance**. The delivery path also requires a Git forge and OCI-compatible registry; reuse the forge's registry where available. Add S3-compatible object storage only when document/sample evidence is required. Reuse the deployment's OIDC provider and secret manager; OpenBao is supported where a self-hosted option is required, but it is not a mandatory MVP service.

PostgreSQL is logically separated into schemas such as `model_registry`, `catalogue`, `runtime`, `governance`, and `audit`. They may share one database for the MVP while retaining explicit ownership and permissions.

See [artifact-management.md](./artifact-management.md) for the complete source/build/runtime matrix and monorepo layout.

## Constrained LinkML compilation

LinkML generators differ in feature coverage, so Ontolox defines and tests a supported authoring profile:

1. CI rejects LinkML features whose required targets cannot represent them faithfully.
2. Every release must generate and parse its required RDF/OWL, SHACL, JSON-LD, and JSON Schema artefacts.
3. Golden positive and negative examples must produce equivalent validation outcomes in the runtime validator and generated SHACL.
4. Generated artefacts carry the source release version and content digest.
5. A failed or lossy compilation blocks release; it is never silently accepted.

The initial supported profile is intentionally small:

| Supported in MVP | Rejected or deferred |
| --- | --- |
| Classes with single inheritance; slots; primitive/custom scalar types | Multiple inheritance, mixins, metaclasses, and custom metamodel extensions |
| Stable `class_uri`/`slot_uri`, descriptions, annotations, and version-pinned internal imports | Unpinned or remote imports |
| Required/optional fields, single/multivalued cardinality, numeric bounds, string patterns | Arbitrary expressions, dynamic rules, and generator-specific extensions |
| Enumerations with stable permissible-value identifiers | Dynamic enums and source-dependent schema generation |
| Object relationships represented by canonical IRI references | Blank-node-dependent identity or unrestricted `owl:sameAs` |
| Closed positive/negative validation examples | Advanced OWL axioms or features that cannot produce equivalent JSON Schema and SHACL checks |

The precise allow-list is executable CI configuration, versioned with the compiler. Adding a LinkML feature requires passing equivalence tests for every mandatory target before model authors may use it.

Agents propose typed patches to the canonical LinkML model. They do not independently author competing Turtle, SHACL, and SQL sources of truth.

## Operational contracts

Each active mapping is released with an operational contract containing at least:

- source and connector version;
- source object/field and canonical ontology property;
- transformation and null/error behaviour;
- canonical identity key and IRI construction rule;
- data classification and allowed readers;
- access mode (`materialised`, `federated`, or `cached`);
- freshness target, quality checks, and accountable owner;
- lineage granularity and retention;
- write-back/action semantics where applicable.

Connector source and reusable templates are reviewed in Git. CI builds a content-addressed OCI image; the release manifest pins its digest. Environment-specific endpoint/schedule settings and secret references live in PostgreSQL, while secret values remain in the secret manager. Secret values never enter proposals, Git, build artefacts, evidence, or agent context.

## Identity

Cross-system identity is explicit, not inferred at query time.

- Every canonical object has a stable IRI built from tenant, object type, and an immutable canonical identifier.
- MVP matching uses declared exact keys only—for example CRM customer ID, project code, and CRM user ID.
- Missing or ambiguous matches are quarantined for review; they are never silently joined.
- Source-key changes, merges, and splits are recorded without reusing an old IRI for a different object.
- Probabilistic entity resolution and unrestricted `owl:sameAs` reasoning are deferred.

## Materialisation and federation

The long-term principle remains **federate by default; materialise with intent**. The MVP deliberately materialises the selected cross-system slice because its acceptance test is a reliable join between a CRM API and a project database.

| Mode | Use when | MVP handling |
| --- | --- | --- |
| **Materialised** | Cross-source joins, repeatable acceptance tests, source load protection | Default for properties required by the complaint-resolution proof |
| **Federated** | One source can answer within a measured latency and availability budget | Not enabled in the MVP |
| **Cached** | Live access is required but bounded staleness is acceptable | Not enabled in the MVP; PostgreSQL cache table is the first later option |

Every materialised row records source keys, source version/timestamp, extraction run, mapping version, and active model release. Raw source systems remain authoritative.

## Versioning and lifecycle

- The canonical source release is a protected Git tag containing ontology, integration code, mappings, contracts, migrations, and tests.
- CI publishes connector/action-adapter images and a generated release bundle to the OCI registry, all addressed by digest rather than mutable tags.
- The build-time release publisher verifies the OCI bundle and writes its immutable manifest copy to PostgreSQL but cannot change the active-version pointer.
- A named deployment operator starts an isolated migration runner using the published OCI bundle; the runner applies/records only manifest-listed migrations and cannot activate a release. After smoke checks, the operator requests activation. The runtime release manager is the sole writer of the active-version pointer and performs the change transactionally.
- Query, lineage, and action records pin the exact active release used.
- SemVer policy: breaking model or contract changes increment major; backward-compatible additions increment minor; non-semantic corrections increment patch.
- Rollback is another operator-requested runtime transaction that moves the pointer to a previously published compatible release; data migrations or incompatible read models require an explicit rollback plan.
- A release is activated only after compilation, validation, golden-query tests, action-contract tests, and required approvals pass.

Proposal paths are:

- accepted: `draft → queued → in_review → validated → approved → released`;
- declined: `draft/queued/in_review/validated → rejected`;
- abandoned: any pre-release state → `withdrawn` or `superseded`.

An amendment after validation or approval returns the proposal to `in_review` and expires prior approvals. `rejected`, `withdrawn`, and `superseded` are terminal. Released proposals link to the published release manifest; activation is recorded separately because a published release may never become active.

## Retention and integrity

- Evidence samples are minimised, classified, encrypted, access-controlled, and deleted according to source-specific retention.
- Append-only audit means application roles cannot update/delete audit rows; database controls and chained record digests provide tamper evidence.
- Rejected and invalid artefacts may be persisted in the evidence/proposal stores, but they are never promoted into an active release or trusted read model.

## Decision points after MVP

1. **Semantic graph runtime** — add Fuseki or another evaluated RDF store only when a tested requirement needs SPARQL, RDF-native materialisation, or OWL inference. Validate SHACL write enforcement and the exact inference profile; do not assume either is automatic.
2. **Live federation** — generalise SQL/API planning only after source capability, latency, failure, and lineage semantics are proven.
3. **Dedicated cache** — add Valkey when PostgreSQL cache tables fail measured throughput or latency targets.
4. **Standard run lineage** — emit OpenLineage when interoperability with external data platforms is required; keep the MVP lineage schema exportable.
5. **Vector service** — add pgvector, then a dedicated vector store, only when retrieval evaluation demonstrates value and scale requires it.
6. **CDC/event streaming** — replace polling with Kafka/CloudEvents when freshness targets cannot be met economically.
7. **Property-graph projection** — evaluate AGE or another engine only for demonstrated traversal workloads.
