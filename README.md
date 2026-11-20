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

| Fichier                 | Contenu                                                                   |
| ----------------------- | ------------------------------------------------------------------------- |
| `users_data.csv`        | Clients (2 000) : âge, revenus, dette, score de crédit                    |
| `cards_data.csv`        | Cartes (6 146) : marque, type, limite de crédit                           |
| `transactions_data.csv` | Transactions (13 305 915, de janvier 2010 à octobre 2019), table de faits |
| `mcc_codes.json`        | Catégories de commerçants (109 codes MCC)                                 |
| `fraud_labels.json`     | Étiquette de fraude (Yes/No) pour 8 914 963 transactions, soit 67,0 %     |

Les tables `users_data` et `cards_data` sont des tables de dimension, reliées à `transactions_data` par `client_id` et `card_id`.

## Structure du dépôt

```
projet5-fraude-bancaire/
├── README.md
├── .gitignore
├── requirements.txt
├── .streamlit/
│   └── config.toml # couleurs du tableau de bord (charte, P1-10)
├── src/
│   ├── __init__.py
│   ├── load_data.py # chargement des fichiers bruts et des tables nettoyées
│   ├── diagnostic.py # contrôles du diagnostic (phase 2)
│   ├── clean_data.py # nettoyage et transformation (phase 3)
│   ├── mcc_families.py # familles de codes MCC (P3-05)
│   ├── charte.py # charte graphique : couleurs, style, enregistrement des figures (P1-10)
│   ├── features.py # table d'analyse et indicateurs (phase 4)
│   ├── profiles.py # profils de clients (phase 5)
│   ├── comparisons.py # taux, tests et tailles d'effet (phases 6 et 7)
│   ├── detection.py # règles, Isolation Forest, score de risque, modèle supervisé (phase 7)
│   └── dashboard_data.py # tables du tableau de bord (P8-03)
├── notebooks/
│   ├── 01_exploration_donnees.ipynb # phase 2 : exploration des fichiers reçus
│   ├── 02_diagnostic_qualite.ipynb # phase 2 : diagnostic de la qualité
│   ├── 03_nettoyage_transformation.ipynb # phase 3 : nettoyage et transformation
│   ├── 04_table_analyse.ipynb # phase 4 : table d'analyse et indicateurs
│   ├── 05_profils_clients.ipynb # phase 5 : profils de clients (Q1)
│   ├── 06_analyse_exploratoire.ipynb # phase 6 : comportements (Q2, Q6)
│   ├── 07_detection_anomalies.ipynb # phase 7 : score de risque et détection (Q3, Q4, Q5)
│   ├── 08_tableau_de_bord.ipynb # phase 8 : données et vérification du tableau de bord (Q7)
│   └── 09_recommandations.ipynb # phase 9 : chiffres de l'éthique et du coût des alertes
├── dashboard/
│   ├── app.py # application Streamlit : filtres et navigation
│   ├── pages.py # les quatre pages (P8-04 à P8-07)
│   └── calculs.py # calculs des chiffres affichés (vérifiés en P8-08)
├── docs/ # une page par ticket, nommée par son numéro (P3-02_...)
│   └── figures/ # visuels des notebooks et captures du tableau de bord
└── data/ # fichiers de données (ignoré par Git)
    ├── clean/ # tables nettoyées et table d'analyse au format Parquet
    ├── resultats/ # liste priorisée et grille de revue (phase 7)
    └── dashboard/ # tables du tableau de bord (P8-03)
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

4. Ouvrir le dossier du dépôt dans VS Code. Le dossier `.vscode/` n'est pas versionné : chacun y garde ses réglages personnels. Chaque membre doit donc créer son propre fichier `.vscode/settings.json` avec ce réglage, qui fait exécuter les notebooks depuis la racine du projet :

   ```json
   {
     "jupyter.notebookFileRoot": "${workspaceFolder}"
   }
   ```

   Sans ce réglage, les imports `from src...` échouent dans les notebooks. Avec lui, on peut écrire :

   ```python
   from src.load_data import load_transactions, load_cards, load_users, load_mcc_codes, load_fraud_labels
   ```

5. Exécuter les notebooks dans l'ordre. Chacun crée les fichiers dont le suivant a besoin (`data/` n'est pas versionné) :

   | Notebook | Durée approximative | Crée |
   | --- | --- | --- |
   | `03_nettoyage_transformation.ipynb` | 4 min | `data/clean/` : tables nettoyées |
   | `04_table_analyse.ipynb` | 4 min | `data/clean/analysis.parquet` |
   | `05_profils_clients.ipynb` | 2 min | `data/clean/client_profiles.parquet` |
   | `06_analyse_exploratoire.ipynb` | 3 min | figures de la phase 6 |
   | `07_detection_anomalies.ipynb` | 14 min (environ 6 Go de mémoire) | `data/clean/risk_scores.parquet`, `data/resultats/` |
   | `08_tableau_de_bord.ipynb` | 1 min | `data/dashboard/` |
   | `09_recommandations.ipynb` | moins d'1 min | chiffres de P9-14 et P9-15 |

   Les tables se relisent ensuite en quelques secondes :

   ```python
   from src.load_data import load_clean_table
   df_transaction = load_clean_table("transactions")
   df = load_clean_table("analysis", columns=["id", "client_id", "amount", "amount_ratio"])
   ```

6. Lancer le tableau de bord, depuis la racine du dépôt :

   ```bash
   streamlit run dashboard/app.py
   ```

   Le navigateur s'ouvre sur `http://localhost:8501`. Mode d'emploi : `docs/P8-11_guide_utilisation.md`.

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
- Les notebooks sont versionnés **avec leurs sorties**, pour que les résultats se lisent directement sur GitHub. Avant de commiter un notebook :
  - l'exécuter en entier, du début à la fin, sans erreur ;
  - vérifier qu'aucune sortie n'affiche de donnée sensible (numéro de carte, CVV, adresse). Ces colonnes sont masquées dans l'exploration (P2-01) et retirées des tables nettoyées (P3-09).
