# P9-12 : Finaliser le dépôt de code

Critère de fin de P9-12 : dépôt prêt à être partagé. Ticket du sprint 5 (14 décembre).

## Ce qui est fait

- [x] README à jour : objectif, données, structure, installation, ordre d'exécution des notebooks, tableau de bord, documentation, livrables.
- [x] `requirements.txt` à jour : `pandas`, `pyarrow`, `jupyter`, `matplotlib`, `scikit-learn`, `scipy`, `streamlit>=1.50`.
- [x] Notebooks 04 à 09 exécutés du début à la fin, sans erreur, avec leurs sorties et leurs constats.
- [x] Code testé avec deux versions de pandas (2.2 et 3.0).
- [x] Notebooks 04 à 09 réexécutés en entier sur l'ordinateur d'un membre de l'équipe (environnement MachineLearning, Python 3.11.10), sans erreur.
- [x] Aucun fichier de données dans le dépôt (`data/` est ignoré par Git).
- [x] Une page de documentation par ticket dans `docs/`, et les figures dans `docs/figures/`.

## À vérifier juste avant la remise

- [ ] Toutes les branches des tickets sont fusionnées dans `main`.
- [ ] Un membre qui n'a pas écrit le code clone le dépôt, installe les dépendances et exécute les notebooks 03 à 09 dans l'ordre (environ 30 minutes au total), puis lance le tableau de bord.
- [ ] Les notebooks 01 à 03 n'ont pas été modifiés par une simple réexécution (sinon, annuler avec `git restore`).
- [ ] Aucune sortie de notebook n'affiche de donnée sensible.

## Ordre d'exécution des notebooks

| Notebook                            | Durée approximative | Crée                                                           |
| ----------------------------------- | ------------------- | -------------------------------------------------------------- |
| `03_nettoyage_transformation.ipynb` | 4 min               | `data/clean/` : tables nettoyées                               |
| `04_table_analyse.ipynb`            | 4 min               | `data/clean/analysis.parquet`                                  |
| `05_profils_clients.ipynb`          | 2 min               | `data/clean/client_profiles.parquet`, `profile_sheets.parquet` |
| `06_analyse_exploratoire.ipynb`     | 3 min               | figures de la phase 6                                          |
| `07_detection_anomalies.ipynb`      | 14 min              | `data/clean/risk_scores.parquet`, `data/resultats/`            |
| `08_tableau_de_bord.ipynb`          | 1 min               | `data/dashboard/`                                              |
| `09_recommandations.ipynb`          | moins d'1 min       | chiffres de P9-14 et P9-15                                     |

Les durées sont celles mesurées sur l'ordinateur d'un membre de l'équipe ; elles peuvent varier. Le notebook 07 demande environ 6 Go de mémoire.
