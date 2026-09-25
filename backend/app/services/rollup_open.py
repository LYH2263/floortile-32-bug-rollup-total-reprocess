"""Open-path handling for multi-room rollup runs.

The batch total is fixed at estimate time: it is the sum of each room's
per-room order_count (waste already applied per room). Opening a saved run
must return that snapshot verbatim — never re-apply waste to the summed
raw_count, and never drop waste by summing raw counts alone.
"""

from __future__ import annotations

from copy import deepcopy


def reprocess_total(result: dict) -> dict:
    """Pin the saved total. No re-derivation on the open path.

    Legacy payloads without a stored total get one assembled purely by
    summing the pinned per-room rows (each row already carries its own
    wasted order_count); waste is never re-applied.
    """
    if not isinstance(result, dict) or result.get("kind") != "batch":
        return result
    out = deepcopy(result)
    rooms = out.get("rooms") or []
    saved_total = out.get("total")
    if isinstance(saved_total, dict) and "order_count" in saved_total:
        return out

    waste = float(out.get("waste_pct") or (saved_total or {}).get("waste_pct") or 0)
    out["total"] = {
        "area_m2": round(sum(float(r.get("area_m2") or 0) for r in rooms), 3),
        "raw_count": sum(int(r.get("raw_count") or 0) for r in rooms),
        "order_count": sum(int(r.get("order_count") or 0) for r in rooms),
        "waste_pct": waste,
    }
    return out
