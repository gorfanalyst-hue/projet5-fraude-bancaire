# P7-04 : Valider le score

## Pourquoi cette étape ?

Un score n'a de valeur que s'il est utilisable et cohérent. Trois contrôles :

- **la charge de travail** : combien de transactions et de clients sont signalés selon le seuil (0,5 %, 1 % ou 2 %) ;
- **la stabilité** : le taux de signalement change-t-il beaucoup d'une année à l'autre ?
- **la revue manuelle** : 50 transactions signalées sont lues une par une. Le signalement est-il compréhensible et crédible ?

Le critère de fin du ticket est : **grille de revue remplie et conclusion**.

## Où est le code ?

- `src/detection.py` : `threshold_summary`, `yearly_flag_rates` et `review_sample`.
- `notebooks/07_detection_anomalies.ipynb` : section P7-04. La grille vide est exportée dans `data/resultats/P7-04_grille_revue.csv` ; la grille remplie est ci-dessous.

## Charge de travail selon le seuil

| Seuil | Score minimal | Transactions signalées | Signalements par jour | Clients signalés | Cartes signalées |
| --- | --- | --- | --- | --- | --- |
| 0,5 % | 68,42 | 66 562 | 18,5 | 1 219 (100 %) | 3 819 |
| 1 % | 62,42 | 133 075 | 37,1 | 1 219 (100 %) | 3 950 |
| 2 % | 59,72 | 266 128 | 74,1 | 1 219 (100 %) | 4 012 |

Sur dix ans, tous les clients actifs ont au moins une transaction signalée, quel que soit le seuil. Passer de 1 % à 2 % double la charge de travail (de 37,1 à 74,1 signalements par jour).

## Stabilité d'une année à l'autre

| Année | Seuil 0,5 % | Seuil 1 % | Seuil 2 % |
| --- | --- | --- | --- |
| 2010 | 1,113 % | 1,683 % | 3,661 % |
| 2011 | 0,670 % | 1,185 % | 2,359 % |
| 2012 | 0,533 % | 1,023 % | 1,986 % |
| 2013 | 0,495 % | 0,985 % | 1,916 % |
| 2014 | 0,422 % | 0,908 % | 1,784 % |
| 2015 | 0,422 % | 0,918 % | 1,756 % |
| 2016 | 0,381 % | 0,874 % | 1,687 % |
| 2017 | 0,342 % | 0,849 % | 1,663 % |
| 2018 | 0,345 % | 0,811 % | 1,648 % |
| 2019 | 0,330 % | 0,825 % | 1,691 % |

Écart relatif entre les années (écart-type / moyenne) : 0,47 au seuil de 0,5 %, 0,26 au seuil de 1 %, 0,31 au seuil de 2 %.

Le score signale deux fois plus en 2010 qu'en 2019. Explication probable : au début des historiques, les clients ont encore beaucoup de « premières fois » (nouveaux commerçants, nouvelles catégories), que la règle R08 et Isolation Forest repèrent. À partir de 2013, le taux au seuil de 1 % reste entre 0,811 % et 0,985 %.

## Revue manuelle de 50 transactions signalées

**Méthode.** 50 transactions tirées au hasard parmi les 133 075 signalées au seuil de 1 % (graine 0). Pour chacune, la « lecture » résume le contexte : canal, famille, montant, rapport au montant habituel, date, activité de la carte, échecs et premières fois. L'avis est donné avec trois critères :

- **plausible** : au moins deux signaux indépendants d'une carte volée ou copiée (montant très inhabituel et nouveau commerçant, achat à l'étranger d'un montant inhabituel, échec sur un achat plus élevé que d'habitude) ;
- **douteux** : un seul signal, faible ou explicable (petit achat en ligne avec un échec, premier achat à l'étranger d'un petit montant) ;
- **faux positif probable** : le signal s'explique par un comportement normal (rafale d'achats courants au montant habituel, remboursement).

La revue a été faite à partir des colonnes du notebook, sans les étiquettes de fraude. Elle reste à confirmer par un membre de l'équipe.

