"""002: Row-Level Security policies.

Enables RLS on every table and creates the instance_isolation policy.
FastAPI middleware injects:
    SET LOCAL app.instance_id = '<jwt-sub-uuid>'
per request so the policy filters rows automatically.

decision_ledger and accountability_link_events are insert-only for owners
(no DELETE policy — audit trail is permanent for the owning instance).

Revision ID: 002_rls_policies
"""
from __future__ import annotations

from alembic import op

revision = "002_rls_policies"
down_revision = "001_initial_schema"
branch_labels = None
depends_on = None


# Tables whose instance_id can be read via the standard policy
_STANDARD_TABLES = (
    "identity_state",
    "goals",
    "tasks",
    "task_dependencies",
    "calendar_sync_state",
    "model_execution_log",
)

# Insert-only audit tables — no DELETE or UPDATE policies
_AUDIT_TABLES = ("decision_ledger", "accountability_link_events")


def upgrade() -> None:
    # ── Standard instance isolation ───────────────────────────────────────────
    for table in _STANDARD_TABLES:
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
        op.execute(f"""
            CREATE POLICY instance_isolation ON {table}
                USING (instance_id = current_setting('app.instance_id', true)::uuid)
        """)

    # ── Audit tables: owners can insert + select; no delete ───────────────────
    for table in _AUDIT_TABLES:
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
        op.execute(f"""
            CREATE POLICY instance_isolation ON {table}
                FOR SELECT
                USING (instance_id = current_setting('app.instance_id', true)::uuid)
        """)
        op.execute(f"""
            CREATE POLICY instance_insert ON {table}
                FOR INSERT
                WITH CHECK (instance_id = current_setting('app.instance_id', true)::uuid)
        """)

    # ── Accountability links: owner sees by owner_instance_id ─────────────────
    # Viewer access uses the token-based endpoint which bypasses RLS.
    op.execute("ALTER TABLE accountability_links ENABLE ROW LEVEL SECURITY")
    op.execute("""
        CREATE POLICY owner_isolation ON accountability_links
            USING (owner_instance_id = current_setting('app.instance_id', true)::uuid)
    """)

    # ── task_dependencies inherits via tasks JOIN — also lock directly ─────────
    # task_dependencies has no instance_id column; the tasks FK join provides
    # the isolation boundary.  We rely on the tasks RLS policy for security.


def downgrade() -> None:
    for table in _STANDARD_TABLES + _AUDIT_TABLES + ("accountability_links",):
        op.execute(f"DROP POLICY IF EXISTS instance_isolation ON {table}")
        op.execute(f"DROP POLICY IF EXISTS instance_insert ON {table}")
        op.execute(f"DROP POLICY IF EXISTS owner_isolation ON {table}")
        op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY")
