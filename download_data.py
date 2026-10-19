"""Download the Default of Credit Card Clients dataset (UCI #350) into data/.

Usage:
    python download_data.py
"""

import io
import zipfile
from pathlib import Path

import pandas as pd
import requests

URL = "https://archive.ics.uci.edu/static/public/350/default+of+credit+card+clients.zip"
OUT = Path(__file__).resolve().parent / "data" / "credit_default.csv"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)

    print(f"Downloading {URL} ...")
    resp = requests.get(URL, timeout=60)
    resp.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        xls_name = next(n for n in zf.namelist() if n.lower().endswith(".xls"))
        with zf.open(xls_name) as f:
            # Row 0 is 'X1, X2, ...'; row 1 holds the real column names.
            df = pd.read_excel(f, header=1)

    df = df.rename(columns={"default payment next month": "default_payment_next_month"})
    df.to_csv(OUT, index=False)
    print(f"Saved {OUT}  ->  shape {df.shape}")


if __name__ == "__main__":
    main()
