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
| `transactions_data.csv` | Transactions (environ 13 millions), table de faits |
| `mcc_codes.json` | Correspondance entre code MCC et catégorie de commerçant |
| `fraud_labels.json` | Étiquette de fraude par transaction |

Les tables `users_data` et `cards_data` sont des tables de dimension, reliées à `transactions_data` par `client_id` et `card_id`.

## Structure du dépôt

```
projet5-fraude-bancaire/
├── README.md
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── load_data.py       # fonctions de chargement communes
│   └── clean_data.py      # fonctions de nettoyage et de transformation
├── notebooks/             # notebooks d'exploration et d'analyse
├── docs/                  # documentation technique de l'équipe
└── data/                  # fichiers de données (ignoré par Git)
```

## Installation

1. Cloner le dépôt :

   ```bash
   git clone https://github.com/NOM-ORGANISATION/projet5-fraude-bancaire.git
   cd projet5-fraude-bancaire
   ```

2. Créer le dossier `data/` à la racine et y placer les cinq fichiers de données reçus (voir tableau ci-dessus).

3. Installer les bibliothèques nécessaires :

   ```bash
   pip install pandas pyarrow jupyter
   ```

4. Ouvrir le dossier du dépôt dans VS Code. Le fichier `.vscode/settings.json` fait exécuter les notebooks depuis la racine du projet, ce qui permet d'écrire :

   ```python
   from src.load_data import load_transactions, load_cards, load_users, load_mcc_codes
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
- Les fichiers de `src/` contiennent des fonctions réutilisables. Les notebooks contiennent l'exécution et l'analyse.
- Ne jamais commiter de fichier de données (`.csv`, `.json`, `.parquet`).
- Avant de commiter un notebook, faire **Clear All Outputs**, car certaines sorties affichent des données sensibles (numéros de carte).
- Éviter que deux personnes modifient le même notebook en même temps.
- Toute transformation de données doit être tracée dans le journal des transformations.

## Documentation

| Document | Contenu |
|---|---|
| `docs/01_chargement_donnees.md` | Fonctions de chargement communes (P3-01) |
| `docs/02_conversion_montants.md` | Conversion des montants en nombres (P3-02) |

## Livrables

| Livrable | Date |
|---|---|
| Phases du projet et tâches granulaires | 5 octobre |
| Diagnostic, nettoyage et transformation des données | 9 novembre |
| Analyse exploratoire, rapport et présentation | 7 décembre |
| Rapport final avec recommandations opérationnelles | 14 décembre |
