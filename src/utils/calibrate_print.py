import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PBIX_DIR = ROOT / "power_bi" / "pbix"
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

test_css = """
    @page {
        size: A4 portrait;
        margin: 8mm 10mm 8mm 10mm;
    }
    * { box-sizing: border-box; }
    body {
        font-family: 'Plus Jakarta Sans', 'Segoe UI', Arial, sans-serif;
        color: #0f172a;
        background: #ffffff;
        margin: 0;
        padding: 0;
        line-height: 1.35;
        font-size: 8pt;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }
    .page {
        page-break-after: always;
        break-after: page;
        height: 100%;
    }
    .page:last-child {
        page-break-after: avoid;
        break-after: avoid;
    }
"""

print("Testing scale and font size...")
