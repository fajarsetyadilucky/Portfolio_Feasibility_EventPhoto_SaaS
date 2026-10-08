# 🖥️ Power BI Dashboard Specification & Wireframes: Investment Feasibility & Risk Simulation
**Industry:** Event-Tech B2B2C SaaS (QR Event Photo Album)  
**Target Audience:** Angel Investor, Founder, Financial Advisory Committee  
**Core Purpose:** Pre-Seed Capital Allocation Decision (Go / No-Go)  

---

## 🗄️ 1. Power BI Data Model Architecture (Star Schema)

* **Fact Tables:**
  * `fact_monte_carlo_runs`: 1.000 baris hasil simulasi stokastik (NPV, Cashflow, Status Profit, Skenario).
  * `fact_cloud_cost_projections`: Proyeksi akumulasi biaya storage S3 & egress per bulan.
  * `fact_monthly_cashflow_base`: Proyeksi arus kas 24 bulan skenario Base Case.
* **Dimension Tables:**
  * `dim_pricing_tiers`: Paket Basic (Rp150k), Standard (Rp250k), Pro B2B Agency (Rp450k).
  * `dim_market_segments`: B2C (Pengantin Langsung) vs B2B (Wedding Organizer / Studio Partner).
  * `dim_date`: Kalender waktu proyeksi 24 bulan.
* **What-If Parameter Tables (Power BI Parameter Generators):**
  * `param_package_price`: Slider Harga Paket (Rp100.000 s/d Rp500.000).
  * `param_monthly_events`: Slider Target Event Bulanan (10 s/d 150 event).
  * `param_cac`: Slider Biaya Akuisisi Iklan per Pelanggan (Rp30.000 s/d Rp180.000).

---

## 📑 2. Dashboard Page Architecture

### 📊 Page 1: Executive Feasibility & Go / No-Go Decision Card
* **Header / Executive Status:**
  * **Dynamic Decision Banner (Card with Conditional Color):**
    * Teks: `[Go No-Go Status]` (Warna Hijau jika GO, Kuning jika Conditional, Merah jika NO-GO).
* **Top Metric Scorecards:**
  * `Estimated CapEx`: Rp75.000.000 (Biaya R&D Pembuatan Platform Awal)
  * `Break-Even Event Run-Rate`: 28 Event / Bulan
  * `Payback Period Horizon`: 11.4 Bulan (Skenario Base)
  * `Probability of Success (12m)`: 72.4% (Hasil Monte Carlo)
* **Main Visualizations:**
  1. **Cumulative Net Cash Flow & Payback Cross (Area/Line Combo Chart):** Grafik kurva modal dari defisit -Rp75jt hingga menembus garis impas (Break-Even Line) di bulan ke-11.
  2. **Market Sizing TAM-SAM-SOM Funnel (Funnel Visual):** 
     * TAM: 1.800.000 Pernikahan Indonesia
     * SAM: 250.000 Pernikahan Perkotaan
     * SOM Target: 1.250 Event/Tahun (0.5% Penetrasi).
  3. **Strategic Verdict Summary Matrix:** Tabel ringkasan 3 skenario: B2C Murni (NO-GO) vs Hybrid (CONDITIONAL) vs B2B Partnership (GO).

---

### ☁️ Page 2: Unit Economics & Cloud Cost Diagnostic
* **Header / Slicers:** Model Bisnis (B2C vs B2B Vendor Partner), Pilihan Kuota Foto per Event.
* **Top Metric Cards:**
  * `Gross Revenue per Unit`: Rp250.000
  * `Variable Cloud + Payment Fee`: Rp22.500 (9.0% dari harga)
  * `Blended CAC`: Rp95.000 (B2C) vs Rp25.000 (B2B Partner)
  * `True Contribution Margin %`: 53.0% (B2C) vs 81.0% (B2B)
* **Main Visualizations:**
  1. **Waterfall Margin Breakdown (Waterfall Chart):** Menunjukkan pengurangan dari Harga Paket Rp250k $\rightarrow$ dikurangi Payment Fee (-Rp7.750) $\rightarrow$ dikurangi Storage S3 (-Rp14.750) $\rightarrow$ dikurangi CAC Marketing (-Rp95.000) $\rightarrow$ Sisa Net Margin.
  2. **Cumulative Cloud Storage Liability (Stacked Bar Chart):** Simulasi akumulasi biaya penyimpanan cloud AWS S3 selama 24 bulan jika foto disimpan selamanya vs jika diterapkan limit retensi 6 bulan.
  3. **Sensitivity Table (Matrix):** Matriks harga paket (sumbu baris) vs estimasi CAC (sumbu kolom) dengan *conditional color formatting* (merah = rugi, hijau = untung).

---

### 🎲 Page 3: Monte Carlo Risk Simulator & What-If Sandbox
* **Header / Interactive Sliders:**
  * 🎚️ **Slider 1: Harga Paket Penjualan (Rp)**
  * 🎚️ **Slider 2: Target Penjualan Event / Bulan**
  * 🎚️ **Slider 3: Realisasi Biaya Iklan (CAC) per Event**
* **Top Dynamic KPI Cards (Otomatis berubah mengikuti slider):**
  * `Dynamic Monthly Profit`: Rp14.250.000 / bulan
  * `Dynamic Payback Horizon`: 9.2 Bulan
  * `Simulated 24-Month Net ROI`: +118.5%
* **Main Visualizations:**
  1. **Monte Carlo Probability Density Distribution (Histogram / Area Chart):** Distribusi kurva lonceng (Bell Curve) dari 1.000 hasil simulasi laba bersih. Garis batas merah menandakan persentase skenario yang mengalami kerugian (*Value at Risk*).
  2. **Cumulative Probability Curve (S-Curve):** Kurva probabilitas kumulatif untuk menjawab pertanyaan investor: *"Berapa peluang proyek ini menghasilkan minimal Rp50 juta profit dalam 2 tahun?"*.
  3. **Scenario Switcher Matrix (Table):** Tabel perbandingan instan skenario Bearish (-20%), Base Case, dan Bullish (+30%).
