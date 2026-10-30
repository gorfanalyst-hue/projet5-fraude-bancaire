# Projet 5 : Détection de fraude bancaire

Analyse des comportements transactionnels et détection de comportements potentiellement frauduleux dans des transactions bancaires.

Projet d'équipe réalisé dans le cadre du cours d'analyse de données. Remise finale : **14 décembre 2026**.

## Équipe

René, Anthony, Channel, Anaclet, Martin, Sherine

## Objectif

Aider la banque à lutter contre la fraude en :

- identifiant les profils de clients et leurs comportements transactionnels
- comparant les transactions légitimes et frauduleuses
- construisant des indicateurs qui repèrent les comportements inhabituels
- formulant des recommandations opérationnelles

## Données

Cinq sources, fournies par le cours. **Elles ne sont pas versionnées dans ce dépôt** (volume important et colonnes sensibles comme `card_number` et `cvv`).

| Fichier | Contenu |
|---|---|
| `users_data.csv` | Clients (2 000) : âge, revenus, dette, score de crédit |
| `cards_data.csv` | Cartes (6 146) : marque, type, limite de crédit |
| `transactions_data.csv` | Transactions (13 305 915, de janvier 2010 à octobre 2019), table de faits |
| `mcc_codes.json` | Catégories de commerçants (109 codes MCC) |
| `fraud_labels.json` | Étiquette de fraude (Yes/No) pour 8 914 963 transactions, soit 67,0 % |

Les tables `users_data` et `cards_data` sont des tables de dimension, reliées à `transactions_data` par `client_id` et `card_id`.

## Structure du dépôt

```
projet5-fraude-bancaire/
├── README.md
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── load_data.py       # chargement des fichiers bruts et des tables nettoyées
│   ├── diagnostic.py      # contrôles du diagnostic (phase 2)
│   ├── clean_data.py      # nettoyage et transformation (phase 3)
│   └── mcc_families.py    # familles de codes MCC (P3-05)
├── notebooks/
│   ├── 01_exploration_donnees.ipynb       # phase 2 : exploration des fichiers reçus
│   ├── 02_diagnostic_qualite.ipynb        # phase 2 : diagnostic de la qualité
│   └── 03_nettoyage_transformation.ipynb  # phase 3 : nettoyage et transformation
├── docs/                  # une page par ticket, nommée par son numéro (P3-02_...)
└── data/                  # fichiers de données (ignoré par Git)
    └── clean/             # tables nettoyées au format Parquet (P3-10)
```

## Installation

1. Cloner le dépôt :

   ```bash
   git clone https://github.com/gorfanalyst-hue/projet5-fraude-bancaire.git
   cd projet5-fraude-bancaire
   ```

2. Créer le dossier `data/` à la racine et y placer les cinq fichiers de données reçus (voir tableau ci-dessus).

3. Installer les bibliothèques nécessaires :

   ```bash
   pip install -r requirements.txt
   ```

4. Ouvrir le dossier du dépôt dans VS Code. Le fichier `.vscode/settings.json` fait exécuter les notebooks depuis la racine du projet, ce qui permet d'écrire :

   ```python
   from src.load_data import load_transactions, load_cards, load_users, load_mcc_codes, load_fraud_labels
   ```

5. Pour travailler sur les données nettoyées, exécuter une fois `notebooks/03_nettoyage_transformation.ipynb` (environ 4 minutes). Il crée les fichiers de `data/clean/`, qui se relisent ensuite en quelques secondes :

   ```python
   from src.load_data import load_clean_table
   df_transaction = load_clean_table("transactions")
   ```

## Règles de travail

**Une branche par ticket Jira.** Personne ne travaille directement sur `main`.

```bash
git checkout main
git pull
git checkout -b P3-02-conversion-montants
# travail, puis :
git add <fichiers>
git commit -m "P3-02: conversion des montants en numérique"
git push -u origin P3-02-conversion-montants
```

Ensuite, ouvrir une **Pull Request** vers `main`. Le relecteur désigné dans Jira la relit et la fusionne.

Règles à respecter :

- Mettre le numéro du ticket dans le nom de la branche et dans le message de commit.
- Un notebook par phase, nommé `<numéro de phase>_<contenu>.ipynb` (exemple : `02_diagnostic_qualite.ipynb`). Une section par ticket, avec son critère de fin et des constats sous chaque résultat.
- Une page de documentation par ticket dans `docs/`, nommée `<ticket>_<contenu>.md` (exemple : `P3-02_conversion_montants.md`).
- Les fichiers de `src/` contiennent des fonctions réutilisables. Les notebooks contiennent l'exécution et l'analyse.
- Ne jamais commiter de fichier de données (`.csv`, `.json`, `.parquet`).
- Avant de commiter un notebook, faire **Clear All Outputs**, car certaines sorties affichent des données sensibles (numéros de carte).
- Éviter que deux personnes modifient le même notebook en même temps.
- Toute transformation de données doit être tracée dans le journal des transformations.

## Documentation

| Document | Contenu |
|---|---|
| `docs/P2-16_rapport_diagnostic.md` | Rapport de diagnostic de la qualité des données (P2-16) |
| `docs/P2-17_etiquettes_fraude.md` | Contrôle des étiquettes de fraude (P2-17) |
| `docs/P3-01_chargement_donnees.md` | Fonctions de chargement communes (P3-01) |
| `docs/P3-02_conversion_montants.md` | Conversion des montants en nombres (P3-02) |
| `docs/P3-03_conversion_dates.md` | Conversion des dates (P3-03) |
| `docs/P3-04_table_mcc.md` | Table des catégories MCC (P3-04) |
| `docs/P3-05_familles_mcc.md` | Regroupement des codes MCC en familles (P3-05) |
| `docs/P3-06_colonne_errors.md` | Transformation de la colonne errors (P3-06) |
| `docs/P3-07_lieu_transactions.md` | Structuration du lieu des transactions (P3-07) |
| `docs/P3-08_valeurs_suspectes.md` | Règles pour les valeurs suspectes (P3-08) |
| `docs/P3-09_colonnes_retirees.md` | Colonnes sensibles et inutiles retirées (P3-09) |
| `docs/P3-10_tables_nettoyees.md` | Tables nettoyées enregistrées en Parquet (P3-10) |
| `docs/P3-11_controles_rejoues.md` | Contrôles rejoués sur les tables nettoyées (P3-11) |
| `docs/P3-12_journal_transformations.md` | Journal des transformations (P3-12) |

## Livrables

| Livrable | Date |
|---|---|
| Phases du projet et tâches granulaires | 5 octobre |
| Diagnostic, nettoyage et transformation des données | 9 novembre |
| Analyse exploratoire, rapport et présentation | 7 décembre |
| Rapport final avec recommandations opérationnelles | 14 décembre |

### Livrable du 9 novembre : diagnostic, nettoyage et transformation

| Partie | Notebook | Documents |
|---|---|---|
| Exploration des fichiers (P2-01) | `notebooks/01_exploration_donnees.ipynb` | |
| Diagnostic de la qualité (phase 2) | `notebooks/02_diagnostic_qualite.ipynb` | `docs/P2-16_rapport_diagnostic.md`, `docs/P2-17_etiquettes_fraude.md` |
| Nettoyage et transformation (phase 3) | `notebooks/03_nettoyage_transformation.ipynb` | `docs/P3-01_...` à `docs/P3-11_...` |
| Synthèse des transformations | | `docs/P3-12_journal_transformations.md` |
