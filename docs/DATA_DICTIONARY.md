# 📖 Data Dictionary & Schema Documentation

Dokumen ini mendokumentasikan skema data, tipe data, sumber data, dan deskripsi bisnis dari seluruh dataset yang digunakan dalam **Portfolio Feasibility Study & Predictive Investment Analysis: QR-Based Event Photo SaaS**.

---

## 🗂️ Struktur Data Layer

Data pipeline dalam proyek ini mengadopsi standar arsitektur **Medallion / Tiered Layering**:
* **Layer 1 - Bronze / Raw (`data/01_raw/`):** Data mentah asli hasil riset pasar, parameter tarif resmi AWS & Midtrans, dan statistik demografi BPS.
* **Layer 2 - Silver / Processed (`data/02_processed/`):** Data hasil standardisasi tipe data, penyesuaian kurs Rupiah, klasifikasi fitur bisnis, dan validasi aritmetika.
* **Layer 3 - Gold / Analytics Marts (`data/03_analytics_marts/`):** Tabel agregasi analitik siap konsumsi untuk Power BI, Streamlit, dan Notebook.
* **Layer 4 - Enterprise Data Model (`power_bi/Feasibility_Study_DataModel_Master.xlsx`):** Konsolidasi seluruh tabel fakta dan dimensi untuk Power BI.

---

## 🥉 Layer 1: Raw Datasets (`data/01_raw/`)

### 1.1 `market_benchmark/competitor_pricing.csv`
Tabel komparasi harga dan spesifikasi kompetitor kamera digital sekali pakai dan photobooth di Indonesia.

| Nama Kolom | Tipe Data | Keterangan Bisnis | Contoh Nilai |
| :--- | :--- | :--- | :--- |
| `competitor` | String | Nama merek/entitas kompetitor | `Satualbum.id`, `Kenang Kurinji`, `Fotoimoet` |
| `product_type` | String | Jenis layanan produk | `direct digital disposable`, `photobooth` |
| `market` | String | Lingkup geografis target | `Indonesia` |
| `package` | String | Nama paket ritel | `Regular`, `Unlimited Guest`, `Standard Booth` |
| `max_guests` | Integer | Kuota maksimal tamu/pemindai QR | `200`, `500`, `9999` (unlimited) |
| `photos_limit` | Integer | Batas maksimal foto yang dapat diunggah | `500`, `1000`, `9999` |
| `price_idr_current` | Float | Harga jual paket aktif (IDR) | `299000`, `79000`, `1800000` |
| `price_idr_normal` | Float | Harga coret / harga sebelum diskon (IDR) | `399000`, `null` |
| `price_per_guest_idr` | Float | Rasio harga per kuota tamu (IDR/guest) | `1495`, `158` |
| `tier_status` | String | Status ketersediaan paket | `active_direct`, `active_hardware` |
| `source_url` | String | Tautan referensi publikasi | `https://satualbum.id/pricing` |
| `data_status` | String | Status validasi data | `verified`, `TO_VERIFY` |

### 1.2 `cloud_cost_models/cloud_cost_parameters.csv`
Parameter teknis biaya penyimpanan cloud AWS, egress bandwidth, dan MDR Payment Gateway Midtrans.

| Nama Kolom | Tipe Data | Keterangan Bisnis | Contoh Nilai |
| :--- | :--- | :--- | :--- |
| `category` | String | Kategori beban biaya | `payment_gateway`, `cloud_storage`, `fx`, `usage` |
| `item` | String | Nama item spesifik | `Midtrans QRIS`, `AWS S3 Standard ap-southeast-3` |
| `value` | Float | Nilai parameter numerik | `0.007`, `0.025`, `16500.0`, `500.0` |
| `unit` | String | Satuan pengukuran | `fraction of transaction`, `USD per GB-month`, `MB` |
| `source` | String | Sumber rujukan data | `midtrans.com/pricing`, `AWS Price List API` |
| `data_status` | String | Status kepastian parameter | `verified`, `ASSUMPTION` |

### 1.3 `wedding_event_demographics/wedding_demographics.csv`
Statistik resmi jumlah pernikahan per tahun berdasarkan publikasi Badan Pusat Statistik (BPS) Republik Indonesia.

| Nama Kolom | Tipe Data | Keterangan Bisnis | Contoh Nilai |
| :--- | :--- | :--- | :--- |
| `year` | Integer | Tahun pencatatan sensus | `2022`, `2023`, `2024` |
| `region` | String | Wilayah provinsi atau cakupan nasional | `Indonesia`, `Jawa Barat`, `DKI Jakarta` |
| `weddings` | Integer | Jumlah peristiwa pernikahan resmi tercatat | `1478302`, `317715`, `47327` |
| `source` | String | Dokumen rujukan BPS | `BPS Statistik Indonesia 2024` |
| `data_status` | String | Status verifikasi | `verified` |

---

## 🥈 Layer 2: Processed Datasets (`data/02_processed/`)

### 2.1 `processed_competitor_benchmark.csv`
Data kompetitor yang telah dilengkapi fitur segmentasi pasar (`market_segment`), diskon moneter (`discount_amount_idr`), dan persentase diskon (`discount_pct`).

### 2.2 `processed_cloud_cost_parameters.csv`
Parameter biaya operasional yang telah dikonversi secara terstandarisasi ke denominasi Rupiah (`value_idr_or_standard`).

### 2.3 `processed_wedding_demographics.csv`
Data demografi BPS yang telah diperkaya metrik tren tahunan (*Year-over-Year Growth* / `yoy_growth_pct`).

