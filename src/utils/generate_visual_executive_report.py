import os
import subprocess
from pathlib import Path
import win32com.client

ROOT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

html_file = REPORTS_DIR / "Ringkasan_Eksekutif_Feasibility_Dashboard.html"
docx_file = REPORTS_DIR / "Ringkasan_Eksekutif_Feasibility_Dashboard.docx"
pdf_file  = REPORTS_DIR / "Ringkasan_Eksekutif_Feasibility_Dashboard.pdf"
preview_img = FIGURES_DIR / "Ringkasan_Eksekutif_Preview.png"

html_content = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<title>Executive Briefing - Event Photo SaaS Indonesia</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
    @page {
        size: A4 portrait;
        margin: 10mm 12mm 10mm 12mm;
    }
    * {
        box-sizing: border-box;
    }
    body {
        font-family: 'Plus Jakarta Sans', 'Segoe UI', -apple-system, sans-serif;
        color: #0f172a;
        background-color: #ffffff;
        margin: 0;
        padding: 0;
        line-height: 1.45;
        font-size: 8.8pt;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }

    /* TOP CORPORATE BANNER */
    .header-banner {
        background: linear-gradient(135deg, #0b132b 0%, #1c2541 50%, #1e3a8a 100%);
        color: #ffffff;
        padding: 14px 18px;
        border-radius: 10px;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.12);
    }
    .header-left h1 {
        margin: 0;
        font-size: 14pt;
        font-weight: 800;
        letter-spacing: -0.2px;
        color: #ffffff;
    }
    .header-left p {
        margin: 3px 0 0 0;
        font-size: 8pt;
        color: #93c5fd;
        font-weight: 500;
    }
    .status-badge {
        background: #10b981;
        color: #ffffff;
        padding: 7px 14px;
        border-radius: 8px;
        font-weight: 800;
        font-size: 10pt;
        text-align: center;
        border: 1px solid #34d399;
        box-shadow: 0 3px 8px rgba(16, 185, 129, 0.3);
    }
    .status-badge small {
        display: block;
        font-size: 6.5pt;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #d1fae5;
    }

    /* 4 HIGHLIGHT KPI TILES */
    .kpi-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 9px;
        margin-bottom: 12px;
    }
    .kpi-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 8px 10px;
        border-top: 3.5px solid #2563eb;
    }
    .kpi-box.emerald { border-top-color: #10b981; background: #f0fdf4; }
    .kpi-box.purple { border-top-color: #8b5cf6; }
    .kpi-box.amber { border-top-color: #f59e0b; }
    .kpi-num {
        font-size: 13.5pt;
        font-weight: 800;
        color: #0f172a;
        margin: 0;
        line-height: 1.1;
    }
    .kpi-box.emerald .kpi-num { color: #047857; }
    .kpi-title {
        font-size: 7.2pt;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        color: #64748b;
        margin-top: 3px;
    }
    .kpi-detail {
        font-size: 6.8pt;
        color: #475569;
        margin-top: 1px;
    }

    /* SECTION HEADERS */
    .sec-header {
        display: flex;
        align-items: center;
        gap: 7px;
        margin: 10px 0 7px 0;
        border-bottom: 1.5px solid #e2e8f0;
        padding-bottom: 3px;
    }
    .sec-circle {
        background: #2563eb;
        color: #ffffff;
        width: 17px;
        height: 17px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 7.5pt;
        font-weight: 800;
        flex-shrink: 0;
    }
    .sec-header h2 {
        margin: 0;
        font-size: 9.5pt;
        font-weight: 800;
        color: #1e3a8a;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }

    /* 3 PAGE WALKTHROUGH CARDS */
    .walkthrough-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 9px;
        margin-bottom: 12px;
    }
    .wt-card {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 9px 10px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .wt-card-top {
        border-bottom: 1px solid #f1f5f9;
        padding-bottom: 5px;
        margin-bottom: 6px;
    }
    .wt-page-tag {
        font-size: 7pt;
        font-weight: 800;
        color: #2563eb;
        text-transform: uppercase;
        display: block;
    }
    .wt-headline {
        font-size: 8.8pt;
        font-weight: 700;
        color: #0f172a;
        margin: 2px 0 0 0;
    }
    .wt-item {
        display: flex;
        align-items: flex-start;
        gap: 5px;
        margin-bottom: 5px;
        font-size: 7.4pt;
        color: #334155;
    }
    .wt-bullet {
        width: 5px;
        height: 5px;
        border-radius: 50%;
        background: #3b82f6;
        margin-top: 3.5px;
        flex-shrink: 0;
    }
    .wt-bullet.red { background: #ef4444; }
    .wt-bullet.green { background: #10b981; }
    .wt-badge-summary {
        background: #f8fafc;
        border-left: 3px solid #2563eb;
        padding: 5px 7px;
        border-radius: 4px;
        font-size: 7.1pt;
        color: #1e293b;
        margin-top: 6px;
    }
    .wt-badge-summary.green { border-left-color: #10b981; background: #f0fdf4; }

    /* CORE UNIFIED TAKEAWAY BOX */
    .unified-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #ffffff;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 12px;
        border-left: 4.5px solid #38bdf8;
    }
    .unified-title-row {
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 4px;
    }
    .unified-pill {
        background: #38bdf8;
        color: #0f172a;
        font-size: 6.5pt;
        font-weight: 800;
        padding: 1.5px 6px;
        border-radius: 4px;
        text-transform: uppercase;
    }
    .unified-heading {
        font-size: 9.5pt;
        font-weight: 800;
        margin: 0;
        color: #f8fafc;
    }
    .unified-text {
        font-size: 7.7pt;
        color: #cbd5e1;
        margin: 0;
        line-height: 1.4;
    }

    /* 4 ACTION ITEMS GRID */
    .action-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 9px;
        margin-bottom: 10px;
    }
    .act-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 8px 10px;
    }
    .act-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 4px;
    }
    .act-tag {
        font-size: 6.5pt;
        font-weight: 800;
        padding: 1.5px 5px;
        border-radius: 3px;
        text-transform: uppercase;
    }
    .act-tag.emerald { background: #d1fae5; color: #065f46; }
    .act-tag.blue { background: #dbeafe; color: #1e40af; }
    .act-tag.amber { background: #fef3c7; color: #92400e; }
    .act-tag.violet { background: #ede9fe; color: #5b21b6; }
    .act-name {
        font-size: 8.3pt;
        font-weight: 700;
        color: #0f172a;
        margin: 0 0 3px 0;
    }
    .act-body {
        font-size: 7.3pt;
        color: #475569;
        margin: 0;
        line-height: 1.35;
    }

    /* FOOTER */
    .doc-footer {
        display: flex;
        justify-content: space-between;
        border-top: 1px solid #e2e8f0;
        padding-top: 6px;
        font-size: 6.8pt;
        color: #94a3b8;
    }
</style>
</head>
<body>

<!-- TOP HEADER BANNER -->
<div class="header-banner">
    <div class="header-left">
        <h1>EXECUTIVE BRIEFING: KELAYAKAN EVENT PHOTO SAAS</h1>
        <p>Laporan Pengambilan Keputusan Bisnis Non-Analis • Lampiran Resmi Power BI (Feasibility dasboard.pbix)</p>
    </div>
    <div class="status-badge">
        <small>Keputusan Final</small>
        ✅ GO (LAYAK)
    </div>
</div>

<!-- 4 TOP KEY METRIC TILES -->
<div class="kpi-row">
    <div class="kpi-box emerald">
        <div class="kpi-num">98.8%</div>
        <div class="kpi-title">Peluang Laba B2B</div>
        <div class="kpi-detail">Probabilitas kas positif 24 bulan</div>
    </div>
    <div class="kpi-box">
        <div class="kpi-num">Rp 299K</div>
        <div class="kpi-title">Harga Paket Ideal</div>
        <div class="kpi-detail">Laba bersih Rp 152K per event</div>
    </div>
    <div class="kpi-box purple">
        <div class="kpi-num">29.3 Event</div>
        <div class="kpi-title">Target Impas Bulanan</div>
        <div class="kpi-detail">Hanya butuh 1 acara per hari</div>
    </div>
    <div class="kpi-box amber">
        <div class="kpi-num">Rp 137 Jt</div>
        <div class="kpi-title">Proyeksi Kas Thn 2</div>
        <div class="kpi-detail">Tumbuh melesat dari Rp 75 Jt</div>
    </div>
</div>

<!-- SECTION 1: PENJELASAN 3 HALAMAN DASHBOARD -->
<div class="sec-header">
    <div class="sec-circle">1</div>
    <h2>PENJELASAN SEDERHANA VISUAL 3 HALAMAN DASHBOARD (BAHASA AWAM)</h2>
</div>

<div class="walkthrough-grid">
    <!-- HALAMAN 1 -->
    <div class="wt-card">
        <div>
            <div class="wt-card-top">
                <span class="wt-page-tag">📊 Halaman 1: Struktur Biaya</span>
                <div class="wt-headline">Berapa Keuntungan Tiap Acara?</div>
            </div>
            <div class="wt-item">
                <div class="wt-bullet green"></div>
                <div><b>Server Sangat Murah:</b> Simpan foto di AWS cuma Rp 17.400/acara dan biaya bank cuma Rp 2.900. Margin kotor tebal <b>73.7%</b>.</div>
            </div>
            <div class="wt-item">
                <div class="wt-bullet red"></div>
                <div><b>Bahaya Paket Rp 79K:</b> Paket murah justru <b>RUGI Rp 23.000</b> (batang merah) karena uang habis buat bayar iklan.</div>
            </div>
            <div class="wt-item">
                <div class="wt-bullet green"></div>
                <div><b>Paket Rp 299K Paling Sehat:</b> Untung bersih Rp 152K/acara. Cukup jual 29 acara/bulan untuk tutup biaya operasional kantor Rp 5 Jt.</div>
            </div>
        </div>
        <div class="wt-badge-summary">
            <b>Inti Halaman 1:</b> Bisnis sangat untung di paket Rp 299K. Haramkan paket di bawah Rp 199K.
        </div>
    </div>

    <!-- HALAMAN 2 -->
    <div class="wt-card">
        <div>
            <div class="wt-card-top">
                <span class="wt-page-tag">🎲 Halaman 2: Ketahanan Kas</span>
                <div class="wt-headline">Apakah Uang Modal Rp 75 Jt Aman?</div>
            </div>
            <div class="wt-item">
                <div class="wt-bullet red"></div>
                <div><b>B2C Pasti Boncos (Peluang 0%):</b> Jual langsung ke pengantin membakar modal Rp 75 Jt karena pengantin cuma nikah 1x (iklan mahal terus).</div>
            </div>
            <div class="wt-item">
                <div class="wt-bullet green"></div>
                <div><b>B2B Tumbuh Eksponensial (98.8%):</b> Jalur Wedding Organizer sempat turun tipis di bln 6 (Rp 59 Jt), lalu melesat jadi <b>Rp 137 Jt di bln 24</b>.</div>
            </div>
            <div class="wt-item">
                <div class="wt-bullet green"></div>
                <div><b>Rahasia J-Curve:</b> Mitra WO naik dari 4 ke 31 mitra, mendongkrak acara dari 11 ke 90 acara/bln tanpa biaya iklan baru!</div>
            </div>
        </div>
        <div class="wt-badge-summary green">
            <b>Inti Halaman 2:</b> Wajib gandeng Wedding Organizer. Tolak jalur jualan eceran langsung ke pengantin.
        </div>
    </div>

    <!-- HALAMAN 3 -->
    <div class="wt-card">
        <div>
            <div class="wt-card-top">
                <span class="wt-page-tag">🏢 Halaman 3: Pasar &amp; Pesaing</span>
                <div class="wt-headline">Di Mana Posisi Kita di Pasar?</div>
            </div>
            <div class="wt-item">
                <div class="wt-bullet"></div>
                <div><b>Pasar Masif:</b> Walaupun tren nikah BPS turun -6.3%, masih ada <b>1.48 Juta pernikahan/tahun</b> (251 Ribu di kota besar).</div>
            </div>
            <div class="wt-item">
                <div class="wt-bullet green"></div>
                <div><b>Harga 7x Lebih Murah:</b> Photobooth fisik mematok Rp 1.5 - 2.1 Juta. Produk kita hanya Rp 299 Ribu (disrupsi harga telak).</div>
            </div>
            <div class="wt-item">
                <div class="wt-bullet green"></div>
                <div><b>Target Realistis:</b> Sukses tahun 1 cuma butuh <b>753 acara</b> (hanya 0.3% ceruk pasar perkotaan lewat 15-20 mitra WO).</div>
            </div>
        </div>
        <div class="wt-badge-summary">
            <b>Inti Halaman 3:</b> Pasar kota besar haus solusi photobooth hemat. Peluang penetrasi terbuka lebar.
        </div>
    </div>
</div>

<!-- SECTION 2: SATU BENANG MERAH UTAMA -->
<div class="sec-header">
    <div class="sec-circle">2</div>
    <h2>SATU INSIGHT UTAMA KESELURUHAN (BENANG MERAH KETIGA HALAMAN)</h2>
</div>

<div class="unified-card">
    <div class="unified-title-row">
        <span class="unified-pill">Sintesis Eksekutif</span>
        <div class="unified-heading">Teknologinya Sangat Untung, Kuncinya Ada pada Siapa yang Menjual</div>
    </div>
    <div class="unified-text">
        Bisnis Event Photo SaaS memiliki <b>margin keuntungan sangat tebal (&gt;70%)</b> dan <b>disrupsi pasar yang masif (7x lebih murah dibanding photobooth biasa)</b>. Namun, kelangsungan modal Pre-Seed Rp 75 Juta <u>DITENTUKAN 100% OLEH MODEL PENJUALAN</u>:
        <br>
        ❌ <b>Jika dijual langsung ke pengantin (B2C):</b> Bisnis PASTI BANGKRUT (Peluang laba 0%) karena modal habis dipakai bakar iklan Meta/TikTok.<br>
        ✅ <b>Jika dijual lewat Wedding Organizer (B2B):</b> Bisnis HAMPIR PASTI SUKSES (Peluang 98.8%), modal Rp 75 Jt berlipat ganda menjadi Rp 137 Jt di tahun ke-2 karena 1 WO membawa 5–10 acara berulang gratis tanpa biaya iklan tambahan.
    </div>
</div>

<!-- SECTION 3: REKOMENDASI KEPUTUSAN BISNIS -->
<div class="sec-header">
    <div class="sec-circle">3</div>
    <h2>REKOMENDASI KEPUTUSAN BISNIS &amp; ALOKASI MODAL PRE-SEED</h2>
</div>

<div class="action-grid">
    <div class="act-box">
        <div class="act-header">
            <span class="act-tag emerald">Keputusan 1</span>
            <span style="font-size:7pt; font-weight:700; color:#047857;">Sinyal: GO</span>
        </div>
        <div class="act-name">Cairkan Modal Pre-Seed Rp 75 Juta</div>
        <div class="act-body">Bisnis sangat layak didanai karena perangkat lunak murni tanpa inventaris fisik, titik impas rendah (1 acara/hari), dan risiko kas aman di jalur B2B.</div>
    </div>

    <div class="act-box">
        <div class="act-header">
            <span class="act-tag blue">Keputusan 2</span>
            <span style="font-size:7pt; font-weight:700; color:#1e40af;">Pricing Policy</span>
        </div>
        <div class="act-name">Kunci Harga Paket di Rp 299.000</div>
        <div class="act-body">Titik paling ideal di pasar (laba bersih Rp 152K/acara). <b>Haramkan paket di bawah Rp 199.000</b> karena margin negatif akan menguras modal kerja.</div>
    </div>

    <div class="act-box">
        <div class="act-header">
            <span class="act-tag amber">Keputusan 3</span>
            <span style="font-size:7pt; font-weight:700; color:#b45309;">Alokasi Modal</span>
        </div>
        <div class="act-name">Bagi Modal Rp 75 Jt (40 : 40 : 20)</div>
        <div class="act-body">• <b>Rp 30 Jt (40%):</b> Web App MVP &amp; Server AWS.<br>• <b>Rp 30 Jt (40%):</b> Rekrutmen &amp; Komisi Mitra WO (20-25%).<br>• <b>Rp 15 Jt (20%):</b> Cadangan Kas penahan lembah kas bulan 6–7.</div>
    </div>

    <div class="act-box">
        <div class="act-header">
            <span class="act-tag violet">Keputusan 4</span>
            <span style="font-size:7pt; font-weight:700; color:#6d28d9;">Target Operasional</span>
        </div>
        <div class="act-name">Kunci 15–20 Mitra WO di Kota Besar</div>
        <div class="act-body">Rekrut 15–20 Wedding Organizer di Jabodetabek &amp; Bandung untuk mengunci <b>753 acara</b> (~63 acara/bln) tanpa bakar uang iklan.</div>
    </div>
</div>

<!-- FOOTER -->
<div class="doc-footer">
    <div><b>Ringkasan Eksekutif Satu Lembar</b> • Portfolio Feasibility Study Event Photo SaaS Indonesia</div>
    <div>Lampiran Resmi Power BI Desktop: <b>Feasibility dasboard.pbix</b></div>
</div>

</body>
</html>
"""

# 1. Write HTML
with open(html_file, "w", encoding="utf-8") as f:
    f.write(html_content)
print("HTML generated successfully.")

# 2. Render to 1-Page PDF via Chrome Headless
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
cmd = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_file}",
    str(html_file)
]
subprocess.run(cmd, capture_output=True)

# Check page count
with open(pdf_file, "rb") as f:
    content = f.read()
print("PDF Page count:", content.count(b"/Type /Page"), "Size:", len(content))

# 3. Take High-Res PNG Screenshot for IDE inspection
cmd_img = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    "--window-size=1200,1650",
    f"--screenshot={preview_img}",
    str(html_file)
]
subprocess.run(cmd_img, capture_output=True)
print("Preview Image generated:", preview_img.exists())

# 4. Generate Word DOCX via Word COM
try:
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    doc = word.Documents.Open(str(html_file))
    doc.SaveAs2(str(docx_file), 16)
    doc.Close()
    word.Quit()
    print("DOCX generated:", docx_file.exists())
except Exception as e:
    print("Word conversion:", e)
