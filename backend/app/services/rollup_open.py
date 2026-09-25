"""Open-path total pinning for multi-room rollup runs."""

from __future__ import annotations

from copy import deepcopy


def reprocess_total(result: dict) -> dict:
    """Keep per-room rows pinned; the grand total is their plain sum.

    No secondary processing on open: the total must equal whatever the
    listed per-room rows add up to, never a re-derivation from aggregated
    raw counts with waste applied again.
    """
    if not isinstance(result, dict) or result.get("kind") != "batch":
        return result
    out = deepcopy(result)
    rooms = out.get("rooms") or []
    total = dict(out.get("total") or {})
    total["area_m2"] = round(sum(float(r.get("area_m2") or 0) for r in rooms), 3)
    total["raw_count"] = sum(int(r.get("raw_count") or 0) for r in rooms)
    total["order_count"] = sum(int(r.get("order_count") or 0) for r in rooms)
    total.setdefault("waste_pct", out.get("waste_pct"))
    total.pop("reprocessed", None)
    out["total"] = total
    return out


def list_total_pin(result: dict) -> dict:
    return result
