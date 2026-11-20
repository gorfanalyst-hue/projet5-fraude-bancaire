# P8-11 : Guide d'utilisation du tableau de bord

Statut : à relire par un membre extérieur à la phase 8 (critère de fin de P8-11).

## Ouvrir le tableau de bord

1. Exécuter une fois `notebooks/08_tableau_de_bord.ipynb` : il crée les tables de `data/dashboard/`.
2. Depuis la racine du dépôt, dans un terminal : `streamlit run dashboard/app.py`.
3. Le navigateur s'ouvre sur `http://localhost:8501`. Pour arrêter : `Ctrl + C` dans le terminal.

## Les filtres (barre de gauche)

- **Années** : glisser les deux poignées. Une seule année : mettre les deux poignées sur la même année.
- **Seuil de signalement** : 0,5 %, 1 % ou 2 % des transactions les plus risquées. Un seuil plus haut signale plus de transactions, donc plus de travail de contrôle et plus de fausses alertes.
- **Canaux de paiement** : bande magnétique, puce, en ligne.

Les filtres s'appliquent à toutes les pages. Exception : les clients actifs et les clients signalés comptent tous les canaux.

## Les pages

| Page                       | À quoi elle sert                                | Comment la lire                                                                                                                                                                                                                                                                                    |
| -------------------------- | ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Vue d'ensemble**         | Volume d'activité et nombre de signalements     | Huit chiffres clés en haut. La courbe montre l'évolution par mois (choisir la mesure au-dessus). Le second graphique montre la part de chaque canal par année. Survoler un point affiche sa valeur.                                                                                                |
| **Profils de clients**     | Comprendre les groupes de clients               | Le visuel montre chaque profil : la couleur dit si le profil est au-dessus (rouge) ou en dessous (bleu) de la moyenne, le texte donne la valeur médiane. Choisir un profil pour voir sa fiche. Le graphique compare les taux de signalement ; la ligne pointillée est le taux de tous les profils. |
| **Lieux et catégories**    | Où et dans quels commerces les clients achètent | Trois chiffres : part des transactions sur place, en ligne et à l'étranger. Puis les 15 États (par nombre ou par taux de signalement), les 10 pays étrangers et les familles de commerçants.                                                                                                       |
| **Transactions signalées** | Liste de travail de l'analyste                  | La liste est triée du score le plus haut au plus bas. Filtrer par client, famille, raison ou score minimal. La colonne « raison principale » explique le signalement. Le bouton télécharge la liste filtrée en CSV.                                                                                |

## Lire les indicateurs

- **Score de risque (0 à 100)** : moitié règles métier, moitié anomalie (Isolation Forest). Plus il est haut, plus la transaction est inhabituelle. Ce n'est pas une probabilité de fraude.
- **Taux de signalement** : transactions signalées divisées par toutes les transactions de la sélection.
- **Raison principale** : la règle déclenchée qui pèse le plus (exemple : « R03 : montant au moins 10 fois plus élevé que d'habitude »). « Comportement atypique » veut dire qu'aucune règle n'est déclenchée, mais que la transaction ressemble peu aux autres.
- **Précision** (encadré bleu de la dernière page) : part de vraies fraudes parmi les transactions signalées, mesurée sur les transactions étiquetées.
- **Rappel** : part des fraudes qui sont signalées.

## En cas de problème

| Message ou symptôme                              | Solution                                                           |
| ------------------------------------------------ | ------------------------------------------------------------------ |
| « Les tables du tableau de bord sont absentes »  | Exécuter `notebooks/08_tableau_de_bord.ipynb`.                     |
| `streamlit` n'est pas reconnu                    | `pip install -r requirements.txt` dans l'environnement du projet.  |
| « Aucune transaction ne correspond aux filtres » | Élargir les années, retirer un filtre ou baisser le score minimal. |
| Le numéro de client est refusé                   | Écrire seulement des chiffres (exemple : 1098).                    |
