# 99x MVP Monorepo Sample

A sample of the Git monorepo layout defined in [artifact-management.md](../../../docs/artifact-management.md), populated with representative artefacts for the project-delivery-assurance MVP described in [mvp-scope.md](../mvp-scope.md).

Everything here is illustrative: identifiers, endpoints, and values are synthetic. Only the `people` source role (the O365 / Microsoft Entra directory) carries a worked connector example; the other integrations follow the same pattern.

## Layout

```text
README.md
CODEOWNERS
.ci/
  release-checks.yaml            # required checks per artifact-management.md
ontology/
  model/
    delivery-assurance.yaml      # canonical LinkML model
  vocabularies/
    delivery-enums.yaml          # controlled enumerations
integrations/
  hr/                        # O365 directory source role
    connector/
      connector.yaml             # reviewed template: fields, capabilities, defaults
      extract.py                 # minimised Microsoft Graph extraction
    tests/
      test_extract.py
mappings/
  99x/
    people-directory.mapping.yaml
contracts/
  operational/
    people-directory.operational.yaml
  queries/
    projects-needing-attention.query.yaml
  actions/
    assign-risk-owner.action.yaml
migrations/
  0001_people_read_model.sql
fixtures/
  conformance/
    person.valid.yaml
    person.invalid.yaml
  golden/
    projects-needing-attention.case-001.yaml
```

Paths from the target layout that have no artefact yet (`integrations/projects`, `integrations/compliance`, `integrations/risks`, `integrations/resources`, `tooling/`, `docs/`) are intentionally absent: a path is added when its first real artefact exists.

## What is deliberately not here

- **Secret values and environment bindings.** Tenant IDs, endpoints, schedules, and credentials live in PostgreSQL and the secret manager; source files carry opaque references such as `secret://99x/hr/reader`.
- **Generated artefacts.** RDF/OWL, SHACL, JSON-LD, JSON Schema, and provenance exports are CI outputs published to the OCI release bundle, never committed here.
- **Real records.** Fixtures are synthetic; no identifiable 99x person, project, or risk data may enter this repository.
