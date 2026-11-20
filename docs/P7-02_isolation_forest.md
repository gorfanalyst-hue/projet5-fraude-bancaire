# P7-02 : Détecter les anomalies avec Isolation Forest

## Pourquoi cette étape ?

Les règles ne voient que ce qu'on a prévu. Isolation Forest repère les transactions qui ressemblent peu aux autres, même sans règle écrite. Le principe : on coupe les données au hasard, encore et encore ; une transaction atypique se retrouve seule après peu de coupes.

Le critère de fin du ticket est : **score calculé pour toutes les transactions**.

## Où est le code ?

- `src/detection.py` : `BEHAVIOUR_FEATURES`, `behaviour_matrix`, `train_isolation_forest` et `anomaly_scores`.
- `notebooks/07_detection_anomalies.ipynb` : section P7-02.

## Les variables de comportement

| Variable | Contenu |
| --- | --- |
| `log_amount` | Logarithme du montant (le signe est gardé pour les remboursements) |
| `log_amount_ratio` | Logarithme du rapport au montant habituel (0 si le rapport n'existe pas) |
| `card_tx_1h`, `card_tx_24h` | Activité de la carte dans l'heure et dans les 24 heures |
| `card_auth_errors_24h` | Échecs d'authentification de la carte dans les 24 heures |
| `hour` | Heure |
| `is_online`, `is_foreign` | Achat en ligne, achat à l'étranger |
| `is_first_merchant`, `is_first_mcc`, `is_first_country` | Premières fois |
| `has_auth_error` | Échec sur la transaction |

## Les fonctions

```python
def train_isolation_forest(x, sample_size=500_000, seed=42):
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(x), size=min(sample_size, len(x)), replace=False)
    model = IsolationForest(n_estimators=100, max_samples=256, random_state=seed, n_jobs=-1)
    return model.fit(x[idx])


def anomaly_scores(model, x, chunk=1_000_000):
    parts = [-model.score_samples(x[i:i + chunk]) for i in range(0, len(x), chunk)]
    return np.concatenate(parts).astype("float32")
```

| Syntaxe | Rôle |
| --- | --- |
| `sample_size=500_000` | Le modèle apprend sur un échantillon aléatoire : 500 000 lignes suffisent, et la mémoire ne permet pas les 13 millions d'un coup. |
| `n_estimators=100`, `max_samples=256` | 100 arbres, chacun construit sur 256 transactions (valeur conseillée par les auteurs de la méthode). |
| `-model.score_samples(...)` | Score d'anomalie : plus il est haut, plus la transaction est atypique. |
| `chunk=1_000_000` | Le score est calculé par morceaux d'un million de lignes. |

## Résultats obtenus

| Mesure | Valeur |
| --- | --- |
| Transactions notées | 13 305 915, sans valeur vide |
| Temps (apprentissage et calcul) | 88 s |
| Score médian | 0,3829 |
| Quantile 99 % | 0,6260 |
| Maximum | 0,7907 |

| Variable (moyenne) | 1 % le plus atypique | Autres transactions |
| --- | --- | --- |
| Premier achat chez ce commerçant | 0,767 | 0,019 |
| Premier achat dans cette catégorie | 0,679 | 0,000 |
| Achat à l'étranger | 0,078 | 0,006 |
| Transactions de la carte en 24 h | 3,853 | 1,891 |
| Échecs d'authentification en 24 h | 0,138 | 0,008 |
| Logarithme du rapport au montant habituel | 0,867 | -0,147 |

**Critère de fin validé.**

## Ce que cette étape ne fait PAS

- Elle n'utilise pas les étiquettes de fraude : Isolation Forest ne sait pas ce qu'est une fraude, il repère seulement ce qui est rare.
