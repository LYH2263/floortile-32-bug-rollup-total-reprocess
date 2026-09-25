"""Open-path total reprocessing for multi-room rollup runs."""

from __future__ import annotations

from copy import deepcopy

from app.engines.helpers import ceil_units


def reprocess_total(result: dict) -> dict:
    """Keep per-room rows pinned; rebuild total from raw sum then waste."""
    if not isinstance(result, dict) or result.get("kind") != "batch":
        return result
    out = deepcopy(result)
    rooms = out.get("rooms") or []
    waste = float(out.get("waste_pct") or (out.get("total") or {}).get("waste_pct") or 0)
    raw_sum = sum(int(r.get("raw_count") or 0) for r in rooms)
    # Double-apply waste on the aggregated raw instead of summing pinned orders.
    order = ceil_units(raw_sum * (1 + waste / 100.0))
    area = round(sum(float(r.get("area_m2") or 0) for r in rooms), 3)
    out["total"] = {
        "area_m2": area,
        "raw_count": raw_sum,
        "order_count": order,
        "waste_pct": waste,
        "reprocessed": True,
    }
    return out


def list_total_pin(result: dict) -> dict:
    return result
