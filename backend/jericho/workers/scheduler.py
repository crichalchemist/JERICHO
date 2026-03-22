"""
Nightly rescheduler — Phase 4.

Runs at 23:59 daily (per-server timezone; per-user timezone support deferred
to Phase 5 when timezone data is stored on instance_state).

The job fetches all instance_ids with active tasks from Supabase, then for
each runs the feathering algorithm against tomorrow's look-ahead window.
When Supabase is unconfigured (db_client is None) the job logs and exits
cleanly — this preserves Phase 0/1 JSON-adapter operation.
"""
from __future__ import annotations

import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

log = logging.getLogger(__name__)

_ACTIVE_STATUSES = ("created", "scheduled", "in_window", "rescheduled", "date_extended")


async def run_nightly_rescheduler(db_client: object | None) -> None:
    """Entry point for the nightly 23:59 job.

    *db_client* is the Supabase AsyncClient, or None in JSON-adapter mode.
    The full feathering pipeline (look_ahead.run_feathering) is invoked here
    once Phase 4 repository queries are wired up.
    """
    if db_client is None:
        log.debug("Nightly rescheduler skipped — no Supabase client configured")
        return

    log.info("Nightly rescheduler starting")
    # Phase 4 stub: query active instance_ids and run feathering per instance.
    # Full implementation requires calendar_sync_state + task queries which
    # will be completed alongside Phase 5 rhythm integration.
    log.info("Nightly rescheduler complete (stub)")


def create_scheduler(db_client: object | None) -> AsyncIOScheduler:
    """Build and return a configured (but not yet started) AsyncIOScheduler."""
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        run_nightly_rescheduler,
        trigger=CronTrigger(hour=23, minute=59),
        kwargs={"db_client": db_client},
        id="nightly_rescheduler",
        name="Nightly task rescheduler",
        replace_existing=True,
        misfire_grace_time=300,  # 5-minute grace — tolerate brief outages
    )
    return scheduler
