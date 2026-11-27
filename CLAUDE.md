# CLAUDE.md

**La Bataille de France** : jeu vidéo open source de reconquête de la France face aux zombies, en 2030. Le projet est en phase de **conception** : le gros du travail est dans la documentation, pas dans le code.

## Langue

- Le projet est français : conversations, documentation et commentaires en **français**.
- Noms de fichiers en ASCII, en minuscules avec des tirets (`tireur-de-precision.md`). Les fichiers d'index sont en majuscules (`UNITS.md`, `SYSTEMES.md`).

## Organisation

- `README.md` : carte locale des dépôts (hors dépôt).
- `BETA1.md` : liste locale (hors dépôt) du travail sur la beta 1 ; la tenir à jour (cocher, ajouter) à chaque étape.
- `.claude/` : ce fichier, les skills et les agents de Claude Code (dépôt `labatailledefrance/agent`).
- `documentation/README.md` : vision du jeu (scénario, gameplay, exigences).
- `documentation/OPEN-PROBLEMS.md` : problèmes techniques et de conception, avec identifiants (A-01, G-03…) et statuts (Ouvert, Piste, Prototype, Décidé).
- `documentation/game-elements/` :
  - `units/UNITS.md` : index et décisions de conception des unités ; une fiche par unité dans `units/<catégorie>/`.
  - `resources/RESOURCES.md` : liste commune des ressources (carburants, munitions, vivres…).
  - `systemes/SYSTEMES.md` : règles de simulation transverses (monde, tiles, combat, logistique…).
  - `zombies/ZOMBIES.md` : comportement des zombies.
  - `constructions/CONSTRUCTIONS.md` : constructions possibles.
  - `locations/LOCATIONS.md` : index des lieux d'intérêt (CTM, centrales, barrages, bases aériennes, gares, ports, mairies, poches de survivants, bases et dépôts militaires, raffineries, usines d'armement, hôpitaux, eau potable), une fiche par type de lieu ; chaque catégorie et chaque couche dynamique a son interrupteur sur la carte (C-02).
  - `assets/ASSETS.md` : liste des assets à trouver (modèles 3D, animations, sons, icônes), avec priorité et statut ; pas de génération par IA des modèles.
- `prototypes/` : prototypes techniques jetables, un sous-dossier par prototype ; la liste (P-00 à P-26) est dans `prototypes/README.md` ; P-24 à P-26 restent en local, non versionnés : leurs enseignements vont dans `OPEN-PROBLEMS.md`. Pour en démarrer un : skill `nouveau-prototype`.
- `documentation/developpement/DEVELOPPEMENT.md` : dépôts du code, standard, pipelines, déploiement.
- Code de la beta 1, sur l'architecture de P-24 (un dépôt chacun) :
  - `.github/` : CONTRIBUTING, SECURITY, modèles d'issues, **workflows réutilisables** (rust, securite, codeql, dco, image, chart), tagués (v2.0.0) et épinglés par SHA dans chaque dépôt ;
  - `beta1-common/` : bibliothèque partagée (geo, codec, protocol et handshake sur FINGERPRINT calculé par `build.rs`, rng, format des tiles et du graphe routier ; bientôt types du catalogue), fuzzée ; les autres dépôts l'épinglent sur un même tag ;
  - `beta1-server/` : serveur Bevy sans rendu à 20 Hz, WebSocket, `--determinism` vérifié en CI à 1 et 16 threads ; plugins par domaine, contenu de base en mod `base` dans `mods/base/` (à poser, E-02, F-01, F-03) ;
  - `beta1-client/` : client Bevy wasm32 / WebGPU ;
  - `beta1-datachain/` : chaîne qui produit les tiles (à porter de P-07 et P-26) ;
  - `beta1-assets/` : manifeste et scripts des assets tiers (à porter de P-24 et P-25) ;
  - `beta1-helm/` : chart `game`, installé sur srv (namespace `labatailledefrance`).
- `data/` : données brutes (`sources/`) et générées (`generated/`), non versionnées.
- `assets/` : modèles 3D, textures, sons ; hors dépôt, jamais versionné, à déplacer dans le manifeste de `beta1-assets`.

La racine du projet n'est **pas** un dépôt git ; ne pas l'initialiser. Chaque sous-dossier versionné est un dépôt **public** de l'organisation, du même nom (`.claude/` est [`labatailledefrance/agent`](https://github.com/labatailledefrance/agent)). Le `README.md` de la racine et `BETA1.md` ne sont dans aucun dépôt.

