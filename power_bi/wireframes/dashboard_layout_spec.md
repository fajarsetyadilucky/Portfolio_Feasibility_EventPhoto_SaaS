# 📱 Power BI Dashboard Blueprint: 3-Page Executive Feasibility Architecture

Dokumen ini mendefinisikan struktur tata letak (wireframe), arsitektur model data, dan panduan visualisasi untuk laporan Power BI (*3-Page Interactive Report*).

---

## 🗺️ Skema Model Data (Star Schema)

```text
       [Dim_Calendar]
              │
              ▼ (1:N)
    [Fact_Transactions] ◄─── (1:N) ─── [Dim_BusinessModel]
              ▲
              │ (1:N)
       [Dim_Competitor]

    [Fact_MonteCarlo] (1.000 Iterasi Skenario - Standalone Fact)
```

---

## 📑 Halaman 1: Executive Summary & Unit Economics
**Tujuan:** Memberikan gambaran ringkas tentang kelayakan produk per unit transaksi dan struktur margin.

* **Header KPI Cards (4 Kolom):**
  1. `Gross Contribution Margin %` (Target > 70%)
  2. `CAC as % of Revenue` (B2C ~40% vs B2B ~8%)
  3. `Monthly BEP Target Volume` (32 Events / Month)
  4. `Pre-Seed CapEx Budget` (Rp75.000.000)
* **Visual Utama (Kiri):** *Waterfall Chart* — Dekomposisi Pendapatan Paket Rp299.000 dikurangi Biaya Cloud AWS S3, Egress, Payment Gateway Fee, dan CAC hingga Contribution Margin bersih.
* **Visual Utama (Kanan):** *Line & Clustered Column Chart* — Kurva Titik Impas (BEP Curve): Volume Event (5 - 60 event) vs Total Revenue vs Total Operating Cost.
* **Tabel Bawah:** Tabel komparasi Model A (B2C Pure) vs Model B (B2B Partner) pada rentang harga Rp79rb sd Rp599rb.

---

## 🎲 Halaman 2: Monte Carlo Predictive Simulation & Risk Modeling
**Tujuan:** Menampilkan hasil 1.000 skenario acak selama 12 bulan dan probabilitas kelangsungan hidup kas.

* **Top KPI Cards (Win-Rate):**
  * `B2C 12-Month Win-Rate:` **6,9%** (Merah / Warning)
  * `B2B 12-Month Win-Rate:` **47,3%** (Hijau / Viable)
  * `Median Net Profit B2B:` **-Rp683.560**
  * `Value at Risk (VaR 95%):` **-Rp20.507.255**
* **Visual Kiri:** *Histogram / Area Chart* — Distribusi Normal Net Profit Kumulatif B2C vs B2B dengan garis vertikal $x = 0$ (Garis Titik Impas).
* **Visual Kanan:** *Multi-Line Chart* — Spaghetti Plot (Proyeksi 50 lintasan saldo kas bulanan terhadap batas modal awal Rp75.000.000).
* **Filter Slicer:** Skenario CAC (Rp80rb - Rp180rb) dan Horizon Waktu (12 Bulan).

---

## 🏢 Halaman 3: Market Demographics & Competitor Benchmarking
**Tujuan:** Menyajikan lanskap pasar makro Indonesia dan peta persaingan harga lokal.

* **Visual Kiri Atas:** *Clustered Bar Chart* — Tren Penurunan Peristiwa Nikah BPS 2022–2024 (1,71 Juta -> 1,48 Juta) dengan persentase penurunan tahunan (-7,5% & -6,3%).
* **Visual Kanan Atas:** *Scatter Plot* — Peta Posisi Harga Kompetitor Indonesia: Kapasitas Tamu ($X$) vs Harga Paket ($Y$) yang membedakan pemain *Direct Disposable* (Satualbum, Kurinji) vs *Substitusi On-site* (Fotoimoet, Viding, Invitato).
* **Visual Bawah:** Matriks Strategi Harga & Rekomendasi Titik Masuk Pasar (Price-Point Positioning).
