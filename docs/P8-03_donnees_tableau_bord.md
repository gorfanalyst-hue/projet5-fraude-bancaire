# P8-03 : Préparer les données du tableau de bord

## Pourquoi cette étape ?

Lire la table d'analyse de 13 millions de lignes à chaque clic rendrait le tableau de bord très lent. On prépare donc, une fois, de petites tables résumées qui contiennent exactement ce que les pages affichent.

Le critère de fin du ticket est : **tables exportées, de taille raisonnable**.

## Où est le code ?

- `src/dashboard_data.py` : `prepare_base`, `build_dashboard_tables` et `save_dashboard_tables`.
- `notebooks/08_tableau_de_bord.ipynb` : section P8-03.

| Fonction                                         | Rôle                                                                                                                                                                                                                      |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `prepare_base(df, scores, profiles)`             | Ajoute à la table d'analyse le canal en français, le lieu, le montant d'achat, les signalements aux trois seuils, la raison principale et le profil. Vérifie que les scores (P7-07) sont dans le même ordre que la table. |
| `build_dashboard_tables(base, profiles, fiches)` | Construit les tables résumées et la table des transactions signalées.                                                                                                                                                     |
| `save_dashboard_tables(tables)`                  | Enregistre chaque table en Parquet dans `data/dashboard/` (non versionné).                                                                                                                                                |

## Les tables

| Table            | Lignes  | Taille  | Contenu                                                                           |
| ---------------- | ------- | ------- | --------------------------------------------------------------------------------- |
| `jours`          | 3 591   | 0,10 Mo | Une ligne par jour                                                                |
| `mois`           | 528     | 0,03 Mo | Par année, mois, canal et lieu                                                    |
| `familles`       | 332     | 0,02 Mo | Par année, famille de commerçants et lieu                                         |
| `etats`          | 512     | 0,02 Mo | Par année et État (achats sur place aux États-Unis)                               |
| `pays`           | 671     | 0,02 Mo | Par année et pays étranger                                                        |
| `profils_annees` | 50      | 0,01 Mo | Par année et profil                                                               |
| `clients_annees` | 11 903  | 0,08 Mo | Par client et année, pour compter les clients actifs d'une période                |
| `profils`        | 4       | 0,01 Mo | Fiches des profils (P5-05)                                                        |
| `signalees`      | 266 128 | 8,55 Mo | Transactions signalées au seuil de 2 %, avec les colonnes des seuils 0,5 % et 1 % |
| `evaluation`     | 3       | 0,00 Mo | Précision et rappel de chaque seuil (P7-11)                                       |

Chaque table résumée contient les transactions, les achats, les erreurs, les achats en ligne et à l'étranger, et les signalements aux trois seuils. Le tableau de bord peut ainsi filtrer par années, canaux et seuil sans relire les transactions.

**Résultat :** 10 tables, 8,8 Mo au total, préparées en 26 s. **Critère de fin validé.**

## Ce que cette étape ne fait PAS

- Elle ne montre aucune donnée personnelle sur un client : les profils sont résumés par groupe. La table des signalées garde seulement les numéros internes du client et de la carte, sans numéro de carte ni CVV (retirés en P3-09).
