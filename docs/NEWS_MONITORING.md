# Surveillance des news macro

Objectif : ne jamais générer de signal pendant une fenêtre de ± 30 minutes
(configurable) autour d'une news macro à fort impact (Fed, NFP, CPI,
décisions de taux, discours majeurs de banques centrales).

## Implémentation actuelle (Phase 1)

- `src/news/news_filter.py` lit une liste d'événements depuis
  `data/news_events.json` (vide par défaut, à committer vide — pas de
  données sensibles).
- Format attendu d'un événement :

```json
{
  "timestamp": "2026-06-18T12:30:00+00:00",
  "currency": "USD",
  "impact": "high",
  "title": "Non-Farm Payrolls"
}
```

- `is_blackout_window(now, events, minutes_before=30, minutes_after=30,
  high_impact_only=True)` renvoie `True` si `now` tombe dans une fenêtre de
  blackout. `src/main.py` appelle cette fonction avant tout calcul de
  signal.

## Options pour alimenter `data/news_events.json` (Phase 2+)

À évaluer avec l'utilisateur avant intégration (aucune clé API n'est
supposée ou codée en dur) :

1. **API de calendrier économique** (ex : fournisseurs spécialisés calendrier
   macro forex). Nécessite une clé API stockée dans `.env`
   (`ECONOMIC_CALENDAR_API_KEY`, voir `config/.env.example`). Un script
   séparé (`scripts/sync_news.py`, à créer en Phase 2) interrogerait l'API
   et écrirait `data/news_events.json`.
2. **Scraping d'un calendrier public** : plus fragile (dépend de la
   structure HTML), à éviter comme solution principale.
3. **Saisie manuelle hebdomadaire** : solution de repli simple, suffisante
   pour un seul actif (XAUUSD/USD) avec peu d'événements à fort impact par
   semaine.

Recommandation : commencer par l'option 3 (manuelle) en Phase 1/2 pour
valider le pipeline, puis automatiser avec l'option 1 en Phase 3 une fois
une API choisie et validée avec l'utilisateur.

## Notifications

- `src/news/notifier.py` expose `send_telegram_alert(message)` : no-op si
  `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` ne sont pas définis dans `.env`.
- Usage prévu : alerter l'utilisateur des créneaux de blackout du jour
  pendant la checklist "Avant la session" (voir `CLAUDE.md` section 3.1),
  et notifier chaque signal théorique journalisé.
