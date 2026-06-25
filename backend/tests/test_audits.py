"""Test the audit framework against the demo_seed state."""
import logging
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

TEST_DB = HERE / "test_audits.db"
TEST_CACHE = HERE / "test_audits_cache"
os.environ["DB_PATH"] = str(TEST_DB)
os.environ["LLM_CACHE_DIR"] = str(TEST_CACHE)

if TEST_DB.exists(): TEST_DB.unlink()
if TEST_CACHE.exists(): shutil.rmtree(TEST_CACHE)

logging.basicConfig(level=logging.WARNING)

from src.sim.demo_seed import reset_and_seed_demo
from src.audits.runner import run_all_audits


def main():
    reset_and_seed_demo()
    r = run_all_audits()

    # Sanity checks
    assert r.total >= 20, f"expected >=20 checks, got {r.total}"
    assert r.fails == 0, f"unexpected FAILs: {[c.name for c in r.checks if c.status=='FAIL']}"

    # Specific: coherence audit should catch the incoherent book demo
    books_coh = next(c for c in r.checks if c.name == "books_coherence")
    assert books_coh.status == "WARN", f"expected WARN on incoherent book, got {books_coh.status}"
    assert any("fuego" in (i.get("tokens_inexistentes") or []) for i in books_coh.items), \
        "expected 'fuego' in books_coherence violations"

    # Specific: moral_lines should catch Borges' short-content attempts
    moral = next(c for c in r.checks if c.name == "moral_lines_respected")
    assert moral.status in ("WARN", "FAIL"), f"expected WARN/FAIL, got {moral.status}"

    # Specific: civilization_output should be PASS (>=3 artifacts)
    civ = next(c for c in r.checks if c.name == "civilization_output")
    assert civ.status == "PASS", f"expected PASS civ output, got {civ.status}"

    # Specific: sealed world action_log_origins must be PASS
    origins = next(c for c in r.checks if c.name == "action_log_origins")
    assert origins.status == "PASS", f"expected PASS origins, got {origins.status}"

    # Specific: artifacts_have_authors must be PASS
    auth = next(c for c in r.checks if c.name == "artifacts_have_authors")
    assert auth.status == "PASS", f"expected PASS authors, got {auth.status}"

    print(f"\nAudit test PASSED. {r.passes} PASS, {r.warns} WARN, "
          f"{r.fails} FAIL, {r.infos} INFO out of {r.total}")
    print("Framework working correctly: detected real warnings (incoherent book, "
          "moral_line violation) and confirmed sealed-world integrity.\n")


if __name__ == "__main__":
    main()
