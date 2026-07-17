# 🚗 Cahier d'entretien auto

Méga cahier d'entretien **par modèle, par moteur et par année** : échéances d'entretien, main-d'œuvre à prévoir et prix approximatifs (France, 2025-2026).

> ⚠️ Les prix sont des **estimations** (fourchette garage indépendant → concession, pièces de qualité équivalente d'origine). Les intervalles indiqués sont les préconisations constructeur, ajustées quand l'expérience terrain impose plus de prudence (ex. courroie humide PureTech / EcoBoost).

## 📋 Index des modèles

### 🏙️ Citadines

| Marque | Modèle | Fiche |
|---|---|---|
| Citroën | C3 (II, III, IV) | [citroen/c3.md](citroen/c3.md) |
| Ford | Fiesta (Mk7, Mk8) | [ford/fiesta.md](ford/fiesta.md) |
| Hyundai | i20 (I, II, III) | [hyundai/i20.md](hyundai/i20.md) |
| Peugeot | 208 (I, II) | [peugeot/208.md](peugeot/208.md) |
| Renault | Clio (III, IV, V) | [renault/clio.md](renault/clio.md) |
| Toyota | Yaris (II, III, IV) | [toyota/yaris.md](toyota/yaris.md) |
| Volkswagen | Polo (V, VI) | [volkswagen/polo.md](volkswagen/polo.md) |

### 🚗 Compactes

| Marque | Modèle | Fiche |
|---|---|---|
| Ford | Focus (Mk3, Mk4) | [ford/focus.md](ford/focus.md) |
| Opel | Astra (J, K, L) | [opel/astra.md](opel/astra.md) |
| Peugeot | 308 (I, II, III) | [peugeot/308.md](peugeot/308.md) |
| Renault | Mégane (III, IV, E-Tech) | [renault/megane.md](renault/megane.md) |
| Toyota | Corolla / Auris | [toyota/corolla.md](toyota/corolla.md) |
| Volkswagen | Golf (VI, VII, VIII) | [volkswagen/golf.md](volkswagen/golf.md) |

### 🚙 SUV urbains & compacts

| Marque | Modèle | Fiche |
|---|---|---|
| Dacia | Duster (I, II, III) | [dacia/duster.md](dacia/duster.md) |
| Nissan | Qashqai (I, II, III) | [nissan/qashqai.md](nissan/qashqai.md) |
| Peugeot | 2008 (I, II) | [peugeot/2008.md](peugeot/2008.md) |
| Peugeot | 3008 (I, II, III) | [peugeot/3008.md](peugeot/3008.md) |
| Renault | Captur (I, II) | [renault/captur.md](renault/captur.md) |

## 🧾 Documents communs

- [Guide des tarifs main-d'œuvre & opérations courantes](guide-tarifs.md)
- [**Guide d'achat occasion (50 000 km et +, cible ≤ 10 000 € / ≤ 130 000 km)**](guide-achat-occasion.md) — méthode, checklist d'inspection, spécificités La Réunion, barème de négociation
- [Modèle de fiche pour ajouter une voiture](templates/modele-fiche.md)

## 🔍 Skill « chasse aux bonnes affaires »

Le skill **`/occasion-reunion`** (dans `.claude/skills/occasion-reunion/`) recherche des occasions à **La Réunion** sur Leboncoin / Facebook Marketplace (max 10 000 €, 50 000 – 130 000 km), croise chaque annonce avec les fiches de ce cahier (échéances dues, points faibles, budget de rattrapage), calcule le **prix réel** et classe les bonnes affaires. On peut aussi lui coller une annonce (texte ou capture) pour analyse directe.

## 🔎 Comment lire une fiche

Chaque fiche contient :

1. **Générations couvertes** — années de production et remarques.
2. **Motorisations** — code moteur, type de distribution (chaîne / courroie / courroie humide) et coût de remplacement.
3. **Plan d'entretien par année / kilométrage** — quoi faire, quand, et pour quel budget.
4. **Spécificités par moteur** — intervalles propres à chaque bloc.
5. **Points faibles connus** — pannes récurrentes à surveiller avant achat.
6. **Budget annuel moyen** — pour comparer les modèles entre eux.

## ➕ Ajouter un modèle

Donne simplement une marque + un modèle à Claude (ex. « ajoute la Volkswagen Golf ») : la fiche est recherchée, créée à partir du [modèle](templates/modele-fiche.md), et l'index ci-dessus est mis à jour automatiquement (voir [CLAUDE.md](../CLAUDE.md)).
