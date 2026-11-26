---
name: traiter-decisions
description: Reporter dans la documentation des réponses données en bloc aux questions ouvertes (format « Fiche / - Question ?: Réponse »), ou toute nouvelle décision de conception. À utiliser dès que l'utilisateur tranche une ou plusieurs questions, même formulées librement.
---

# Traiter des décisions

L'utilisateur répond aux questions ouvertes en bloc :

```
Fiche / - Question ?: Réponse
```

`Fiche` est une fiche (`rafale`, `ports`…), un document transverse (`SYSTEMES`) ou un identifiant de `OPEN-PROBLEMS.md` (`A-13`, `H-04`). Une réponse vide, « jsp » ou « je zappe » n'est **pas** une décision : la question reste ouverte. Si la réponse est une recommandation de ma part que l'utilisateur me laisse choisir, l'écrire « recommandation adoptée par défaut, révisable ».

## Pour chaque réponse

1. **Remplacer la question** par une entrée dans la section **Décisions** de la fiche, ou passer le problème au statut **Décidé** dans `documentation/OPEN-PROBLEMS.md`. Garder les constats et les mesures : une décision abandonnée reste écrite, marquée « (abandonnée) », suivie de la nouvelle.
2. **Ajuster le reste de la fiche** pour qu'il ne contredise plus la décision (Identité, Mobilité, Besoins logistiques…).
3. **Reporter la règle** dans le document transverse concerné si elle dépasse une seule unité ou un seul lieu : `SYSTEMES.md`, `ZOMBIES.md`, `CONSTRUCTIONS.md`, `RESOURCES.md`, `UNITS.md`, `LOCATIONS.md`. Une décision structurante va aussi dans `.claude/CLAUDE.md` (section *Décisions structurantes*), en une ligne, avec son identifiant.
4. **Chercher les conséquences** ailleurs : grep des mots-clés de la décision (termes, noms d'unités, identifiants) dans `documentation/`, `prototypes/README.md` et les README des prototypes concernés. Corriger ce qui contredit ; noter ce qui demande une nouvelle décision.

## Règles de rédaction

- Français, phrases courtes, gras sur l'élément décisif.
- **Pas de chiffres** pour les statistiques de jeu (niveaux qualitatifs). Les chiffres d'architecture et de mesure sont permis.
- Noms de ressources exactement ceux de `RESOURCES.md`.
- Ce qui est incertain sur l'arsenal réel ou une technologie : « à vérifier ».
- Liens : relatifs dans un même dépôt ; URL `https://github.com/labatailledefrance/<dépôt>/blob/main/<chemin>` d'un dépôt à l'autre. Les ancres suivent les titres (`### H-04 — Vote sur …` → `#h-04--vote-sur-…`).

## Pour finir

1. Lancer le skill `verifier-liens`.
2. Pour une série de plusieurs décisions, lancer l'agent `relecteur-coherence` avec la liste des décisions.
3. Dans la réponse à l'utilisateur : ce qui a changé (fichiers, en bref), les contradictions trouvées, puis les **nouvelles questions** au format en bloc :

```
Fiche / - Question ?:
```

Ne pas ouvrir de PR sans que l'utilisateur le demande ; jamais de push direct sur `main` (branche, `git commit -s -S`, PR, squash).
