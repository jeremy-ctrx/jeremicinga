"""Filtre de blackout autour des news macro a fort impact.

Phase 1 : chargement depuis un fichier JSON local (rempli manuellement ou
par un script de synchronisation a part, voir docs/NEWS_MONITORING.md).
Phase 2+ : remplacement par un appel a une API de calendrier economique,
sans changer la signature de `is_blackout_window`.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class NewsEvent:
    timestamp: pd.Timestamp
    currency: str
    impact: str  # "high" | "medium" | "low"
    title: str


def load_events_from_json(path: str | Path) -> list[NewsEvent]:
    path = Path(path)
    if not path.exists():
        return []

    raw = json.loads(path.read_text())
    events = []
    for item in raw:
        events.append(
            NewsEvent(
                timestamp=pd.Timestamp(item["timestamp"], tz="UTC"),
                currency=item["currency"],
                impact=item["impact"],
                title=item["title"],
            )
        )
    return events


def is_blackout_window(now: pd.Timestamp, events: list[NewsEvent],
                        minutes_before: int = 30, minutes_after: int = 30,
                        high_impact_only: bool = True) -> bool:
    """True si `now` tombe dans une fenetre de blackout autour d'une news."""
    window_before = pd.Timedelta(minutes=minutes_before)
    window_after = pd.Timedelta(minutes=minutes_after)

    for event in events:
        if high_impact_only and event.impact != "high":
            continue
        if event.timestamp - window_before <= now <= event.timestamp + window_after:
            return True
    return False