- Éviter que deux personnes modifient le même notebook en même temps.
- Toute transformation de données doit être tracée dans le journal des transformations.

## Documentation

Une page par ticket. Les visuels sont dans `docs/figures/`.

| Document | Contenu |
| --- | --- |
| `docs/P1-04_dictionnaire_donnees.md` | Dictionnaire des données |
| `docs/P1-10_charte_graphique.md` | Charte graphique |
| `docs/P2-16_rapport_diagnostic.md` | Rapport de diagnostic de la qualité des données |
| `docs/P2-17_etiquettes_fraude.md` | Contrôler les étiquettes de fraude |
| `docs/P3-01_chargement_donnees.md` | Fonction de chargement commune des données |
| `docs/P3-02_conversion_montants.md` | Conversion des montants en nombres |
| `docs/P3-03_conversion_dates.md` | Conversion des dates |
| `docs/P3-04_table_mcc.md` | Table des catégories MCC |
| `docs/P3-05_familles_mcc.md` | Regrouper les codes MCC en familles |
| `docs/P3-06_colonne_errors.md` | Transformer la colonne errors |
| `docs/P3-07_lieu_transactions.md` | Structurer le lieu des transactions |
| `docs/P3-08_valeurs_suspectes.md` | Appliquer les règles aux valeurs suspectes |
| `docs/P3-09_colonnes_retirees.md` | Retirer les colonnes sensibles et inutiles |
| `docs/P3-10_tables_nettoyees.md` | Enregistrer les tables nettoyées |
| `docs/P3-11_controles_rejoues.md` | Rejouer les contrôles du diagnostic |
| `docs/P3-12_journal_transformations.md` | Journal des transformations |
| `docs/P4-01_table_analyse.md` | Construire la table d'analyse |
| `docs/P4-02_variables_temps.md` | Créer les variables de temps |
| `docs/P4-03_age_transaction.md` | Calculer l'âge du client à la date de la transaction |
| `docs/P4-04_ecart_montant_habituel.md` | Mesurer l'écart au montant habituel du client |
| `docs/P4-05_frequence_carte.md` | Mesurer la fréquence d'utilisation de la carte |
| `docs/P4-06_echecs_authentification.md` | Compter les échecs d'authentification récents |
| `docs/P4-07_premieres_fois.md` | Repérer les premières fois |
| `docs/P4-08_indicateurs_contexte.md` | Créer les indicateurs de contexte |
| `docs/P4-09_catalogue_indicateurs.md` | Catalogue des indicateurs (Q5) |
| `docs/P4-10_controle_enregistrement.md` | Contrôler et enregistrer la table d'analyse |
| `docs/P5-01_population_clients.md` | Décrire la population des clients |
| `docs/P5-02_variables_profil.md` | Construire les variables de profil |
| `docs/P5-03_preparation_segmentation.md` | Préparer la segmentation |
| `docs/P5-04_segmentation_kmeans.md` | Segmenter les clients avec K-means |
| `docs/P5-05_fiches_profils.md` | Décrire et nommer chaque profil |
| `docs/P5-06_stabilite_profils.md` | Vérifier la stabilité des profils |
| `docs/P5-07_visuel_profils.md` | Visuel clé des profils (Q1) |
| `docs/P5-08_section_profils.md` | Section « Profils de clients » du rapport (Q1) |
| `docs/P6-01_montants.md` | Analyser les montants |
| `docs/P6-02_canaux_paiement.md` | Analyser les canaux de paiement |
| `docs/P6-03_evolution_temps.md` | Analyser l'évolution dans le temps (Q6) |
| `docs/P6-04_geographie.md` | Analyser la géographie (Q6) |
| `docs/P6-05_categories_commercants.md` | Analyser les catégories de commerçants (Q6) |
| `docs/P6-06_erreurs_refus.md` | Analyser les erreurs et les refus |
| `docs/P6-07_comportements_profils.md` | Croiser comportements et profils de clients |
| `docs/P6-08_visuels_comportements.md` | Visuels clés des comportements (Q2, Q6) |
| `docs/P6-09_section_comportements.md` | Section « Comportements » du rapport (Q2, Q6) |
| `docs/P7-01_regles_metier.md` | Coder les règles métier |
| `docs/P7-02_isolation_forest.md` | Détecter les anomalies avec Isolation Forest |
| `docs/P7-03_score_risque.md` | Construire le score de risque |
| `docs/P7-04_validation_score.md` | Valider le score |
| `docs/P7-05_comparaison_signalees.md` | Comparer les transactions signalées aux autres (Q3) |
| `docs/P7-06_caracteristiques_risque.md` | Identifier les caractéristiques liées au risque (Q4) |
| `docs/P7-07_liste_priorisee.md` | Produire la liste priorisée (Q5) |
| `docs/P7-08_modele_supervise.md` | Modèle supervisé (variante avec étiquettes de fraude) |
| `docs/P7-09_visuels_detection.md` | Visuels clés de la détection (Q3, Q4) |
| `docs/P7-10_section_detection.md` | Section « Détection » du rapport (Q3, Q4, Q5) |
| `docs/P7-11_evaluation_etiquettes.md` | Évaluer le score avec les étiquettes de fraude (variante avec étiquettes) |
| `docs/P8-01_utilisateurs_indicateurs.md` | Définir les utilisateurs et les indicateurs clés |
| `docs/P8-02_outil_maquette.md` | Choisir l'outil et dessiner la maquette |
| `docs/P8-03_donnees_tableau_bord.md` | Préparer les données du tableau de bord |
| `docs/P8-04_page_vue_ensemble.md` | Créer la page « Vue d'ensemble » |
| `docs/P8-05_page_profils.md` | Créer la page « Profils de clients » |
| `docs/P8-06_page_lieux_categories.md` | Créer la page « Lieux et catégories » |
| `docs/P8-07_page_transactions_signalees.md` | Créer la page « Transactions signalées » |
| `docs/P8-08_verification_chiffres.md` | Vérifier les chiffres du tableau de bord |
| `docs/P8-09_tests_utilisateurs.md` | Faire tester le tableau de bord par trois personnes extérieures |
| `docs/P8-10_ameliorations.md` | Améliorer le tableau de bord après les tests |
| `docs/P8-11_guide_utilisation.md` | Guide d'utilisation du tableau de bord |
| `docs/P9-01_reponses_questions.md` | Répondre aux questions de recherche |
| `docs/P9-02_recommandations.md` | Formuler les recommandations |
| `docs/P9-03_limites.md` | Limites de l'étude |
| `docs/P9-04_rapport_final.md` | Assembler le rapport final |
| `docs/P9-05_relecture.md` | Relire le rapport à deux |
| `docs/P9-06_fil_conducteur.md` | Fil conducteur de la présentation |
| `docs/P9-07_gabarit_diapositives.md` | Créer le gabarit et les diapositives de structure |
| `docs/P9-08_repartition_parole.md` | Répartir la parole |
| `docs/P9-09_questions_probables.md` | Questions probables de l'enseignant |
| `docs/P9-10_plan_b.md` | Plan B pour la démonstration |
| `docs/P9-11_repetitions.md` | Répéter la présentation deux fois |
| `docs/P9-12_finalisation_depot.md` | Finaliser le dépôt de code |
| `docs/P9-13_retours_presentation.md` | Intégrer les retours de la présentation |
| `docs/P9-14_recommandations_operationnelles.md` | Détailler les recommandations opérationnelles |
| `docs/P9-15_ethique_variables.md` | Justifier l'usage éthique des variables dans le score |
| `docs/P9-16_relecture_finale.md` | Relire et finaliser le rapport final |
| `docs/P9-17_diapositives_resultats.md` | Compléter les diapositives avec les résultats |
| `docs/T-12_remise_livrable_4.md` | Remettre le livrable 4 (analyse exploratoire, rapport, présentation) |
| `docs/T-13_remise_rapport_final.md` | Remettre le rapport final avec recommandations opérationnelles |

