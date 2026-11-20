# P5-06 : Vérifier la stabilité des profils

## Pourquoi cette étape ?

K-means part de centres tirés au hasard. Si les profils changent beaucoup quand on change le hasard ou les clients, ils ne décrivent rien de solide. On relance donc la segmentation de deux façons et on compare.

Le critère de fin du ticket est : **profils retrouvés à l'identique ou presque**.

## Où est le code ?

- `src/profiles.py` : `check_stability`.
- `notebooks/05_profils_clients.ipynb` : section P5-06.

`check_stability` relance K-means avec cinq autres graines aléatoires, puis sur cinq échantillons de 80 % des clients. Chaque essai est comparé aux profils de référence avec l'**indice de Rand ajusté** (ARI) : 1 veut dire des groupes identiques, 0 des groupes au hasard.

## Résultats obtenus

| Essai | Clients | ARI |
| --- | --- | --- |
| Graines 1 à 5 | 1 208 | 0,996 à chaque fois |
| Échantillon 1 (80 %) | 966 | 0,915 |
| Échantillon 2 (80 %) | 966 | 0,967 |
| Échantillon 3 (80 %) | 966 | 0,950 |
| Échantillon 4 (80 %) | 966 | 0,940 |
| Échantillon 5 (80 %) | 966 | 0,973 |

ARI moyen : 0,972. ARI le plus bas : 0,915.

**Critère de fin validé** : les profils sont retrouvés presque à l'identique, même sans 20 % des clients.
