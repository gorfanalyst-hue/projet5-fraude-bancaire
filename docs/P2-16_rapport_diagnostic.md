# P2-16 : Rapport de diagnostic de la qualité des données

Statut : à valider par l'équipe (critère de fin de P2-16). Ce rapport deviendra la section « Données » du rapport final.

Tous les chiffres viennent des sorties de `notebooks/02_diagnostic.ipynb`, sauf la ligne P3-01, qui vient de `docs/01_chargement_donnees.md`.

## Les données contrôlées

| Table | Lignes | Colonnes |
|---|---|---|
| `transactions_data.csv` | 13 305 915 | 12 |
| `cards_data.csv` | 6 146 | 13 |
| `users_data.csv` | 2 000 | 14 |
| `mcc_codes.json` | 109 | 2 |
| `fraud_labels.json` | 8 914 963 | 2 |

## Contrôles sans problème

- **Liens entre les tables (P2-02) :** 0 ligne orpheline pour les quatre liens (transactions vers clients, cartes et codes MCC ; cartes vers clients).
- **Titulaire de la carte (P2-03) :** le client de la transaction est toujours le titulaire de la carte.
- **Continuité (P2-15) :** les 118 mois de janvier 2010 à octobre 2019 sont présents. Le plus faible est février 2010 (93 470 transactions), le plus fort décembre 2015 (119 396).
- **Valeurs manquantes :** aucune dans `cards` et `users`.
- **Codes d'États (P2-08) :** aucun code à deux lettres inconnu.
- **Dates des cartes (P2-11) :** aucune carte n'expire avant l'ouverture du compte.
- **Étiquettes de fraude (P2-17) :** aucun identifiant en double, aucun identifiant absent des transactions.

## Problèmes et règles de traitement

| Problème | Ampleur | Conséquence pour l'analyse | Règle | Ticket |
|---|---|---|---|---|
| Montants et dates stockés en texte | `amount`, `credit_limit`, `per_capita_income`, `yearly_income`, `total_debt`, `expires`, `acct_open_date` | Aucun calcul possible | Convertir en nombres et en dates | P3-02, P3-03 (fait) |
| Type `category` perdu au chargement | 4 colonnes des transactions ; mémoire pandas de 4 321,9 Mo au lieu de 1 371,0 Mo | Notebooks lents et lourds | Remettre le type `category` après la lecture par morceaux | P3-01 (fait) |
| `merchant_state` manquant | 1 563 700, tous des achats en ligne | Aucune : manquant expliqué | Valeur explicite « ONLINE » | P3-07 (fait) |
| `zip` manquant | 1 652 706 : 1 563 700 en ligne, 89 006 à l'étranger | Aucune : manquant expliqué | Valeurs explicites « ONLINE » et « FOREIGN_NO_ZIP » | P3-07 (fait) |
| États et pays mélangés dans `merchant_state` | 52 codes américains, 147 noms de pays | Lieu mal lu | Colonnes séparées `merchant_country` et `merchant_state_clean` | P3-07 (fait) |
| Ville « ONLINE » avec le canal « Chip Transaction » | 5 788 transactions | Canal incertain | Gardées, signalées par `online_channel_mismatch` | P3-07 (fait) |
| Erreurs combinées dans `errors` | 211 393 transactions, 7 types | Comptage difficile | Une colonne binaire par type | P3-06 (fait) |
| Montants négatifs | 660 049 transactions ; minimum -500,0 | Fausseraient les moyennes de dépenses | Gardés, signalés par `is_negative_amount` | P3-08 |
| Montants nuls | 10 639 transactions | Même effet | Gardés, signalés par `is_zero_amount` | P3-08 |
| Revenus suspects | 8 revenus annuels inférieurs à 1 000 ; 15 revenus par habitant nuls | Profils de clients faussés | Signalés par `suspicious_income` | P3-08 |
| Limites de crédit nulles | 31 cartes | Rapport dépenses / limite impossible | Signalées par `zero_credit_limit` | P3-08 |
| Transactions répétées sans erreur | 15 groupes de deux lignes (sur 100 groupes répétés) | Double débit possible | Seconde ligne signalée par `is_repeated` | P3-08 |
| Colonne à valeur unique | `card_on_dark_web` | Aucune information | Colonne retirée | P3-09 |
| Colonnes sensibles | `card_number`, `cvv`, `address` | Confidentialité | Colonnes retirées | P3-09 |
| Informations des clients et des cartes datées de février 2020 | Âge calculé à la fin de février 2020 ; 1 189 cartes ouvertes après la dernière transaction | Âge faux pour les transactions anciennes | Âge recalculé à la date de chaque transaction | P4-03 |
| Transactions hors de la période de validité de la carte | 309 transactions avant l'ouverture (264 cartes) ; 83 après l'expiration (35 cartes) | Signal possible de fraude | Gardées ; indicateur créé en phase 4 | Phase 4 |
| Clients et cartes sans transaction | 781 clients sur 2 000 ; 2 075 cartes sur 6 146 | Profils de comportement vides | Gardés ; exclus des profils de comportement | P5-01, P5-02 |
| Étiquettes de fraude partielles | 8 914 963 transactions étiquetées (67,0 %) ; 13 332 fraudes (0,150 %) | Q3 et Q4 se limitent à la partie étiquetée | Analyses de la fraude sur la partie étiquetée | Phase 7 |

## Cas gardés sans règle

| Cas | Ampleur | Raison |
|---|---|---|
| Dette totale nulle | 102 clients | Situation possible |
| Revenu par habitant supérieur au revenu annuel | 34 clients | Pas de règle sûre pour corriger |
| Changement de PIN après l'année d'expiration | 268 cartes | Pas d'effet sur les analyses prévues |
| Montants élevés | Quantile 99,9 % : 891,54 ; maximum : 6 820,2 | Aucun signe d'erreur |
| Montants entiers | 80,6 % des transactions en services professionnels et financiers | Liés au type de commerce |
