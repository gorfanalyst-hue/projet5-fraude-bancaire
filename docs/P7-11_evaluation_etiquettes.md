# P7-11 : Évaluer le score avec les étiquettes de fraude (variante avec étiquettes)

## Pourquoi cette étape ?

Le score de risque a été construit sans les étiquettes (P7-01 à P7-03). Les étiquettes permettent maintenant de mesurer ce qu'il vaut : combien de vraies fraudes il signale, et combien il en rate.

Le critère de fin du ticket est : **tableau précision et rappel commenté**.

## Où est le code ?

- `src/detection.py` : `precision_recall_fixed_threshold`.
- `notebooks/07_detection_anomalies.ipynb` : section P7-11.

Les seuils de 0,5 %, 1 % et 2 % sont ceux de P7-03, fixés sur toutes les transactions. On mesure ensuite, parmi les 8 914 963 transactions étiquetées (13 332 fraudes, taux de 0,150 %) :

- la **précision** : part de vraies fraudes parmi les transactions signalées ;
- le **rappel** : part des fraudes qui sont signalées.

## Résultats obtenus

| Seuil | Signalées (étiquetées) | Fraudes signalées | Précision | Rappel | Précision / taux de fraude |
| --- | --- | --- | --- | --- | --- |
| 0,5 % | 44 573 | 2 608 | 5,85 % | 19,56 % | 39,1 |
| 1 % | 89 483 | 3 191 | 3,57 % | 23,93 % | 23,9 |
| 2 % | 178 605 | 5 361 | 3,00 % | 40,21 % | 20,1 |

Rappel au seuil de 1 % selon le canal : 0,268 par puce, 0,237 par bande magnétique, 0,229 en ligne.

Précision au seuil de 1 % selon la raison principale :

| Raison principale | Signalées (étiquetées) | Fraudes | Précision |
| --- | --- | --- | --- |
| R10 : achat en ligne | 27 | 4 | 14,81 % |
| R06 : nouveau pays | 2 606 | 360 | 13,81 % |
| R08 : nouveau commerçant et nouvelle catégorie | 16 903 | 1 432 | 8,47 % |
| R07 : achat à l'étranger | 8 109 | 541 | 6,67 % |
| R03 : montant inhabituel | 17 506 | 439 | 2,51 % |
| R01 : échecs d'authentification répétés | 1 100 | 25 | 2,27 % |
| R09 : achat de nuit | 1 305 | 29 | 2,22 % |
| R02 : échec d'authentification | 16 401 | 336 | 2,05 % |
| R12 : hors validité de la carte | 152 | 1 | 0,66 % |
| R05 : journée très active | 3 315 | 15 | 0,45 % |
| R04 : rafale dans l'heure | 22 057 | 9 | 0,04 % |
| R13 : doublon possible | 2 | 0 | 0,00 % |

**Critère de fin validé.**

## Commentaire

- **Le score est utile, sans être précis.** Au seuil de 1 %, une transaction signalée a 23,9 fois plus de chances d'être une fraude qu'une transaction prise au hasard. Mais la grande majorité des signalements restent des fausses alertes, et le score rate environ trois fraudes sur quatre.
- **Plus le seuil monte, plus on trouve de fraudes, mais moins chaque alerte est précise** : le rappel double de 0,5 % à 2 % (de 19,56 % à 40,21 %), la précision baisse (de 5,85 % à 3,00 %).
- **Les meilleures règles** : nouveau pays (13,81 %), nouveau commerçant dans une nouvelle catégorie (8,47 %), achat à l'étranger (6,67 %). Ce sont aussi les variables les plus utiles au modèle supervisé (P7-08).
- **Les rafales ne signalent pas la fraude dans ces données** : la règle R04 a une précision de 0,04 %, plus basse que le taux de fraude moyen (0,150 %). R04 et R05 donnent pourtant 22 057 et 3 315 des signalements étiquetés.
- **Le seuil fixé sur dix ans signale trop les premières années** (P7-04). Classées à l'intérieur de 2019 seulement, les 1 % de transactions au score le plus haut trouvent 49,93 % des fraudes (P7-08), contre 23,93 % ici sur toute la période.

## Ce que ces résultats changent pour la suite

Ces résultats ne modifient pas le score de la phase 7 : le changer après avoir vu les étiquettes fausserait son évaluation. Ils alimentent les recommandations (P9-02) : retirer ou alléger les règles de rafales, renforcer les règles de lieu et de nouveauté, recalculer le seuil chaque année, et valider la nouvelle version sur des données qui n'ont servi à rien d'autre.
