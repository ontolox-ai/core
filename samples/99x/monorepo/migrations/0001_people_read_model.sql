-- 0001: materialised read model for the people/team slice.
-- Applied only by the isolated migration runner from the published release
-- bundle; filename and ID are immutable after publication.

CREATE SCHEMA IF NOT EXISTS read_model;

CREATE TABLE read_model.person (
    person_id        text PRIMARY KEY,          -- immutable Entra user object ID
    display_name     text NOT NULL,
    active           boolean NOT NULL,
    -- field-level lineage
    source_version   text NOT NULL,             -- directory delta/version marker
    extraction_run   uuid NOT NULL,
    mapping_version  text NOT NULL,
    model_release    text NOT NULL,
    materialised_at  timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE read_model.team (
    team_id          text PRIMARY KEY,          -- immutable Entra group object ID
    name             text NOT NULL,
    active           boolean NOT NULL,
    team_lead_id     text REFERENCES read_model.person (person_id),
    source_version   text NOT NULL,
    extraction_run   uuid NOT NULL,
    mapping_version  text NOT NULL,
    model_release    text NOT NULL,
    materialised_at  timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE read_model.team_membership (
    team_id          text NOT NULL REFERENCES read_model.team (team_id),
    person_id        text NOT NULL REFERENCES read_model.person (person_id),
    source_version   text NOT NULL,
    extraction_run   uuid NOT NULL,
    PRIMARY KEY (team_id, person_id)
);

-- Quarantined directory records: never joined, always reported.
CREATE TABLE read_model.people_quarantine (
    quarantine_id    bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    object_type      text NOT NULL CHECK (object_type IN ('user', 'group', 'membership')),
    source_id        text NOT NULL,
    rule             text NOT NULL,
    detail           jsonb NOT NULL,
    extraction_run   uuid NOT NULL,
    recorded_at      timestamptz NOT NULL DEFAULT now()
);
