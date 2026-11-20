# P9-15 : Justifier l'usage éthique des variables dans le score

Critère de fin de P9-15 : décision écrite et vérification chiffrée. Les chiffres viennent de `notebooks/09_recommandations.ipynb`.

## La décision

**Le genre et l'âge ne sont pas utilisés dans le score de risque (P7-03), ni dans le modèle supervisé (P7-08), ni dans la formation des profils (P5-03).**

Raisons :

- **Équité** : signaler une transaction parce que le client est une femme ou parce qu'il a 25 ans traiterait des clients différemment pour ce qu'ils sont, pas pour ce qu'ils font.
- **Loi** : le genre et l'âge sont des motifs de discrimination protégés (par exemple, la Loi canadienne sur les droits de la personne et l'Equal Credit Opportunity Act aux États-Unis).
- **Utilité** : la fraude dépend du comportement de la carte (lieu, nouveauté, montant), pas de la personne. Les tests de P7-05 le confirment : le genre (V de Cramér de 0,002) et l'âge (corrélation de -0,035) ne distinguent pas les transactions signalées.

Le genre et l'âge restent dans les données, mais seulement pour **contrôler** que le score ne désavantage personne.

## La vérification chiffrée (seuil de 1 %)

| Groupe          | Taux de signalement | Fausses alertes | Rappel   |
| --------------- | ------------------- | --------------- | -------- |
| Femmes          | 1,016 %             | 0,987 %         | 22,959 % |
| Hommes          | 0,983 %             | 0,951 %         | 25,008 % |
| Moins de 30 ans | 1,108 %             | 1,085 %         | 24,905 % |
| 30 à 44 ans     | 1,056 %             | 1,029 %         | 24,541 % |
| 45 à 59 ans     | 0,979 %             | 0,945 %         | 23,600 % |
| 60 à 74 ans     | 0,979 %             | 0,947 %         | 22,198 % |
| 75 ans et plus  | 0,771 %             | 0,729 %         | 25,369 % |

- **Fausses alertes** : part des transactions étiquetées « pas de fraude » qui sont quand même signalées.
- **Rappel** : part des fraudes signalées dans le groupe.
- **Rapport le plus bas / le plus haut du taux de signalement** : 0,97 pour le genre, 0,70 pour l'âge. Un rapport sous 0,8 mérite une alerte (règle des quatre cinquièmes).

## Conclusion

- **Genre : aucun désavantage.** Les taux sont presque égaux (rapport de 0,97).
- **Âge : un écart à surveiller.** Les clients de moins de 30 ans reçoivent plus de fausses alertes que les clients de 75 ans et plus (1,085 % contre 0,729 %, rapport de 0,70). L'âge n'est pas dans le score : l'écart vient de comportements plus fréquents chez les jeunes et repérés par les règles. Le rappel, lui, est le même pour tous les âges.
- La taille d'effet reste négligeable (V de Cramér de 0,008), mais l'écart touche directement l'expérience des jeunes clients (achats bloqués ou contrôlés).

## Ce qui est recommandé (R-12 de P9-02)

- Ne jamais ajouter le genre ni l'âge au score, même si cela améliorait la précision.
- Suivre chaque trimestre le rapport des fausses alertes par groupe d'âge. S'il reste sous 0,8, chercher les règles qui le causent et les corriger, plutôt que d'utiliser l'âge.
