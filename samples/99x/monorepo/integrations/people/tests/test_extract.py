"""Contract tests for the O365 directory extraction against stubbed Graph pages."""

from integrations.people.connector.extract import extract_users, extract_group_members

PAGE_1 = {
    "value": [
        {"id": "u-001", "displayName": "Synthetic One", "accountEnabled": True,
         "mail": "must-not-be-extracted@example.test"},
        {"id": "u-002", "displayName": "Synthetic Two", "accountEnabled": False},
    ],
    "@odata.nextLink": "https://graph.microsoft.com/v1.0/users/delta?$skiptoken=page2",
}

PAGE_2 = {
    "value": [
        {"id": "u-003", "@removed": {"reason": "deleted"}},
    ],
    "@odata.deltaLink": "https://graph.microsoft.com/v1.0/users/delta?$deltatoken=next-run",
}

MEMBERS_PAGE = {"value": [{"id": "u-001"}, {"id": "u-002"}]}


def stub_get(url: str) -> dict:
    if "skiptoken=page2" in url:
        return PAGE_2
    if "/members" in url:
        return MEMBERS_PAGE
    return PAGE_1


def test_extracts_all_pages_and_returns_delta_link():
    records, delta = extract_users(stub_get, delta_link=None)
    assert [r.source_id for r in records] == ["u-001", "u-002", "u-003"]
    assert delta == "https://graph.microsoft.com/v1.0/users/delta?$deltatoken=next-run"


def test_payloads_are_minimised_to_supported_fields():
    records, _ = extract_users(stub_get, delta_link=None)
    assert set(records[0].payload) == {"id", "displayName", "accountEnabled"}
    assert "mail" not in records[0].payload


def test_removed_users_become_tombstones():
    records, _ = extract_users(stub_get, delta_link=None)
    tombstones = [r for r in records if r.tombstone]
    assert [r.source_id for r in tombstones] == ["u-003"]


def test_group_members_returns_ids_only():
    assert extract_group_members(stub_get, "g-100") == ["u-001", "u-002"]
