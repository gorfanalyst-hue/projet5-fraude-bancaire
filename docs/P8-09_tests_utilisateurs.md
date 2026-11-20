# P8-09 : Faire tester le tableau de bord par trois personnes extérieures

Statut : **à faire par l'équipe**. Ce document donne le protocole et la grille à remplir. Le critère de fin est : **retours des trois testeurs consignés**.

## Pourquoi cette étape ?

L'équipe connaît trop bien le tableau de bord pour voir ce qui gêne un nouvel utilisateur. Trois personnes extérieures au projet (autre équipe, famille, amis) font des tâches réelles. On note le temps et les difficultés, puis on corrige (P8-10).

## Préparation

1. Exécuter `notebooks/08_tableau_de_bord.ipynb` pour créer les tables de `data/dashboard/`.
2. Lancer le tableau de bord depuis la racine du dépôt : `streamlit run dashboard/app.py`.
3. Remettre les filtres par défaut (toutes les années, seuil de 1 %, tous les canaux) avant chaque testeur.
4. Donner au testeur une seule phrase d'explication : « C'est un tableau de bord pour repérer les transactions bancaires à risque. »
5. Ne pas aider pendant le scénario. Noter les hésitations à voix haute.

## Les scénarios

| N°  | Scénario                                                                                                   | Réponse attendue (pour l'observateur)                                            | Temps visé |
| --- | ---------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ---------- |
| 1   | Combien de transactions ont été signalées en 2018, au seuil de 1 % ?                                       | Chiffre « Transactions signalées » de la page Vue d'ensemble, années 2018 à 2018 | 1 min      |
| 2   | Quel mois a compté le plus de transactions en 2015 ?                                                       | Survol de la courbe mensuelle                                                    | 1 min 30   |
| 3   | Quel profil de clients a le taux de signalement le plus haut ?                                             | Page Profils de clients, graphique des taux                                      | 1 min      |
| 4   | Dans quelle famille de commerçants le taux de signalement est-il le plus élevé ?                           | Page Lieux et catégories, tableau des familles                                   | 1 min 30   |
| 5   | Trouver les 10 transactions les plus risquées du client 1098 (ou d'un autre client présent dans la liste). | Page Transactions signalées, filtre « Client »                                   | 2 min      |
| 6   | Pourquoi la première transaction de cette liste est-elle signalée ?                                        | Colonne « raison principale »                                                    | 30 s       |
| 7   | Télécharger la liste des transactions signalées en ligne pour 2019.                                        | Filtres années et canal, bouton de téléchargement                                | 2 min      |

## Grille à remplir (une par testeur)

Testeur : ........ Date : ........ Observateur : ........

| N°  | Réussi (oui / non / avec aide) | Temps | Difficultés observées | Remarque du testeur |
| --- | ------------------------------ | ----- | --------------------- | ------------------- |
| 1   |                                |       |                       |                     |
| 2   |                                |       |                       |                     |
| 3   |                                |       |                       |                     |
| 4   |                                |       |                       |                     |
| 5   |                                |       |                       |                     |
| 6   |                                |       |                       |                     |
| 7   |                                |       |                       |                     |

Questions finales :

- Qu'est-ce qui était le plus clair ?
- Qu'est-ce qui était le plus difficile ?
- Un mot ou un chiffre que vous n'avez pas compris ?

## Synthèse des trois testeurs (à remplir)

| Difficulté | Testeurs concernés | Gravité (bloquante / gênante / mineure) | Correction prévue (P8-10) |
| ---------- | ------------------ | --------------------------------------- | ------------------------- |
|            |                    |                                         |                           |
