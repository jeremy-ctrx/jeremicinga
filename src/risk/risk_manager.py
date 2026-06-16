"""Calcul de taille de position theorique et controle des limites de risque.

Aucune fonction ici n'envoie d'ordre. Voir CLAUDE.md section 2 pour les
valeurs de reference (a synchroniser avec config/settings.yaml).
"""

from __future__ import annotations

from dataclasses import dataclass


class RiskLimitExceeded(Exception):
    """Leve quand une regle de risque (CLAUDE.md section 2) est violee."""


@dataclass(frozen=True)
class PositionSizeResult:
    risk_amount: float
    position_size_units: float
    risk_reward: float


def compute_position_size(equity: float, risk_per_trade_pct: float,
                           entry_price: float, stop_loss_price: float,
                           take_profit_price: float) -> PositionSizeResult:
    """Calcule une taille de position theorique en unites de l'actif (ex: onces XAUUSD).

    Ne prend pas en compte la taille de lot/contrat specifique au broker :
    a adapter avec la valeur de pip/point d'IronFX avant usage en demo.
    """
    if risk_per_trade_pct <= 0 or risk_per_trade_pct > 1.0:
        raise RiskLimitExceeded(
            f"risk_per_trade_pct={risk_per_trade_pct} hors limites (0-1%, voir CLAUDE.md section 2)"
        )

    stop_distance = abs(entry_price - stop_loss_price)
    if stop_distance <= 0:
        raise ValueError("entry_price et stop_loss_price ne peuvent pas etre egaux")

    risk_amount = equity * (risk_per_trade_pct / 100)
    position_size_units = risk_amount / stop_distance

    reward_distance = abs(take_profit_price - entry_price)
    risk_reward = reward_distance / stop_distance

    return PositionSizeResult(risk_amount, position_size_units, risk_reward)


def enforce_min_risk_reward(risk_reward: float, min_risk_reward: float = 2.0) -> None:
    if risk_reward < min_risk_reward:
        raise RiskLimitExceeded(
            f"Ratio risque/gain {risk_reward:.2f} < minimum requis {min_risk_reward} (CLAUDE.md section 2)"
        )


class DailyLossTracker:
    """Suit la perte cumulee de la journee et bloque les nouveaux trades si
    la limite (par defaut 3% du capital, CLAUDE.md section 2) est atteinte.
    """

    def __init__(self, starting_equity: float, max_daily_loss_pct: float = 3.0):
        self.starting_equity = starting_equity
        self.max_daily_loss_pct = max_daily_loss_pct
        self.realized_pnl = 0.0

    def record_trade_result(self, pnl: float) -> None:
        self.realized_pnl += pnl

    @property
    def daily_loss_pct(self) -> float:
        if self.starting_equity == 0:
            return 0.0
        return max(0.0, -self.realized_pnl) / self.starting_equity * 100

    def trading_allowed(self) -> bool:
        return self.daily_loss_pct < self.max_daily_loss_pct
