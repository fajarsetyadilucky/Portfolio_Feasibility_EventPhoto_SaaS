"""Pipeline Data Processing (RAW -> PROCESSED Layer)
Membaca dataset mentah dari data/01_raw/, melakukan validasi tipe data,
transformasi fitur, standardisasi kurs Rupiah, dan menyimpan dataset
yang sudah matang (clean & analysis-ready) ke data/02_processed/.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "01_raw"
PROCESSED_DIR = ROOT / "data" / "02_processed"


def process_market_benchmark() -> pd.DataFrame:
    """Proses dan matangkan data kompetitor pasar Indonesia."""
    file_path = RAW_DIR / "market_benchmark" / "competitor_pricing.csv"
    df = pd.read_csv(file_path)

    # Filter kompetitor aktif dengan harga yang valid
    df["price_idr_current"] = pd.to_numeric(df["price_idr_current"], errors="coerce")
    df["price_idr_normal"] = pd.to_numeric(df["price_idr_normal"], errors="coerce")
    df["max_guests"] = pd.to_numeric(df["max_guests"], errors="coerce")

    # Hitung diskon promo jika ada harga normal
    df["discount_amount_idr"] = np.where(
        df["price_idr_normal"].notna() & (df["price_idr_normal"] > df["price_idr_current"]),
        df["price_idr_normal"] - df["price_idr_current"],
        0.0,
    )
    df["discount_pct"] = np.where(
        df["price_idr_normal"].notna() & (df["price_idr_normal"] > 0),
        ((df["discount_amount_idr"] / df["price_idr_normal"]) * 100).round(1),
        0.0,
    )

    # Kategorisasi segmen pasar
    def classify_segment(prod_type: str) -> str:
        if "direct digital disposable" in prod_type:
            return "Direct Disposable Camera (Head-to-Head)"
        elif "bundled" in prod_type:
            return "Bundling Invitation + Camera"
        elif "photobooth" in prod_type:
            return "On-Site Hardware / Photobooth"
        elif "guestbook" in prod_type:
            return "On-Site Guest Management"
        return "Other"

    df["market_segment"] = df["product_type"].apply(classify_segment)

    # Simpan dataset matang
    out_file = PROCESSED_DIR / "processed_competitor_benchmark.csv"
    df.to_csv(out_file, index=False)
    print(f"[OK] Market Benchmark processed -> {out_file} ({len(df)} baris)")
    return df


def process_cloud_parameters() -> pd.DataFrame:
    """Proses dan strukturkan parameter operasional cloud & payment gateway."""
    file_path = RAW_DIR / "cloud_cost_models" / "cloud_cost_parameters.csv"
    df = pd.read_csv(file_path)

    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    # Tambahkan konversi nilai ke satuan moneter IDR terstandar
    fx_rate = df.loc[df["item"] == "USD to IDR", "value"].iloc[0]

    def convert_to_idr(row):
        val = row["value"]
        unit = str(row["unit"])
        if "USD per GB-month" in unit:
            return val * fx_rate  # IDR per GB-month
        elif "USD per GB" in unit:
            return val * fx_rate  # IDR per GB
        elif "fraction" in unit:
            return val * 100  # Persentase (%)
        elif "IDR" in unit:
            return val
        return val

    df["value_idr_or_standard"] = df.apply(convert_to_idr, axis=1)

    out_file = PROCESSED_DIR / "processed_cloud_cost_parameters.csv"
    df.to_csv(out_file, index=False)
    print(f"[OK] Cloud Parameters processed -> {out_file} ({len(df)} baris)")
    return df


def process_wedding_demographics() -> pd.DataFrame:
    """Proses demografi pernikahan dan kalkulasi estimasi TAM/SAM/SOM."""
    file_path = RAW_DIR / "wedding_event_demographics" / "wedding_demographics.csv"
    df = pd.read_csv(file_path)

    df["weddings"] = pd.to_numeric(df["weddings"], errors="coerce")

    # Hitung pertumbuhan YoY nasional
    nat_df = df[df["region"] == "Indonesia"].sort_values("year").copy()
    nat_df["yoy_growth_pct"] = (nat_df["weddings"].pct_change() * 100).round(2)

    # Merge YoY growth back
    df = df.merge(
        nat_df[["year", "region", "yoy_growth_pct"]],
        on=["year", "region"],
        how="left",
    )

    out_file = PROCESSED_DIR / "processed_wedding_demographics.csv"
    df.to_csv(out_file, index=False)
    print(f"[OK] Wedding Demographics processed -> {out_file} ({len(df)} baris)")
    return df


if __name__ == "__main__":
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    print("Memulai pipeline pematangan data (01_raw -> 02_processed)...")
    process_market_benchmark()
    process_cloud_parameters()
    process_wedding_demographics()
    print("Semua data matang berhasil disimpan di data/02_processed/!")
