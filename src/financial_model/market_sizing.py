"""TAM, SAM, SOM Market Sizing Model (Indonesia Wedding & Event-Tech SaaS)
Menghitung estimasi potensi pasar secara kuantitatif berdasarkan data resmi BPS 2024,
tingkat penetrasi perkotaan, daya beli, dan proyeksi nilai moneter Rupiah tahun 1-2.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = ROOT / "data" / "02_processed"
ANALYTICS_DIR = ROOT / "data" / "03_analytics_marts"


def calculate_tam_sam_som(price_per_event_idr: float = 299_000.0) -> pd.DataFrame:
    df_demo = pd.read_csv(PROCESSED_DIR / "processed_wedding_demographics.csv")
    nat_2024 = df_demo[(df_demo["region"] == "Indonesia") & (df_demo["year"] == 2024)]["weddings"].iloc[0]

    # 1. TAM (Total Addressable Market) - Seluruh pernikahan resmi di Indonesia
    tam_volume = int(nat_2024)
    tam_value_idr = tam_volume * price_per_event_idr

    # 2. SAM (Serviceable Available Market) - Pernikahan urban kelas menengah ke atas
    # Asumsi berbasis demografi: ~17% pernikahan di kota besar tier 1-2 dengan penetrasi internet/smartphone tinggi
    sam_pct = 0.17
    sam_volume = int(tam_volume * sam_pct)  # ~251.300 event/tahun
    sam_value_idr = sam_volume * price_per_event_idr

    # 3. SOM (Serviceable Obtainable Market) - Target penetrasi realistis tahun 1 & tahun 2
    # Tahun 1: 0.3% dari SAM (~750 event)
    som_y1_volume = int(sam_volume * 0.003)
    som_y1_value_idr = som_y1_volume * price_per_event_idr

    # Tahun 2: 0.8% dari SAM (~2.010 event)
    som_y2_volume = int(sam_volume * 0.008)
    som_y2_value_idr = som_y2_volume * price_per_event_idr

    data = [
        {
            "tier": "TAM (Total Addressable Market)",
            "scope": "Total Pernikahan Resmi Indonesia (BPS 2024)",
            "annual_volume_events": tam_volume,
            "annual_market_value_idr": tam_value_idr,
            "pct_of_tam": 100.0,
            "benchmark_basis": "Statistik BPS 2024",
        },
        {
            "tier": "SAM (Serviceable Available Market)",
            "scope": "Segmen Perkotaan Menengah-Atas (Tier 1-2)",
            "annual_volume_events": sam_volume,
            "annual_market_value_idr": sam_value_idr,
            "pct_of_tam": round(sam_pct * 100, 1),
            "benchmark_basis": "17% Konsentrasi Urban Wedding",
        },
        {
            "tier": "SOM Tahun 1 (Target Realistis)",
            "scope": "Penetrasi Awal Tahun 1 (Go-To-Market)",
            "annual_volume_events": som_y1_volume,
            "annual_market_value_idr": som_y1_value_idr,
            "pct_of_tam": round((som_y1_volume / tam_volume) * 100, 3),
            "benchmark_basis": "0.3% Penetrasi SAM (Kemitraan 15-20 WO)",
        },
        {
            "tier": "SOM Tahun 2 (Target Ekspansi)",
            "scope": "Penetrasi Tahun 2 (Multi-City Expansion)",
            "annual_volume_events": som_y2_volume,
            "annual_market_value_idr": som_y2_value_idr,
            "pct_of_tam": round((som_y2_volume / tam_volume) * 100, 3),
            "benchmark_basis": "0.8% Penetrasi SAM (Kemitraan 50+ WO)",
        },
    ]

    df_out = pd.DataFrame(data)
    return df_out


if __name__ == "__main__":
    ANALYTICS_DIR.mkdir(parents=True, exist_ok=True)
    df_market = calculate_tam_sam_som()
    out_file = ANALYTICS_DIR / "tam_sam_som_market_sizing.csv"
    df_market.to_csv(out_file, index=False)
    print(f"[OK] Market Sizing Model saved -> {out_file}")
    print(df_market[["tier", "annual_volume_events", "annual_market_value_idr", "pct_of_tam"]].to_string(index=False))
