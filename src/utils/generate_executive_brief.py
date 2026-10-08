import os
from pathlib import Path
import win32com.client

ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

html_file = REPORTS_DIR / "Ringkasan_Eksekutif_Feasibility_Dashboard.html"
docx_file = REPORTS_DIR / "Ringkasan_Eksekutif_Feasibility_Dashboard.docx"
pdf_file  = REPORTS_DIR / "Ringkasan_Eksekutif_Feasibility_Dashboard.pdf"
md_file   = REPORTS_DIR / "Ringkasan_Eksekutif_Feasibility_Dashboard.md"

html_content = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Executive Briefing: Kelayakan Investasi Event Photo SaaS</title>
<style>
    body {
        font-family: 'Calibri', 'Segoe UI', Arial, sans-serif;
        margin: 36px 48px;
        color: #1e293b;
        line-height: 1.5;
        font-size: 11pt;
    }
    h1 {
        color: #0f172a;
        font-size: 19pt;
        border-bottom: 2px solid #2563eb;
        padding-bottom: 6px;
        margin-bottom: 2px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .subtitle {
        color: #64748b;
        font-size: 10.5pt;
        margin-top: 2px;
        margin-bottom: 18px;
        font-style: italic;
    }
    .verdict-banner {
        background-color: #f0fdf4;
        border: 2px solid #16a34a;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 20px;
    }
    .badge {
        background-color: #16a34a;
        color: white;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 9.5pt;
        display: inline-block;
        margin-bottom: 6px;
    }
    h2 {
        color: #1e3a8a;
        font-size: 13pt;
        border-left: 4px solid #2563eb;
        padding-left: 10px;
        margin-top: 22px;
        margin-bottom: 10px;
    }
    h3 {
        color: #0284c7;
        font-size: 11.5pt;
        margin-top: 14px;
        margin-bottom: 6px;
    }
    p {
        margin-top: 4px;
        margin-bottom: 8px;
        text-align: justify;
    }
    ul {
        margin-top: 4px;
        margin-bottom: 12px;
        padding-left: 22px;
    }
    li {
        margin-bottom: 6px;
    }
    .highlight-box {
        background-color: #eff6ff;
        border: 1px solid #bfdbfe;
        border-left: 4px solid #3b82f6;
        border-radius: 6px;
        padding: 12px 14px;
        margin: 14px 0;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 14px 0;
        font-size: 10pt;
    }
    th {
        background-color: #1e3a8a;
        color: white;
        padding: 8px 10px;
        text-align: left;
    }
    td {
        border: 1px solid #cbd5e1;
        padding: 7px 10px;
        vertical-align: top;
    }
    tr:nth-child(even) {
        background-color: #f8fafc;
    }
    .footer-note {
        margin-top: 28px;
        border-top: 1px solid #e2e8f0;
        padding-top: 8px;
        font-size: 8.5pt;
        color: #94a3b8;
        text-align: right;
    }
</style>
</head>
<body>

<h1>Executive Briefing: Kelayakan Investasi Event Photo SaaS</h1>
<p class="subtitle">Dokumen Laporan Resmi Pengambilan Keputusan Strategis Berdasarkan Dashboard Power BI (.PBIX)</p>

<div class="verdict-banner">
    <span class="badge">SINYAL KEPUTUSAN FINAL: &nbsp;GO (SANGAT LAYAK)</span>
    <p style="margin: 4px 0 0 0; font-size: 10.5pt;">
        <b>Kesimpulan Strategis:</b> Bisnis QR-Based Event Photo SaaS terbukti <b>Sangat Layak Didanai</b> dengan modal Pre-Seed <b>Rp 75.000.000</b>. Model ini memiliki margin laba kotor sangat tebal (<b>73.7%</b>) dan potensi kas melimpah hingga <b>Rp 137 Juta di bulan ke-24</b>. <u>Syarat mutlak keberhasilan:</u> Seluruh fokus diarahkan ke kemitraan B2B Wedding Organizer, menetapkan harga paket di Rp 299.000, dan menolak penjualan langsung ke pengantin (B2C).
    </p>
</div>

<h2>BAGIAN 1: PENJELASAN SEDERHANA VISUAL SETIAP HALAMAN DASHBOARD</h2>

<h3>Halaman 1: Struktur Biaya & Titik Impas (Executive & Unit Economics)</h3>
<ul>
    <li><b>4 Kartu KPI Atas:</b> Menampilkan <i>Margin Laba Kotor 73.7%</i> dan <i>Margin Laba Bersih 52.8%</i>. Untuk menutup biaya operasional kantor Rp 5.000.000/bulan, bisnis ini hanya butuh menjual <b>29.3 acara per bulan</b> (~1 acara per hari di seluruh Indonesia). Statusnya dinilai <b>✅ Viable (Sangat Terjangkau)</b>.</li>
    <li><b>Grafik Dekomposisi Aliran Biaya (Kiri):</b> Memperlihatkan bahwa biaya server cloud AWS S3 sangat murah (hanya <b>Rp 17.400/acara</b>) dan biaya gerbang pembayaran (Midtrans/QRIS) hanya <b>Rp 2.900/acara</b>. Namun, beban terbesar terletak pada biaya iklan akuisisi pelanggan (CAC), yaitu Rp 120.000 di B2C vs hanya Rp 25.000 di B2B.</li>
    <li><b>Grafik Kurva Titik Impas (Kanan):</b> Memperlihatkan bahwa paket murah <b>Rp 79.000 justru merugi (-Rp 23.000 per acara)</b> karena termakan biaya iklan. Sebaliknya, pada paket <b>Rp 299.000</b>, laba melonjak menjadi Rp 152.000 per acara dan target titik impas langsung melandai ke angka yang sangat aman.</li>
    <li><b>Tabel Rekapitulasi (Bawah):</b> Menegaskan perbandingan 10 variasi paket dan membuktikan bahwa paket di atas Rp 199.000 adalah zona aman profitabilitas.</li>
</ul>

<h3>Halaman 2: Uji Stres Monte Carlo & Ketahanan Kas 24 Bulan (Risk Simulation)</h3>
<ul>
    <li><b>4 Kartu KPI Win-Rate:</b> Peluang untung model B2C di tahun pertama adalah <b>0.0%</b> (pasti defisit). Sebaliknya, model B2B memiliki peluang untung <b>27.2%</b> di tahun pertama dan melonjak drastis ke <b>98.8%</b> di tahun ke-2 dengan median laba bersih <b>+Rp 64 Juta</b>.</li>
    <li><b>Grafik Proyeksi Saldo Kas 24 Bulan (Kiri):</b> Garis merah B2C terus merosot dari Rp 72M ke Rp 40M (modal terbakar habis). Sementara garis biru B2B membentuk kurva <i>J-Curve</i>: sempat turun tipis di bulan ke 6-7 ke titik terendah Rp 59M, lalu berbalik naik menembus modal awal Rp 75M di bulan ke-14, dan mencapai <b>Rp 137 Juta di bulan ke-24</b>.</li>
    <li><b>Grafik Mesin Pertumbuhan B2B (Kanan):</b> Mengungkapkan rahasia kebangkitan kas B2B: jumlah mitra Wedding Organizer (WO) aktif tumbuh dari 4 menjadi <b>31 mitra</b>, yang otomatis mendongkrak volume acara dari 11 menjadi <b>90 acara per bulan</b> tanpa perlu biaya iklan tambahan.</li>
    <li><b>Tabel Matriks Uji Stres (Bawah):</b> Menunjukkan risiko terburuk (VaR 95%) di tahun pertama: B2C berisiko rugi hingga -Rp 33M, sedangkan B2B di tahun kedua menghasilkan akumulasi kas aman berkat retensi mitra WO.</li>
</ul>

<h3>Halaman 3: Lanskap Pasar Indonesia & Peta Kompetitor (Market Benchmark)</h3>
<ul>
    <li><b>4 Kartu KPI Pasar:</b> Mengukur Total Pasar Nasional (TAM) <b>1.48 Juta pernikahan/tahun</b>, Tren Penurunan Nikah BPS <b>-6.3% YoY</b>, Pasar Perkotaan Modern (SAM) <b>251.000 acara/tahun</b>, dan Target Realistis Tahun 1 (SOM) hanya <b>753 acara</b> (~63 acara/bulan).</li>
    <li><b>Grafik Tren Pernikahan BPS (Kiri):</b> Memperlihatkan penurunan resmi dari 1.71M (2022) ➔ 1.58M (2023) ➔ 1.48M (2024), menegaskan perlunya fokus pada ceruk pasar perkotaan yang melek digital.</li>
    <li><b>Grafik Ranking Harga Kompetitor (Kanan):</b> Memperlihatkan jurang pemisah harga: Pemain photobooth fisik (Fotoimoet, Invitato, Viding) mematok harga jutaan rupiah (<b>Rp 1.4M s/d Rp 2.1M</b>). Sedangkan pemain SaaS QR Foto (Satualbum, Kurinji, produk kita) berada di ratusan ribu (<b>Rp 79K s/d Rp 467K</b>).</li>
    <li><b>Tabel Piramida Ukuran Pasar (Bawah):</b> Menunjukkan bahwa target tahun pertama kita (753 acara) hanya butuh menyerap <b>0.3% dari ceruk pasar perkotaan</b>, target yang sangat realistis untuk dieksekusi.</li>
</ul>

<h2>BAGIAN 2: SINTESIS SATU INSIGHT UTAMA SECARA KESELURUHAN</h2>
<div class="highlight-box">
    <p style="margin: 0 0 6px 0; font-size: 11pt; font-weight: bold; color: #1e3a8a;">
        Benang Merah Ketiga Halaman Dashboard:
    </p>
    <p style="margin: 0 0 8px 0;">
        Bisnis Event Photo SaaS di Indonesia memiliki <b>keunggulan ekonomi unit yang sangat prima (Margin Kotor > 70%)</b> dan <b>peluang disrupsi harga yang masif (7x lebih murah dibanding photobooth fisik)</b>, <u>DENGAN SATU SYARAT MUTLAK:</u> <b>Model Go-To-Market WAJIB mengandalkan kemitraan Wedding Organizer (B2B), dan BUKAN iklan langsung ke pengantin (B2C)</b>.
    </p>
    <p style="margin: 0;">
        Jika modal Pre-Seed Rp 75 Juta dipakai untuk iklan digital B2C, bisnis dipastikan bangkrut (Peluang Laba 0.0%) karena pengantin tidak memiliki retensi belanja (menikah sekali seumur hidup). Namun jika modal difokuskan untuk merekrut 15–20 mitra Wedding Organizer, bisnis memiliki <b>probabilitas kelangsungan hidup 98.8%</b> dan melipatgandakan kas menjadi <b>Rp 137 Juta</b> di bulan ke-24.
    </p>
</div>

<h2>BAGIAN 3: REKOMENDASI STRATEGIS & JAWABAN PERTANYAAN BISNIS UTAMA</h2>
<table>
    <thead>
        <tr>
            <th style="width: 32%;">Pertanyaan Bisnis Utama</th>
            <th>Jawaban Strategis & Rencana Aksi Eksekutif</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><b>1. Apakah bisnis ini layak didanai dengan modal Pre-Seed Rp 75 Juta?</b></td>
            <td>
                <b>SANGAT LAYAK (GO)</b>. Model SaaS murni memiliki skalabilitas tinggi tanpa beban armada kru fisik, margin kontribusi 52.8%, dan titik impas rendah (1 acara/hari). Risiko kehabisan kas mendekati 0% jika menggunakan jalur kemitraan WO.
            </td>
        </tr>
        <tr>
            <td><b>2. Berapa harga paket yang wajib dijual ke pasar?</b></td>
            <td>
                Tetapkan harga paket utama di <b>Rp 299.000</b>. Posisi ini 7x lebih murah dari photobooth konvensional namun tetap menghasilkan laba bersih Rp 152.000/event. <b>Haramkan paket di bawah Rp 199.000</b> karena margin negatif akan menguras modal kerja.
            </td>
        </tr>
        <tr>
            <td><b>3. Bagaimana alokasi modal Pre-Seed Rp 75 Juta yang optimal?</b></td>
            <td>
                • <b>40% (Rp 30.000.000):</b> Pengembangan Web App MVP (Kamera Instan QR, Cloud AWS S3, Pembayaran QRIS Midtrans).<br>
                • <b>40% (Rp 30.000.000):</b> Operasional Akuisisi Mitra WO (B2B Sales Kit, Komisi Mitra 20-25%, Testing Acara Perdana).<br>
                • <b>20% (Rp 15.000.000):</b> Cadangan Kas Penahan (Cash Runway Buffer untuk melewati lembah kas di bulan ke 6-7).
            </td>
        </tr>
        <tr>
            <td><b>4. Apa target operasional kunci di Tahun Pertama?</b></td>
            <td>
                Kunci kemitraan dengan <b>15–20 Wedding Organizer aktif</b> di wilayah Jabodetabek dan Bandung untuk mengamankan <b>753 acara per tahun</b> (~63 acara/bulan).
            </td>
        </tr>
    </tbody>
</table>

<div class="footer-note">
    Dokumen Laporan Eksekutif Resmi • Portfolio Feasibility Study Event Photo SaaS Indonesia • File PBIX: Feasibility dasboard.pbix
</div>

</body>
</html>
"""

# 1. Write HTML
with open(html_file, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"HTML generated: {html_file}")

# 2. Convert to DOCX and PDF using Word COM
try:
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    doc = word.Documents.Open(str(html_file))
    
    # 16 = wdFormatXMLDocument (.docx)
    doc.SaveAs2(str(docx_file), 16)
    print(f"DOCX generated: {docx_file}")
    
    # 17 = wdFormatPDF (.pdf)
    doc.SaveAs2(str(pdf_file), 17)
    print(f"PDF generated: {pdf_file}")
    
    doc.Close()
    word.Quit()
except Exception as e:
    print(f"Word COM Conversion Error: {e}")

# 3. Also write a clean Markdown version
md_content = """# 📋 EXECUTIVE BRIEFING: KELAYAKAN INVESTASI EVENT PHOTO SAAS
**Dokumen Laporan Resmi Pengambilan Keputusan Strategis Berdasarkan Dashboard Power BI (.PBIX)**  
**Status Keputusan:** ✅ **GO (SANGAT LAYAK DIDANAI)**

---

## 📌 RINGKASAN EKSEKUTIF SINGKAT
Bisnis QR-Based Event Photo SaaS terbukti **Sangat Layak Didanai** dengan modal Pre-Seed **Rp 75.000.000**. Model ini memiliki margin laba kotor sangat tebal (**73.7%**) dan potensi kas melimpah hingga **Rp 137 Juta di bulan ke-24**.  
**Syarat mutlak keberhasilan:** Seluruh fokus diarahkan ke kemitraan B2B Wedding Organizer, menetapkan harga paket di **Rp 299.000**, dan menolak penjualan langsung ke pengantin (B2C).

---

## 🔍 BAGIAN 1: PENJELASAN SEDERHANA VISUAL SETIAP HALAMAN DASHBOARD

### Halaman 1: Struktur Biaya & Titik Impas (Executive & Unit Economics)
* **4 Kartu KPI Atas:** Menampilkan *Margin Laba Kotor 73.7%* dan *Margin Laba Bersih 52.8%*. Untuk menutup biaya operasional kantor Rp 5 Juta/bulan, bisnis hanya butuh menjual **29.3 acara/bulan** (~1 acara/hari). Statusnya: **✅ Viable (Sangat Terjangkau)**.
* **Grafik Dekomposisi Aliran Biaya (Kiri):** Memperlihatkan bahwa biaya server cloud AWS S3 sangat murah (hanya **Rp 17.400/acara**) dan biaya gerbang pembayaran (Midtrans) hanya **Rp 2.900/acara**. Namun, beban terbesar terletak pada biaya iklan akuisisi pelanggan (CAC), yaitu Rp 120.000 di B2C vs hanya Rp 25.000 di B2B.
* **Grafik Kurva Titik Impas (Kanan):** Memperlihatkan bahwa paket murah **Rp 79.000 justru merugi (-Rp 23.000 per acara)** karena termakan biaya iklan. Sebaliknya, pada paket **Rp 299.000**, laba melonjak menjadi Rp 152.000 per acara dan target titik impas langsung melandai ke angka aman.
* **Tabel Rekapitulasi (Bawah):** Menegaskan perbandingan 10 variasi paket dan membuktikan bahwa paket di atas Rp 199.000 adalah zona aman profitabilitas.

### Halaman 2: Uji Stres Monte Carlo & Ketahanan Kas 24 Bulan (Risk Simulation)
* **4 Kartu KPI Win-Rate:** Peluang untung model B2C di tahun pertama adalah **0.0%** (pasti defisit). Sebaliknya, model B2B memiliki peluang untung **27.2%** di tahun pertama dan melonjak drastis ke **98.8%** di tahun ke-2 dengan median laba bersih **+Rp 64 Juta**.
* **Grafik Proyeksi Saldo Kas 24 Bulan (Kiri):** Garis merah B2C terus merosot dari Rp 72M ke Rp 40M (modal terbakar habis). Sementara garis biru B2B membentuk kurva *J-Curve*: sempat turun tipis di bulan ke 6-7 ke titik terendah Rp 59M, lalu berbalik naik menembus modal awal Rp 75M di bulan ke-14, dan mencapai **Rp 137 Juta di bulan ke-24**.
* **Grafik Mesin Pertumbuhan B2B (Kanan):** Mengungkapkan rahasia kebangkitan kas B2B: jumlah mitra Wedding Organizer (WO) aktif tumbuh dari 4 menjadi **31 mitra**, yang otomatis mendongkrak volume acara dari 11 menjadi **90 acara per bulan** tanpa perlu biaya iklan tambahan.
* **Tabel Matriks Uji Stres (Bawah):** Menunjukkan risiko terburuk (VaR 95%) di tahun pertama: B2C berisiko rugi hingga -Rp 33M, sedangkan B2B di tahun kedua menghasilkan akumulasi kas aman berkat retensi mitra WO.

### Halaman 3: Lanskap Pasar Indonesia & Peta Kompetitor (Market Benchmark)
* **4 Kartu KPI Pasar:** Mengukur Total Pasar Nasional (TAM) **1.48 Juta pernikahan/tahun**, Tren Penurunan Nikah BPS **-6.3% YoY**, Pasar Perkotaan Modern (SAM) **251.000 acara/tahun**, dan Target Realistis Tahun 1 (SOM) hanya **753 acara** (~63 acara/bulan).
* **Grafik Tren Pernikahan BPS (Kiri):** Memperlihatkan penurunan resmi dari 1.71M (2022) ➔ 1.58M (2023) ➔ 1.48M (2024), menegaskan perlunya fokus pada ceruk pasar perkotaan yang melek digital.
* **Grafik Ranking Harga Kompetitor (Kanan):** Memperlihatkan jurang pemisah harga: Pemain photobooth fisik (Fotoimoet, Invitato, Viding) mematok harga jutaan rupiah (**Rp 1.4M s/d Rp 2.1M**). Sedangkan pemain SaaS QR Foto (Satualbum, Kurinji, produk kita) berada di ratusan ribu (**Rp 79K s/d Rp 467K**).
* **Tabel Piramida Ukuran Pasar (Bawah):** Menunjukkan bahwa target tahun pertama kita (753 acara) hanya butuh menyerap **0.3% dari ceruk pasar perkotaan**, target yang sangat realistis untuk dieksekusi.

---

## 💡 BAGIAN 2: SINTESIS SATU INSIGHT UTAMA SECARA KESELURUHAN

> **Benang Merah Ketiga Halaman Dashboard:**  
> Bisnis Event Photo SaaS di Indonesia memiliki **keunggulan ekonomi unit yang sangat prima (Margin Kotor > 70%)** dan **peluang disrupsi harga yang masif (7x lebih murah dibanding photobooth fisik)**, **DENGAN SATU SYARAT MUTLAK: Model Go-To-Market WAJIB mengandalkan kemitraan Wedding Organizer (B2B), dan BUKAN iklan langsung ke pengantin (B2C)**.  
> 
> Jika modal Pre-Seed Rp 75 Juta dipakai untuk iklan digital B2C, bisnis dipastikan bangkrut (Peluang Laba 0.0%) karena pengantin tidak memiliki retensi belanja (menikah sekali seumur hidup). Namun jika modal difokuskan untuk merekrut 15–20 mitra Wedding Organizer, bisnis memiliki **probabilitas kelangsungan hidup 98.8%** dan melipatgandakan kas menjadi **Rp 137 Juta** di bulan ke-24.

---

## 🎯 BAGIAN 3: REKOMENDASI STRATEGIS & JAWABAN PERTANYAAN BISNIS UTAMA

| Pertanyaan Bisnis Utama | Jawaban Strategis & Rencana Aksi Eksekutif |
| :--- | :--- |
| **1. Apakah bisnis ini layak didanai dengan modal Pre-Seed Rp 75 Juta?** | **SANGAT LAYAK (GO)**. Model SaaS murni memiliki skalabilitas tinggi tanpa beban armada kru fisik, margin kontribusi 52.8%, dan titik impas rendah (1 acara/hari). Risiko kehabisan kas mendekati 0% jika menggunakan jalur kemitraan WO. |
| **2. Berapa harga paket yang wajib dijual ke pasar?** | Tetapkan harga paket utama di **Rp 299.000**. Posisi ini 7x lebih murah dari photobooth konvensional namun tetap menghasilkan laba bersih Rp 152.000/event. **Haramkan paket di bawah Rp 199.000** karena margin negatif akan menguras modal kerja. |
| **3. Bagaimana alokasi modal Pre-Seed Rp 75 Juta yang optimal?** | • **40% (Rp 30.000.000):** Pengembangan Web App MVP (Kamera Instan QR, Cloud AWS S3, Pembayaran QRIS Midtrans).<br>• **40% (Rp 30.000.000):** Operasional Akuisisi Mitra WO (B2B Sales Kit, Komisi Mitra 20-25%, Testing Acara Perdana).<br>• **20% (Rp 15.000.000):** Cadangan Kas Penahan (Cash Runway Buffer untuk melewati lembah kas di bulan ke 6-7). |
| **4. Apa target operasional kunci di Tahun Pertama?** | Kunci kemitraan dengan **15–20 Wedding Organizer aktif** di wilayah Jabodetabek dan Bandung untuk mengamankan **753 acara per tahun** (~63 acara/bulan). |
"""

with open(md_file, "w", encoding="utf-8") as f:
    f.write(md_content)
print(f"MD generated: {md_file}")
