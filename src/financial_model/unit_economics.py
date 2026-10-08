"""Unit Economics, Break-Even & Sensitivity Analysis Engine (Milestone 2)
Memodelkan struktur biaya per unit, contribution margin, BEP operasional,
analisis payback period (dalam bulan dan volume), serta sensitivitas CAC vs Pricing.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = ROOT / "data" / "02_processed"
ANALYTICS_DIR = ROOT / "data" / "03_analytics_marts"


@dataclass(frozen=True)
class FinancialConfig:
    capex_idr: float = 75_000_000.0          # CapEx Pengembangan & Branding Awal
    fixed_opex_monthly_idr: float = 5_000_000.0  # Hosting, domain, maintenance
    cac_b2c_base_idr: float = 120_000.0      # Rentang Rp80rb - Rp180rb
    b2b_wholesale_discount: float = 0.40     # WO dapat margin 40% (harga beli 60%)
    b2b_cac_amortized_idr: float = 15_000.0  # CAC B2B via kemitraan direct sales


def load_processed_parameters():
    df_cloud = pd.read_csv(PROCESSED_DIR / "processed_cloud_cost_parameters.csv")
    val_map = df_cloud.set_index("item")["value"].to_dict()
    return val_map


def calculate_unit_cost(photos_per_event: int = 500, mb_per_photo: float = 5.0):
    params = load_processed_parameters()
    fx = params.get("USD to IDR", 16500.0)
    s3_rate = params.get("AWS S3 Standard ap-southeast-3", 0.025)
    egress_rate = params.get("AWS Data Transfer Out to Internet", 0.132)
    retention_months = params.get("Masa retensi album", 12.0)
    download_ratio = params.get("Rasio guest view/download terhadap storage", 1.0)

    gb_stored = (photos_per_event * mb_per_photo) / 1024.0
    storage_cost_idr = gb_stored * s3_rate * retention_months * fx
    egress_cost_idr = gb_stored * download_ratio * egress_rate * fx
    total_cloud_cost_idr = storage_cost_idr + egress_cost_idr

    return {
        "gb_stored": gb_stored,
        "storage_cost_idr": storage_cost_idr,
        "egress_cost_idr": egress_cost_idr,
        "total_cloud_cost_idr": total_cloud_cost_idr,
    }


def calculate_payment_gateway_fee(price_idr: float):
    # Asumsi bauran pembayaran Indonesia: 60% QRIS (0.7%), 20% GoPay (2%), 20% VA (Rp4.000)
    params = load_processed_parameters()
    qris_fee = price_idr * params.get("Midtrans QRIS", 0.007)
    gopay_fee = price_idr * params.get("Midtrans GoPay", 0.02)
    va_fee = params.get("Midtrans Virtual Account", 4000.0)
    blended_fee = (0.60 * qris_fee) + (0.20 * gopay_fee) + (0.20 * va_fee)
    return blended_fee


def generate_unit_economics_table(
    target_prices: list[float] = [79_000, 199_000, 299_000, 439_000, 599_000],
    config: FinancialConfig = FinancialConfig(),
) -> pd.DataFrame:
    unit_cost = calculate_unit_cost(photos_per_event=500, mb_per_photo=5.0)
    cloud_cost = unit_cost["total_cloud_cost_idr"]

    records = []
    # 1. Model A: B2C Pure (Direct to Bride/Groom)
    for p in target_prices:
        pg_fee = calculate_payment_gateway_fee(p)
        gross_margin = p - cloud_cost - pg_fee
        contribution_margin = gross_margin - config.cac_b2c_base_idr
        cm_ratio = (contribution_margin / p) * 100 if p > 0 else 0

        # BEP Volume (Events / month)
        bep_monthly_events = (
            config.fixed_opex_monthly_idr / contribution_margin
            if contribution_margin > 0
            else np.nan
        )

        records.append({
            "business_model": "Model A (B2C Pure)",
            "package_price_idr": p,
            "revenue_per_event_idr": p,
            "cloud_cost_idr": cloud_cost,
            "pg_fee_idr": pg_fee,
            "cac_idr": config.cac_b2c_base_idr,
            "gross_margin_idr": gross_margin,
            "contribution_margin_idr": contribution_margin,
            "cm_ratio_pct": cm_ratio,
            "cac_ratio_pct": (config.cac_b2c_base_idr / p) * 100,
            "bep_monthly_events": bep_monthly_events,
            "bep_status": "Viable" if contribution_margin > 0 else "Infeasible (Negative CM)",
        })

    # 2. Model B: B2B Pivot (Wedding Organizer / Agency Partner)
    for p in target_prices:
        wholesale_price = p * (1.0 - config.b2b_wholesale_discount)
        pg_fee = calculate_payment_gateway_fee(wholesale_price)
        gross_margin = wholesale_price - cloud_cost - pg_fee
        contribution_margin = gross_margin - config.b2b_cac_amortized_idr
        cm_ratio = (contribution_margin / wholesale_price) * 100 if wholesale_price > 0 else 0

        bep_monthly_events = (
            config.fixed_opex_monthly_idr / contribution_margin
            if contribution_margin > 0
            else np.nan
        )

        records.append({
            "business_model": "Model B (B2B WO Partner)",
            "package_price_idr": p,
            "revenue_per_event_idr": wholesale_price,
            "cloud_cost_idr": cloud_cost,
            "pg_fee_idr": pg_fee,
            "cac_idr": config.b2b_cac_amortized_idr,
            "gross_margin_idr": gross_margin,
            "contribution_margin_idr": contribution_margin,
            "cm_ratio_pct": cm_ratio,
            "cac_ratio_pct": (config.b2b_cac_amortized_idr / wholesale_price) * 100,
            "bep_monthly_events": bep_monthly_events,
            "bep_status": "Viable" if contribution_margin > 0 else "Infeasible (Negative CM)",
        })

    df = pd.DataFrame(records)
    return df


def generate_cac_sensitivity_matrix(
    price: float = 299_000,
    cac_range: list[float] = [60_000, 80_000, 100_000, 120_000, 140_000, 160_000, 180_000],
    monthly_volumes: list[int] = [15, 25, 35, 50, 75, 100],
    config: FinancialConfig = FinancialConfig(),
) -> pd.DataFrame:
    unit_cost = calculate_unit_cost(photos_per_event=500, mb_per_photo=5.0)
    cloud_cost = unit_cost["total_cloud_cost_idr"]
    pg_fee = calculate_payment_gateway_fee(price)

    matrix = []
    for cac in cac_range:
        row = {"cac_idr": cac, "cac_pct_of_price": round((cac / price) * 100, 1)}
        cm_unit = price - cloud_cost - pg_fee - cac
        row["cm_unit_idr"] = cm_unit
        row["bep_events_month"] = round(config.fixed_opex_monthly_idr / cm_unit, 1) if cm_unit > 0 else np.nan

        for vol in monthly_volumes:
            net_operating_profit = (cm_unit * vol) - config.fixed_opex_monthly_idr
            row[f"profit_vol_{vol}"] = net_operating_profit
        matrix.append(row)

    return pd.DataFrame(matrix)


if __name__ == "__main__":
    ANALYTICS_DIR.mkdir(parents=True, exist_ok=True)
    print("Menghitung model Unit Economics & Break-Even...")
    df_ue = generate_unit_economics_table()
    out_ue = ANALYTICS_DIR / "unit_economics_bep_scenarios.csv"
    df_ue.round(2).to_csv(out_ue, index=False)
    print(f"[OK] Unit Economics & BEP Scenarios -> {out_ue}")

    print("Menghitung matriks sensitivitas CAC vs Volume...")
    df_sens = generate_cac_sensitivity_matrix(price=299_000)
    out_sens = ANALYTICS_DIR / "cac_sensitivity_matrix.csv"
    df_sens.round(2).to_csv(out_sens, index=False)
    print(f"[OK] CAC Sensitivity Matrix -> {out_sens}")
    print("\nRingkasan Model Finansial:")
    print(df_ue[["business_model", "package_price_idr", "contribution_margin_idr", "bep_monthly_events", "bep_status"]].to_string(index=False))