## Livrables

| Livrable                                            | Date        |
| --------------------------------------------------- | ----------- |
| Phases du projet et tâches granulaires              | 5 octobre   |
| Diagnostic, nettoyage et transformation des données | 9 novembre  |
| Analyse exploratoire, rapport et présentation       | 7 décembre  |
| Rapport final avec recommandations opérationnelles  | 14 décembre |

### Livrable du 9 novembre : diagnostic, nettoyage et transformation

| Partie                                | Notebook                                      | Documents                                                             |
| ------------------------------------- | --------------------------------------------- | --------------------------------------------------------------------- |
| Exploration des fichiers (P2-01)      | `notebooks/01_exploration_donnees.ipynb`      | `docs/P1-04_dictionnaire_donnees.md`                                  |
| Diagnostic de la qualité (phase 2)    | `notebooks/02_diagnostic_qualite.ipynb`       | `docs/P2-16_rapport_diagnostic.md`, `docs/P2-17_etiquettes_fraude.md` |
| Nettoyage et transformation (phase 3) | `notebooks/03_nettoyage_transformation.ipynb` | `docs/P3-01_...` à `docs/P3-11_...`                                   |
| Synthèse des transformations          |                                               | `docs/P3-12_journal_transformations.md`                               |

### Livrable du 7 décembre : analyse exploratoire, rapport et présentation

