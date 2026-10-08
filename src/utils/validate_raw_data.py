"""Validasi data RAW (Milestone 1). Jalankan: python src/utils/validate_raw_data.py

Cek: skema, nilai kosong, konsistensi aritmetika, rentang wajar, dan status verifikasi.
Exit code 1 jika ada pelanggaran ERROR.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

RAW = Path(__file__).resolve().parents[2] / "data" / "01_raw"
errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def check_schema(df: pd.DataFrame, cols: list[str], name: str) -> bool:
    missing = set(cols) - set(df.columns)
    if missing:
        err(f"[{name}] kolom hilang: {sorted(missing)}")
    return not missing


# ---------- 1. competitor_pricing ----------
cp = pd.read_csv(RAW / "market_benchmark" / "competitor_pricing.csv")
if check_schema(cp, ["competitor", "market", "package", "max_guests", "price_idr_current",
                     "price_per_guest_idr", "tier_status", "data_status"], "competitor_pricing"):
    if (cp["market"] != "Indonesia").any():
        err("[competitor_pricing] ada baris non-Indonesia (di luar lingkup)")
    if cp.duplicated(["competitor", "package"]).any():
        err("[competitor_pricing] duplikat (competitor, package)")
    sat = cp[(cp.competitor == "Satualbum.id") & cp.max_guests.notna() & (cp.max_guests < 9999)
             & (cp.price_idr_current > 0)]
    calc = (sat.price_idr_current / sat.max_guests).round()
    bad = sat[(calc - sat.price_per_guest_idr).abs() > 1]
    if len(bad):
        err(f"[competitor_pricing] price_per_guest tidak konsisten: {bad.package.tolist()}")
    paid = cp[cp.price_idr_current.fillna(0) > 0]
    if (paid.price_idr_current % 1000 != 0).any():
        warn("[competitor_pricing] ada harga yang bukan kelipatan Rp1.000")
    normal = cp.dropna(subset=["price_idr_normal", "price_idr_current"])
    if (normal.price_idr_normal < normal.price_idr_current).any():
        err("[competitor_pricing] harga normal < harga saat ini")
    active = cp[cp.tier_status.str.startswith("active")]
    sat_active = active[active.competitor == "Satualbum.id"].sort_values("max_guests")
    if not sat_active.price_idr_current.is_monotonic_increasing:
        err("[competitor_pricing] harga tier aktif Satualbum tidak naik monoton")
    unverified = cp[cp.data_status.str.contains("TO_VERIFY", na=False)]
    for _, r in unverified.iterrows():
        warn(f"[competitor_pricing] belum terverifikasi: {r.competitor} - {r.package}")
    n_comp = active[active.price_idr_current.notna() & (active.price_idr_current > 0)].competitor.nunique()
    if n_comp < 3:
        warn(f"[competitor_pricing] hanya {n_comp} kompetitor ber-harga di lingkup Indonesia (disarankan >=3)")

# ---------- 2. cloud_cost_parameters ----------
cc = pd.read_csv(RAW / "cloud_cost_models" / "cloud_cost_parameters.csv")
if check_schema(cc, ["category", "item", "value", "unit", "source", "data_status"], "cloud_cost"):
    required = ["Midtrans QRIS", "Midtrans GoPay", "Midtrans Virtual Account",
                "AWS S3 Standard ap-southeast-3", "AWS Data Transfer Out to Internet", "USD to IDR",
                "Foto per event (min)", "Foto per event (max)", "Ukuran rata-rata per foto",
                "Rasio guest view/download terhadap storage", "Masa retensi album"]
    for item in required:
        if item not in set(cc["item"]):
            err(f"[cloud_cost] parameter wajib hilang: {item}")
    v = cc.set_index("item")["value"]
    if "Foto per event (min)" in v and v["Foto per event (min)"] >= v["Foto per event (max)"]:
        err("[cloud_cost] foto min >= max")
    for item in ("Midtrans QRIS", "Midtrans GoPay"):
        if item in v and not 0 < v[item] < 0.1:
            err(f"[cloud_cost] {item} di luar rentang wajar (0-10%)")
    if "USD to IDR" in v and not 10_000 < v["USD to IDR"] < 25_000:
        err("[cloud_cost] kurs USD/IDR di luar rentang wajar")
    gb_min = v["Foto per event (min)"] * v["Ukuran rata-rata per foto"] / 1024
    gb_max = v["Foto per event (max)"] * v["Ukuran rata-rata per foto"] / 1024
    if not (1 <= gb_min and gb_max <= 12):
        warn(f"[cloud_cost] ukuran data/event {gb_min:.1f}-{gb_max:.1f} GB; README menyebut 3-8 GB")
    for _, r in cc[cc.data_status == "ASSUMPTION"].iterrows():
        warn(f"[cloud_cost] ASUMSI (belum data riil): {r['item']} = {r.value}")

# ---------- 3. wedding_demographics ----------
wd = pd.read_csv(RAW / "wedding_event_demographics" / "wedding_demographics.csv")
if check_schema(wd, ["year", "region", "weddings", "source", "data_status"], "wedding_demographics"):
    if wd.duplicated(["year", "region"]).any():
        err("[wedding_demographics] duplikat (year, region)")
    if (wd.weddings <= 0).any():
        err("[wedding_demographics] nilai pernikahan <= 0")
    nat = wd[wd.region == "Indonesia"].set_index("year").weddings.sort_index()
    if not nat.is_monotonic_decreasing:
        warn("[wedding_demographics] tren nasional tidak turun monoton (cek data)")
    for yr in wd.year.unique():
        prov = wd[(wd.year == yr) & (wd.region != "Indonesia")].weddings.sum()
        if yr in nat.index and prov > nat[yr]:
            err(f"[wedding_demographics] jumlah provinsi {yr} melebihi nasional")
    if len(nat) >= 2:
        yoy = nat.pct_change().dropna() * 100
        print("YoY nasional (%):", yoy.round(1).to_dict())
    print(f"Pernikahan nasional terbaru: {nat.iloc[-1]:,} ({nat.index[-1]})")

# ---------- laporan ----------
print(f"\nERROR  : {len(errors)}")
for e in errors:
    print("  X", e)
print(f"WARNING: {len(warnings)}")
for w in warnings:
    print("  !", w)
sys.exit(1 if errors else 0)
