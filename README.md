# XAUUSD London Breakout — Signal Engine

Système d'analyse et de préparation de trades court terme sur XAUUSD
(breakout de la session de Londres, tendance MA50/MA200 + RSI), avec
surveillance des news macro et gestion de risque stricte.

**Ce dépôt ne contient aucun code d'exécution automatique d'ordres réels.**
Le moteur lit des données de marché, calcule des signaux théoriques, calcule
une taille de position théorique, et journalise tout. Toute exécution reste
manuelle ou confirmée explicitement par l'utilisateur (voir `CLAUDE.md`).

- Stratégie, règles de risque, checklists et roadmap : voir [`CLAUDE.md`](./CLAUDE.md)
- Architecture détaillée : voir [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md)
- Surveillance des news macro : voir [`docs/NEWS_MONITORING.md`](./docs/NEWS_MONITORING.md)

## Installation rapide

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp config/.env.example .env        # puis remplir les valeurs localement
cp config/settings.example.yaml config/settings.yaml
python -m src.main --mode backtest --input data/historical/xauusd_m15.csv
```

Aucun identifiant ne doit être commité. `.env` et `config/settings.yaml`
sont ignorés par Git (voir `.gitignore`).
