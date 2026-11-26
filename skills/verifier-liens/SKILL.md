---
name: verifier-liens
description: Vérifier tous les liens Markdown de l'espace de travail (relatifs, ancres, URL entre dépôts labatailledefrance). À lancer après toute modification de structure, tout déplacement ou renommage de fichier ou de titre, et à la fin du skill traiter-decisions.
---

# Vérifier les liens

Depuis la racine de l'espace de travail :

```
python3 .claude/skills/verifier-liens/verifier-liens.py
```

Le script parcourt `documentation/`, `prototypes/` (sans les `target/`), `.claude/`, `.github/`, les dépôts `beta1-*` et le `README.md` de la racine. Il vérifie :

- que chaque **fichier** visé existe ;
- que chaque **ancre** (`#…`) correspond à un titre du fichier visé, selon la règle de GitHub ;
- que les URL `https://github.com/labatailledefrance/<dépôt>/blob/main/…` pointent vers un fichier du dépôt cloné en local (`agent` = `.claude/`) ;
- qu'aucun lien relatif ne **sort de son dépôt** (cassé sur GitHub : il faut une URL complète) ;
- qu'aucun lien ne vise `data/` (non versionné) ou `CLAUDE.md` (chemin en texte à la place).

Code de sortie 1 s'il reste un problème.

## Corriger

- **Titre renommé** : mettre à jour toutes les ancres qui le visaient (grep de l'ancienne ancre).
- **Lien entre dépôts** : `https://github.com/labatailledefrance/<dépôt>/blob/main/<chemin>` (`tree` pour un dossier, rien après le nom du dépôt pour sa racine).
- **Lien vers `data/` ou `CLAUDE.md`** : garder le texte, en code (`` `data/generated/p01-tiles/` ``), sans lien.
- Une ancre vers une section qui **n'existe pas encore** (README de prototype incomplet) : la signaler à l'utilisateur plutôt que d'inventer la section.
