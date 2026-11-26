# Agent

Configuration de Claude Code pour La Bataille de France, jeu de reconquête de la France face aux zombies : instructions du projet, skills et agents.

## Installation

Ce dépôt se clone dans le dossier `.claude/` à la racine de l'espace de travail, à côté des autres dépôts. La racine elle-même n'est pas un dépôt git.

```
mkdir labatailledefrance && cd labatailledefrance
git clone https://github.com/labatailledefrance/agent .claude
git clone https://github.com/labatailledefrance/documentation
git clone https://github.com/labatailledefrance/prototypes
git clone https://github.com/labatailledefrance/.github
for d in common server client datachain assets helm; do git clone https://github.com/labatailledefrance/beta1-$d; done
```

Les commits sont signés (configuration globale `commit.gpgsign = true`, clé sur YubiKey) avec `Signed-off-by` (`git commit -s -S`) et passent par une PR fusionnée en squash : `main` est protégée.

Claude Code lit `.claude/CLAUDE.md` comme instructions du projet, et charge les skills de `.claude/skills/` et les agents de `.claude/agents/`.

## Contenu

- [CLAUDE.md](CLAUDE.md) : langue, organisation, conventions, décisions structurantes, profil de l'utilisateur.
- Skills :
  - [traiter-decisions](skills/traiter-decisions/SKILL.md) : reporter des réponses données en bloc aux questions ouvertes ;
  - [verifier-liens](skills/verifier-liens/SKILL.md) : vérifier liens, ancres et URL entre dépôts ;
  - [nouveau-prototype](skills/nouveau-prototype/SKILL.md) : démarrer et terminer un prototype, avec son [modèle](skills/nouveau-prototype/modele/).
- Agent [relecteur-coherence](agents/relecteur-coherence.md) : chercher, en lecture seule, ce qui contredit encore des décisions récentes.

Un skill ou un agent n'entre ici que s'il sert régulièrement : chacun coûte du contexte.
