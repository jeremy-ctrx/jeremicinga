---
name: occasion-reunion
description: Recherche de bonnes affaires en véhicules d'occasion à La Réunion (974) sur Leboncoin et Facebook Marketplace — budget max 10 000 €, kilométrage 50 000 à 130 000 km — en croisant chaque annonce avec le cahier d'entretien du dépôt. Utiliser quand l'utilisateur demande de chercher/trouver une occasion, une bonne affaire, ou d'analyser une annonce de voiture.
---

# Chasse aux bonnes affaires — véhicules d'occasion à La Réunion

## Critères par défaut (sauf indication contraire de l'utilisateur)

- **Lieu** : La Réunion (974) — toute l'île
- **Prix** : ≤ **~13 000 €** (le sweet spot « bonne affaire » reste ≤ 10 000 € ; signaler quand une annonce dépasse 10 000 €)
- **Kilométrage** : 50 000 – 130 000 km
- **Modèles** : celui donné en argument, sinon les modèles du cahier (`cahier-entretien/README.md`), en privilégiant les mieux notés en budget/fiabilité : Toyota Yaris hybride, Corolla/Auris hybride, Renault Clio IV/V TCe, Captur, Dacia Duster, Peugeot 208/2008 (PureTech **uniquement** si courroie faite), VW Polo 1.0 TSI.

## Étape 1 — Recherche des annonces

Essayer dans cet ordre (les sites bloquent souvent les robots — ne pas s'acharner, passer au fallback) :

1. **WebSearch** avec des requêtes ciblées :
   - `site:leboncoin.fr <modèle> réunion 974`
   - `<modèle> occasion réunion 974 leboncoin`
   - `<modèle> occasion "la réunion" marketplace`
2. **WebFetch** sur les URL de recherche Leboncoin (adapter le modèle) :
   - `https://www.leboncoin.fr/recherche?category=2&text=<modèle>&locations=r_26&price=0-10000&mileage=50000-130000`
   - (`r_26` = région Réunion ; si le code ne fonctionne pas, essayer `locations=La%20Réunion`)
3. **Fallback si accès bloqué** (cas fréquent) : générer pour l'utilisateur des **liens de recherche prêts à cliquer** (Leboncoin avec filtres pré-remplis + Facebook Marketplace `https://www.facebook.com/marketplace/108424535853549/search?query=<modèle>` — Saint-Denis, rayon max) et lui demander de coller le texte ou les captures des annonces intéressantes pour analyse.

L'utilisateur peut aussi coller directement une annonce (texte ou capture d'écran) : passer alors directement à l'étape 2.

## Étape 2 — Analyse de chaque annonce via le cahier d'entretien

Pour chaque annonce, identifier **modèle + génération + moteur + année + km**, puis ouvrir la fiche correspondante dans `cahier-entretien/<marque>/<modele>.md` et vérifier :

1. **Élimination immédiate** (voir aussi `cahier-entretien/guide-achat-occasion.md` §6) :
   - PureTech / EcoBoost sans mention de courroie humide remplacée (> 6 ans ou > 100 000 km) → seulement si le prix absorbe les 900-1 400 € de courroie
   - ETG5, DSG7 sec, PowerShift, CVT sans historique de vidange
   - 1.2 TCe Renault / 1.2 DIG-T Nissan sans factures d'huile
   - Diesel avec profil 100 % urbain
2. **Échéances dues à ce kilométrage/âge** (section « Plan d'entretien » de la fiche) : distribution, bougies, liquides, vidange BVA…
3. **Points faibles de la version** (section « Points faibles connus ») : symptômes à vérifier à l'essai.
4. **Calcul du prix réel** :
   `prix réel = prix affiché + rattrapage entretien estimé (section « Achat d'occasion » de la fiche) + échéances < 12 mois`
5. **Score bonne affaire** : ★★★ (prix réel nettement sous le marché local, historique complet) / ★★ (correct, à négocier) / ★ (cher ou risqué).

## Étape 3 — Restitution

Présenter un tableau trié par score :

| Annonce | Année / km | Prix affiché | Rattrapage estimé | **Prix réel** | Score | Alerte principale |
|---|---|---|---|---|---|---|

Puis pour les 2-3 meilleures :
- les **questions à poser au vendeur** (factures précises à exiger, tirées de la fiche) ;
- les **points de contrôle à l'essai** (points faibles de la version) ;
- une **fourchette de négociation** (barème du guide achat occasion §5) ;
- le rappel des spécificités Réunion : corrosion sous caisse, clim, prix locaux +10-20 % vs métropole.

## Règles

- Ne jamais présenter un prix ou une cote comme exact : toujours des fourchettes.
- Ne pas contacter de vendeur ni créer de compte : la prise de contact reste à l'utilisateur.
- Si un modèle demandé n'a pas de fiche dans `cahier-entretien/`, la créer d'abord (voir `CLAUDE.md` racine), puis analyser.
- Toujours mentionner Histovec (gratuit) avant tout engagement.