| N° | Transaction | Score | Règles | Lecture | Avis | Commentaire |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 15904899 | 87,3 | R04, R05, R10 | en ligne, Transport, carburant et automobile ; 75,02 $ ; 1,4 fois le montant habituel (54,41 $) ; 2015-04-04 16:47 ; 6 transactions de la carte dans l'heure, 15 en 24 h | douteux | Rafale en ligne au montant habituel : à surveiller. |
| 2 | 15693460 | 81,2 | R03, R08 | bande magnétique, Transport, carburant et automobile ; 458,15 $ ; 112,3 fois le montant habituel (4,08 $) ; 2015-02-18 06:53 ; 0 transactions de la carte dans l'heure, 4 en 24 h ; première fois : commerçant, catégorie | plausible | Montant inhabituel chez un nouveau commerçant, dans une nouvelle catégorie. |
| 3 | 9797474 | 81,2 | R03, R08 | bande magnétique, Industrie et fabrication ; 867,60 $ ; 71,8 fois le montant habituel (12,09 $) ; 2011-07-14 15:16 ; première fois : commerçant, catégorie | plausible | Montant inhabituel chez un nouveau commerçant, dans une nouvelle catégorie. |
| 4 | 14251992 | 81,2 | R03, R08 | bande magnétique, Transport, carburant et automobile ; 327,17 $ ; 29,0 fois le montant habituel (11,27 $) ; 2014-04-10 07:57 ; première fois : commerçant, catégorie | plausible | Montant inhabituel chez un nouveau commerçant, dans une nouvelle catégorie. |
| 5 | 16200267 | 81,2 | R04, R05 | puce, Alimentation ; -69,00 $ ; 2015-06-07 09:45 ; 5 transactions de la carte dans l'heure, 16 en 24 h | faux positif probable | Remboursement pendant une journée chargée : rien d'anormal. |
| 6 | 13254009 | 80,5 | R03, R09, R11 | bande magnétique, Voyage et hébergement ; 453,00 $ ; 21,1 fois le montant habituel (21,52 $) ; 2013-09-03 01:10 ; 0 transactions de la carte dans l'heure, 2 en 24 h ; première fois : commerçant | plausible | Montant très éloigné des habitudes du client. |
| 7 | 10845684 | 74,9 | R08, R10, R11 | en ligne, Voyage et hébergement ; 481,00 $ ; 12,4 fois le montant habituel (38,78 $) ; 2012-03-12 10:38 ; 0 transactions de la carte dans l'heure, 3 en 24 h ; première fois : commerçant, catégorie | plausible | Montant inhabituel chez un nouveau commerçant, dans une nouvelle catégorie. |
| 8 | 11206846 | 74,8 | R08, R10, R11 | en ligne, Voyage et hébergement ; 185,00 $ ; 5,5 fois le montant habituel (33,42 $) ; 2012-06-02 11:52 ; 0 transactions de la carte dans l'heure, 1 en 24 h ; première fois : commerçant, catégorie | douteux | Nouveau commerçant, montant modéré. |
| 9 | 15660650 | 74,6 | R02, R09, R10 | en ligne, Loisirs, culture et divertissement ; 17,66 $ ; 0,3 fois le montant habituel (50,92 $) ; 2015-02-11 00:59 ; 1 transactions de la carte dans l'heure, 2 en 24 h ; 0 échecs d'authentification en 24 h, échec sur cette transaction | douteux | Échec sur un achat proche des habitudes : erreur de saisie possible. |
| 10 | 18742487 | 74,4 | R04, R11 | puce, Alimentation ; 50,00 $ ; 0,9 fois le montant habituel (58,33 $) ; 2016-12-02 08:56 ; 5 transactions de la carte dans l'heure, 11 en 24 h | faux positif probable | Rafale d'achats courants, proche du montant habituel. |
| 11 | 12628972 | 74,1 | R04, R11 | bande magnétique, Transport, carburant et automobile ; 78,00 $ ; 1,0 fois le montant habituel (79,79 $) ; 2013-04-18 12:28 ; 5 transactions de la carte dans l'heure, 8 en 24 h | faux positif probable | Rafale d'achats courants, proche du montant habituel. |
| 12 | 10459690 | 74,0 | R04, R11 | bande magnétique, Alimentation ; 52,00 $ ; 2,0 fois le montant habituel (26,01 $) ; 2011-12-14 10:02 ; 5 transactions de la carte dans l'heure, 9 en 24 h | faux positif probable | Rafale d'achats courants, proche du montant habituel. |
| 13 | 10085751 | 73,9 | R04, R11 | bande magnétique, Transport, carburant et automobile ; 65,00 $ ; 1,7 fois le montant habituel (37,51 $) ; 2011-09-19 08:54 ; 5 transactions de la carte dans l'heure, 8 en 24 h | faux positif probable | Rafale d'achats courants, proche du montant habituel. |
| 14 | 19008573 | 73,7 | R03, R10 | en ligne, Voyage et hébergement ; 688,84 $ ; 26,0 fois le montant habituel (26,49 $) ; 2017-01-27 21:23 ; 0 transactions de la carte dans l'heure, 3 en 24 h | plausible | Montant très éloigné des habitudes du client. |
| 15 | 15735848 | 73,5 | R03, R10 | en ligne, Loisirs, culture et divertissement ; 313,31 $ ; 114,3 fois le montant habituel (2,74 $) ; 2015-02-27 11:20 ; 0 transactions de la carte dans l'heure, 4 en 24 h | plausible | Montant très éloigné des habitudes du client. |
| 16 | 22387264 | 73,3 | R04, R11 | puce, Transport, carburant et automobile ; 85,00 $ ; 1,4 fois le montant habituel (62,00 $) ; 2019-01-13 17:56 ; 5 transactions de la carte dans l'heure, 6 en 24 h | faux positif probable | Rafale d'achats courants, proche du montant habituel. |
| 17 | 11433461 | 71,9 | R04, R11 | bande magnétique, Transport, carburant et automobile ; 71,00 $ ; 1,9 fois le montant habituel (37,11 $) ; 2012-07-23 14:29 ; 5 transactions de la carte dans l'heure, 5 en 24 h | faux positif probable | Rafale d'achats courants, proche du montant habituel. |
| 18 | 22783801 | 71,5 | R06, R07 | puce, Alimentation ; 31,32 $ ; 0,6 fois le montant habituel (48,65 $) ; 2019-04-07 17:06 ; à l'étranger (Brazil) ; 0 transactions de la carte dans l'heure, 1 en 24 h ; première fois : pays | douteux | Premier achat dans un pays, petit montant par puce : voyage probable. |
| 19 | 8081632 | 68,7 | R08, R10 | en ligne, Loisirs, culture et divertissement ; 164,09 $ ; 18,3 fois le montant habituel (8,98 $) ; 2010-06-01 23:48 ; 0 transactions de la carte dans l'heure, 1 en 24 h ; première fois : commerçant, catégorie | plausible | Montant inhabituel chez un nouveau commerçant, dans une nouvelle catégorie. |
| 20 | 11263097 | 68,6 | R08, R10 | en ligne, Voyage et hébergement ; 297,37 $ ; 13,3 fois le montant habituel (22,29 $) ; 2012-06-15 07:54 ; première fois : commerçant, catégorie | plausible | Montant inhabituel chez un nouveau commerçant, dans une nouvelle catégorie. |
| 21 | 8875772 | 68,6 | R08, R11 | bande magnétique, Maison, jardin et électronique ; 385,00 $ ; 16,1 fois le montant habituel (23,86 $) ; 2010-12-10 13:47 ; première fois : commerçant, catégorie | plausible | Montant inhabituel chez un nouveau commerçant, dans une nouvelle catégorie. |
| 22 | 14502047 | 68,6 | R08, R11 | bande magnétique, Services publics et télécommunications ; 120,00 $ ; 4,3 fois le montant habituel (28,21 $) ; 2014-06-03 23:43 ; première fois : commerçant, catégorie | douteux | Nouveau commerçant, montant modéré. |
| 23 | 9710795 | 68,6 | R08, R11 | bande magnétique, Industrie et fabrication ; 320,00 $ ; 11,1 fois le montant habituel (28,90 $) ; 2011-06-24 13:48 ; première fois : commerçant, catégorie | plausible | Montant inhabituel chez un nouveau commerçant, dans une nouvelle catégorie. |
| 24 | 12317735 | 68,6 | R04 | bande magnétique, Alimentation ; -59,00 $ ; 2013-02-08 08:59 ; 5 transactions de la carte dans l'heure, 6 en 24 h ; 1 échecs d'authentification en 24 h | faux positif probable | Remboursement pendant une journée chargée : rien d'anormal. |
| 25 | 11876594 | 68,6 | R08, R10 | en ligne, Maison, jardin et électronique ; 316,15 $ ; 12,7 fois le montant habituel (24,93 $) ; 2012-10-31 16:28 ; 0 transactions de la carte dans l'heure, 1 en 24 h ; première fois : commerçant, catégorie | plausible | Montant inhabituel chez un nouveau commerçant, dans une nouvelle catégorie. |
| 26 | 11235155 | 68,5 | R08, R11 | bande magnétique, Industrie et fabrication ; 430,00 $ ; 11,4 fois le montant habituel (37,87 $) ; 2012-06-08 18:55 ; 0 transactions de la carte dans l'heure, 3 en 24 h ; première fois : commerçant, catégorie | plausible | Montant inhabituel chez un nouveau commerçant, dans une nouvelle catégorie. |
| 27 | 9404582 | 68,5 | R02, R10 | en ligne, Transport, carburant et automobile ; 10,71 $ ; 0,3 fois le montant habituel (31,43 $) ; 2011-04-14 08:26 ; 1 transactions de la carte dans l'heure, 8 en 24 h ; 0 échecs d'authentification en 24 h, échec sur cette transaction | douteux | Échec sur un achat proche des habitudes : erreur de saisie possible. |
| 28 | 23732577 | 68,5 | R08, R11 | bande magnétique, Industrie et fabrication ; 446,00 $ ; 16,6 fois le montant habituel (26,88 $) ; 2019-10-25 16:05 ; 0 transactions de la carte dans l'heure, 1 en 24 h ; première fois : commerçant, catégorie | plausible | Montant inhabituel chez un nouveau commerçant, dans une nouvelle catégorie. |
| 29 | 8141656 | 68,5 | R08, R10 | en ligne, Loisirs, culture et divertissement ; 68,64 $ ; 1,6 fois le montant habituel (43,10 $) ; 2010-06-16 14:45 ; 0 transactions de la carte dans l'heure, 2 en 24 h ; première fois : commerçant, catégorie | douteux | Nouveau commerçant, montant modéré. |
| 30 | 8069516 | 68,4 | R08, R10 | en ligne, Transport, carburant et automobile ; 33,25 $ ; 2,3 fois le montant habituel (14,77 $) ; 2010-05-30 07:12 ; 0 transactions de la carte dans l'heure, 1 en 24 h ; première fois : commerçant, catégorie | douteux | Nouveau commerçant, montant modéré. |
| 31 | 8377619 | 68,4 | R08, R11 | bande magnétique, Industrie et fabrication ; 206,00 $ ; 3,4 fois le montant habituel (60,93 $) ; 2010-08-12 19:34 ; 0 transactions de la carte dans l'heure, 1 en 24 h ; première fois : commerçant, catégorie | douteux | Nouveau commerçant, montant modéré. |
| 32 | 8240164 | 68,3 | R04 | bande magnétique, Transport, carburant et automobile ; 54,50 $ ; 0,9 fois le montant habituel (58,00 $) ; 2010-07-10 16:57 ; 5 transactions de la carte dans l'heure, 7 en 24 h ; 1 échecs d'authentification en 24 h | douteux | Rafale avec un échec récent, mais montant habituel. |
| 33 | 11279817 | 68,3 | R02, R10 | en ligne, Transport, carburant et automobile ; 22,71 $ ; 0,6 fois le montant habituel (40,62 $) ; 2012-06-18 22:19 ; 1 transactions de la carte dans l'heure, 5 en 24 h ; 0 échecs d'authentification en 24 h, échec sur cette transaction | douteux | Échec sur un achat proche des habitudes : erreur de saisie possible. |
| 34 | 21633803 | 68,2 | R03, R11 | bande magnétique, Industrie et fabrication ; 437,00 $ ; 54,7 fois le montant habituel (7,99 $) ; 2018-08-07 09:15 ; 0 transactions de la carte dans l'heure, 4 en 24 h | plausible | Montant très éloigné des habitudes du client. |
| 35 | 9917301 | 68,1 | R04 | bande magnétique, Transport, carburant et automobile ; 43,92 $ ; 1,6 fois le montant habituel (28,06 $) ; 2011-08-11 12:08 ; 5 transactions de la carte dans l'heure, 11 en 24 h | faux positif probable | Rafale d'achats courants, proche du montant habituel. |
| 36 | 10092343 | 68,0 | R04 | bande magnétique, Transport, carburant et automobile ; -58,00 $ ; 2011-09-20 16:14 ; 5 transactions de la carte dans l'heure, 7 en 24 h | faux positif probable | Remboursement pendant une journée chargée : rien d'anormal. |
| 37 | 7845853 | 67,9 | R04 | bande magnétique, Alimentation ; 129,85 $ ; 2,2 fois le montant habituel (60,00 $) ; 2010-04-04 13:59 ; 5 transactions de la carte dans l'heure, 9 en 24 h | faux positif probable | Rafale d'achats courants, proche du montant habituel. |
| 38 | 16801182 | 67,8 | R02, R10 | en ligne, Transport, carburant et automobile ; 19,02 $ ; 0,8 fois le montant habituel (23,62 $) ; 2015-10-13 16:21 ; 1 transactions de la carte dans l'heure, 2 en 24 h ; 0 échecs d'authentification en 24 h, échec sur cette transaction | douteux | Échec sur un achat proche des habitudes : erreur de saisie possible. |
| 39 | 18106982 | 67,7 | R02, R10 | en ligne, Transport, carburant et automobile ; 22,92 $ ; 0,9 fois le montant habituel (25,29 $) ; 2016-07-19 15:28 ; 1 transactions de la carte dans l'heure, 2 en 24 h ; 0 échecs d'authentification en 24 h, échec sur cette transaction | douteux | Échec sur un achat proche des habitudes : erreur de saisie possible. |
| 40 | 16536702 | 67,6 | R01 | puce, Alimentation ; 39,47 $ ; 1,1 fois le montant habituel (36,79 $) ; 2015-08-18 07:46 ; 2 transactions de la carte dans l'heure, 6 en 24 h ; 2 échecs d'authentification en 24 h | douteux | Deux échecs en 24 h, mais achat habituel par puce. |
| 41 | 18806560 | 67,5 | R07, R11 | puce, Maison, jardin et électronique ; 360,00 $ ; 17,6 fois le montant habituel (20,49 $) ; 2016-12-15 18:23 ; à l'étranger (Canada) ; 0 transactions de la carte dans l'heure, 2 en 24 h | plausible | Achat à l'étranger d'un montant inhabituel. |
| 42 | 14511653 | 67,3 | R02, R10 | en ligne, Services publics et télécommunications ; 222,33 $ ; 3,1 fois le montant habituel (70,76 $) ; 2014-06-06 08:34 ; 0 transactions de la carte dans l'heure, 1 en 24 h ; 0 échecs d'authentification en 24 h, échec sur cette transaction | plausible | Échec d'authentification sur un achat plus élevé que d'habitude. |
| 43 | 19454944 | 66,8 | R07, R11 | puce, Maison, jardin et électronique ; 392,00 $ ; 5,8 fois le montant habituel (67,72 $) ; 2017-05-02 17:37 ; à l'étranger (Finland) ; 0 transactions de la carte dans l'heure, 2 en 24 h | plausible | Achat à l'étranger d'un montant inhabituel. |
| 44 | 14077324 | 66,8 | R02, R10 | en ligne, Services publics et télécommunications ; 119,30 $ ; 3,5 fois le montant habituel (34,01 $) ; 2014-03-02 16:55 ; 0 échecs d'authentification en 24 h, échec sur cette transaction | douteux | Échec sur un achat proche des habitudes : erreur de saisie possible. |
| 45 | 13962889 | 66,5 | R02, R10 | en ligne, Transport, carburant et automobile ; 21,10 $ ; 1,0 fois le montant habituel (21,92 $) ; 2014-02-05 17:48 ; 0 échecs d'authentification en 24 h, échec sur cette transaction | douteux | Échec sur un achat proche des habitudes : erreur de saisie possible. |
| 46 | 21490161 | 66,5 | R02, R11 | puce, Services professionnels et financiers ; 120,00 $ ; 1,5 fois le montant habituel (80,00 $) ; 2018-07-07 17:26 ; 1 transactions de la carte dans l'heure, 7 en 24 h ; 0 échecs d'authentification en 24 h, échec sur cette transaction | douteux | Échec sur un achat proche des habitudes : erreur de saisie possible. |
| 47 | 16183182 | 63,1 | R02, R11 | puce, Services professionnels et financiers ; 60,00 $ ; 1,3 fois le montant habituel (46,50 $) ; 2015-06-03 13:05 ; 1 transactions de la carte dans l'heure, 5 en 24 h ; 0 échecs d'authentification en 24 h, échec sur cette transaction | douteux | Échec sur un achat proche des habitudes : erreur de saisie possible. |
| 48 | 12563287 | 62,8 | R03 | bande magnétique, Transport, carburant et automobile ; 672,41 $ ; 32,8 fois le montant habituel (20,50 $) ; 2013-04-03 21:56 | plausible | Montant très éloigné des habitudes du client. |
| 49 | 11287940 | 62,7 | R03, R11 | bande magnétique, Transport, carburant et automobile ; 693,00 $ ; 24,1 fois le montant habituel (28,81 $) ; 2012-06-20 16:21 | plausible | Montant très éloigné des habitudes du client. |
| 50 | 8429045 | 62,4 | R08 | bande magnétique, Industrie et fabrication ; 268,19 $ ; 18,0 fois le montant habituel (14,92 $) ; 2010-08-25 09:10 ; 2 transactions de la carte dans l'heure, 2 en 24 h ; première fois : commerçant, catégorie | plausible | Montant inhabituel chez un nouveau commerçant, dans une nouvelle catégorie. |

