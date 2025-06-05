# Évolution du simulateur V2H – Semaines 1 à 10

## 🔹 Semaine 1
- Début du développement d’une application Streamlit pour simuler le comportement d’un VE dans un système énergétique.
- Première version fonctionnelle avec interface, graphique horaire et logique de charge/décharge.
- Création d’un schéma simplifié expliquant le fonctionnement V2H.

## 🔹 Semaine 2
- Amélioration du graphique (axes, couleurs, interactivité).
- Ajout d’indicateurs visuels : phases de charge et SoC insuffisant.
- Intégration de la production photovoltaïque dans la simulation.
- Création d’un diagramme UML et d’un arbre de décision V2H.

## 🔹 Semaine 3
- Refonte complète en Python orienté objet.
- Ajout de règles : recharge pendant surplus PV, décharge en heure de pointe, respect du SoC minimum.
- Correction du calcul du SoC avec montée progressive (max 11 kWh/h).
- Ajout d’un tableau d’événements clés (surplus PV, SoC insuffisant, etc.).

## 🔹 Semaine 4
- Intégration des données horaires réelles de production PV (PVGIS).
- Conversion et restructuration des données (W/m² → kW).
- Tests sur plusieurs mois pour valider la cohérence des courbes.

## 🔹 Semaine 5/6
- Calcul et affichage de premiers indicateurs de performance (KPI).
- Ajout d’un algorithme de décharge intelligente (aide maison sans compromettre le SoC final).
- Garantie d’atteinte du SoC cible grâce à un algorithme de contrôle.

## 🔹 Semaine 7
- Ajout de nouveaux KPI pour mieux mesurer les performances du système.
- Intégration des créneaux horaires (off-peak, mid-peak, peak).
- Génération d’un premier tableau Excel avec les entrées/sorties.

## 🔹 Semaine 8
- Réflexion approfondie sur les comportements pendant les heures pleines et en cas de surplus PV.
- Ajustements de la stratégie de charge/décharge.

## 🔹 Semaine 9
- Ajout de différents modèles de véhicules (caractéristiques batterie et puissance).
- Finalisation du simulateur Python.
- Génération automatique des scénarios + remplissage des tableaux de comparaison.

## 🔹 Semaine 10
- Création du GitHub pour héberger le simulateur.
- Organisation propre du dépôt : fichiers `.py`, notebooks, données.
- Préparation du passage vers une version app utilisable par d'autres.

