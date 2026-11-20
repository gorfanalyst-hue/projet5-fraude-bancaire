# P8-10 : Améliorer le tableau de bord après les tests

Statut : **en partie fait**. Les corrections du pré-test interne sont faites et vérifiées. Les corrections demandées par les trois testeurs extérieurs (P8-09) restent à faire quand leurs retours seront consignés. Critère de fin : corrections faites et vérifiées.

## Corrections du pré-test interne

Avant les testeurs, l'équipe a parcouru les quatre pages avec les scénarios de P8-09. Problèmes trouvés et corrigés :

| Problème                                                                 | Page                                                 | Correction                                                                                    |
| ------------------------------------------------------------------------ | ---------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Libellés coupés dans les graphiques en barres (« Transport, carbur... ») | Profils, Lieux et catégories, Transactions signalées | Largeur des libellés augmentée (`labelLimit=320`), hauteur des barres augmentée               |
| Raisons trop longues pour le graphique                                   | Transactions signalées                               | Libellés courts (exemple : « R04 : rafale dans l'heure ») ; la liste garde la raison complète |
| Nombres à l'anglaise dans les graphiques (120,000) et mois en anglais    | Toutes                                               | Format français des nombres et des dates dans les graphiques (`LOCALE_FR`)                    |
| Valeurs coupées dans les chiffres clés (« 87,6 % des transac... »)       | Lieux et catégories                                  | Chiffre seul en grand, « des transactions » écrit en dessous                                  |
| Libellé trop long : « Clients avec au moins un signalement »             | Vue d'ensemble                                       | « Clients signalés », avec l'explication dans l'aide                                          |
| Texte anglais « Choose options » dans les listes de choix                | Toutes                                               | Textes « Toutes » ou « Tous »                                                                 |
| Couleurs rouges par défaut de Streamlit                                  | Toutes                                               | Thème aux couleurs de la charte (`.streamlit/config.toml`)                                    |

Après ces corrections, la section P8-08 du notebook 08 a été relancée : 62 contrôles, aucun écart.

## Corrections après les tests extérieurs (à remplir)

| Difficulté (P8-09) | Correction | Vérifiée (P8-08 relancé) |
| ------------------ | ---------- | ------------------------ |
|                    |            |                          |
