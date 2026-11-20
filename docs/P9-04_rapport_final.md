# P9-04 : Assembler le rapport final

Critère de fin de P9-04 : rapport complet. Le rapport complet, mis en page pour la remise, est exporté en Word ou en PDF. Cette page donne son plan, son résumé d'une page et son glossaire. Les sections viennent des documents des phases, harmonisés.

## Plan du rapport

| Partie                     | Contenu                                                      | Source                                                      |
| -------------------------- | ------------------------------------------------------------ | ----------------------------------------------------------- |
| Résumé                     | Une page : problème, méthode, résultats, recommandations     | Cette page                                                  |
| 1. Contexte et questions   | Objectif de la banque, questions Q1 à Q7, lecture de Q3      | README, P1-02                                               |
| 2. Données et qualité      | Les cinq fichiers, problèmes trouvés et règles de traitement | `P2-16_rapport_diagnostic.md`, `P2-17_etiquettes_fraude.md` |
| 3. Préparation des données | Nettoyage, table d'analyse, journal des transformations      | `P3-12_journal_transformations.md`, `P4-01` à `P4-10`       |
| 4. Indicateurs             | Catalogue des 16 indicateurs                                 | `P4-09_catalogue_indicateurs.md`                            |
| 5. Profils de clients (Q1) | Méthode, quatre profils, limites                             | `P5-08_section_profils.md`                                  |
| 6. Comportements (Q2, Q6)  | Huit constats avec leurs visuels                             | `P6-09_section_comportements.md`                            |
| 7. Détection (Q3, Q4, Q5)  | Score, validation, tests, variante avec étiquettes           | `P7-10_section_detection.md`                                |
| 8. Tableau de bord (Q7)    | Utilisateurs, pages, vérification, guide                     | `P8-01`, `P8-03` à `P8-08`, `P8-11`                         |
| 9. Réponses aux questions  | Une réponse chiffrée par question                            | `P9-01_reponses_questions.md`                               |
| 10. Recommandations        | Douze recommandations reliées aux résultats                  | `P9-02_recommandations.md`                                  |
| 11. Éthique                | Genre et âge exclus, vérification chiffrée                   | `P9-15_ethique_variables.md`                                |
| 12. Limites                | Données et méthodes                                          | `P9-03_limites.md`                                          |
| Glossaire                  | Termes techniques                                            | Cette page                                                  |

Version du 14 décembre : ajouter les recommandations opérationnelles (`P9-14_recommandations_operationnelles.md`) et les corrections après la présentation (P9-13).

## Résumé d'une page

**Le problème.** Une banque veut lutter contre la fraude. Elle dispose de 13 305 915 transactions de janvier 2010 à octobre 2019, de 2 000 clients et de 6 146 cartes, mais d'aucune colonne qui indique la fraude.

**Les données.** Le diagnostic a trouvé des montants et des dates en texte, des lieux mélangés, des erreurs combinées et des informations clients datées de février 2020. Tout a été corrigé ou signalé, sans perdre une seule ligne. Les étiquettes de fraude fournies par l'enseignant couvrent 67 % des transactions (0,150 % de fraudes).

**Les profils (Q1).** Les clients actifs forment quatre profils stables : clients courants (686), clients aisés et voyageurs (321), acheteurs en ligne très actifs (138) et clients sans dette (63).

**Les comportements (Q2, Q6).** De petits achats fréquents (médiane de 31,92 $), de jour, sur place aux États-Unis (87,58 %), surtout en transport et en alimentation. L'activité monte jusqu'en 2015, et la puce remplace d'un coup la bande magnétique en 2015.

**La détection (Q3, Q4, Q5).** Un score de risque de 0 à 100 combine 13 règles métier et Isolation Forest. Au seuil de 1 %, il signale 37,1 transactions par jour, avec une raison écrite pour chacune. Le risque est le plus élevé à l'étranger (19,437 % de transactions signalées), en voyage et en industrie, en ligne et la nuit. Évalué avec les étiquettes, il trouve 23,9 fois plus de fraudes que le hasard, mais il rate environ trois fraudes sur quatre. Un modèle supervisé, possible grâce aux étiquettes, fait mieux (64,49 % des fraudes de 2019 trouvées au seuil de 0,5 %).

**Le tableau de bord (Q7).** Quatre pages Streamlit, avec des filtres et la liste priorisée. 62 chiffres vérifiés, aucun écart.

**Les recommandations.** Utiliser la liste priorisée chaque matin au seuil de 1 % ; enregistrer le résultat de chaque contrôle pour créer la colonne de fraude qui manque ; retirer la règle des rafales, qui ne signale pas la fraude ; renforcer les règles de lieu et de nouveauté ; recalculer le seuil chaque année ; ne jamais utiliser le genre ni l'âge, et suivre les fausses alertes par âge.

## Glossaire

| Terme                            | Définition                                                                                                                       |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **ARI (indice de Rand ajusté)**  | Mesure de la ressemblance entre deux découpages en groupes : 1 = identiques, 0 = au hasard.                                      |
| **Étiquette de fraude**          | Information « fraude » ou « pas de fraude » donnée pour une transaction (`fraud_labels.json`).                                   |
| **Faux positif (fausse alerte)** | Transaction signalée qui n'est pas une fraude.                                                                                   |
| **Isolation Forest**             | Méthode qui repère les transactions atypiques : plus une transaction s'isole en peu de coupes au hasard, plus elle est atypique. |
| **K-means**                      | Méthode qui regroupe les clients qui se ressemblent en k groupes.                                                                |
| **Khi-deux (test du)**           | Test qui vérifie si deux variables catégorielles sont liées.                                                                     |
| **Mann-Whitney (test de)**       | Test qui compare les valeurs d'une variable numérique entre deux groupes.                                                        |
| **MCC**                          | Code de catégorie du commerçant (Merchant Category Code), regroupé en 12 familles.                                               |
| **Montant habituel**             | Médiane des achats précédents d'un client.                                                                                       |
| **Parquet**                      | Format de fichier léger qui garde les types des colonnes.                                                                        |
| **Précision**                    | Part de vraies fraudes parmi les transactions signalées.                                                                         |
| **Rappel**                       | Part des fraudes qui sont signalées.                                                                                             |
| **Règle métier**                 | Condition simple qui traduit un signal de fraude (exemple : 2 échecs d'authentification en 24 heures).                           |
| **Score de risque**              | Note de 0 à 100 : moitié règles métier, moitié anomalie. Ce n'est pas une probabilité de fraude.                                 |
| **Score de silhouette**          | Mesure de la séparation des groupes de K-means, de -1 à 1.                                                                       |
| **Seuil de signalement**         | Part des transactions les plus risquées qui sont signalées (0,5 %, 1 % ou 2 %).                                                  |
| **Taille d'effet**               | Mesure de l'importance d'un écart, indépendante du nombre de lignes (V de Cramér, corrélation rang-bisériale).                   |
| **V de Cramér**                  | Taille d'effet du khi-deux, de 0 (aucun lien) à 1 (lien parfait).                                                                |
