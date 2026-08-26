# Ontolox.ai — Product Concept

## Executive summary

Ontolox.ai is an AI-native Ontology Operating System for the enterprise. It turns an organisation's fragmented systems, data, documents, and operational knowledge into a living ontology: a trusted, business-readable model of how the enterprise works that can both understand data and safely act on it.

Unlike ontology programmes that depend on long consulting engagements, manual semantic modelling, and prebuilt integrations, Ontolox uses coordinated AI assistance to discover sources, propose and test integrations, explore schemas and samples, infer domain concepts and relationships, and propose mapping repairs as systems change. Accountable owners approve trusted model and production-access changes; runtime services execute approved contracts. The result is an operational ontology layer that gives people and software a consistent way to query and safely write back to the enterprise.

Ontolox makes enterprise ontology engineering an agent-assisted, governed software process, with autonomy introduced only where quality, rollback, and policy controls have been proven.

## The problem

Enterprise data is distributed across databases, SaaS applications, APIs, data lakes, spreadsheets, documents, and line-of-business systems. Each source represents only a partial, technical view of the organisation. The shared meaning behind terms such as *customer*, *order*, *asset*, *risk*, or *case* lives in people, process documents, and tribal knowledge—not in a durable system of record.

This fragmentation creates persistent constraints:

- Data teams spend disproportionate time connecting systems, reconciling schemas, and repairing pipelines.
- Business logic is reimplemented across reports, applications, and AI workflows, producing inconsistent answers and brittle automation.
- Semantic modelling and ontology programmes are valuable but expensive, slow to implement, and difficult to keep current.
- Most analytics layers are read-only. They can describe the enterprise, but cannot reliably drive governed action back into operational systems.
- Generative AI lacks a dependable grounding layer, so its outputs are often disconnected from enterprise context, permissions, and operational truth.

The consequence is an enterprise that has data everywhere but a coherent, actionable model of itself nowhere.

## Product thesis

The next enterprise system of intelligence will be built around a living ontology, not a static data catalogue or a collection of disconnected copilots.

That ontology must be able to evolve at software speed. AI agents should perform the repetitive, evidence-driven work that has traditionally required specialist integration and ontology teams, while people retain control over policy, high-impact decisions, and semantic approval. The ontology must also be operational: it should provide a governed interface for both reading enterprise state and executing approved actions.

Ontolox is built on three beliefs:

1. **The ontology is the enterprise interface.** It expresses business objects, relationships, rules, and actions in terms users and AI systems can understand.
2. **Ontology engineering should be agent-led and human-governed by design.** Agents gather evidence and propose, generate, test, monitor, and repair; domain and technical owners approve every change that affects the runtime-trusted model or production access.
3. **Context is only useful when it can drive work.** The same model that answers a question should be able to initiate a governed update, workflow, or write-back to the system of record.

## What is an AI-native Ontology Operating System?

An AI-native Ontology Operating System is a platform that continuously creates, operates, and evolves a semantic model of an enterprise from its real systems and knowledge.

It unifies five capabilities in one governed platform:

- **Discovery:** identify sources, interfaces, structures, and business context.
- **Integration:** configure, generate, test, and maintain connections and data movement.
- **Understanding:** infer entities, attributes, relationships, definitions, and business rules from technical metadata and organisational evidence.
- **Operations:** expose the ontology as a controlled read/write/action interface for users, applications, workflows, and agents.
- **Governance:** maintain lineage, access controls, confidence, review workflows, observability, and auditability throughout the lifecycle.

The ontology is therefore not a documentation artefact layered over data. It is a persistent operational model that connects enterprise intent to enterprise systems.

## Four logical product capabilities

These capabilities describe the target product. The first implementation runs discovery, profiling, proposal, review, and validation as one orchestrated pipeline; it does not require four independently deployed autonomous agent systems.

### 1. Source discovery and integration

This pipeline creates the enterprise's connectivity foundation. Discovery agents inventory databases, warehouses, APIs, file stores, SaaS applications, event streams, and unstructured repositories. They inspect available metadata, interfaces, permissions, and change signals to identify viable sources.

Integration agents propose connector metadata, authentication patterns, extraction methods, and sync schedules. They generate versioned integration definitions and validate them in a controlled profile mode. Technical owners approve production access and secret references; runtime deploys the approved connector version and reports health or schema changes. CDC is introduced only when polling cannot meet an agreed freshness target.

