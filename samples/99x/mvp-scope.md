# MVP Scope

## Target users and priority use cases

The MVP is proven against **99x operations**: a live professional-services enterprise whose people, projects, commercial pipeline, delivery work, and facilities already span many systems.

### Primary users

- 99x leadership who need a single, governed view of how the company is operating.
- Delivery, people, finance, sales, marketing, and facilities owners who work across systems today.
- Platform and data teams responsible for connecting those systems and keeping meaning consistent.
- Application and AI-agent builders who need safe, business-level data and action interfaces.

### Design partner and proving ground

99x is the first operational domain. The ontology is built from how 99x actually works—not from a generic industry template. Success is measured by whether 99x can ask cross-system questions with lineage and execute a limited set of governed actions.

### 99x operational model

The initial ontology covers these business objects and the relationships between them:

- **Employees:** identity, role, team, location, utilisation, allocation, and employment status.
- **Employee HR activities:** leave requests and balances, training enrolments and completions, onboarding, and other people-ops events.
- **Projects:** engagements, teams, customers, timelines, delivery status, and commercial terms.
- **Project risks:** identified risks, owners, likelihood, impact, mitigation, and status against the related project.
- **Project compliance:** contractual obligations, audit evidence, process controls, and exception cases.
- **Client relations:** account ownership, stakeholder contacts, relationship health, meetings, and ongoing engagement context.
- **Employee career development:** skills, goals, reviews, learning, progression, and succession signals.
- **Financial information:** revenue, cost, margins, forecasts, invoices, and project economics.
- **Prospects and sales:** accounts, opportunities, proposals, stages, owners, and conversion history.
- **Marketing activities:** campaigns, events, content, leads, and attribution to the pipeline.
- **Facilities and buildings:** offices, rooms, capacity, occupancy, and workplace services.
- **Engineer work entries:** commits, pull requests, time entries, and issues linked to people and projects.
- **Customer complaints:** cases, severity, owners, related projects or contracts, and resolution state.

### Initial use cases

- **Delivery and utilisation:** who is on which project, how capacity is used, and where allocation, leave, or compliance is at risk.
- **Project risk and compliance:** surface open risks, owners, and control exceptions against live delivery and contract obligations.
- **Career, HR, and staffing:** match employee skills, leave, training, development goals, and availability to project demand.
- **Client relations:** connect account health, stakeholders, and complaints to the responsible project, team, and commercial owner.
- **Commercial and financial performance:** connect pipeline, live projects, invoices, and margins without reconciling spreadsheets.
- **Engineering work evidence:** relate commits, pull requests, issues, and time entries to projects, customers, and people.
- **Service and complaints:** close the loop from customer issues back to the responsible project, team, and contract.
- **Workplace operations:** relate people and teams to facilities, occupancy, and building services.
- **Enterprise AI grounding:** give copilots and agents permission-aware 99x context, source lineage, and approved action tools.

## Product principles

1. **Business meaning first.** Technical structures matter because they support a clear representation of the domain.
2. **Evidence over assertion.** Every semantic proposal and generated mapping should be explainable, traceable, and measurable.
3. **Human authority, agent leverage.** Automate labour, not accountability.
4. **Federate by default; materialise with intent.** Preserve systems of record while optimising selectively for operational workloads.
5. **Read and act through the same model.** Insight without governed execution is incomplete.
6. **Change is a first-class object.** Versioning, impact analysis, monitoring, and repair are core product capabilities.
7. **Secure by construction.** Permissions, policy, privacy, and auditability travel with data, meaning, and action.

## Initial MVP scope

The MVP should prove the complete loop against 99x operations rather than attempt universal enterprise coverage.

**MVP outcome:** connect a small set of 99x systems, automatically construct a reviewable ontology of 99x operations, answer cross-system questions with lineage, and execute a limited set of governed write-back actions.

**Included capabilities:**

- Connectors for a relational database, a SaaS application, file/document storage, and a REST API—used against 99x sources such as HR, project, finance, CRM, engineering, and facilities systems.
- Guided agent-led source discovery, schema profiling, and sample-data analysis.
- A semantic workbench where agents propose entities, relationships, definitions, and mappings for the 99x operational model, for review.
- A versioned ontology graph with provenance, confidence, and source lineage.
- Ontology query API and natural-language exploration with cited source paths.
- Policy-based access control and approval workflows, including tighter controls for financial, people, and customer data.
- One read scenario and one write/action scenario drawn from 99x operations—for example, a utilisation or complaint-resolution question, and a governed update such as assigning an owner or recording a compliance exception.
- Monitoring for source freshness, schema drift, mapping health, and agent evaluation.

**Explicitly deferred:** a broad connector marketplace, fully autonomous production changes, universal domain coverage beyond 99x operations, complex multi-region governance, and large-scale operational graph materialisation.

## Future roadmap

### Phase 1 — Prove the ontology loop on 99x operations

Deliver the MVP for the 99x operational model, demonstrate time-to-ontology, and validate reliable read and controlled write-back across people, HR, projects, risks, clients, commercial, engineering, and workplace data.

### Phase 2 — Expand autonomy and coverage

Add more connector patterns, reusable ontology templates derived from the 99x model, schema-drift remediation, richer workflow actions, and multi-agent collaboration across technical and business roles.

### Phase 3 — Build the enterprise ontology network

Support cross-domain ontology composition, reusable industry models, policy-as-code, simulation and impact analysis, high-scale graph workloads, and a developer ecosystem for ontology-native applications and agents.

### Phase 4 — Autonomous enterprise operations

Enable policy-bounded agents that continuously detect conditions, reason over enterprise state, propose decisions, and execute approved operations with explainability and full audit trails.

## Positioning and messaging

### Category

**AI-native Ontology Operating System**

### Core positioning

Ontolox.ai turns fragmented enterprise systems into a living, operational ontology that AI agents continuously build, maintain, and use to drive governed decisions and actions.

### One-liner

**Ontolox is the AI-native operating system that gives your enterprise a shared model of itself—and the ability to act on it.**

### Short pitch

Enterprise AI fails when it lacks trusted context and safe access to real operations. Ontolox agents discover and connect your systems, build and maintain the business ontology that unifies them, and expose it as a governed interface for questions, workflows, applications, and write-back actions.

The first proving ground is 99x: employees, HR activities, projects, risks, compliance, client relations, careers, finance, sales, marketing, facilities, engineering work, and customer complaints—unified into one operational model.

### Messaging pillars

- **From disconnected data to business reality:** unify systems around the objects, relationships, and rules that matter.
- **From consulting projects to continuous intelligence:** agents make ontology creation and maintenance an always-on capability.
- **From answers to outcomes:** read, write, and act through one governed enterprise model.
- **From AI experiments to trusted operations:** ground every agent in permissions, lineage, policy, and enterprise semantics.
