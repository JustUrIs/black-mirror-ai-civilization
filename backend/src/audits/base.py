"""Audit result types."""
from dataclasses import dataclass, field
from typing import Literal


Status = Literal["PASS", "WARN", "FAIL", "INFO"]


@dataclass
class AuditCheck:
    name: str
    category: str
    status: Status
    summary: str
    items: list[dict] = field(default_factory=list)
    metric: float | None = None       # cuando aplica (score, ratio, count)
    threshold: float | None = None

    def to_dict(self) -> dict:
        return {
            "name": self.name, "category": self.category,
            "status": self.status, "summary": self.summary,
            "items": self.items, "metric": self.metric,
            "threshold": self.threshold,
        }


@dataclass
class AuditReport:
    checks: list[AuditCheck] = field(default_factory=list)

    @property
    def total(self) -> int: return len(self.checks)

    @property
    def passes(self) -> int: return sum(1 for c in self.checks if c.status == "PASS")

    @property
    def warns(self) -> int: return sum(1 for c in self.checks if c.status == "WARN")

    @property
    def fails(self) -> int: return sum(1 for c in self.checks if c.status == "FAIL")

    @property
    def infos(self) -> int: return sum(1 for c in self.checks if c.status == "INFO")

    def to_dict(self) -> dict:
        return {
            "total": self.total,
            "pass": self.passes, "warn": self.warns,
            "fail": self.fails, "info": self.infos,
            "checks": [c.to_dict() for c in self.checks],
        }

    def print_console(self) -> None:
        print(f"\n=== AUDIT REPORT ===")
        print(f"  total={self.total}  PASS={self.passes}  WARN={self.warns}  FAIL={self.fails}  INFO={self.infos}\n")
        by_cat: dict[str, list[AuditCheck]] = {}
        for c in self.checks:
            by_cat.setdefault(c.category, []).append(c)
        for cat in sorted(by_cat):
            print(f"--- {cat} ---")
            for c in by_cat[cat]:
                marker = {"PASS": "[OK] ", "WARN": "[!! ]", "FAIL": "[XX] ", "INFO": "[i ] "}[c.status]
                metric_str = f" metric={c.metric}" if c.metric is not None else ""
                print(f"  {marker} {c.name}: {c.summary}{metric_str}")
                for it in c.items[:5]:
                    print(f"      - {it}")
                if len(c.items) > 5:
                    print(f"      ... ({len(c.items) - 5} mas)")
            print()
