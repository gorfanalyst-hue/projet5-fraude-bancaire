# P6-07 : Croiser comportements et profils de clients

## Pourquoi cette étape ?

Les profils de la phase 5 sont construits avec sept variables. Il faut vérifier s'ils se distinguent aussi sur d'autres comportements : nuit, week-end, erreurs, remboursements, familles de commerçants.

Le critère de fin du ticket est : **tableau comparatif des profils**.

## Où est le code ?

`notebooks/06_analyse_exploratoire.ipynb`, section P6-07. Les profils viennent de `data/clean/client_profiles.parquet` (P5-05).

## Résultats obtenus

| Comportement | Acheteurs en ligne très actifs | Clients aisés et voyageurs | Clients courants | Clients sans dette |
| --- | --- | --- | --- | --- |
| Clients | 138 | 321 | 686 | 63 |
| Transactions par client | 16 808 | 11 435 | 9 519 | 11 287 |
| Part en ligne | 35,12 % | 8,12 % | 5,9 % | 8,65 % |
| Part à l'étranger | 0,44 % | 1,32 % | 0,4 % | 0,53 % |
| Part de nuit | 6,48 % | 5,79 % | 5,56 % | 5,95 % |
| Part le week-end | 28,56 % | 28,55 % | 28,58 % | 28,58 % |
| Taux d'erreur | 1,6 % | 1,55 % | 1,63 % | 1,47 % |
| Part de remboursements | 4,18 % | 5,65 % | 4,96 % | 4,2 % |
| Achat médian | 30,12 $ | 45,13 $ | 28,25 $ | 27,79 $ |
| Famille principale | Transport | Alimentation | Alimentation | Alimentation |

| Lien entre le profil et... | V de Cramér | Lecture |
| --- | --- | --- |
| l'achat en ligne | 0,335 | moyen |
| l'achat à l'étranger | 0,050 | négligeable |
| l'achat de nuit | 0,016 | négligeable |
| l'erreur | 0,007 | négligeable |

## Constats

- Les acheteurs en ligne très actifs se distinguent nettement : un tiers de leurs transactions en ligne, le plus de transactions par client, et le transport comme famille principale.
- Les clients aisés et voyageurs achètent le plus à l'étranger, ont l'achat médian le plus élevé et le plus de remboursements.
- La nuit, le week-end et les erreurs varient très peu d'un profil à l'autre.
- Seul le lien avec l'achat en ligne a une taille d'effet moyenne : les profils ne changent presque rien au moment des achats ni aux erreurs.

**Critère de fin validé.**
