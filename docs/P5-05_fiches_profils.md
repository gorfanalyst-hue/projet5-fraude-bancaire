# P5-05 : Décrire et nommer chaque profil

## Pourquoi cette étape ?

Un numéro de groupe ne dit rien à un lecteur. Chaque profil reçoit une fiche : taille, portrait type (valeurs médianes) et traits distinctifs, puis un nom qui résume ces traits.

Le critère de fin du ticket est : **une fiche par profil**.

## Où est le code ?

- `src/profiles.py` : `profile_medians`, `profile_zscores` et `distinctive_traits`.
- `notebooks/05_profils_clients.ipynb` : section P5-05.

Un trait est **distinctif** quand la moyenne du profil est à plus d'un demi écart-type de la moyenne de tous les clients (écart noté entre parenthèses : +1,0 veut dire un écart-type au-dessus).

Les profils sont enregistrés dans `data/clean/client_profiles.parquet` (une ligne par client actif, avec `profil` et `profil_nom`) et les fiches dans `data/clean/profile_sheets.parquet`, pour les phases 6 à 8.

## Les fiches

### Profil 1 : Clients courants (686 clients)

- **Traits distinctifs :** aucun, le profil est proche de la moyenne sur les sept variables.
- **Portrait type :** revenu de 34 928 $, dette de 47 568 $, score de crédit de 715, 75 transactions par mois, achat moyen de 45,02 $, part en ligne de 0,058, part à l'étranger de 0,003.
- C'est le groupe le plus nombreux : plus de la moitié des clients segmentés.

### Profil 2 : Clients aisés et voyageurs (321 clients)

- **Traits distinctifs :** revenu élevé (+1,0), montant moyen élevé (+0,9), part à l'étranger élevée (+0,8).
- **Portrait type :** revenu de 59 872 $, dette de 87 082 $, achat moyen de 67,17 $, dépenses de 5 611 $ par mois, part à l'étranger de 0,010, 353 commerçants différents.

### Profil 3 : Acheteurs en ligne très actifs (138 clients)

- **Traits distinctifs :** part en ligne élevée (+2,3), fréquence élevée (+1,0).
- **Portrait type :** 131 transactions par mois, part en ligne de 0,352, achat moyen de 42,93 $, dépenses de 5 571 $ par mois.

### Profil 4 : Clients sans dette (63 clients)

- **Traits distinctifs :** dette faible (-3,7) : leur dette est nulle.
- **Portrait type :** dette de 0 $, score de crédit de 733 (le plus haut des quatre profils), revenu de 39 809 $, 94 transactions par mois. Part de femmes de 58,7 %, la plus forte des quatre profils.

## Ce que les fiches ont en commun

- Âge médian de 50 ou 51 ans et 3 cartes en médiane dans les quatre profils : les profils se distinguent par les finances et les habitudes, pas par l'âge.
- La part de nuit est proche partout (de 0,028 à 0,034).

Les 11 clients au revenu suspect restent hors profils, sous le nom « Revenu suspect (non classé) ».

**Critère de fin validé.**
