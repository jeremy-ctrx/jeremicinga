# Architecture du moteur de signaux

Référence détaillée ; les règles métier restent définies dans `CLAUDE.md`.

```
src/
  data/
    market_data.py     # CsvMarketDataProvider : lecture OHLC + resample HTF
  strategy/
    indicators.py       # moving_average(), rsi()
    london_breakout.py   # trend_bias(), asian_session_range(), evaluate_signal()
  risk/
    risk_manager.py      # compute_position_size(), DailyLossTracker, garde-fous
  news/
    news_filter.py        # NewsEvent, is_blackout_window()
    notifier.py            # send_telegram_alert() (no-op si non configuré)
  signals/
    signal_logger.py        # log_signal_to_csv()
  main.py                    # orchestration CLI (lecture -> calcul -> log)
```

## Flux de données

```
CSV OHLC (M15) --> CsvMarketDataProvider.load()
                --> resample() vers H4/D1 (contexte de tendance)
                        |
                        v
            trend_bias(H4) -> BUY / SELL / NONE
                        |
            asian_session_range(M15) -> haut/bas asiatique
                        |
            is_blackout_window(news) -> bloque si vrai
                        |
            evaluate_signal() -> Signal | None
                        |
            enforce_min_risk_reward() + compute_position_size()
                        |
            log_signal_to_csv() -> data/signals_log.csv
                        |
            affichage console : "CONFIRMATION MANUELLE REQUISE"
```

## Principe de conception

- Chaque module est testable isolément (pas de dépendance broker dans
  `strategy/`, `risk/`, `news/`).
- Aucun module ne possède de méthode `send_order` / `place_trade`. L'ajout
  d'une telle fonctionnalité (Phase 3/4) doit être proposé explicitement et
  rester derrière une confirmation manuelle (voir `CLAUDE.md` section 0).
- `src/data/market_data.py` est le seul point qui sera remplacé par une
  intégration broker live (MT5 bridge / API REST IronFX) en Phase 3/4 ; le
  reste du pipeline (stratégie, risk, news, logging) restera inchangé.

## Intégration broker (Phase 3/4 — non implémentée)

Options à évaluer le moment venu, sans implémentation prématurée :
- Pont fichiers CSV avec un Expert Advisor MT4/MT5 (l'EA exporte les
  données, le moteur Python lit/écrit dans un dossier partagé).
- Bibliothèque Python pour MT5 (`MetaTrader5` package, Windows uniquement
  en général) si le terminal tourne sur une VM Windows.
- API REST si IronFX en propose une (à vérifier auprès du broker — aucune
  URL n'a été confirmée, ne pas en deviner).

Dans tous les cas : compte démo par défaut, ordre réel = confirmation
manuelle systématique.
