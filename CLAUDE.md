# Instructions projet — Cahier d'entretien auto

Ce dépôt contient un cahier d'entretien automobile dans `cahier-entretien/`, organisé par marque puis par modèle (`cahier-entretien/<marque>/<modele>.md`).

## Ajout automatique d'un modèle

Quand l'utilisateur mentionne une marque et/ou un modèle de voiture (ex. « ajoute la Golf », « et la Toyota Yaris ? », « Dacia Sandero »), **sans qu'il ait besoin de le demander explicitement** :

1. **Rechercher** les informations à jour (WebSearch si disponible, sinon connaissances internes) :
   - générations et années de production (se concentrer sur les 15-20 dernières années) ;
   - motorisations essence / diesel / hybride / électrique avec codes moteur ;
   - type de distribution par moteur (chaîne, courroie sèche, courroie humide) et intervalle de remplacement ;
   - intervalles d'entretien constructeur ;
   - points faibles / rappels connus ;
   - prix approximatifs des opérations en France (fourchette indépendant → concession).
2. **Créer la fiche** `cahier-entretien/<marque>/<modele>.md` en suivant strictement la structure de `cahier-entretien/templates/modele-fiche.md` (mêmes sections, mêmes formats de tableaux, prix en €).
3. **Mettre à jour l'index** dans `cahier-entretien/README.md` (tableau « Index des modèles », trié par marque puis modèle).
4. **Committer et pousser** sur la branche de travail avec un message du type `Ajout fiche entretien <Marque> <Modèle>`.

## Conventions

- Langue : **français**.
- Prix : fourchettes en euros, pièces + main-d'œuvre incluses, marché français.
- Intervalles : préconisation constructeur, avec recommandation « prudente » quand le terrain le justifie (courroies humides, boîtes à problèmes, etc.).
- Noms de fichiers : minuscules, sans accents (ex. `megane.md`, `c3-aircross.md`).
- Ne jamais présenter les prix comme exacts : ce sont des ordres de grandeur.
