# simulateurV2H

Ce dépôt contient le code du simulateur énergétique V2H (Vehicle-to-Home), développé pendant un stage au laboratoire LUCAMI.

## Objectif

Ce simulateur permet de modéliser les échanges d’énergie entre :
- une maison,
- une production solaire (photovoltaïque),
- et un véhicule électrique.

Il prend en compte :
- les heures de connexion du véhicule,
- la consommation de la maison,
- la production solaire,
- les contraintes de recharge (puissance max, SoC, etc.).

## Organisation des fichiers

- `src/` : code Python
- `data/` : fichiers de données (PV, profils utilisateurs…)
- `results/` : résultats (graphiques, tableaux…)
- `notebooks/` : notebooks d’analyse
- `docs/` : schémas, explications
- `requirements.txt` : bibliothèques utilisées
- `CHANGELOG.md` : journal de bord

## Utilisation

Le simulateur fonctionne en Python ou dans un notebook Jupyter.
