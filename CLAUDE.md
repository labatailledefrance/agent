# CLAUDE.md

Jeu vidéo open source de reconquête de la France face aux zombies, en 2030. Le projet est en phase de **conception** : le gros du travail est dans la documentation, pas dans le code.

## Langue

- Le projet est français : conversations, documentation et commentaires en **français**.
- Noms de fichiers en ASCII, en minuscules avec des tirets (`tireur-de-precision.md`). Les fichiers d'index sont en majuscules (`UNITS.md`, `SYSTEMES.md`).

## Organisation

- `README.md` : carte locale des dépôts (hors dépôt).
- `.claude/` : ce fichier, les skills et les agents de Claude Code (dépôt `fafapiti/agent`).
- `documentation/README.md` : vision du jeu (scénario, gameplay, exigences).
- `documentation/OPEN-PROBLEMS.md` : problèmes techniques et de conception, avec identifiants (A-01, G-03…) et statuts (Ouvert, Piste, Prototype, Décidé).
- `documentation/game-elements/` :
  - `units/UNITS.md` : index et décisions de conception des unités ; une fiche par unité dans `units/<catégorie>/`.
  - `resources/RESOURCES.md` : liste commune des ressources (carburants, munitions, vivres…).
  - `systemes/SYSTEMES.md` : règles de simulation transverses (monde, tiles, combat, logistique…).
  - `zombies/ZOMBIES.md` : comportement des zombies.
  - `constructions/CONSTRUCTIONS.md` : constructions possibles.
  - `locations/LOCATIONS.md` : index des lieux d'intérêt (CTM, centrales, bases aériennes, gares, ports, mairies, poches de survivants), une fiche par type de lieu.
- `prototypes/` : prototypes techniques jetables, un sous-dossier par prototype ; la liste (P-00 à P-23) est dans `prototypes/README.md`. Pour en démarrer un : skill `nouveau-prototype`.
- `game/` : code Rust du jeu, futur dépôt git (pas encore commencé).
- `data/` : données brutes (`sources/`) et générées (`generated/`), non versionnées.
- `assets/` : modèles 3D, textures, sons.

