"""Audit runner: orchestrates all categories, returns AuditReport."""
import logging
from sqlalchemy.orm import Session

from ..db.session import get_session
from ..db.schema import WorldState
from .base import AuditReport
from .coherence import run_coherence_checks
from .personality import run_personality_checks
from .sealed_world import run_sealed_world_checks
from .capability import run_capability_checks


log = logging.getLogger("audit")


def run_all_audits(session: Session | None = None) -> AuditReport:
    own_session = False
    if session is None:
        session = get_session()
        own_session = True
    try:
        ws = session.get(WorldState, 1)
        report = AuditReport()
        report.checks.extend(run_coherence_checks(session, ws))
        report.checks.extend(run_personality_checks(session))
        report.checks.extend(run_sealed_world_checks(session))
        report.checks.extend(run_capability_checks(session))
        return report
    finally:
        if own_session:
            session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    r = run_all_audits()
    r.print_console()
