# CLAUDE.md — Référentiel du projet XAUUSD London Breakout

> Ce fichier est la **source de vérité** du projet. Avant toute modification de
> code, de stratégie, de paramètres de risque, ou ajout d'automatisation,
> Claude doit :
> 1. Relire ce fichier en entier.
> 2. Vérifier que la demande est cohérente avec les règles et limites ci-dessous.
> 3. Si la demande entre en conflit avec une règle existante, proposer une
>    mise à jour explicite de ce fichier (avec justification) **avant**
>    de toucher au code.

---

## 0. Périmètre et limites strictes de Claude sur ce projet

**Claude PEUT :**
- Écrire, modifier, tester et documenter du code (Python, scripts, configs).
- Générer des signaux de trading théoriques (calculs, logs, notifications).
- Calculer des tailles de position théoriques (jamais les envoyer).
- Proposer des architectures, des intégrations API, des scripts d'installation.
- Backtester des stratégies sur données historiques.
- Faire tourner le moteur en **mode démo / paper trading**.

**Claude NE DOIT JAMAIS :**
- Envoyer un ordre réel sur le compte réel IronFX (`IronFx-Real1`) de manière autonome.
- Désactiver, contourner ou affaiblir une règle de risk management sans
  validation explicite de l'utilisateur et mise à jour de ce fichier.
- Stocker un identifiant, mot de passe, clé API ou token dans le dépôt Git
  (toujours via variables d'environnement / fichiers `*.example` non commités).
- Prendre une décision d'investissement à la place de l'utilisateur.
- Construire un pipeline "full auto" vers le compte réel sans étape de
  confirmation humaine explicite.

**Toute action sur le compte réel reste MANUELLE ou CONFIRMÉE explicitement
par l'utilisateur.** Le système ne fait que : observer, calculer, journaliser,
notifier.

---

## 1. Stratégie : XAUUSD "Tendance + Cassure Londres"

### 1.1 Cadre temporel
- Contexte / tendance : **H4 / D1**
- Entrées : **M15 / H1**
- Fenêtre de trading : ouverture de session de Londres et chevauchement
  Londres / New York (forte liquidité). Pas de nouvelle position en dehors
  de ces créneaux.

### 1.2 Indicateurs
- **MA50** et **MA200** (déterminent le biais de tendance).
- **RSI(14)**, seuils de lecture : 30 / 50 / 70.

### 1.3 Règles de biais directionnel
- `MA50 > MA200` → on ne cherche **que des ACHATS**.
- `MA50 < MA200` → on ne cherche **que des VENTES**.
- Si les deux MA sont quasi plates / entrelacées → **pas de trade** (range,
  absence de tendance exploitable).

### 1.4 Construction du setup
1. Tracer le **plus haut et le plus bas de la session asiatique**.
2. Identifier les niveaux de support/résistance récents (derniers swing
   highs/lows significatifs).
3. Attendre une **cassure nette** (clôture de bougie au-delà du niveau, pas
   juste une mèche) **dans le sens de la tendance** (MA50/MA200).
4. La cassure doit se produire pendant la fenêtre Londres / Londres-NY.

### 1.5 Filtre RSI (confirmation, pas signal seul)
- Achat : RSI > 50 au moment de la cassure haussière (idéalement pas déjà
  en zone de surachat extrême > 70 sans pullback).
- Vente : RSI < 50 au moment de la cassure baissière.

### 1.6 Pseudo-code de la logique de signal

```text
fonction evaluer_signal(bougies_h4, bougies_m15, heure_actuelle, news_events):

    si est_en_blackout_news(heure_actuelle, news_events):
        retourner AUCUN_SIGNAL  # fenêtre macro à risque

    si non est_dans_fenetre_londres(heure_actuelle):
        retourner AUCUN_SIGNAL

    ma50  = moyenne_mobile(bougies_h4, 50)
    ma200 = moyenne_mobile(bougies_h4, 200)

    si ma50 et ma200 trop proches (range):
        retourner AUCUN_SIGNAL

    biais = ACHAT si ma50 > ma200 sinon VENTE

    haut_asie, bas_asie = niveaux_session_asiatique(bougies_m15)
    rsi = rsi_14(bougies_m15)

    derniere_bougie = bougies_m15[-1]

    si biais == ACHAT
       et cloture(derniere_bougie) > haut_asie
       et rsi > 50:
        signal = construire_signal(ACHAT, derniere_bougie, bas_asie)

    sinon si biais == VENTE
       et cloture(derniere_bougie) < bas_asie
       et rsi < 50:
        signal = construire_signal(VENTE, derniere_bougie, haut_asie)

    sinon:
        retourner AUCUN_SIGNAL

    si non valide_ratio_risque_gain(signal, min_rr=2.0):
        retourner AUCUN_SIGNAL

    retourner signal  # signal théorique, AUCUN ordre envoyé
```

---

## 2. Règles de gestion du risque (non négociables)

| Règle                                   | Valeur                                   |
|------------------------------------------|-------------------------------------------|
| Risque max par trade                     | 0,5 % – 1 % du capital                    |
| Stop Loss                                 | Obligatoire, derrière le dernier creux/sommet |
| Ratio Risque/Gain minimum                 | 1:2 (risque 10 € → objectif ≥ 20 €)       |
| Limite de perte journalière               | 3 % du capital → arrêt des trades du jour |
| Trade pendant news à fort impact          | Interdit (± 30 min autour de l'event)     |
| Effet de levier                           | Risque calculé sur le capital, pas sur l'exposition notionnelle |

Toute modification de ces valeurs doit être :
1. demandée explicitement par l'utilisateur,
2. répercutée dans ce fichier (section 2) avec la date du changement (voir
   Changelog),
3. répercutée dans `src/risk/risk_manager.py` (constantes de configuration).

---

## 3. Workflows opérationnels

### 3.1 Checklist — Avant la session (avant ouverture Londres)
- [ ] Vérifier le calendrier économique du jour (news rouges/orange à venir).
- [ ] Noter les plages horaires de blackout news.
- [ ] Identifier MA50 / MA200 sur H4/D1 → biais du jour (achat / vente / neutre).
- [ ] Tracer haut/bas de la session asiatique.
- [ ] Identifier niveaux S/R récents pertinents.
- [ ] Vérifier que la perte journalière (si trade plus tôt) n'a pas atteint
      la limite de 3 %.

### 3.2 Checklist — Pendant la session
- [ ] Surveiller la formation d'une cassure nette (clôture, pas mèche).
- [ ] Vérifier cohérence avec le biais de tendance.
- [ ] Vérifier RSI (confirmation > 50 pour achat / < 50 pour vente).
- [ ] Vérifier qu'on n'est pas dans une fenêtre de blackout news.
- [ ] Calculer la taille de position théorique (0,5–1 % de risque).
- [ ] Vérifier le ratio risque/gain ≥ 1:2.
- [ ] Si tout est validé → **signal journalisé**, proposition envoyée à
      l'utilisateur pour **confirmation manuelle**. Aucun ordre automatique.

### 3.3 Checklist — Après la session / après un trade
- [ ] Journaliser le résultat du trade (entrée, sortie, R, raison de sortie).
- [ ] Mettre à jour le suivi de perte/gain journalier.
- [ ] Si limite de perte journalière atteinte → flag "STOP TRADING TODAY".
- [ ] Revue rapide : le setup respectait-il toutes les règles ? Sinon, noter
      l'écart pour amélioration du système (pas de modification impulsive
      des règles).

---

## 4. Surveillance des news macro

- Objectif : ne jamais ouvrir de **nouvelle** position dans une fenêtre de
  ± 30 minutes autour d'une news à fort impact (Fed, NFP, CPI, décisions de
  taux, discours de banquiers centraux majeurs).
