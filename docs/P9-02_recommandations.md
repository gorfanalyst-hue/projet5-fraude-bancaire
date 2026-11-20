# P9-02 : Formuler les recommandations

Statut : à valider par l'équipe (critère de fin de P9-02). Chaque recommandation est reliée au résultat qui la justifie. Les détails opérationnels (qui, quand, coût, suivi) sont dans `docs/P9-14_recommandations_operationnelles.md`.

## Règles d'alerte

| N°  | Recommandation                                                                                                                                  | Résultat qui la justifie                                                                                                                            |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| R-1 | **Mettre en place le score de risque avec un seuil de 1 %**, et contrôler les transactions dans l'ordre de la liste priorisée.                  | 37,1 alertes par jour ; 23,9 fois plus de fraudes que le hasard parmi les signalées (P7-04, P7-11).                                                 |
| R-2 | **Retirer la règle des rafales (R04) et alléger R05** dans la prochaine version du score.                                                       | R04 : 0,04 % de vraies fraudes, moins que le taux moyen (0,150 %). Elle produit les 11 faux positifs probables de la revue manuelle (P7-04, P7-11). |
| R-3 | **Donner plus de poids aux règles de lieu et de nouveauté** : nouveau pays, achat à l'étranger, nouveau commerçant dans une nouvelle catégorie. | Les plus précises : 13,81 %, 6,67 % et 8,47 % (P7-11). L'étranger est aussi la variable la plus utile au modèle supervisé (P7-08).                  |
| R-4 | **Surveiller en priorité les achats à l'étranger et les familles voyage et industrie.**                                                         | Taux de signalement de 19,437 % à l'étranger, 18,933 % en voyage, 14,926 % en industrie (P7-06).                                                    |

## Seuils

| N°  | Recommandation                                                                                              | Résultat qui la justifie                                                                            |
| --- | ----------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| R-5 | **Recalculer le seuil chaque année** (le score qui correspond au 1 % le plus risqué de l'année précédente). | Avec un seuil fixe, le taux de signalement baisse de 1,683 % en 2010 à 0,825 % en 2019 (P7-04).     |
| R-6 | **Garder le seuil de 0,5 % pour les jours de forte charge.**                                                | 18,5 alertes par jour et 5,85 % de précision, contre 37,1 et 3,57 % au seuil de 1 % (P7-04, P7-11). |

## Priorités de contrôle

| N°  | Recommandation                                                                                                                                         | Résultat qui la justifie                                                                               |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ |
| R-7 | **Contrôler d'abord les signalements dont la raison est un nouveau pays, un achat à l'étranger ou un nouveau commerçant dans une nouvelle catégorie.** | Ce sont les raisons avec la meilleure précision (P7-11).                                               |
| R-8 | **Traiter à part les achats en ligne** : la fraude y est la plus fréquente et les erreurs de CVV, numéro et expiration n'arrivent qu'en ligne.         | Taux de fraude de 0,841 % en ligne contre 0,099 % par puce (P2-17) ; types d'erreur par canal (P6-06). |

## Modèle et données à collecter

| N°   | Recommandation                                                                                                                                | Résultat qui la justifie                                                                                                             |
| ---- | --------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| R-9  | **Passer au modèle supervisé** dès que les étiquettes de fraude sont tenues à jour, et garder le score par règles pour expliquer les alertes. | Au seuil de 0,5 %, le modèle trouve 64,49 % des fraudes de 2019, contre 22,06 % pour le score (P7-08).                               |
| R-10 | **Enregistrer le résultat de chaque contrôle** (fraude confirmée ou non) dans une colonne de fraude.                                          | Sans colonne de fraude, on mesure l'inhabituel, pas la fraude ; les étiquettes ne couvrent que 67 % des transactions (P2-17, P7-10). |
| R-11 | **Garder l'historique des cartes et des clients** (date de chaque changement de carte, de revenu, de score de crédit).                        | Les informations des cartes et des clients datent de février 2020 : 1 189 cartes ouvertes après la dernière transaction (P2-12).     |

## Éthique

| N°   | Recommandation                                                                                                                  | Résultat qui la justifie                                                                                                                         |
| ---- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| R-12 | **Ne jamais utiliser le genre ni l'âge dans le score**, et suivre chaque trimestre le taux de fausses alertes par groupe d'âge. | Les moins de 30 ans sont signalés 1,108 % du temps contre 0,771 % à 75 ans et plus (rapport de 0,70), sans que l'âge soit dans le score (P9-15). |
