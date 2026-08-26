# Artifact and Repository Management

How Ontolox versions, stores, builds, and promotes ontology and integration artefacts without creating competing sources of truth.

Related docs: [buildtime-architecture.md](./buildtime-architecture.md) (proposal and release flow) · [runtime-architecture.md](./runtime-architecture.md) (activation and execution) · [storage.md](./storage.md) (persistent stores) · [standards.md](./standards.md) (portable formats).

## Decisions

1. **Git is the desired-state system of record** for reviewed ontology and integration source.
2. **One monorepo is used for the MVP** so coupled model, connector, mapping, contract, migration, and test changes can be released together.
3. **An OCI registry stores immutable build outputs**: connector/action images and generated release bundles.
4. **PostgreSQL stores operational state**: release/activation state, environment bindings, governance, runtime data, lineage, and audit.
5. **Evidence, secrets, telemetry, and business records remain in their specialised systems.**
6. A merge publishes source; it never activates production. A deployment operator requests activation after migration and smoke checks.

## Artefact storage map

### Source and release artefacts

| Artefacts | System of record | Writer | Runtime use |
| --- | --- | --- | --- |
| LinkML, vocabularies, mappings, identity rules, contracts | Git | Model/domain/data owners through approved pull requests | Compiled projections in PostgreSQL |
| Connector/action-adapter code, migration source, CI definitions, synthetic fixtures and tests | Git | Engineers/agents through technical review | Images and executable migrations are published in the OCI release |
| Pull requests, technical reviews and CI results | Git forge | Git forge and CI identities | Check/review IDs linked from the release |
| Domain, data-owner and action approvals | PostgreSQL governance schema | Governance service after authenticated decisions | Required by the release gate |
| Connector/action images | OCI registry | CI build identity | Deployment pulls exact digest |
| Generated RDF/OWL, SHACL, JSON-LD, JSON Schema, executable migrations, provenance, reports and SBOM | OCI release bundle | CI release identity | Projections/migrations loaded and digests verified at deployment |
| Immutable release manifest content | OCI release bundle | CI release identity | Verified copy and digest in PostgreSQL |
| Published release record and manifest copy | PostgreSQL model registry | Build-time release publisher | Release manager verifies before activation |
| Active release pointer and activation/rollback history | PostgreSQL model registry | Runtime release manager only, after operator request | Pinned by every ingestion, query and action |

### Runtime, evidence and external records

| Artefacts | System of record | Writer | Runtime use |
| --- | --- | --- | --- |
| Endpoints, schedules, tenant settings, enabled fields and secret references | PostgreSQL catalogue/runtime schemas | Platform/integration owner through governance API | Connector environment binding |
| Registered sources, schema profiles, classifications and freshness observations | PostgreSQL catalogue schema | Platform/integration owner and approved profile service | Discovery, policy and operations |
| Credentials, tokens, certificates and encryption keys | Deployment secret manager | Authorised secret administrator/platform | Resolved directly by connector/action process |
| Schema snapshots, bounded samples and source documents | S3-compatible evidence store | Approved profile/evidence service | Metadata, classification and digest indexed in PostgreSQL |
| Connector checkpoints, leases, retries, quarantine and reconciliation | PostgreSQL runtime schema | Connector/runtime services | Durable operational state |
| Identity registry and materialised business objects | PostgreSQL runtime schema | Identity/materialisation services | Query and action resolution |
| Proposals, approvals, lineage, audit and action state | PostgreSQL governance/audit schemas | Governance/runtime services through controlled APIs | Review, policy and traceability |
| Metrics, logs and traces | Deployment observability system | Instrumented services/connectors | Operations and incident response |
| Project, team/person, compliance, risk, and resource-allocation records | Respective 99x systems of record | Source applications/users; approved risk adapter for owner changes | Lineage-bearing materialised projection |

Never place secret values, identifiable source samples, runtime checkpoints, or business records in Git. Never hand-edit compiled PostgreSQL projections or store source code/container images as database or evidence blobs.

## MVP monorepo layout

```text
README.md
docs/
ontology/
  model/
  vocabularies/
integrations/
  projects/
    connector/
    tests/
  people/
    connector/
    tests/
  compliance/
    connector/
    tests/
  risks/
    connector/
    actions/
    tests/
  resources/
    connector/
    tests/
mappings/
  99x/
contracts/
  operational/
  queries/
  actions/
migrations/
fixtures/
  conformance/
  golden/
tooling/
  compiler/
  release/
.ci/
CODEOWNERS
```

This is a target layout, not a reason to create empty directories. Add a path when its first real artefact exists.

## Configuration boundary

