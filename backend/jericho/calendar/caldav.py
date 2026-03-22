"""
CalDAV backend.

Correlation: VEVENT UID is set to task.id so we can reliably look up
events without storing a separate external_event_id (the UID *is* the id).
The custom X-JERICHO-TASK-ID property carries the same value for integrations
that parse raw iCalendar data directly (e.g., native iOS client).

Duration is stored as an all-day event (DATE, not DATETIME) matching the
Google backend — Jericho schedules at day granularity.
"""
from __future__ import annotations

from datetime import date, timedelta

import caldav  # type: ignore[import-untyped]
from caldav import DAVClient  # type: ignore[import-untyped]

from jericho.domain.types import Task

_VCALENDAR_TEMPLATE = """\
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Jericho//Jericho 2.0//EN
BEGIN:VEVENT
UID:{uid}
SUMMARY:{summary}
DTSTART;VALUE=DATE:{dtstart}
DTEND;VALUE=DATE:{dtend}
X-JERICHO-TASK-ID:{uid}
END:VEVENT
END:VCALENDAR"""


def _fallback_date() -> date:
    """Return today when task has no scheduled_date (should not normally occur)."""
    from datetime import date as _date
    return _date.today()


def _build_ical(task: Task) -> str:
    day = task.scheduled_date or _fallback_date()
    # DTEND is exclusive in iCalendar; add 1 day for single-day all-day events.
    return _VCALENDAR_TEMPLATE.format(
        uid=task.id,
        summary=task.title,
        dtstart=day.strftime("%Y%m%d"),
        dtend=(day + timedelta(days=1)).strftime("%Y%m%d"),
    )


class CalDAVBackend:
    """CalDAV calendar backend."""

    def __init__(self, url: str, username: str, password: str) -> None:
        self._client = DAVClient(url=url, username=username, password=password)

    def _calendar(self) -> caldav.Calendar:
        principal = self._client.principal()
        calendars = principal.calendars()
        if not calendars:
            raise RuntimeError("No calendars found for CalDAV account")
        # Use the first calendar (typically the default one).
        return calendars[0]

    async def create_event(self, task: Task) -> str:
        """Add a VEVENT and return task.id as external_event_id."""
        cal = self._calendar()
        cal.save_event(_build_ical(task))
        # The UID (task.id) is the stable identifier — return it as the external id.
        return task.id

    async def update_event(self, task: Task, external_event_id: str) -> None:
        """Fetch event by UID and overwrite with fresh iCalendar data."""
        cal = self._calendar()
        results = cal.search(uid=external_event_id, event=True)
        if not results:
            # Event was deleted externally — recreate it.
            cal.save_event(_build_ical(task))
            return
        event = results[0]
        event.data = _build_ical(task)
        event.save()

    async def delete_event(self, external_event_id: str) -> None:
        """Delete event by UID; silently succeeds if already gone."""
        cal = self._calendar()
        results = cal.search(uid=external_event_id, event=True)
        if results:
            results[0].delete()
