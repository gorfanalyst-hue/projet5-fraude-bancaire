# P5-03 : Préparer la segmentation

## Pourquoi cette étape ?

K-means mesure des distances. Deux problèmes peuvent fausser les groupes :

- deux variables qui disent la même chose comptent deux fois ;
- une variable en dollars (revenu : des dizaines de milliers) écrase une variable entre 0 et 1 (part en ligne).

Il faut donc choisir des variables peu liées entre elles, puis les mettre à la même échelle.

Le critère de fin du ticket est : **choix des variables justifié par écrit**.

## Où est le code ?

- `src/profiles.py` : `CLUSTER_VARIABLES`, `LOG_VARIABLES` et `prepare_features`.
- `notebooks/05_profils_clients.ipynb` : section P5-03.

## Les corrélations entre les variables candidates

Corrélation de Spearman (de -1 à 1), calculée sur les 1 219 clients actifs. Paires à 0,5 ou plus :

| Paire | Corrélation | Décision |
| --- | --- | --- |
| Dette et dette / revenu | 0,89 | On garde la dette |
| Montant moyen et montant médian | 0,80 | On garde le montant moyen |
| Transactions par mois et dépenses par mois | 0,74 | On garde les transactions par mois |
| Dépenses par mois et commerçants différents | 0,63 | Aucune des deux n'est gardée |
| Part à l'étranger et commerçants différents | 0,52 | On garde la part à l'étranger |
| Dépenses par mois et montant médian | 0,51 | Aucune des deux n'est gardée |

## Le choix des variables

Sept variables, dont aucune paire ne dépasse 0,5 :

| Variable | Groupe | Raison du choix |
| --- | --- | --- |
| Revenu annuel | Finances | Capacité de dépense |
| Dette | Finances | Situation financière |
| Score de crédit | Finances | Fiabilité financière |
| Montant moyen des achats | Dépenses | Niveau de dépense par achat |
| Transactions par mois | Dépenses | Fréquence d'utilisation |
| Part en ligne | Dépenses | Canal préféré |
| Part à l'étranger | Dépenses | Voyages |

Le genre et l'âge n'entrent pas dans la segmentation : un profil doit décrire un comportement, pas une caractéristique personnelle. Ils servent seulement à décrire les profils (P5-05).

Les 11 clients au revenu suspect (P3-08) sont écartés : leur revenu (parfois 1 $) créerait un groupe artificiel. 1 208 clients sont segmentés.

## La mise à l'échelle

```python
LOG_VARIABLES = ["yearly_income", "total_debt", "mean_purchase", "tx_per_month", "share_foreign"]

def prepare_features(profiles, variables=CLUSTER_VARIABLES, log_variables=LOG_VARIABLES):
    x = profiles[variables].astype(float).copy()
    for col in log_variables:
        x[col] = np.log1p(x[col])
    scaled = StandardScaler().fit_transform(x)
    return pd.DataFrame(scaled, index=profiles.index, columns=variables)
```

| Syntaxe | Rôle |
| --- | --- |
| `np.log1p(x)` | log(1 + x) : resserre les variables très asymétriques (quelques revenus ou dettes très élevés). Le « + 1 » garde la dette nulle à 0. |
| `StandardScaler()` | Met chaque variable à une moyenne de 0 et un écart-type de 1. |

Après la mise à l'échelle, chaque variable a bien une moyenne de 0 et un écart-type de 1.

**Critère de fin validé.**
