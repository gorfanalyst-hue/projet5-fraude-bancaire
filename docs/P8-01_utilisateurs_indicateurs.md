# P8-01 : Définir les utilisateurs et les indicateurs clés

Statut : à valider par l'équipe (critère de fin de P8-01).

## Pourquoi cette étape ?

Un tableau de bord sert des personnes précises. Avant de dessiner les pages, il faut savoir qui le consulte, quelles questions ces personnes se posent et quels chiffres elles suivent. Sinon, on montre tout et personne ne trouve ce qu'il cherche.

Le critère de fin du ticket est : **liste des indicateurs clés validée**.

## Les utilisateurs

| Utilisateur                      | Ce qu'il fait avec le tableau de bord                                                                       | Fréquence      |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------- | -------------- |
| **Analyste de la fraude**        | Ouvre la liste priorisée, contrôle les transactions les plus risquées, cherche les transactions d'un client | Chaque jour    |
| **Responsable de la fraude**     | Suit le nombre de signalements et la charge de travail, choisit le seuil, repère les hausses                | Chaque semaine |
| **Relation client ou marketing** | Comprend les profils de clients et leurs habitudes (canaux, lieux, catégories)                              | Chaque mois    |

## Leurs questions et les indicateurs qui répondent

| Question                                                      | Indicateur                                                                          | Page                                   |
| ------------------------------------------------------------- | ----------------------------------------------------------------------------------- | -------------------------------------- |
| Quel est le volume d'activité sur la période ?                | Transactions, montant des achats, achat moyen, clients actifs                       | Vue d'ensemble                         |
| Combien de transactions faut-il contrôler ?                   | Transactions signalées et taux de signalement, au seuil choisi                      | Vue d'ensemble, Transactions signalées |
| Combien de clients sont touchés par un signalement ?          | Clients avec au moins un signalement                                                | Vue d'ensemble                         |
| L'activité monte-t-elle ou baisse-t-elle ?                    | Courbe mensuelle des transactions, des achats et des signalements                   | Vue d'ensemble                         |
| Comment les clients paient-ils ?                              | Part de chaque canal (bande, puce, en ligne) par année, part des achats en ligne    | Vue d'ensemble                         |
| Quels sont les profils de clients ?                           | Taille, revenu médian, fréquence, achat moyen, traits distinctifs de chaque profil  | Profils de clients                     |
| Un profil est-il plus exposé ?                                | Taux de signalement par profil                                                      | Profils de clients                     |
| Où les clients achètent-ils ?                                 | Part en ligne, sur place, à l'étranger ; États et pays les plus fréquents           | Lieux et catégories                    |
| Quels commerces pèsent le plus et lesquels sont risqués ?     | Part des transactions et du montant, taux de signalement par famille de commerçants | Lieux et catégories                    |
| Quelles transactions contrôler en premier ?                   | Liste triée par score, avec la raison principale                                    | Transactions signalées                 |
| Pourquoi cette transaction est-elle signalée ?                | Raison principale et règles déclenchées                                             | Transactions signalées                 |
| Quelles sont les transactions les plus risquées d'un client ? | Liste filtrée sur le numéro du client                                               | Transactions signalées                 |
| Le score est-il fiable ?                                      | Précision et rappel mesurés sur les transactions étiquetées (P7-11)                 | Transactions signalées                 |

## Les filtres communs

- **Années** : de 2010 à 2019, ou une seule année.
- **Seuil de signalement** : 0,5 %, 1 % ou 2 % des transactions les plus risquées (P7-04).
- **Canaux de paiement** : bande magnétique, puce, en ligne.

## Ce que cette étape ne fait PAS

- Elle ne choisit pas l'outil et ne dessine pas les pages : c'est P8-02.
- Elle ne montre aucune donnée personnelle (revenu ou dette d'un client précis) : les profils sont présentés par groupe.