| Partie | Notebook | Documents |
| --- | --- | --- |
| Table d'analyse et indicateurs (phase 4) | `notebooks/04_table_analyse.ipynb` | `docs/P4-01_...` à `docs/P4-10_...` |
| Profils de clients, Q1 (phase 5) | `notebooks/05_profils_clients.ipynb` | `docs/P5-01_...` à `docs/P5-08_section_profils.md` |
| Comportements, Q2 et Q6 (phase 6) | `notebooks/06_analyse_exploratoire.ipynb` | `docs/P6-01_...` à `docs/P6-09_section_comportements.md` |
| Détection, Q3 à Q5 (phase 7) | `notebooks/07_detection_anomalies.ipynb` | `docs/P7-01_...` à `docs/P7-11_...` |
| Tableau de bord, Q7 (phase 8) | `notebooks/08_tableau_de_bord.ipynb`, `dashboard/` | `docs/P8-01_...` à `docs/P8-11_guide_utilisation.md` |
| Rapport et présentation (phase 9) | `notebooks/09_recommandations.ipynb` | `docs/P9-01_...` à `docs/P9-17_...`, `docs/T-12_remise_livrable_4.md` |

### Livrable du 14 décembre : rapport final avec recommandations opérationnelles

| Partie | Documents |
| --- | --- |
| Recommandations opérationnelles | `docs/P9-14_recommandations_operationnelles.md` |
| Retours de la présentation et relecture finale | `docs/P9-13_retours_presentation.md`, `docs/P9-16_relecture_finale.md` |
| Dépôt finalisé | `docs/P9-12_finalisation_depot.md` |
| Liste de remise | `docs/T-13_remise_rapport_final.md` |
