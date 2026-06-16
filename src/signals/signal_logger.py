"""Journalisation des signaux theoriques. Aucune execution d'ordre ici."""

from __future__ import annotations

import csv
from pathlib import Path

from src.strategy.london_breakout import Signal

LOG_COLUMNS = [
    "timestamp", "direction", "entry_price", "stop_loss", "take_profit",
    "risk_reward", "reason",
]


def log_signal_to_csv(signal: Signal, log_path: str | Path) -> None:
    log_path = Path(log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    is_new_file = not log_path.exists()
    with log_path.open("a", newline="") as f:
        writer = csv.writer(f)
        if is_new_file:
            writer.writerow(LOG_COLUMNS)
        writer.writerow([
            signal.timestamp.isoformat(),
            signal.direction.value,
            signal.entry_price,
            signal.stop_loss,
            signal.take_profit,
            round(signal.risk_reward, 2),
            signal.reason,
        ])
