# P9-10 : Plan B pour la démonstration

Critère de fin de P9-10 : plan B testé. Le tableau de bord tourne sur un ordinateur portable : si l'ordinateur, Python ou le projecteur pose problème, la démonstration doit continuer.

## Ce qui est prêt

| Élément                           | Où                                                                                   | Utilité                                              |
| --------------------------------- | ------------------------------------------------------------------------------------ | ---------------------------------------------------- |
| Captures d'écran des quatre pages | `docs/figures/P8-04_page_vue_ensemble.png` à `P8-07_page_transactions_signalees.png` | Montrer les pages sans lancer l'application          |
| Diapositives de démonstration     | Dans la présentation, après la partie « Score de risque »                            | Les captures sont déjà dans les diapositives         |
| Copie locale des tables           | `data/dashboard/` (8,8 Mo)                                                           | Lancer le tableau de bord sans refaire les notebooks |
| Guide                             | `docs/P8-11_guide_utilisation.md`                                                    | Rappel des clics de la démonstration                 |

## Avant la présentation (la veille)

1. Copier sur une clé USB : le dossier du projet **avec** `data/dashboard/` et `docs/figures/`, et la présentation exportée en PDF.
2. Sur l'ordinateur de démonstration, lancer `streamlit run dashboard/app.py` et faire le scénario complet une fois.
3. Vérifier que le PDF de la présentation s'ouvre sans Internet.

## Scénario de démonstration (3 minutes)

1. **Vue d'ensemble** : lire les chiffres clés, puis changer le seuil de 1 % à 2 % (les signalements doublent).
2. **Profils de clients** : choisir « Acheteurs en ligne très actifs » et montrer leur taux de signalement.
3. **Lieux et catégories** : classer les États par taux de signalement ; montrer voyage et industrie dans le tableau des familles.
4. **Transactions signalées** : entrer un numéro de client, montrer les 10 transactions les plus risquées et leur raison, puis télécharger la liste.

## Si quelque chose ne marche pas

| Problème                                                         | Solution                                                                |
| ---------------------------------------------------------------- | ----------------------------------------------------------------------- |
| L'application ne se lance pas                                    | Montrer les captures d'écran dans les diapositives                      |
| L'ordinateur ne s'allume pas ou ne se connecte pas au projecteur | Présentation en PDF depuis la clé USB, sur un autre ordinateur          |
| L'application est lente                                          | Rester sur la page en cours ; passer aux captures pour les autres pages |

## Test du plan B (à remplir)

| Date | Testé par | Application lancée depuis la clé | PDF ouvert sans Internet | Remarques |
| ---- | --------- | -------------------------------- | ------------------------ | --------- |
|      |           |                                  |                          |           |