| Concern | Example | Store |
| --- | --- | --- |
| Connector implementation and defaults | REST pagination, supported fields, timeout | Git → OCI image |
| Mapping and contract | `risk.project_ref → Project.project_code` | Git |
| Environment binding | Source URL, tenant, schedule, enabled fields | PostgreSQL |
| Secret reference | `secret://99x/risk/writer` | PostgreSQL |
| Secret value | OAuth secret or database password | Secret manager |
| Runtime state | Cursor, watermark, last poll, lease | PostgreSQL |

This keeps semantic/executable logic reviewable without putting secrets or mutable environment state in source control.

## Change and release flow

1. The workbench creates a PostgreSQL proposal with evidence, rationale, affected artefacts and required approvers.
2. A release bot opens an isolated Git branch and pull request linked to the proposal.
3. CI validates the exact candidate commit. Failures return structured findings to the proposal.
4. Domain/data/action owners approve the CI-passing commit in the workbench; technical code owners approve the same pull request commit.
5. A required check confirms that CI and approvals reference the same commit. Amendments—including a rebase—expire approvals and restart validation.
6. The release bot fast-forwards the protected branch and creates the SemVer tag on that exact approved commit. If the target branch has advanced, it creates a new candidate instead of producing an unapproved merge commit.
7. CI publishes digest-addressed images and one generated release bundle to the OCI registry. The release publisher writes the verified manifest to PostgreSQL.
8. The deployment operator runs migrations and smoke tests, then requests activation. The runtime release manager verifies prerequisites and atomically changes the active pointer.

Git is authoritative for the source diff, Git-forge metadata for technical review/CI checks, and PostgreSQL governance for business/domain approvals. The release manifest links all three.

## Required release checks

- secret/private-key/sensitive-sample scanning;
- formatting, unit, type and dependency tests;
- supported LinkML profile, stable IRI and mapping checks;
- deterministic generation and runtime-validator ↔ SHACL equivalence tests;
- connector, migration, identity, quarantine and golden-query tests;
- action idempotency, stale-version, timeout and reconciliation tests;
- image vulnerability scan, SBOM/build provenance and reproducible digest checks;
- breaking-change and required-approver calculation.

## Release bundle and manifest

The OCI release bundle contains generated ontology exports/schemas/provenance, the exact executable migration scripts and plan, test report, SBOM/build provenance, and an immutable manifest. Runtime references OCI digests, never mutable tags such as `latest`.

The manifest records:

- release ID, SemVer, Git commit/tag and proposal/approval IDs;
- release-bundle and connector/action image digests;
- model, mapping, identity, query, and action digests;
- the ordered migration IDs, paths, and payload digests contained in the bundle;
- compiler/dependency-lock and test-report digests;
- compatibility, activation prerequisites and rollback constraints.

PostgreSQL stores a verified manifest copy plus publication/activation state for efficient policy checks. It does not replace the immutable OCI bundle.

## Migration and activation

CI tests migrations but never applies them to production:

1. The deployment operator starts an isolated runner using the published bundle digest.
2. The runner locks the environment, verifies the current schema and each bundled script digest, applies only manifest-listed migrations from that bundle, and records their digests/results.
3. Failed transactional migrations roll back. Destructive/non-transactional changes require an approved recovery plan and compatible parallel read model.
4. After smoke tests, the operator requests activation with the migration/smoke-run IDs.
5. The runtime release manager verifies approvals, Git/OCI digests, migration state and compatibility; loads versioned projections; then changes the active pointer transactionally.

The migration runner cannot activate a release. The release manager cannot execute unlisted SQL or alter a manifest.

## Versioning and security

- The product release has one SemVer; connector images may also have package versions, but runtime pins digests.
- Compatible fixes are patch releases, compatible additions are minor releases, and breaking semantics/contracts/schemas are major releases.
- Published tags, migration IDs and OCI artefacts are immutable.
- Use protected branches, required checks, CODEOWNERS, least-privilege bots and short-lived CI identity.
- Agent changes use isolated branches and the same checks as human changes.
- Git fixtures are synthetic or irreversibly de-identified; CI retrieves minimum sandbox secrets from the secret manager and redacts logs/reports.

## Recovery

Git and OCI restore desired source/build outputs; PostgreSQL restores release, governance and runtime state; object storage restores retained evidence; the secret manager follows its own recovery procedure.

Recovery order:

1. Platform administrators restore identity/secrets, PostgreSQL, OCI and object-store access without starting connectors/actions.
2. The runtime release manager verifies the active manifest, Git/OCI digests, migrations, bindings and secret references; deployment nodes re-pull images by digest.
3. The release manager retains the active pointer only when all artefacts are consistent; otherwise it clears the pointer and the deployment operator replays the normal migration/smoke/activation flow for a known release.
4. The deployment operator resumes queries, then read connectors. Writes resume only after uncertain actions are reconciled against the risk system.

Git alone is never sufficient to recover runtime state or authorise a release/write.