**Output:** governed source connections with technical metadata, freshness signals, and documented operational contracts.

### 2. Data exploration and extraction

Once connected, exploration agents profile schemas, sample records, data quality, keys, enumerations, and usage patterns. They detect likely joins, identify sensitive fields, distinguish transactional from reference data, and trace useful signals from both structured and unstructured material.

Extraction agents create the transformations and incremental pipelines needed to make relevant data available for ontology-backed reads. They preserve source-level lineage and avoid unnecessary centralisation: data can be federated, materialised, or cached according to latency, scale, and governance needs.

**Output:** a quality-assessed, traceable evidence layer that supports semantic modelling and reliable access.

### 3. Semantic ontology engineering

Semantic agents translate technical structures and business evidence into an evolving domain model. They propose business entities, properties, relationships, classifications, definitions, lifecycle states, calculations, constraints, and mappings to source fields.

They use multiple evidence types—schemas, samples, documentation, APIs, dashboards, tickets, and expert feedback—to build confidence and explain every proposal. When concepts conflict across systems, agents surface the ambiguity rather than silently flattening it. Domain owners review and approve material semantic decisions; approved definitions become reusable enterprise primitives.

**Output:** a versioned ontology with business semantics, source mappings, provenance, confidence, and review history.

### 4. Ontology operations

Deterministic query and action services make the ontology useful in daily work. Applications call versioned contracts directly; AI agents may translate natural-language requests into approved query templates or action requests. They cannot invent unrestricted source queries, bypass policy, or execute unapproved writes.

For approved actions, the action service resolves an intent—such as updating an account, opening a case, assigning inventory, or launching a workflow—through a versioned adapter and contract. Schema validation, permissions, exact-payload approval, idempotency, source-version checks, reconciliation, and audit trails protect operational integrity.

**Output:** a consistent read/write/action interface for people, applications, and AI agents.

## The persistent ontology layer

At the centre of Ontolox is a persistent ontology layer: a durable, versioned representation of business reality that remains stable even as underlying systems change.

It holds:

- **Business objects:** customers, products, assets, employees, orders, contracts, cases, and domain-specific concepts.
- **Semantic relationships:** ownership, dependency, hierarchy, eligibility, containment, causality, and lifecycle links.
- **Definitions and rules:** canonical terms, calculations, policies, constraints, and permitted actions.
- **Mappings and lineage:** the connection from every ontology property and relationship back to source systems, fields, transformations, and evidence.
- **Operational contracts:** data freshness, quality expectations, access policies, write-back semantics, and action approvals.
- **Knowledge of change:** versions, confidence, proposed updates, approvals, and impact analysis.

The layer is logical, not a requirement for one physical datastore. The MVP keeps ontology and integration source—LinkML, connectors, mappings, contracts, migrations, and tests—in one Git monorepo; CI publishes generated standards artefacts and connector images to an OCI-compatible registry; PostgreSQL operates the approved projections and runtime state. Future workloads may justify a live semantic graph, federated access, caches, or graph projections.

## Read, write, and action capability

Ontolox treats enterprise operations as a closed loop:

> **Sources → evidence and data → ontology → insight or action → systems of record**

**Read** gives users and agents a business-level way to ask questions across systems—for example, “Which customers are at risk because of unresolved delivery exceptions?”—with permissions, semantics, and lineage applied consistently.

**Write** allows controlled changes through ontology objects. A user or agent can update an approved property while Ontolox resolves the correct source, validates policy and schema constraints, executes the change, and records the result.

**Action** extends write capability to multi-step business operations: trigger a workflow, create a service case, hold an order, request approval, notify an owner, or invoke an external automation. Every action is governed by role, policy, execution mode, and audit requirements.

## How the agents maintain the system

Ontolox agents operate as a continuous lifecycle rather than a one-time implementation project:

1. Detect a new source, changed schema, failing integration, altered data pattern, or emerging business concept.
2. Gather evidence and assess impact on existing mappings, definitions, downstream queries, and actions.
3. Propose a connector change, pipeline repair, ontology update, or mapping revision with confidence and rationale.
4. Test the proposal in a safe environment against policy, quality checks, and known behaviours.
5. Store non-authoritative observations automatically; route every runtime-trusted model, mapping, identity, connector-access, or action-contract change to the appropriate owner for approval.
6. Monitor the live result, preserve lineage and version history, and learn from feedback.

