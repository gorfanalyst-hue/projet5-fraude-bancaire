# P3-11 : Rejouer les contrôles du diagnostic

## Pourquoi cette étape ?

Les contrôles de la phase 2 sont relancés sur les tables **relues depuis `data/clean/`**. On vérifie ainsi ce qui a vraiment été enregistré, et pas seulement ce qui était en mémoire.

Le critère de fin du ticket est : **tous les contrôles passent**.

## Où est le code ?

Dans `src/diagnostic.py` : `check_clean_tables`. Elle réutilise les contrôles de la phase 2 (`check_table_links`, `check_card_owner`) et retourne une ligne par contrôle, avec le résultat obtenu et le statut.

Deux références sont mesurées au chargement des fichiers bruts, au début de `notebooks/03_nettoyage.ipynb` :

- le nombre de lignes de chaque table ;
- les totaux des types d'erreur (comme en P2-13).

## Comment l'utiliser dans le notebook

```python
lignes_avant = {name: n for name, (n, cols) in etat_avant.items()}
controles = check_clean_tables(tables, lignes_avant, ref_erreurs)
print("Tous les contrôles passent :", controles["statut"].all())
```

## Résultats obtenus

| Contrôle | Obtenu | Passe |
|---|---|---|
| Lignes de transactions | 13 305 915 | oui |
| Lignes de cards | 6 146 | oui |
| Lignes de users | 2 000 | oui |
| Lignes de mcc | 109 | oui |
| Lignes de fraud_labels | 8 914 963 | oui |
| Montants non numériques | aucun | oui |
| Montants manquants | 0 | oui |
| Dates non converties | aucune | oui |
| Dates manquantes | 0 | oui |
| Lignes orphelines (P2-02) | 0 | oui |
| Client différent du titulaire (P2-03) | 0 | oui |
| Codes MCC sans famille | 0 | oui |
| Lieux manquants ou « UNKNOWN » (P3-07) | 0 | oui |
| Totaux des erreurs différents de P2-13 | aucun | oui |
| Colonnes retirées encore présentes (P3-09) | aucune | oui |
| Indicateurs P3-08 absents | aucun | oui |
| Identifiants de transaction en double | 0 | oui |
| Étiquettes sans transaction (P2-17) | 0 | oui |

**Les 18 contrôles passent. Critère de fin validé.**

## Ce que cette étape ne fait PAS

- Elle ne corrige rien : si un contrôle échoue, il faut revenir à l'étape concernée.
- Elle ne refait pas les mesures descriptives du diagnostic (montants, revenus, répartition par mois) : seules les règles de cohérence sont rejouées.

## À noter dans le journal des transformations (P3-12)

Contrôles rejoués sur les tables relues depuis `data/clean/` : 18 contrôles, tous réussis.