## GitHub

- Organisation **`labatailledefrance`** (via `gh`). Les dépôts y sont créés **au besoin**.
- **Commits signés** avec la YubiKey de l'utilisateur (clé GPG `E9F8ED1DC0CD00CE`, configuration globale `commit.gpgsign = true`) : ne jamais désactiver la signature dans un dépôt. Chaque commit demande le PIN ou un contact sur la clé ; si la signature échoue, s'arrêter et prévenir l'utilisateur, sans commiter en clair.
- **`main` protégée partout** (ruleset « main protégée ») : une branche par changement, `git commit -s -S` (Signed-off-by et signature), PR, CI verte, fusion en **squash** (`gh pr merge --squash`, GitHub signe le commit). **Jamais de push direct sur `main`**, documentation comprise.
- Les workflows des contributeurs extérieurs attendent une approbation.

## Règles du code (beta 1)

Détail et justification : `documentation/developpement/DEVELOPPEMENT.md` et `.github/CONTRIBUTING.md`.

- Code en français, **termes techniques en anglais** (handshake, encode, Reader, broadcast, `--listen`…).
- Rust édition 2024, chaîne fixée par `rust-toolchain.toml` ; **pas d'`unsafe`** (`unsafe_code = "forbid"`) ; clippy `-D warnings` ; rustfmt (`max_width = 120`).
- **Dépendances** : versions exactes (`=x.y.z`), publiées depuis au moins **deux semaines**, licence compatible AGPL (`cargo deny`). Images et charts tiers : **dhi.io** d'abord, toujours **par digest**. Actions GitHub épinglées par SHA.
- **Déterminisme** : même hash d'état quel que soit le nombre de threads ; tout calcul en tâche de fond rend son résultat à un tick fixé.
- **Organisation du serveur** : un plugin Bevy par domaine (n'écrit que ses composants, communique par messages), phases ordonnées dans `app.rs`, détection d'ambiguïté en erreur ; tout ce qui décrit le jeu est en TOML dans des mods (`mods/base/`), le comportement en Rust (E-02, F-01).
- **Déployer** : `cosign verify` (cosign ≥ 3 ; celui de la distribution ne lit pas les signatures) du chart et des digests d'images publiés par la CI, puis sur srv `KUBECONFIG=/etc/rancher/k3s/k3s.yaml helm upgrade game oci://ghcr.io/labatailledefrance/charts/game …` (commande complète dans le README de `beta1-helm`). Une mise à jour du serveur remet le monde à zéro (H-01). P-26 ne tourne plus sur srv (namespace supprimé le 2026-11-27) ; ses fichiers restent dans `/srv/zombie-p26`.

## Conventions de documentation

- **Fiches d'unités** : même structure partout. Identité, Versions, Postes, Ordres possibles (ordres propres à l'unité), Armement, Équipement, Besoins logistiques, Mobilité, Interactions, Face aux zombies, Décisions, Questions ouvertes.
- **Pas de chiffres** pour les statistiques de jeu : niveaux qualitatifs (faible / moyen / élevé). Les chiffres viendront plus tard, dans le catalogue TOML de `beta1-server` (E-02), jamais dans les fiches.
- **Ressources** : dans les fiches, utiliser exactement les noms de `RESOURCES.md`.
- **Exactitude** : les informations sur l'arsenal réel dont on n'est pas sûr sont marquées « à vérifier ».
- **Liens** : relatifs, entre fichiers `.md` d'un **même dépôt**. D'un dépôt à l'autre, URL GitHub complète (`https://github.com/labatailledefrance/<dépôt>/blob/main/<chemin>`). Pas de lien vers `data/` (non versionné) ni vers `CLAUDE.md` : chemin en texte. Après une modification de structure, vérifier qu'aucun lien n'est cassé (skill `verifier-liens`).

## Traitement des décisions

L'utilisateur répond souvent aux questions ouvertes **en bloc**, sous la forme `Fiche / - Question ?: Réponse`. Pour les reporter : skill `traiter-decisions` ; après une série de décisions, l'agent `relecteur-coherence` cherche ce qui les contredit encore.

Quand on propose des questions à l'utilisateur, les donner dans ce même format pour qu'il puisse y répondre en bloc.

## Décisions structurantes (à respecter)

