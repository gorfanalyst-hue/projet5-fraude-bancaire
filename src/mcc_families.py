"""
Table de correspondance des codes MCC (P3-05).

Chaque code MCC est classé dans UNE seule famille. Les familles et les
descriptions sont en français. Ce fichier est écrit en Python (et non en CSV)
parce que le .gitignore du dépôt ignore les fichiers .csv et .json : une table
CSV ne serait pas partagée avec l'équipe.

Pour modifier le classement, déplacer un code d'une liste à une autre dans
MCC_FAMILLES. Le contrôle d'unicité se fait à l'import du module.
"""

MCC_FAMILLES = {
    "Alimentation": [
        5411,  # Épiceries et supermarchés
        5499,  # Magasins d'alimentation divers
        5921,  # Magasins de bière, vin et spiritueux
    ],
    "Restauration et bars": [
        5812,  # Restaurants et lieux de restauration
        5813,  # Débits de boissons (alcool)
        5814,  # Restauration rapide
    ],
    "Transport, carburant et automobile": [
        3722,  # Chemins de fer de voyageurs
        3771,  # Transport ferroviaire de voyageurs
        3775,  # Transport ferroviaire de marchandises
        4111,  # Transport local et de banlieue
        4112,  # Chemins de fer de voyageurs
        4121,  # Taxis et limousines
        4131,  # Lignes d'autobus
        4214,  # Transport routier de marchandises
        4784,  # Péages et frais de pont
        5533,  # Magasins de pièces et accessoires automobiles
        5541,  # Stations-service
        7531,  # Carrosseries automobiles
        7538,  # Ateliers d'entretien automobile
        7542,  # Lave-autos
        7549,  # Services de remorquage
    ],
    "Voyage et hébergement": [
        4411,  # Croisières
        4511,  # Compagnies aériennes
        4722,  # Agences de voyages
        7011,  # Hébergement : hôtels, motels, centres de villégiature
    ],
    "Vêtements, beauté et services personnels": [
        3132,  # Articles en cuir (à valider : Industrie ?)
        5094,  # Pierres et métaux précieux
        5621,  # Prêt-à-porter féminin
        5651,  # Vêtements pour toute la famille
        5655,  # Vêtements de sport et d'équitation
        5661,  # Magasins de chaussures
        5977,  # Magasins de cosmétiques
        7210,  # Services de blanchisserie
        7230,  # Salons de beauté et barbiers
    ],
    "Maison, jardin et électronique": [
        1711,  # Entrepreneurs en chauffage, plomberie et climatisation
        3144,  # Magasins de revêtements de sol
        3174,  # Magasins de tapisserie et de rideaux
        3256,  # Briques, pierre et matériaux apparentés
        3260,  # Poterie et céramique (à valider : Industrie ?)
        3504,  # Fournitures de jardinage
        5045,  # Ordinateurs et périphériques
        5193,  # Fournitures pour fleuristes, pépinières et fleurs
        5211,  # Bois et matériaux de construction
        5251,  # Quincailleries
        5261,  # Magasins de pelouse et jardin
        5712,  # Meubles, articles d'ameublement et équipement
        5719,  # Magasins d'articles d'ameublement divers
        5722,  # Magasins d'appareils électroménagers
        5732,  # Magasins d'électronique
    ],
    "Santé et soins": [
        5912,  # Pharmacies
        8011,  # Médecins
        8021,  # Dentistes et orthodontistes
        8041,  # Chiropraticiens
        8043,  # Optométristes et articles d'optique
        8049,  # Podologues
        8062,  # Hôpitaux
        8099,  # Services médicaux
    ],
    "Loisirs, culture et divertissement": [
        5192,  # Livres, périodiques et journaux
        5733,  # Magasins de musique et d'instruments de musique
        5815,  # Biens numériques : médias, livres, applications
        5816,  # Biens numériques : jeux
        5941,  # Magasins d'articles de sport
        5942,  # Librairies
        5970,  # Fournitures d'artistes et magasins d'artisanat
        7801,  # Terrains de sport et sports commerciaux
        7802,  # Sports récréatifs et clubs
        7832,  # Cinémas
        7922,  # Producteurs de théâtre
        7995,  # Paris et jeux (loterie, casinos)
        7996,  # Parcs d'attractions, carnavals et cirques
    ],
    "Services publics et télécommunications": [
        3780,  # Services de réseaux informatiques
        4814,  # Services de télécommunications
        4899,  # Câble, satellite et autres services de télévision payante
        4900,  # Services publics : électricité, gaz, eau, assainissement
        9402,  # Services postaux (gouvernement uniquement)
    ],
    "Services professionnels et financiers": [
        4829,  # Transferts d'argent
        6300,  # Vente d'assurances et souscription
        7276,  # Préparation de déclarations d'impôts
        7349,  # Services de nettoyage et d'entretien
        7393,  # Agences de détectives et services de sécurité
        8111,  # Services juridiques et avocats
        8931,  # Comptabilité, audit et tenue de livres
    ],
    "Grandes surfaces et commerces divers": [
        5300,  # Clubs-entrepôts
        5310,  # Magasins à rabais
        5311,  # Grands magasins
        5932,  # Magasins d'antiquités
        5947,  # Magasins de cadeaux, cartes et articles de fantaisie
    ],
    "Industrie et fabrication": [
        3000,  # Sidérurgie
        3001,  # Fabrication de produits en acier
        3005,  # Fabrication métallique diverse
        3006,  # Produits métalliques fabriqués divers
        3007,  # Produits revêtus et laminés
        3008,  # Fûts et barils en acier
        3009,  # Structures métalliques fabriquées
        3058,  # Fabrication d'outils, pièces et fournitures
        3066,  # Métaux divers
        3075,  # Fabrication de boulons, écrous, vis et rivets
        3359,  # Fonderies de métaux non ferreux
        3387,  # Services de galvanoplastie, placage et polissage
        3389,  # Services de métaux non précieux
        3390,  # Travaux de métallurgie divers
        3393,  # Services de traitement thermique des métaux
        3395,  # Réparation par soudure
        3405,  # Ferronnerie
        3509,  # Équipement et fournitures industriels
        3596,  # Fabrication de machines et pièces diverses
        3640,  # Éclairage, luminaires et fournitures électriques
        3684,  # Semi-conducteurs et dispositifs apparentés
        3730,  # Fournitures pour navires
    ],
}