Automation is bounded by governance. Non-authoritative catalogue observations—profile runs, freshness, and schema hashes—may be recorded automatically. Any enrichment of the active model, mapping, identity rule, source access, or action contract requires explicit accountable-owner review.

## Conceptual architecture

| Layer | Primary responsibility |
| --- | --- |
| **Enterprise sources** | Operational systems, warehouses, APIs, files, documents, events, and knowledge repositories. |
| **Connectivity and data plane** | Connectors, authentication, extraction, change capture, transformation, federation, and materialisation. |
| **Agent orchestration plane** | Evidence gathering and constrained proposals across discovery, integration, exploration, semantic modelling, monitoring, and remediation. |
| **Ontology and knowledge plane** | Entities, relationships, rules, mappings, lineage, versioning, evidence, confidence, graph services, and retrieval. |
| **Governance and control plane** | Identity, entitlements, policy, approval workflows, privacy controls, evaluation, observability, and audit. |
| **Experience and action plane** | Search, analytical apps, APIs, SDKs, workflows, copilots, autonomous agents, and controlled write-back. |

## First implementation profile

The 99x MVP deliberately proves one vertical slice before broad enterprise coverage:

- **Scenario:** unresolved customer complaints connected to active/at-risk projects and current owners.
- **Sources:** one CRM REST API and one project SQL database; optional documents are evidence, not a mandatory live join.
- **Model:** Complaint, Project, Customer, Owner, and Contract only where needed.
- **Read:** a materialised, versioned query contract with field-level lineage, freshness, and explicit partial/stale outcomes.
- **Write:** one governed CRM owner-assignment action with exact-payload approval, idempotency, source-version checks, and reconciliation.
- **Source and delivery:** one Git monorepo for ontology/integration source and one OCI registry for digest-pinned release bundles and connector images.
- **Runtime:** PostgreSQL; reuse deployment OIDC and secret management; object storage only when document evidence is required.
- **Interfaces:** REST/OpenAPI, with optional MCP wrappers and natural-language selection of approved query templates.
- **Deferred:** live runtime federation, live OWL/SPARQL reasoning, automatic model repair, general NL planning, GraphQL/GQL, and extra infrastructure without a measured requirement.

See [samples/99x/mvp-scope.md](./samples/99x/mvp-scope.md) for acceptance gates.

## Documentation

Technical design for the first implementation:

| Document | What it covers |
| --- | --- |
| [Build-time architecture](./docs/buildtime-architecture.md) | How source evidence becomes an approved, immutable model release. |
| [Runtime architecture](./docs/runtime-architecture.md) | How a release governs ingestion, a cross-system read, and one safe write-back. |
| [Artifact management](./docs/artifact-management.md) | Git as source of truth, OCI release bundles, and promotion without competing stores. |
| [Storage](./docs/storage.md) | What the MVP persists and where (Git, OCI, PostgreSQL). |
| [Standards](./docs/standards.md) | Open standards by adoption level (Core, Recommended, Watch). |

## Differentiation

| Dimension | Traditional ontology platform | Palantir-style ontology approach | Ontolox.ai |
| --- | --- | --- | --- |
| Creation model | Manual modelling by specialists | Powerful platform, typically configured through implementation programmes | Agents gather evidence and propose changes; deterministic tooling generates/tests artefacts; accountable owners approve releases |
| Integration model | Connector-led, hand-configured | Broad integration tooling, often implementation-intensive | Agents propose and test versioned integration definitions; approved runtime connectors execute and report drift |
| Semantic lifecycle | Project-based and documentation-heavy | Operational but commonly expert-led | Continuous, evidence-backed, versioned, and maintained through agent-proposed changes |
| AI role | Often an add-on for search or assistance | AI runs on top of a configured ontology | AI is native to the creation, maintenance, and operation of the ontology |
| Adaptation to change | Manual remediation | Requires platform and delivery-team intervention | Detect–assess–test–propose loop; policy and accountable owners govern repair promotion |
| User experience | Technical semantic tooling | Sophisticated enterprise applications | Business-readable enterprise interface for humans and AI agents, with lineage and action controls |

The distinction is not “Palantir, with a chatbot.” Palantir demonstrated the value of an operational ontology. Ontolox is designed to make building and evolving that ontology an evidence-backed, governed, repeatable software capability that can earn bounded autonomy over time.
