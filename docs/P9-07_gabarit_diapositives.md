# P9-07 : Créer le gabarit et les diapositives de structure

Critère de fin de P9-07 : gabarit et diapositives de structure prêts. Les diapositives de résultats sont décrites dans `docs/P9-17_diapositives_resultats.md`. La présentation est exportée en PowerPoint ou en PDF pour la remise (T-12) et pour le plan B (P9-10).

## Le gabarit

Le gabarit applique la charte graphique (P1-10) aux diapositives.

| Élément                            | Choix                                                                                        |
| ---------------------------------- | -------------------------------------------------------------------------------------------- |
| Format                             | 16:9 (1920 × 1080 px), marges de 128 px                                                      |
| Titres                             | Space Grotesk, gras, bleu nuit `#0f2340`                                                     |
| Texte                              | Inter, presque noir `#14181f` ; texte secondaire gris `#4a4f57`                              |
| Fond des diapositives de contenu   | Crème `#f7f6f2`                                                                              |
| Fond de la couverture et de la fin | Bleu nuit `#0f2340`, texte clair                                                             |
| Fond de la diapositive du score    | Bleu clair `#e8f0fb`, pour marquer le passage à la détection                                 |
| Couleur principale                 | Bleu `#2a78d6` (couleur 1 de la charte)                                                      |
| Couleur d'alerte                   | Orange `#eb6834` (couleur 2 de la charte) : seuil, chiffres à retenir                        |
| Chiffres clés                      | Grand chiffre, courte étiquette dessous, trait de couleur au-dessus                          |
| Visuels                            | Images de `docs/figures/`, déjà conformes à la charte                                        |
| Source                             | Une ligne en bas de la diapositive : fichier, notebook ou section d'où viennent les chiffres |
| Notes de l'orateur                 | Sous chaque diapositive : qui parle (P9-08) et ce qu'il faut dire                            |

## Les règles d'écriture

- Un seul message par diapositive, écrit en titre sous forme de phrase.
- Un visuel au plus par diapositive.
- Nombres à la française (13 305 915 ; 0,150 %).
- Chiffres arrondis à l'oral ; les chiffres exacts restent dans le rapport.
- Pas de paragraphe : des blocs courts, chacun avec un titre en gras.

## Les diapositives de structure

Elles posent le problème, les données et la méthode. Les diapositives de résultats se placent entre elles (P9-17).

| N°  | Partie (P9-06)         | Titre (message)                                                 | Contenu                                                                                                                     |
| --- | ---------------------- | --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| 1   | Problème               | Détection de fraude bancaire                                    | Projet, date du livrable, noms de l'équipe                                                                                  |
| 2   | Problème               | Quelles transactions la banque doit-elle contrôler en premier ? | Quatre chiffres clés : 13,3 M de transactions, 2 000 clients et 6 146 cartes, 109 codes de commerçants, 0 colonne de fraude |
| 3   | Problème               | Sept questions de recherche                                     | Q1 à Q7, avec la phase qui répond à chaque question                                                                         |
| 4   | Données et préparation | Des données fiables, sans perdre une seule ligne                | Ce qui a été corrigé, signalé ou retiré ; étiquettes de fraude (67 % des transactions, dont 0,150 % de fraudes)             |
| 9   | Score de risque        | 16 indicateurs pour repérer l'inhabituel                        | Six groupes d'indicateurs et leur vérification                                                                              |
| 10  | Score de risque        | Un score de risque de 0 à 100                                   | Règles métier, Isolation Forest, seuil de 1 %                                                                               |
| 18  | Questions              | Questions ?                                                     | Ouverture aux questions (P9-09)                                                                                             |

## À faire par l'équipe

- Valider le gabarit et l'ordre des diapositives.
- Exporter la présentation en PowerPoint ou en PDF et la remettre avec le rapport (T-12).