MCC_DESCRIPTIONS_FR = {
    1711: "Entrepreneurs en chauffage, plomberie et climatisation",
    3000: "Sidérurgie",
    3001: "Fabrication de produits en acier",
    3005: "Fabrication métallique diverse",
    3006: "Produits métalliques fabriqués divers",
    3007: "Produits revêtus et laminés",
    3008: "Fûts et barils en acier",
    3009: "Structures métalliques fabriquées",
    3058: "Fabrication d'outils, pièces et fournitures",
    3066: "Métaux divers",
    3075: "Fabrication de boulons, écrous, vis et rivets",
    3132: "Articles en cuir",
    3144: "Magasins de revêtements de sol",
    3174: "Magasins de tapisserie et de rideaux",
    3256: "Briques, pierre et matériaux apparentés",
    3260: "Poterie et céramique",
    3359: "Fonderies de métaux non ferreux",
    3387: "Services de galvanoplastie, placage et polissage",
    3389: "Services de métaux non précieux",
    3390: "Travaux de métallurgie divers",
    3393: "Services de traitement thermique des métaux",
    3395: "Réparation par soudure",
    3405: "Ferronnerie",
    3504: "Fournitures de jardinage",
    3509: "Équipement et fournitures industriels",
    3596: "Fabrication de machines et pièces diverses",
    3640: "Éclairage, luminaires et fournitures électriques",
    3684: "Semi-conducteurs et dispositifs apparentés",
    3722: "Chemins de fer de voyageurs",
    3730: "Fournitures pour navires",
    3771: "Transport ferroviaire de voyageurs",
    3775: "Transport ferroviaire de marchandises",
    3780: "Services de réseaux informatiques",
    4111: "Transport local et de banlieue",
    4112: "Chemins de fer de voyageurs",
    4121: "Taxis et limousines",
    4131: "Lignes d'autobus",
    4214: "Transport routier de marchandises",
    4411: "Croisières",
    4511: "Compagnies aériennes",
    4722: "Agences de voyages",
    4784: "Péages et frais de pont",
    4814: "Services de télécommunications",
    4829: "Transferts d'argent",
    4899: "Câble, satellite et autres services de télévision payante",
    4900: "Services publics : électricité, gaz, eau, assainissement",
    5045: "Ordinateurs et périphériques",
    5094: "Pierres et métaux précieux",
    5192: "Livres, périodiques et journaux",
    5193: "Fournitures pour fleuristes, pépinières et fleurs",
    5211: "Bois et matériaux de construction",
    5251: "Quincailleries",
    5261: "Magasins de pelouse et jardin",
    5300: "Clubs-entrepôts",
    5310: "Magasins à rabais",
    5311: "Grands magasins",
    5411: "Épiceries et supermarchés",
    5499: "Magasins d'alimentation divers",
    5533: "Magasins de pièces et accessoires automobiles",
    5541: "Stations-service",
    5621: "Prêt-à-porter féminin",
    5651: "Vêtements pour toute la famille",
    5655: "Vêtements de sport et d'équitation",
    5661: "Magasins de chaussures",
    5712: "Meubles, articles d'ameublement et équipement",
    5719: "Magasins d'articles d'ameublement divers",
    5722: "Magasins d'appareils électroménagers",
    5732: "Magasins d'électronique",
    5733: "Magasins de musique et d'instruments de musique",
    5812: "Restaurants et lieux de restauration",
    5813: "Débits de boissons (alcool)",
    5814: "Restauration rapide",
    5815: "Biens numériques : médias, livres, applications",
    5816: "Biens numériques : jeux",
    5912: "Pharmacies",
    5921: "Magasins de bière, vin et spiritueux",
    5932: "Magasins d'antiquités",
    5941: "Magasins d'articles de sport",
    5942: "Librairies",
    5947: "Magasins de cadeaux, cartes et articles de fantaisie",
    5970: "Fournitures d'artistes et magasins d'artisanat",
    5977: "Magasins de cosmétiques",
    6300: "Vente d'assurances et souscription",
    7011: "Hébergement : hôtels, motels, centres de villégiature",
    7210: "Services de blanchisserie",
    7230: "Salons de beauté et barbiers",
    7276: "Préparation de déclarations d'impôts",
    7349: "Services de nettoyage et d'entretien",
    7393: "Agences de détectives et services de sécurité",
    7531: "Carrosseries automobiles",
    7538: "Ateliers d'entretien automobile",
    7542: "Lave-autos",
    7549: "Services de remorquage",
    7801: "Terrains de sport et sports commerciaux",
    7802: "Sports récréatifs et clubs",
    7832: "Cinémas",
    7922: "Producteurs de théâtre",
    7995: "Paris et jeux (loterie, casinos)",
    7996: "Parcs d'attractions, carnavals et cirques",
    8011: "Médecins",
    8021: "Dentistes et orthodontistes",
    8041: "Chiropraticiens",
    8043: "Optométristes et articles d'optique",
    8049: "Podologues",
    8062: "Hôpitaux",
    8099: "Services médicaux",
    8111: "Services juridiques et avocats",
    8931: "Comptabilité, audit et tenue de livres",
    9402: "Services postaux (gouvernement uniquement)",
}

# Dictionnaire inversé : code -> famille. Le contrôle d'unicité est fait ici :
# un code classé dans deux familles provoque une erreur à l'import.
MCC_TO_FAMILLE = {}
for _famille, _codes in MCC_FAMILLES.items():
    for _code in _codes:
        if _code in MCC_TO_FAMILLE:
            raise ValueError(
                f"Code MCC {_code} classé dans deux familles : "
                f"« {MCC_TO_FAMILLE[_code]} » et « {_famille} »"
            )
        MCC_TO_FAMILLE[_code] = _famille