---

## 🥇 Layer 3: Analytics Marts (`data/03_analytics_marts/`)

### 3.1 `tam_sam_som_market_sizing.csv`
Piramida estimasi potensi pasar pernikahan Indonesia dan penetrasi target bisnis.

| Nama Kolom | Tipe Data | Keterangan Bisnis |
| :--- | :--- | :--- |
| `tier` | String | Tingkatan pasar (`TAM`, `SAM`, `SOM Tahun 1`, `SOM Tahun 2`) |
| `scope` | String | Lingkup deskriptif kelompok pasar |
| `annual_volume_events` | Integer | Estimasi kuantitas acara pernikahan per tahun |
| `annual_market_value_idr` | Float | Estimasi nilai perputaran moneter pasar (IDR) |
| `pct_of_tam` | Float | Proporsi persentase terhadap TAM (%) |
| `benchmark_basis` | String | Dasar asumsi metodologis |

### 3.2 `unit_economics_bep_scenarios.csv`
Simulasi margin kontribusi dan kuantitas titik impas (BEP) bulanan untuk berbagai skenario harga paket dan model bisnis.

| Nama Kolom | Tipe Data | Keterangan Bisnis |
| :--- | :--- | :--- |
| `business_model` | String | Model bisnis (`Model A (B2C Pure)` vs `Model B (B2B WO Partner)`) |
| `package_price_idr` | Float | Harga paket ritel acuan (IDR) |
| `revenue_per_event_idr` | Float | Pendapatan bersih platform per acara (IDR) |
| `cloud_cost_idr` | Float | Biaya komputasi AWS S3 dan data transfer per acara (IDR) |
| `pg_fee_idr` | Float | Estimasi fee payment gateway campuran per acara (IDR) |
| `cac_idr` | Float | Beban Customer Acquisition Cost per transaksi (IDR) |
| `gross_margin_idr` | Float | Laba kotor per unit sebelum CAC (IDR) |
| `contribution_margin_idr` | Float | Margin kontribusi riil per unit setelah CAC (IDR) |
| `cm_ratio_pct` | Float | Rasio margin kontribusi terhadap pendapatan (%) |
| `cac_ratio_pct` | Float | Rasio beban CAC terhadap pendapatan (%) |
| `bep_monthly_events` | Float | Kuantitas transaksi/acara per bulan untuk menutup OpEx tetap |
| `bep_status` | String | Status kelayakan matematis (`Viable` vs `Infeasible`) |

### 3.3 `cac_sensitivity_matrix.csv`
Matriks uji stres sensitivitas dampak kenaikan biaya iklan Meta/TikTok terhadap laba operasional bulanan pada berbagai skala volume acara (15 hingga 100 acara/bulan).

### 3.4 `monte_carlo_simulation_results.csv`
Hasil komputasi 1.000 iterasi stokastik simulasi Monte Carlo untuk horizon 12 bulan dan 24 bulan.

| Nama Kolom | Tipe Data | Keterangan Bisnis |
| :--- | :--- | :--- |
| `simulation_id` | Integer | Nomor identifikasi skenario (1 s/d 1.000) |
| `b2c_profit_m12` | Float | Kumulatif laba bersih Model B2C pada akhir Bulan 12 (IDR) |
| `b2b_profit_m12` | Float | Kumulatif laba bersih Model B2B pada akhir Bulan 12 (IDR) |
| `b2c_profit_m24` | Float | Kumulatif laba bersih Model B2C pada akhir Bulan 24 (IDR) |
| `b2b_profit_m24` | Float | Kumulatif laba bersih Model B2B pada akhir Bulan 24 (IDR) |
| `b2c_profitable_m12` | Boolean | Apakah Model B2C membukukan laba positif di M12? |
| `b2b_profitable_m12` | Boolean | Apakah Model B2B membukukan laba positif di M12? |
| `b2c_profitable_m24` | Boolean | Apakah Model B2C membukukan laba positif di M24? |
| `b2b_profitable_m24` | Boolean | Apakah Model B2B membukukan laba positif di M24? |
| `b2c_depleted` | Boolean | Indikator kehabisan modal kas (*runway depletion*) B2C |
| `b2b_depleted` | Boolean | Indikator kehabisan modal kas (*runway depletion*) B2B |

### 3.5 `monte_carlo_monthly_trajectories.csv`
Lintasan saldo kas bulanan (bulan 1 hingga 24) dari 50 skenario acak untuk memetakan kurva *J-Curve* kas operasional.

---

## 🏛️ Power BI Master Model Sheets (`power_bi/Feasibility_Study_DataModel_Master.xlsx`)

File Excel ini bertindak sebagai database sumber untuk Power BI Desktop:
1. `Fact_UnitEconomics_BEP` ➔ Tabel fakta unit economics dan skenario BEP.
2. `Fact_MonteCarlo_Simulations` ➔ Tabel fakta 1.000 hasil simulasi stokastik.
3. `Fact_Monthly_Cashflow_Paths` ➔ Tabel fakta lintasan kas bulanan 24 bulan.
4. `Dim_Competitor_Benchmark` ➔ Tabel dimensi peta kompetitor lokal.
5. `Dim_Wedding_Demographics` ➔ Tabel dimensi data tren pernikahan BPS.
6. `Dim_Market_Sizing` ➔ Tabel dimensi hierarki TAM, SAM, SOM.
7. `Dim_CAC_Sensitivity` ➔ Tabel dimensi sensitivitas biaya iklan.
