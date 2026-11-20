# P9-03 : Limites de l'étude

Critère de fin de P9-03 : section rédigée.

## Les données

- **Pas de colonne de fraude dans les quatre fichiers de départ.** Le score de risque repère l'inhabituel, pas la fraude. Les étiquettes ajoutées par l'enseignant permettent de l'évaluer, mais elles ne couvrent que 67,0 % des transactions (P2-17).
- **Le taux de fraude varie beaucoup selon l'année** : de 0,004 % en 2011 à 0,309 % en 2010 (P2-17). Une évaluation sur une seule année peut donc changer beaucoup d'une année à l'autre.
- **Les informations des clients et des cartes datent de février 2020**, après la dernière transaction (P2-12). Revenu, dette, score de crédit, type de carte et limite de crédit peuvent avoir changé depuis 2010. 1 189 cartes ont même été ouvertes après la dernière transaction.
- **Le jour de naissance n'est pas connu** : l'âge à la transaction peut être faux d'un an pendant le mois de naissance (P4-03).
- **Données probablement synthétiques ou retravaillées** : la puce passe de 0 % à 70,8 % d'un coup en 2015 (P6-02), et le nombre de transactions par jour de la semaine est presque identique. Les conclusions valent pour ces données, pas forcément pour une vraie banque.

## Les méthodes

- **Seuils et poids des règles choisis par l'équipe**, sans étiquettes, à partir des distributions (P7-01). La règle des rafales semblait logique mais ne signale pas la fraude (P7-11).
- **Résultats en partie circulaires** : les caractéristiques qui servent au score (étranger, en ligne, nuit) ont mécaniquement plus de signalements (P7-06).
- **Seuil fixé sur dix ans** : il signale deux fois plus en 2010 qu'en 2019 (P7-04).
- **Premières fois sans limite de temps** : un commerçant revu après cinq ans n'est plus compté comme nouveau (P4-07).
- **Profils peu séparés** (silhouette de 0,235) et calculés sur dix ans : ils ne montrent pas les changements d'habitudes (P5-04).
- **Revue manuelle faite sur dossier** : sans contacter les clients, une revue ne peut pas confirmer une fraude (P7-04).
- **Significativité trompeuse** : avec 13 millions de lignes, presque tous les tests sont significatifs. Nos conclusions s'appuient sur les tailles d'effet (P6-06, P7-05).

## Ce que l'étude ne permet pas de dire

- Le coût réel de la fraude et des contrôles : le temps de contrôle par alerte (5 minutes) est une hypothèse (P9-14).
- Si les fraudeurs changeront de comportement une fois les règles connues.
- Si les profils et le score fonctionnent pour les clients sans transaction, plus jeunes (P5-01).
