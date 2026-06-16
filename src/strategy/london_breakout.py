"""Strategie XAUUSD 'Tendance + Cassure Londres'.

Voir CLAUDE.md section 1 pour les regles completes et le pseudo-code de
reference. Ce module ne fait que calculer un Signal theorique : aucun ordre
n'est envoye ici.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import time
from enum import Enum

import pandas as pd

from src.strategy.indicators import moving_average, rsi


class Direction(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class Bias(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    NONE = "NONE"


@dataclass(frozen=True)
class Signal:
    direction: Direction
    entry_price: float
    stop_loss: float
    take_profit: float
    reason: str
    timestamp: pd.Timestamp

    @property
    def risk_reward(self) -> float:
        risk = abs(self.entry_price - self.stop_loss)
        reward = abs(self.take_profit - self.entry_price)
        return reward / risk if risk else 0.0


def trend_bias(df_htf: pd.DataFrame, ma_fast: int = 50, ma_slow: int = 200,
                flat_threshold_pct: float = 0.05) -> Bias:
    """Determine le biais de tendance sur le timeframe haut (H4/D1).

    flat_threshold_pct : ecart relatif minimal entre MA50/MA200 pour
    considerer qu'il y a une tendance exploitable (sinon -> range -> NONE).
    """
    closes = df_htf["close"]
    fast = moving_average(closes, ma_fast).iloc[-1]
    slow = moving_average(closes, ma_slow).iloc[-1]

    if pd.isna(fast) or pd.isna(slow) or slow == 0:
        return Bias.NONE

    spread_pct = abs(fast - slow) / slow * 100
    if spread_pct < flat_threshold_pct:
        return Bias.NONE

    return Bias.BUY if fast > slow else Bias.SELL


def asian_session_range(df_ltf: pd.DataFrame, session_date: pd.Timestamp,
                         start_hour_utc: int = 0, end_hour_utc: int = 7) -> tuple[float, float]:
    """Retourne (haut, bas) de la session asiatique pour la date donnee (UTC)."""
    day_start = session_date.normalize() + pd.Timedelta(hours=start_hour_utc)
    day_end = session_date.normalize() + pd.Timedelta(hours=end_hour_utc)

    mask = (df_ltf["timestamp"] >= day_start) & (df_ltf["timestamp"] < day_end)
    window = df_ltf.loc[mask]
    if window.empty:
        raise ValueError("Pas de donnees pour la session asiatique demandee")

    return float(window["high"].max()), float(window["low"].min())


def is_london_window(ts: pd.Timestamp, start_utc: time = time(7, 0),
                      end_utc: time = time(16, 0)) -> bool:
    """Fenetre ouverture Londres -> chevauchement Londres/New York (UTC)."""
    t = ts.time()
    return start_utc <= t <= end_utc


def evaluate_signal(df_htf: pd.DataFrame, df_ltf: pd.DataFrame,
                     rsi_period: int = 14, min_risk_reward: float = 2.0) -> Signal | None:
    """Evalue un signal theorique sur la derniere bougie disponible en df_ltf.

    Ne renvoie un Signal que si toutes les conditions de CLAUDE.md (section
    1) sont reunies. Ne genere et n'envoie aucun ordre.
    """
    last_candle = df_ltf.iloc[-1]
    ts = last_candle["timestamp"]

    if not is_london_window(ts):
        return None

    bias = trend_bias(df_htf)
    if bias == Bias.NONE:
        return None

    high_asia, low_asia = asian_session_range(df_ltf, ts)

    rsi_series = rsi(df_ltf["close"], rsi_period)
    last_rsi = rsi_series.iloc[-1]
    if pd.isna(last_rsi):
        return None

    close = float(last_candle["close"])

    signal: Signal | None = None
    if bias == Bias.BUY and close > high_asia and last_rsi > 50:
        entry = close
        stop = low_asia
        take_profit = entry + min_risk_reward * (entry - stop)
        signal = Signal(Direction.BUY, entry, stop, take_profit,
                         reason="Cassure haussiere du haut de session asiatique, tendance haussiere, RSI>50",
                         timestamp=ts)

    elif bias == Bias.SELL and close < low_asia and last_rsi < 50:
        entry = close
        stop = high_asia
        take_profit = entry - min_risk_reward * (stop - entry)
        signal = Signal(Direction.SELL, entry, stop, take_profit,
                         reason="Cassure baissiere du bas de session asiatique, tendance baissiere, RSI<50",
                         timestamp=ts)

    if signal is None:
        return None

    if signal.risk_reward < min_risk_reward:
        return None

    return signal
