# P8-08 : Vérifier les chiffres du tableau de bord

## Pourquoi cette étape ?

Un chiffre faux dans un tableau de bord fait perdre confiance dans tout le reste. Chaque chiffre affiché doit être égal au résultat des notebooks, et les filtres doivent changer les chiffres comme prévu.

Le critère de fin du ticket est : **aucun écart constaté**.

## Où est le code ?

`notebooks/08_tableau_de_bord.ipynb`, section P8-08.

## La méthode

1. **Calcul direct.** Chaque chiffre est recalculé à partir de la table d'analyse et des scores (13 millions de lignes), sans passer par les tables du tableau de bord.
2. **Calcul du tableau de bord.** Le même chiffre est obtenu avec les fonctions de `dashboard/calculs.py`, celles que les pages utilisent.
3. **Comparaison.** L'écart doit être nul (à la précision des calculs près).
4. **Lecture dans l'application.** La page « Vue d'ensemble » est lancée par un test automatique de Streamlit (`AppTest`), et les chiffres affichés sont lus et comparés.

## Ce qui est vérifié

| Contrôle                                                                                                                        | Nombre |
| ------------------------------------------------------------------------------------------------------------------------------- | ------ |
| Chiffres clés (transactions, achats, signalées, part en ligne, clients actifs, clients signalés) pour 4 combinaisons de filtres | 24     |
| Transactions et signalées de chaque famille de commerçants                                                                      | 24     |
| Transactions des 5 premiers États                                                                                               | 5      |
| Signalées de chaque profil                                                                                                      | 5      |
| Taille de la liste des signalées à chaque seuil                                                                                 | 3      |
| Les 10 transactions les plus risquées d'un client (mêmes identifiants)                                                          | 1      |
| **Total**                                                                                                                       | **62** |

Combinaisons de filtres : toute la période au seuil de 1 % ; l'année 2015 au seuil de 0,5 % ; le canal en ligne au seuil de 2 % ; puce et bande magnétique de 2012 à 2018 au seuil de 1 %.

## Résultats obtenus

- **62 contrôles, 0 écart.**
- Chiffres lus dans l'application (filtres par défaut) :

| Chiffre                | Affiché    | Attendu    |
| ---------------------- | ---------- | ---------- |
| Transactions           | 13 305 915 | 13 305 915 |
| Transactions signalées | 133 075    | 133 075    |
| Clients actifs         | 1 219      | 1 219      |

**Critère de fin validé.**

## À refaire

Après chaque correction du tableau de bord (P8-10), relancer le notebook 08 : la section P8-08 refait tous les contrôles en une minute environ.
