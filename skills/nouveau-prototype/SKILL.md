---
name: nouveau-prototype
description: Démarrer un prototype technique (P-xx) dans prototypes/ avec le squelette commun (README, Cargo.toml, run.sh), ou en terminer un (mesures, conclusion, décisions reportées). À utiliser dès que l'utilisateur lance ou reprend un prototype de prototypes/README.md.
---

# Nouveau prototype

Un prototype est **jetable** : il valide une hypothèse de `documentation/OPEN-PROBLEMS.md`, puis son code est abandonné. Ce qui reste, ce sont ses **mesures** et ses **décisions**.

## Démarrer

1. Lire la fiche du prototype dans `prototypes/README.md` (problème, objectif, méthode, critères) et les problèmes visés dans `OPEN-PROBLEMS.md`, avec leurs constats.
2. Créer `prototypes/pXX-nom-court/` (ASCII, minuscules, tirets ; même numéro que la fiche) à partir de `modele/` :
   - `README.md` : remplacer les `<…>` ; garder **toutes** les sections, même vides au départ.
   - `Cargo.toml` : `name` = nom du dossier. Dépendances **à versions exactes** (`=x.y.z`), vérifiées sur crates.io et **vieilles d'au moins deux semaines** ; noter la date de vérification en commentaire. Reprendre la configuration Bevy d'un prototype antérieur plutôt que d'en inventer une.
   - `run.sh` : la campagne de mesures complète, reproductible, avec un mode `ESSAI=1` rapide.
3. Données : lues dans `../../data/sources/` et `../../data/generated/` (jamais versionnées, jamais liées depuis les README : chemin en texte).
4. Le `.gitignore` du dépôt exclut déjà `target/` et `target-*/`.

## Mesurer

- Sur la **machine de mesure** (Ryzen 7 5700X, RTX 3060), sans rien de lourd en parallèle ; indiquer dans *Machine* ce qui tournait.
- Résultats bruts dans `resultats/` (CSV, texte), images dans `images/` ; les sections *Mesures* y renvoient.
- Toujours une **somme de contrôle** ou une empreinte quand deux méthodes doivent donner le même résultat.
- Rapporter p50 et **p99**, pas seulement la moyenne.
- Ne pas anticiper les contraintes du serveur de production : on mesure ce que le prototype doit établir, rien de plus.

## Terminer

1. Remplir *Analyse*, *Conclusion* et *Recommandations* ; proposer les décisions à l'utilisateur au format en bloc (`P-XX / - Question ?: Réponse`).
2. Après sa réponse, remplir *Décisions*, puis les reporter avec le skill `traiter-decisions` : un **Constat** et une **Décision** `(P-XX, [résultats](…))` dans chaque problème concerné d'`OPEN-PROBLEMS.md`, la ligne *Résultats* de la fiche dans `prototypes/README.md`, et `.claude/CLAUDE.md` si la décision est structurante.
3. Liens vers la documentation : URL `https://github.com/labatailledefrance/documentation/blob/main/…`. Lancer `verifier-liens`.