La racine du projet n'est **pas** un dépôt git ; ne pas l'initialiser. Les sous-dossiers deviennent des dépôts au besoin : `documentation/` est [`fafapiti/documentation`](https://github.com/fafapiti/documentation), `prototypes/` est [`fafapiti/prototypes`](https://github.com/fafapiti/prototypes), `.claude/` est [`fafapiti/agent`](https://github.com/fafapiti/agent) (privés) ; `game/` le deviendra. Le `README.md` de la racine n'est dans aucun dépôt.

## GitHub

- Organisation **`fafapiti`** (via `gh`). Les dépôts y sont créés **au besoin**.
- **Pas de signature de commit** : la configuration globale signe les commits (`commit.gpgsign = true`) ; chaque dépôt du projet la désactive localement (`git config commit.gpgsign false`).

## Conventions de documentation

- **Fiches d'unités** : même structure partout. Identité, Versions, Postes, Ordres possibles (unités [A]), Armement, Équipement, Besoins logistiques, Mobilité, Interactions, Face aux zombies, Décisions, Questions ouvertes.
- **Pas de chiffres** pour les statistiques de jeu : niveaux qualitatifs (faible / moyen / élevé). Les chiffres viendront plus tard.
- **Ressources** : dans les fiches, utiliser exactement les noms de `RESOURCES.md`.
- **Exactitude** : les informations sur l'arsenal réel dont on n'est pas sûr sont marquées « à vérifier ».
- **Liens** : relatifs, entre fichiers `.md` d'un **même dépôt**. D'un dépôt à l'autre, URL GitHub complète (`https://github.com/fafapiti/<dépôt>/blob/main/<chemin>`). Pas de lien vers `data/` (non versionné) ni vers `CLAUDE.md` : chemin en texte. Après une modification de structure, vérifier qu'aucun lien n'est cassé (skill `verifier-liens`).

## Traitement des décisions

L'utilisateur répond souvent aux questions ouvertes **en bloc**, sous la forme `Fiche / - Question ?: Réponse`. Pour les reporter : skill `traiter-decisions` ; après une série de décisions, l'agent `relecteur-coherence` cherche ce qui les contredit encore.

Quand on propose des questions à l'utilisateur, les donner dans ce même format pour qu'il puisse y répondre en bloc.

## Décisions structurantes (à respecter)

- Monde à l'échelle **1:1**, métropole et outre-mer seulement, **sans les TAAF, Clipperton ni le Pacifique** (Nouvelle-Calédonie, Polynésie française, Wallis-et-Futuna, hors des données de l'IGN) ; le reste du globe est affiché en gris. Les navires naviguent réellement sur toutes les mers (G-01).
- **Temps réel**, sans accélération ; si le calcul ne suit plus, le temps ralentit sous ×1 pour tous (A-02).
- **Multijoueur seulement** : une seule partie officielle, sur un serveur unique qui fait autorité (`srv.chelsea486mhz.fr`, pile native Kubernetes : ingress Traefik, qui filtre les abus ; tiles et client servis par nginx) ; monde persistant ; remise à zéro décidée par l'administrateur, et **toute mise à jour du serveur remet le monde à zéro** (pas de migration) ; instantané toutes les 5 min (A-12, A-13, H-01, H-07).
- **Jeu en navigateur** : client Bevy en WebAssembly, **WebGPU seul** ; il affiche et envoie des ordres, il ne simule rien (F-01, F-04).
- **Pas de compte** (pour le moment), anonymat total ; **tout le monde commande tout**, sans verrou, le dernier ordre l'emporte (« le joueur » = n'importe quel joueur) ; actions irréversibles (nucléaire, frappe sur un barrage, liste close) soumises au **vote des joueurs connectés** (majorité, une voix par adresse IP) (H-02 à H-04).
- Objectif de **1 000 joueurs simultanés** sur 1 Gbit/s, sans CDN (H-05).
- Données géographiques : **IGN** (BD TOPO, RGE ALTI) en priorité, OpenStreetMap en complément. Tiles **précalculées par le projet** (chaîne en Rust, un processus par département) installées sur le serveur, téléchargées par le client à la demande et gardées en cache (H-06) ; relief en nœuds de 2 m (B-01, P-07).
- **Positions** : tile (zone de projection, ix, iy) + position locale f32 centrée ; ECEF f64 pour les navires en mer ; rendu relatif à la caméra, recalé au-delà de 5 km ; ticks en u64 (dates relatives compactes en u32 modulaire), shaders nourris de phases (C-01).
- **Bâtiments générés au chargement** depuis la BD TOPO, jamais stockés ; porte calculée par la chaîne ; rendu en morceaux fusionnés de 250 m ; monuments fidèles sur liste écrite à la main (B-02, P-08).
- **Recherche de chemin routière** : graphe national unique, CCH (ordre calculé par la chaîne, une métrique par classe d'itinéraire, personnalisation partielle après une coupure), replanification en tâche de fond ; sens uniques respectés sur les seules chaussées séparées ; un pont du jeu = une traversée (tabliers regroupés) (A-07, B-03, P-09).
- **Simulation par tiles** d'environ 1 km : actives, inertes ou sûres. Pas d'**auto-résolution** des combats, sauf à l'intérieur d'un bâtiment (contenant, intérieur non simulé, B-02).
- **Efficacité réaliste** de l'arsenal face aux zombies : c'est voulu.
- **Logistique complète** : tout ce qui est consommé est produit, transporté et livré. Exception : les ressources que la France ne peut pas produire sont fournies par des pays non spécifiés, ajoutées aux stocks des ports d'outre-mer environ toutes les deux semaines (livraison non simulée), puis transportées par le joueur (G-03).
- **Scénario** : métropole entièrement zombifiée (rares poches de survivants) ; environ 10 M d'humains en outre-mer ; les civils de métropole sont des **colons** débarqués par les ports reconquis (A-10, A-15). Aucune condition de victoire (G-07).
- **Pas de politique** simulée ; l'arme nucléaire est utilisable.
- Jeu **100 % open source**, code en **Rust portable**. Licence à choisir plus tard.
- Moteur **Bevy** : serveur sans rendu (simulation sur l'exécuteur multi-thread), client complet en WebAssembly. Données mises à jour ensemble groupées dans un même composant ; taille de lot minimale sur toute requête parallèle ; états fréquents en champs, marqueurs réservés aux changements rares (F-01, F-02).
- **Pas de sandbox de sécurité** pour les mods : ce n'est pas un objectif. Les mods ne tournent que côté serveur (F-03).
- Références (F-02) : **serveur** `srv.chelsea486mhz.fr` (EPYC 7351P, 16 cœurs / 32 threads, 128 Go, 2 × 8 To HDD en RAID 0, 1 Gbit/s, k3s + Traefik) pour le budget de simulation ; **client** et mesure des prototypes : Ryzen 7 5700X, 32 Go de DDR4, RTX 3060 12 Go.

## Utilisateur

DevSecOps / RSSI, sans expérience du jeu vidéo. Expliquer les notions de développement de jeu avec des analogies tirées de l'infrastructure, des systèmes distribués ou de la sécurité. Donner des recommandations franches plutôt que des listes d'options.