- Source de données : calendrier économique (API externe — voir
  `docs/NEWS_MONITORING.md` pour les options évaluées).
- Comportement attendu :
  - Le module `src/news/news_filter.py` expose `is_blackout_window(...)`.
  - Le moteur de signal interroge ce module **avant** toute évaluation de
    setup ; en cas de blackout, aucun signal n'est généré, un log "skip:
    news blackout" est écrit.
  - Notification optionnelle (Telegram/log) pour informer l'utilisateur des
    créneaux à risque du jour.

---

## 5. Architecture du code (résumé — détails dans `docs/ARCHITECTURE.md`)

```
src/
  data/      -> récupération / lecture des données OHLC XAUUSD (pas d'ordres)
  strategy/  -> calcul MA/RSI, détection de cassure, génération de Signal
  risk/      -> taille de position théorique, contrôle drawdown journalier
  news/      -> calendrier macro, fenêtres de blackout
  signals/   -> journalisation des signaux (fichier / log), pas d'exécution
  main.py    -> orchestration en mode lecture/calcul/log uniquement
```

Aucun module de ce dépôt n'envoie d'ordre. L'intégration broker (MT4/MT5 /
API IronFX) fait partie de la **Phase 4** et nécessitera une validation
explicite avant tout développement (voir Roadmap).

---

## 6. Roadmap

- **Phase 1 — Conception (en cours)**
  - Stratégie formalisée, `CLAUDE.md`, squelette de code, structure du dépôt.
- **Phase 2 — Backtest**
  - Tester la stratégie sur données historiques XAUUSD, mesurer winrate,
    expectancy, max drawdown. Aucune connexion live.
- **Phase 3 — Démo / Paper trading**
  - Faire tourner le moteur de signaux en continu sur le compte démo IronFX
    ou en paper trading, avec notifications, sans aucun ordre envoyé
    automatiquement.
- **Phase 4 — Réel (sous contrôle strict)**
  - Uniquement après validation des résultats en Phase 2 et 3, et seulement
    avec confirmation manuelle systématique de chaque ordre. Pas de "full
    auto" sur le compte réel.

---

## 7. Changelog

| Date       | Modification                                                       |
|------------|----------------------------------------------------------------------|
| 2026-06-16 | Création initiale : stratégie, règles de risque, checklists, squelette de code (data/strategy/risk/news/signals), structure de dépôt. |

---

## 8. Notes d'environnement

- Hébergement prévu : LXC/VM "trading-engine" sur Proxmox (Python).
- Aucune clé API, identifiant ou mot de passe ne doit apparaître en clair
  dans le dépôt. Utiliser `config/.env.example` comme modèle et un fichier
  `.env` local (ignoré par Git) pour les vraies valeurs.
- Compte réel IronFX (`IronFx-Real1`, ~100 €) : capital faible, effet de
  levier élevé → discipline de risque non négociable (section 2).
