"""Orchestration du moteur de signaux XAUUSD London Breakout.

IMPORTANT (voir CLAUDE.md section 0) : ce script ne se connecte a aucun
broker et n'envoie aucun ordre. Il lit des donnees OHLC (CSV), calcule un
signal theorique, verifie les regles de risque, journalise le resultat et
affiche un message demandant une confirmation manuelle de l'utilisateur.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

from src.data.market_data import CsvMarketDataProvider
from src.news.news_filter import is_blackout_window, load_events_from_json
from src.risk.risk_manager import (
    RiskLimitExceeded,
    compute_position_size,
    enforce_min_risk_reward,
)
from src.signals.signal_logger import log_signal_to_csv
from src.strategy.london_breakout import evaluate_signal

DEFAULT_SETTINGS_PATH = "config/settings.yaml"
DEFAULT_NEWS_PATH = "data/news_events.json"
DEFAULT_LOG_PATH = "data/signals_log.csv"


def load_settings(path: str) -> dict:
    settings_path = Path(path)
    if not settings_path.exists():
        raise FileNotFoundError(
            f"{settings_path} introuvable. Copier config/settings.example.yaml -> config/settings.yaml"
        )
    return yaml.safe_load(settings_path.read_text())


def run(input_csv: str, settings_path: str = DEFAULT_SETTINGS_PATH,
        news_path: str = DEFAULT_NEWS_PATH, log_path: str = DEFAULT_LOG_PATH) -> int:
    settings = load_settings(settings_path)

    provider = CsvMarketDataProvider(input_csv)
    df_ltf = provider.load()  # M15
    df_htf = provider.resample(df_ltf, settings["strategy"]["trend_timeframe"])

    news_events = load_events_from_json(news_path)
    last_ts = df_ltf.iloc[-1]["timestamp"]

    if is_blackout_window(
        last_ts, news_events,
        minutes_before=settings["news"]["blackout_minutes_before"],
        minutes_after=settings["news"]["blackout_minutes_after"],
        high_impact_only=settings["news"]["high_impact_only"],
    ):
        print("Aucun signal : fenetre de blackout news active.")
        return 0

    signal = evaluate_signal(
        df_htf, df_ltf,
        rsi_period=settings["strategy"]["rsi_period"],
        min_risk_reward=settings["risk"]["min_risk_reward"],
    )

    if signal is None:
        print("Aucun signal valide selon la strategie (voir CLAUDE.md section 1).")
        return 0

    try:
        enforce_min_risk_reward(signal.risk_reward, settings["risk"]["min_risk_reward"])
        position = compute_position_size(
            equity=settings["account"]["capital_eur"],
            risk_per_trade_pct=settings["risk"]["risk_per_trade_pct"],
            entry_price=signal.entry_price,
            stop_loss_price=signal.stop_loss,
            take_profit_price=signal.take_profit,
        )
    except RiskLimitExceeded as exc:
        print(f"Signal rejete par le risk manager : {exc}")
        return 0

    log_signal_to_csv(signal, log_path)

    print("=== SIGNAL THEORIQUE (AUCUN ORDRE ENVOYE) ===")
    print(f"Direction       : {signal.direction.value}")
    print(f"Entree          : {signal.entry_price}")
    print(f"Stop Loss       : {signal.stop_loss}")
    print(f"Take Profit     : {signal.take_profit}")
    print(f"Risque/Gain     : {signal.risk_reward:.2f}")
    print(f"Taille position : {position.position_size_units:.4f} unites "
          f"(risque {position.risk_amount:.2f} EUR)")
    print(f"Raison          : {signal.reason}")
    print(">>> CONFIRMATION MANUELLE REQUISE avant tout passage d'ordre. <<<")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["backtest", "signal"], default="signal",
                         help="backtest: traite tout l'historique ; signal: derniere bougie uniquement")
    parser.add_argument("--input", required=True, help="Chemin du CSV OHLC M15")
    parser.add_argument("--settings", default=DEFAULT_SETTINGS_PATH)
    parser.add_argument("--news", default=DEFAULT_NEWS_PATH)
    parser.add_argument("--log", default=DEFAULT_LOG_PATH)
    args = parser.parse_args()

    sys.exit(run(args.input, args.settings, args.news, args.log))


if __name__ == "__main__":
    main()
