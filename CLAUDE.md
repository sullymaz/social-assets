# social-assets

Dépôt de travail pour les publications Facebook / Instagram de Remix Web. Échanger en français.

## Publication

- Compte par défaut : page Facebook **Remix Web** (id `461058557416429`) et Instagram **@remixwebagency** (id `17841457268969492`).
- La publication passe par l'API Graph de Meta avec la variable d'environnement `META_TOKEN` (ne jamais l'afficher ni la committer).
- Ne jamais publier sans avoir montré le post final (visuel, texte, hashtags) et obtenu un accord explicite.
- La musique de la bibliothèque Instagram n'est pas accessible par l'API : les Reels embarquent un morceau de `musiques/`.

## Organisation

- `musiques/` : morceaux libres de droits classés par ambiance ; provenance à noter dans `musiques/LICENCES.md`.
- `publications/année-mois-sujet/` : visuels, vidéo et `legende.md` de chaque publication, avec son statut.
- `outils/` : scripts de génération (Python, Pillow, numpy, ffmpeg).
- `instagram/` : fichiers lus et écrits par les skills `ig-*` (`voice.md`, `plan.md`, `swipe.md`, `log.md`).
- `.claude/skills/ig-*` : skills de Jakeschincariol/instagram-agent-skill (MIT), pensés pour l'anglais ; adapter au français.

## Style des visuels

Fond sombre `#181412`, accent terracotta `#D6784A`, texte crème `#F5ECE0`, police Inter.
Publication : 1080×1350. Reel : 1080×1920, textes entre 250 et 1500 px de haut.
