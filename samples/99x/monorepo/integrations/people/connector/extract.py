"""Minimised extraction of users and groups from the O365 directory.

The connector requests only the fields declared in connector.yaml, follows
OData pagination, and resumes incrementally from a stored delta link. It
returns raw source records tagged with run metadata; canonical mapping to
Person/Team happens downstream against the reviewed mapping release.
"""

from dataclasses import dataclass
from typing import Callable, Iterator

GRAPH_BASE = "https://graph.microsoft.com/v1.0"

USER_FIELDS = ("id", "displayName", "accountEnabled")
GROUP_FIELDS = ("id", "displayName", "membershipRule")

# Injected by the runtime: performs an authenticated GET and returns parsed
# JSON. Credentials are resolved from the secret reference by the platform;
# this module never sees a token value.
GraphGet = Callable[[str], dict]


@dataclass(frozen=True)
class SourceRecord:
    object_type: str          # "user" | "group"
    source_id: str
    payload: dict             # only supported fields
    tombstone: bool = False   # delta feed reported removal


def _minimise(item: dict, fields: tuple[str, ...]) -> dict:
    return {field: item.get(field) for field in fields}


def _paginate(get: GraphGet, url: str) -> Iterator[tuple[dict, str | None]]:
    """Yield (item, delta_link) pairs; delta_link is set on the final page."""
    while url:
        page = get(url)
        delta_link = page.get("@odata.deltaLink")
        next_link = page.get("@odata.nextLink")
        for item in page.get("value", []):
            yield item, delta_link if not next_link else None
        url = next_link


def extract_users(get: GraphGet, delta_link: str | None) -> tuple[list[SourceRecord], str | None]:
    """Extract users incrementally. Returns records and the next delta link."""
    url = delta_link or f"{GRAPH_BASE}/users/delta?$select={','.join(USER_FIELDS)}"
    records: list[SourceRecord] = []
    next_delta = None
    for item, delta in _paginate(get, url):
        next_delta = delta or next_delta
        records.append(
            SourceRecord(
                object_type="user",
                source_id=item["id"],
                payload=_minimise(item, USER_FIELDS),
                tombstone="@removed" in item,
            )
        )
    return records, next_delta


def extract_group_members(get: GraphGet, group_id: str) -> list[str]:
    """Return member user object IDs for one delivery-team group."""
    url = f"{GRAPH_BASE}/groups/{group_id}/members?$select=id"
    return [item["id"] for item, _ in _paginate(get, url)]