- **Nom du jeu** : « La Bataille de France » ; domaine `labatailledefrance.fr`, organisation GitHub `labatailledefrance`.
- Monde à l'échelle **1:1**, métropole et outre-mer seulement, **sans les TAAF, Clipperton ni le Pacifique** (Nouvelle-Calédonie, Polynésie française, Wallis-et-Futuna, hors des données de l'IGN) ; le reste du globe est affiché en gris. Les navires naviguent réellement sur toutes les mers (G-01).
- **Temps réel**, sans accélération ; si le calcul ne suit plus, le temps ralentit sous ×1 pour tous (A-02).
- **Multijoueur seulement** : une seule partie officielle, sur un serveur unique qui fait autorité, en WebSocket seul (`srv.labatailledefrance.fr`, pile native Kubernetes : ingress Traefik, qui filtre les abus ; tiles et client servis par nginx) ; monde persistant ; remise à zéro décidée par l'administrateur, et **toute mise à jour du serveur remet le monde à zéro** (pas de migration) ; instantané toutes les 5 min (A-12, A-13, H-01, H-07).
- **Jeu en navigateur** : client Bevy en WebAssembly, **WebGPU seul** ; il affiche et envoie des ordres, il ne simule rien (F-01, F-04).
- **Pas de compte** (pour le moment), anonymat total ; **tout le monde commande tout**, sans verrou, le dernier ordre l'emporte (« le joueur » = n'importe quel joueur) ; **pas de pilotage manuel** : on commande une unité, même seule, par des ordres, jamais au clavier ; un seul ordre à la fois (un ordre de groupe remplace ceux des membres) ; l'unité choisit ses cibles, pas de micro-management, sauf missions de feu sur zone, destructions d'infrastructure et frappes votées, ordonnées par le joueur (D-02) ; actions irréversibles (nucléaire, frappe sur un barrage, liste close) soumises au **vote des joueurs connectés** (majorité, une voix par adresse IP) (H-02 à H-04).
- Objectif de **1 000 joueurs simultanés** sur 1 Gbit/s, sans CDN (H-05).
- Données géographiques : **IGN** (BD TOPO, RGE ALTI) en priorité, OpenStreetMap en complément. Tiles **précalculées par le projet** (chaîne en Rust, un processus par département) installées sur le serveur, téléchargées par le client à la demande et gardées en cache (H-06) ; relief en nœuds de 2 m (B-01, P-07), de 1 m à partir de P-26, depuis le **RGE ALTI 1 m** seul (5 m en secours) : **pas de LiDAR HD** (B-01).
- **Positions** : tile (zone de projection, ix, iy) + position locale f32 centrée ; ECEF f64 pour les navires en mer ; rendu relatif à la caméra, recalé au-delà de 5 km ; ticks en u64 (dates relatives compactes en u32 modulaire), shaders nourris de phases (C-01).
- **Tiles dans le chart `game`**, un seul namespace : un Job `datachain-<hash>` (pas un hook Helm) remplit la PVC `tiles` depuis la PVC `sources` (toutes deux gardées à la désinstallation) ; un nginx de tiles les sert, le serveur les lit ; publication adressée par ses entrées (manifeste + digest de l'image), le Job ne refait rien si elle existe (H-06).
- **Bâtiments générés au chargement** depuis la BD TOPO, jamais stockés ; porte calculée par la chaîne ; rendu en morceaux fusionnés de 250 m ; monuments fidèles sur liste écrite à la main (B-02, P-08).
- **Recherche de chemin routière** : graphe national unique, CCH (ordre calculé par la chaîne, une métrique par classe d'itinéraire, personnalisation partielle après une coupure), replanification en tâche de fond ; sens uniques respectés sur les seules chaussées séparées ; un pont du jeu = une traversée (tabliers regroupés) (A-07, B-03, P-09).
- **Simulation par tiles** d'environ 1 km : actives, inertes ou sûres. Pas d'**auto-résolution** des combats, sauf à l'intérieur d'un bâtiment (contenant, intérieur non simulé, B-02).
- **Direction artistique low-poly**, dans l'esprit de Project Zomboid, textures peu détaillées ; assets existants, **pas de modèles générés par IA** ; **passe pixel art** plein écran légère (pixel de 1, palette à 60 %, contours) sur des maillages, sans Gaussian splats (E-01, P-24).
- **Météo réelle** (Météo-France en direct, CronJob `meteo`, ingérée à tick fixé ; météo calme sans jeton) et **marées** calculées depuis FES2022, prévisibles (annuaire, lune) : on planifie sur les marées à des semaines, sur la météo à quelques jours (A-11).
- **Commandement et IA** : échelons réels dans le catalogue, un ordre à un échelon est décomposé par l'IA du chef ; un ordre est un état désiré que l'unité poursuit (boucle de réconciliation, réflexes par scores d'utilité) ; sans ordre, elle tient sa position et se défend ; alertes communes, sans résumé du front (D-01 à D-04).
- **Limites du monde** : frontières terrestres infranchissables, sans zombie entrant ; les zombies ne vont pas en mer au-delà de l'estran (outre-mer et navires au mouillage = refuges) ; relief modifiable (cratères, fossés, talus) en différences dans le fichier de la tile (G-01, G-02, B-05).
- **État initial** : infrastructure intacte mais à l'arrêt, dégâts sur liste écrite à la main, stocks militaires partiels ; force d'invasion décrite dans le mod `base` (G-06).
- **Efficacité réaliste** de l'arsenal face aux zombies : c'est voulu.
- **Logistique complète** : tout ce qui est consommé est produit, transporté et livré. Exception : les ressources que la France ne peut pas produire sont fournies par des pays non spécifiés, ajoutées aux stocks des ports d'outre-mer environ toutes les deux semaines (livraison non simulée), puis transportées par le joueur (G-03).
- **Scénario** : métropole entièrement zombifiée (rares poches de survivants) ; environ 10 M d'humains en outre-mer ; les civils de métropole sont des **colons** débarqués par les ports reconquis (A-10, A-15). Aucune condition de victoire (G-07).
- **Pas de politique** simulée ; l'arme nucléaire est utilisable.
- Jeu **100 % open source**, code en **Rust portable**, sous licence **AGPL-3.0-or-later** ; documentation sous **CC-BY-SA-4.0** ; contributions sous DCO (F-05).
- Moteur **Bevy** : serveur sans rendu (simulation sur l'exécuteur multi-thread), client complet en WebAssembly. Données mises à jour ensemble groupées dans un même composant ; taille de lot minimale sur toute requête parallèle ; états fréquents en champs, marqueurs réservés aux changements rares (F-01, F-02).
- **Tâches de fond à tick fixé** : tout calcul asynchrone (chemins, flow fields) rend son résultat à un tick fixé à son lancement, que le tick attend ; les tâches de fond ne cassent plus le déterminisme (A-12, P-24).
- **Code du jeu** : les dépôts `beta1-*` suivent l'architecture de P-24 (bibliothèque commune carte + protocole, binaires serveur et client, protocole binaire écrit à la main, file d'envoi bornée par client) ; on y porte P-26, module par module. Zombies individuels jusqu'à ~1 km de la caméra, carte de densité au-delà ; objectif 60 ko/s par client (F-01, H-05, P-24).
- **Données du jeu en TOML** : un fichier par objet, dans des mods (contenu de base = mod `base`, `beta1-server/mods/base/`, à la Factorio), validation stricte au démarrage (`--check` en CI), compilées en `Catalogue` indexé par entiers, hash dans le hash d'état, envoyé au client au handshake, JSON Schema versionné et vérifié en CI ; pas de rechargement à chaud ; textes en clés de traduction Fluent, français seul (E-02, E-05) ; un instantané d'un autre hash de catalogue n'est pas repris (A-13).
- **Mods de données seulement** (`mod.toml`, ordre par dépendances, fournis par une PVC ; la partie officielle ne charge que `base`), pas de code de mod chargé à l'exécution ; un mod de comportement est un fork. **Pas de sandbox de sécurité** : ce n'est pas un objectif. Les mods ne tournent que côté serveur (F-03).
- Références (F-02) : **serveur** `srv.labatailledefrance.fr` (EPYC 7351P, 16 cœurs / 32 threads, 128 Go, 2 × 8 To HDD en RAID 0, 1 Gbit/s, k3s + Traefik) pour le budget de simulation ; **client** et mesure des prototypes : Ryzen 7 5700X, 32 Go de DDR4, RTX 3060 12 Go.

## Utilisateur

DevSecOps / RSSI, sans expérience du jeu vidéo. Expliquer les notions de développement de jeu avec des analogies tirées de l'infrastructure, des systèmes distribués ou de la sécurité. Donner des recommandations franches plutôt que des listes d'options.
