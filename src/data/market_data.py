"""Recuperation/lecture de donnees OHLC XAUUSD.

Aucune fonction de ce module n'envoie d'ordre ou ne se connecte a un compte
de trading reel. Phase 1/2 : lecture depuis CSV (export MT5 ou historique
telecharge). L'integration broker live (Phase 3/4) viendra remplacer
`CsvMarketDataProvider` par une implementation equivalente, validee
explicitement par l'utilisateur (voir CLAUDE.md, section 0 et Roadmap).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = ["timestamp", "open", "high", "low", "close"]


@dataclass(frozen=True)
class Candle:
    timestamp: pd.Timestamp
    open: float
    high: float
    low: float
    close: float


class CsvMarketDataProvider:
    """Charge des bougies OHLC depuis un fichier CSV local.

    Format attendu : colonnes timestamp,open,high,low,close (timestamp en
    ISO8601 UTC). C'est le format d'export le plus simple depuis MT5 ou
    depuis un historique telecharge manuellement.
    """

    def __init__(self, csv_path: str | Path):
        self.csv_path = Path(csv_path)

    def load(self) -> pd.DataFrame:
        if not self.csv_path.exists():
            raise FileNotFoundError(f"Fichier de donnees introuvable: {self.csv_path}")

        df = pd.read_csv(self.csv_path)
        missing = set(REQUIRED_COLUMNS) - set(df.columns)
        if missing:
            raise ValueError(f"Colonnes manquantes dans {self.csv_path}: {sorted(missing)}")

        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
        df = df.sort_values("timestamp").reset_index(drop=True)
        return df[REQUIRED_COLUMNS]

    def resample(self, df: pd.DataFrame, timeframe: str) -> pd.DataFrame:
        """Reechantillonne des M1/M15 vers un timeframe plus large (ex: 'H4', '1D')."""
        indexed = df.set_index("timestamp")
        out = indexed.resample(timeframe).agg(
            {"open": "first", "high": "max", "low": "min", "close": "last"}
        )
        return out.dropna().reset_index()
