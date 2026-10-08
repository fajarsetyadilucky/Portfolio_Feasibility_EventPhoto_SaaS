import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT / "reports"
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

content = (REPORTS_DIR / "Laporan_Kelayakan_Bisnis_CEO_EventPhoto_SaaS.html").read_text(encoding="utf-8")
parts = content.split("<!-- ====================")

head = parts[0]
for i in range(1, 4):
    part_content = parts[i]
    part_html = head + "<!-- ====================" + part_content + "</body></html>"
    temp_file = REPORTS_DIR / f"temp_page_{i}.html"
    temp_pdf = REPORTS_DIR / f"temp_page_{i}.pdf"
    temp_img = REPORTS_DIR / f"temp_page_{i}.png"
    temp_file.write_text(part_html, encoding="utf-8")
    
    # PDF
    subprocess.run([
        chrome_path, "--headless", "--disable-gpu", "--no-pdf-header-footer",
        f"--print-to-pdf={temp_pdf}", str(temp_file)
    ], capture_output=True)
    
    # Screenshot
    subprocess.run([
        chrome_path, "--headless", "--disable-gpu", "--window-size=1200,1650",
        f"--screenshot={temp_img}", str(temp_file)
    ], capture_output=True)
    
    pdf_bytes = temp_pdf.read_bytes()
    page_count = pdf_bytes.count(b"/Type /Page")
    print(f"Part {i} standalone page count: {page_count}")
    for p in (temp_file, temp_pdf, temp_img):
        if p.exists():
            p.unlink()
