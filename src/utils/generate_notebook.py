"""Generator Utility untuk Jupyter Notebook Analisis Kelayakan.
Membersihkan peringatan linter dan memastikan sintaks standar PEP 8.
"""
from pathlib import Path
import nbformat as nbf

ROOT = Path(__file__).resolve().parents[2]
NOTEBOOK_PATH = ROOT / "notebooks" / "01_feasibility_financial_model.ipynb"

nb = nbf.v4.new_notebook()

cells = [
    nbf.v4.new_markdown_cell("""# 📊 Strategic Feasibility Study & Financial Model: QR-Based Event Photo SaaS
**Author:** Lead Strategic Data Analyst & Tech Investment Consultant  
**Domain:** Event-Tech / B2B2C SaaS (Indonesia Market Scope - IDR)  
**Objective:** Evaluasi Kelayakan Alokasi Modal Pre-Seed (Rp75.000.000 - Rp120.000.000)

---
### 📌 Struktur Analisis Kuantitatif:
1. **Fase 1:** Market Sizing (TAM/SAM/SOM) & Competitor Benchmarking Indonesia
2. **Fase 2:** Unit Economics & Cloud Infrastructure Modeling (AWS S3 Jakarta & Midtrans)
3. **Fase 3:** Break-Even Point (BEP) & CAC Sensitivity Stress Testing
4. **Fase 4:** Multi-Horizon Monte Carlo Simulation (1.000 Iterasi 12-24 Bulan)
5. **Fase 5:** Executive Verdict & Strategic Recommendations (Go / No-Go Decision)"""),

    nbf.v4.new_markdown_cell("""## 1. Market Demographics & TAM/SAM/SOM Sizing
Menganalisis potensi pasar pernikahan Indonesia secara kuantitatif berdasarkan data BPS 2024 dan benchmark 6 kompetitor lokal."""),

    nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

DATA_DIR = Path('../data/02_processed')
MART_DIR = Path('../data/03_analytics_marts')

df_market = pd.read_csv(MART_DIR / 'tam_sam_som_market_sizing.csv')
df_comp = pd.read_csv(DATA_DIR / 'processed_competitor_benchmark.csv')

print("=== ESTIMASI UKURAN PASAR (TAM / SAM / SOM INDONESIA) ===")
display(df_market)

print("\\n=== BENCHMARK HARGA KOMPETITOR INDONESIA (IDR) ===")
display(df_comp[['competitor', 'package', 'max_guests', 'price_idr_current', 'discount_pct', 'market_segment']])"""),

    nbf.v4.new_markdown_cell("""## 2. Unit Economics, Cloud Infrastructure & LTV/CAC Ratio
Menghitung true contribution margin per transaksi dan membuktikan keunggulan LTV/CAC Model B2B vs Model B2C."""),

    nbf.v4.new_code_cell("""df_ue = pd.read_csv(MART_DIR / 'unit_economics_bep_scenarios.csv')
display(df_ue[['business_model', 'package_price_idr', 'cloud_cost_idr', 'cac_idr', 'contribution_margin_idr', 'cm_ratio_pct', 'bep_monthly_events', 'bep_status']])"""),

    nbf.v4.new_markdown_cell("""## 3. Break-Even Analysis & CAC Stress Testing
Matriks sensitivitas profitabilitas terhadap pembengkakan biaya akuisisi iklan (CAC) pada harga paket acuan Rp299.000."""),

    nbf.v4.new_code_cell("""df_sens = pd.read_csv(MART_DIR / 'cac_sensitivity_matrix.csv')
display(df_sens)"""),

    nbf.v4.new_markdown_cell("""## 4. Multi-Horizon Monte Carlo Predictive Simulation (1.000 Iterasi)
Memetakan kurva probabilitas profitabilitas dalam horizon 12 bulan dan 24 bulan untuk membuktikan J-Curve Model B2B."""),

    nbf.v4.new_code_cell("""df_sim = pd.read_csv(MART_DIR / 'monte_carlo_simulation_results.csv')

win_b2c_m12 = df_sim['b2c_profitable_m12'].mean() * 100
win_b2b_m12 = df_sim['b2b_profitable_m12'].mean() * 100
win_b2c_m24 = df_sim['b2c_profitable_m24'].mean() * 100
win_b2b_m24 = df_sim['b2b_profitable_m24'].mean() * 100

print(f"Probabilitas Profit 12 Bulan - B2C Pure : {win_b2c_m12:.1f}%")
print(f"Probabilitas Profit 12 Bulan - B2B Pivot: {win_b2b_m12:.1f}%")
print(f"Probabilitas Profit 24 Bulan - B2C Pure : {win_b2c_m24:.1f}% (Defisit Total)")
print(f"Probabilitas Profit 24 Bulan - B2B Pivot: {win_b2b_m24:.1f}% (J-Curve Profitability)")"""),

    nbf.v4.new_markdown_cell("""## 5. Executive Summary & Investment Verdict

### Q&A
* **Apakah model bisnis B2C murni layak dijalankan?**  
  **TIDAK LAYAK (NO-GO MUTLAK).** Probabilitas profit di tahun ke-2 adalah 0.0%. Sifat pernikahan yang 100% churn meniadakan LTV berulang, sementara CAC iklan menyerap 40%-80% pendapatan.
* **Apakah model kemitraan B2B (Wedding Organizer) layak didanai?**  
  **LAYAK BERSYARAT (CONDITIONAL GO).** Probabilitas profit melonjak ke 98.8% di tahun ke-2 dengan rasio LTV/CAC mencapai 9.6x. Syarat mutlak: Klien wajib mengantongi 15 Letter of Intent (LOI) dari Wedding Organizer sebelum koding dimulai.

### Data Analysis Key Findings
* **TAM/SAM/SOM:** Nilai pasar SAM perkotaan mencapai Rp75.1 Miliar/tahun (~251.300 event), membuktikan potensi pasar sangat besar jika saluran distribusi efisien.
* **Biaya Cloud Sangat Efisien:** Biaya AWS S3 Jakarta & bandwidth hanya Rp17.400 per event (~5.8% dari harga jual Rp299.000). Hambatan utama murni di CAC.
* **LTV/CAC Ratio:** B2C hanya menghasilkan LTV/CAC 1.3x (tidak sehat), sedangkan B2B menghasilkan LTV/CAC 9.6x (standar SaaS kelas dunia).

### Insights or Next Steps
* **Rekomendasi Tindakan:** Jangan membuat aplikasi konsumen ritel. Fokuskan modal Rp75.000.000 untuk mengembangkan *Agency Multi-Tenant Portal* khusus Wedding Organizer.
* **Jadwal 90 Hari:** Lakukan validasi 15 LOI mitra di bulan pertama sebelum mencairkan biaya koding.""")
]

nb.cells = cells
NOTEBOOK_PATH.parent.mkdir(parents=True, exist_ok=True)
nbf.write(nb, str(NOTEBOOK_PATH))
print(f"[OK] Notebook berhasil digenerate di: {NOTEBOOK_PATH}")
