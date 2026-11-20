# P9-14 : Détailler les recommandations opérationnelles

Statut : à valider par l'équipe (critère de fin de P9-14). Ce tableau détaille les recommandations de P9-02. Les chiffres du coût des fausses alertes viennent de `notebooks/09_recommandations.ipynb`.

## Coût des fausses alertes selon le seuil

Hypothèse : **5 minutes de contrôle par alerte** (à remplacer par la mesure réelle de l'équipe de la banque).

| Seuil | Alertes par jour | Fausses alertes par jour | Heures de contrôle par jour | Fraudes trouvées (étiquetées) | Fraudes ratées (étiquetées) | Fausses alertes pour une fraude trouvée |
| ----- | ---------------- | ------------------------ | --------------------------- | ----------------------------- | --------------------------- | --------------------------------------- |
| 0,5 % | 18,5             | 17,5                     | 1,5                         | 2 608                         | 10 724                      | 16,1                                    |
| 1 %   | 37,1             | 35,7                     | 3,1                         | 3 191                         | 10 141                      | 27,0                                    |
| 2 %   | 74,1             | 71,9                     | 6,2                         | 5 361                         | 7 971                       | 32,3                                    |

Lecture : passer de 1 % à 2 % double la charge (de 3,1 à 6,2 heures par jour) pour trouver 5 361 fraudes au lieu de 3 191 sur dix ans de transactions étiquetées. Le seuil de 1 % est un compromis : environ une demi-journée de contrôle par jour.

## Tableau des recommandations opérationnelles

| N°   | Recommandation                                                                                                             | Qui agit                                                       | Quand                                                                           | Indicateur de suivi                                                             | Ordre |
| ---- | -------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ----- |
| R-1  | Score de risque au seuil de 1 %, contrôle dans l'ordre de la liste                                                         | Analystes de la fraude                                         | Revue a posteriori, chaque matin, sur les transactions de la veille             | Alertes traitées par jour ; part des fraudes confirmées                         | 1     |
| R-7  | Contrôler d'abord les raisons « nouveau pays », « achat à l'étranger », « nouveau commerçant dans une nouvelle catégorie » | Analystes de la fraude                                         | Chaque matin, en tête de liste                                                  | Précision par raison principale                                                 | 1     |
| R-10 | Enregistrer le résultat de chaque contrôle (fraude confirmée ou non)                                                       | Analystes de la fraude                                         | À chaque contrôle                                                               | Part des alertes avec un résultat enregistré (objectif : toutes)                | 1     |
| R-12 | Ne pas utiliser le genre ni l'âge ; suivre les fausses alertes par groupe d'âge                                            | Responsable de la fraude, avec la conformité                   | Chaque trimestre                                                                | Rapport le plus bas / le plus haut du taux de fausses alertes (alerte sous 0,8) | 1     |
| R-6  | Passer au seuil de 0,5 % les jours de forte charge                                                                         | Responsable de la fraude                                       | Chaque jour, selon le nombre d'alertes en attente                               | Alertes en attente à la fin de la journée                                       | 2     |
| R-2  | Retirer la règle R04 et alléger R05, puis valider sur des données nouvelles                                                | Équipe d'analyse de données                                    | Prochaine version du score (sous un mois)                                       | Précision et rappel avant et après, sur une année jamais utilisée               | 2     |
| R-3  | Plus de poids aux règles de lieu et de nouveauté                                                                           | Équipe d'analyse de données                                    | Prochaine version du score, avec R-2                                            | Précision des règles R06, R07 et R08                                            | 2     |
| R-8  | Contrôle spécifique des achats en ligne (CVV, numéro, expiration)                                                          | Analystes de la fraude, avec le service des paiements en ligne | Temps réel pour les échecs répétés, revue a posteriori pour le reste            | Taux de fraude en ligne ; échecs de CVV par jour                                | 2     |
| R-4  | Surveillance des achats à l'étranger, du voyage et de l'industrie                                                          | Analystes de la fraude                                         | Temps réel pour un premier achat dans un pays, revue a posteriori pour le reste | Taux de signalement et précision par famille et par lieu                        | 2     |
| R-5  | Recalculer le seuil chaque année                                                                                           | Équipe d'analyse de données                                    | Chaque janvier                                                                  | Taux de signalement de l'année (objectif : 1 %)                                 | 3     |
| R-11 | Garder l'historique des cartes et des clients                                                                              | Équipe des données de la banque                                | Dès maintenant, pour les nouvelles données                                      | Part des changements datés                                                      | 3     |
| R-9  | Passer au modèle supervisé, garder les règles pour expliquer                                                               | Équipe d'analyse de données                                    | Quand au moins une année de résultats de contrôle est enregistrée (R-10)        | Rappel au seuil de 0,5 % (modèle : 64,49 % en 2019)                             | 4     |

## Temps réel ou revue a posteriori ?

- **Revue a posteriori** (le lendemain) pour la liste priorisée : le score utilise l'historique du client et Isolation Forest, faciles à calculer chaque nuit.
- **Temps réel** seulement pour deux signaux simples, connus au moment du paiement : un premier achat dans un pays et des échecs d'authentification répétés en ligne. Ils peuvent déclencher une confirmation par message au client.

## Ordre de mise en œuvre

1. **Tout de suite** : R-1, R-7, R-10, R-12 (le score existe déjà, il faut l'utiliser et enregistrer les résultats).
2. **Sous un mois** : R-2, R-3, R-4, R-6, R-8 (améliorer le score et l'organisation des contrôles).
3. **Chaque année** : R-5 ; **dès maintenant pour l'avenir** : R-11.
4. **Après un an de résultats enregistrés** : R-9.
