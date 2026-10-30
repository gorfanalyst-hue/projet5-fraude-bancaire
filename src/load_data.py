import pandas as pd
import json
from pathlib import Path

# Dossier data/ situé à la racine du dépôt (un niveau au-dessus de src/)
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def load_csv_chunked(path, dtype=None, parse_dates=None, chunksize=500_000, **kwargs):
    """
    Fonction commune : lit un CSV par morceaux pour limiter la mémoire,
    avec des dtypes légers définis à l'avance.
    """
    chunks = [
        chunk for chunk in pd.read_csv(
            path, dtype=dtype, parse_dates=parse_dates,
            chunksize=chunksize, low_memory=False, **kwargs
        )
    ]
    df = pd.concat(chunks, ignore_index=True)

    # Correction P3-01 : pd.concat ne garde le type "category" que si tous les
    # morceaux ont exactement les mêmes catégories. Sinon, la colonne redevient
    # du texte (object), qui prend beaucoup plus de mémoire. On remet donc le
    # type "category" après la concaténation.
    if dtype:
        for col, col_type in dtype.items():
            if col_type == "category" and col in df.columns:
                df[col] = df[col].astype("category")
    return df


def load_transactions(path=DATA_DIR / "transactions_data.csv", usecols=None):
    """
    Charge les transactions. Le paramètre usecols permet de ne lire que
    certaines colonnes, par exemple ["id", "date", "use_chip"], pour économiser
    la mémoire (ajout P2-17). Sans usecols, toutes les colonnes sont lues.
    """
    dtype = {
        "id": "int32", "client_id": "int32", "card_id": "int32",
        "use_chip": "category", "merchant_id": "int32",
        "merchant_city": "category", "merchant_state": "category",
        "mcc": "int16", "errors": "category",
        # amount reste en texte ($...) -> conversion en P3-02
    }
    if usecols is not None:
        dtype = {col: t for col, t in dtype.items() if col in usecols}
    parse_dates = ["date"] if usecols is None or "date" in usecols else None
    return load_csv_chunked(path, dtype=dtype, parse_dates=parse_dates, usecols=usecols)


def load_cards(path=DATA_DIR / "cards_data.csv"):
    dtype = {
        "id": "int32", "client_id": "int32",
        "card_brand": "category", "card_type": "category",
        "has_chip": "category", "num_cards_issued": "int8",
        "card_on_dark_web": "category",
        # credit_limit en texte -> P3-02 ; expires/acct_open_date -> P3-03
    }
    return load_csv_chunked(path, dtype=dtype)


def load_users(path=DATA_DIR / "users_data.csv"):
    dtype = {
        "id": "int32", "current_age": "int8", "retirement_age": "int8",
        "birth_year": "int16", "birth_month": "int8", "gender": "category",
        "credit_score": "int16", "num_credit_cards": "int8",
        # per_capita_income, yearly_income, total_debt en texte -> P3-02
    }
    return load_csv_chunked(path, dtype=dtype)


def load_mcc_codes(path=DATA_DIR / "mcc_codes.json"):
    with open(path) as f:
        data = json.load(f)
    df = pd.DataFrame(list(data.items()), columns=["mcc_code", "description"])
    df["mcc_code"] = df["mcc_code"].astype("int16")
    return df


def load_fraud_labels(path=DATA_DIR / "fraud_labels.json"):
    """
    Charge les étiquettes de fraude (P2-17).

    Le fichier a la forme {"target": {"<id de transaction>": "Yes" ou "No", ...}}
    et ne couvre qu'une partie des transactions.

    Retourne une table à deux colonnes :
    - id : identifiant de la transaction (même clé que transactions_data)
    - is_fraud : 1 pour une fraude, 0 sinon
    """
    with open(path, encoding="utf-8") as f:
        labels = json.load(f)["target"]

    values = pd.Series(list(labels.values()))
    unknown = set(values.unique()) - {"Yes", "No"}
    if unknown:
        raise ValueError(f"Valeurs d'étiquette inattendues : {sorted(unknown)}")

    return pd.DataFrame({
        "id": pd.to_numeric(pd.Series(list(labels.keys()))).astype("int32"),
        "is_fraud": (values == "Yes").astype("int8"),
    })



CLEAN_DIR = DATA_DIR / "clean"


def load_clean_table(name, columns=None, folder=CLEAN_DIR):
    """
    Charge une table nettoyée enregistrée en P3-10 :
    "transactions", "cards", "users", "mcc" ou "fraud_labels".
    columns permet de ne lire que certaines colonnes.
    """
    return pd.read_parquet(folder / f"{name}.parquet", columns=columns)