### Bilan de la revue

| Avis | Transactions |
| --- | --- |
| Plausible | 21 |
| Douteux | 18 |
| Faux positif probable | 11 |

- Les 11 faux positifs probables viennent tous de la règle des rafales (R04) : achats courants au montant habituel, ou remboursements pendant une journée chargée.
- La plupart des signalements plausibles combinent un montant de 11 à 114 fois plus élevé que d'habitude avec un nouveau commerçant. Les autres sont des achats à l'étranger d'un montant inhabituel, ou un échec sur un achat plus élevé que d'habitude.
- Contrôle après la revue, avec les étiquettes (P7-11) : 41 des 50 transactions sont étiquetées et une seule est une fraude (n° 30, jugée douteuse). Les 11 faux positifs probables sont bien tous étiquetés « pas de fraude ». La revue repère donc bien les fausses alertes, mais elle ne suffit pas à confirmer une fraude.

## Conclusion

- **Le seuil de 1 % est retenu** : 37 signalements par jour, une charge réaliste pour une petite équipe. Le seuil de 0,5 % peut servir aux jours chargés.
- **La règle des rafales (R04) produit la plupart des fausses alertes.** Sa précision mesurée en P7-11 le confirme (0,04 %). Il faut baisser son poids ou la retirer dans la prochaine version du score.
- **Le seuil doit être recalculé chaque année** : le taux de signalement baisse de 1,683 % en 2010 à 0,825 % en 2019 au seuil de 1 %.

**Critère de fin validé** (grille remplie, à confirmer par un membre de l'équipe).
