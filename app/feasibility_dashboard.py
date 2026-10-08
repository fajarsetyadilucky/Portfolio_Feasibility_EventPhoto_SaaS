"""Executive Feasibility Dashboard & Interactive Financial Simulator
Tech Stack: Streamlit, Plotly, Pandas, NumPy
Fokus: Evaluasi Kelayakan Investasi Pre-Seed QR-Based Event Photo SaaS (Indonesia Scope - IDR)
"""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Setup Path Data
ROOT = Path(__file__).resolve().parents[1]
DATA_PROCESSED = ROOT / "data" / "02_processed"
DATA_MARTS = ROOT / "data" / "03_analytics_marts"

st.set_page_config(
    page_title="Executive Feasibility Study | Event-Photo SaaS Indonesia",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .metric-card {
        background-color: #1e293b;
        border-radius: 10px;
        padding: 16px;
        border: 1px solid #334155;
    }
    .verdict-box {
        background-color: #0f172a;
        border-left: 5px solid #ef4444;
        padding: 18px;
        border-radius: 8px;
        margin-bottom: 24px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    df_comp = pd.read_csv(DATA_PROCESSED / "processed_competitor_benchmark.csv")
    df_demo = pd.read_csv(DATA_PROCESSED / "processed_wedding_demographics.csv")
    df_market = pd.read_csv(DATA_MARTS / "tam_sam_som_market_sizing.csv")
    df_ue = pd.read_csv(DATA_MARTS / "unit_economics_bep_scenarios.csv")
    df_sim = pd.read_csv(DATA_MARTS / "monte_carlo_simulation_results.csv")
    df_traj = pd.read_csv(DATA_MARTS / "monte_carlo_monthly_trajectories.csv")
    return df_comp, df_demo, df_market, df_ue, df_sim, df_traj


df_comp, df_demo, df_market, df_ue, df_sim, df_traj = load_data()

# ----------------- SIDEBAR PARAMETER WHAT-IF -----------------
st.sidebar.title("🎛️ Simulator Parameter Finansial")
st.sidebar.markdown("Uji ketahanan model finansial terhadap perubahan harga, CAC, dan skala event:")

selected_price = st.sidebar.select_slider(
    "Harga Paket Retail (IDR):",
    options=[79_000, 199_000, 299_000, 439_000, 599_000, 999_000],
    value=299_000,
    format_func=lambda x: f"Rp{x:,.0f}",
)

selected_cac_b2c = st.sidebar.slider(
    "Estimasi CAC B2C (Ads Meta/TikTok):",
    min_value=50_000,
    max_value=200_000,
    value=120_000,
    step=10_000,
    format_func=lambda x: f"Rp{x:,.0f}",
)

selected_photos = st.sidebar.slider(
    "Rata-rata Foto per Event:",
    min_value=200,
    max_value=1500,
    value=500,
    step=50,
)

fixed_opex = st.sidebar.number_input(
    "Fixed OpEx Bulanan (IDR):",
    min_value=2_000_000,
    max_value=15_000_000,
    value=5_000_000,
    step=500_000,
    format_func=lambda x: f"Rp{x:,.0f}",
)

capex_budget = st.sidebar.number_input(
    "Anggaran Modal Awal / CapEx (IDR):",
    min_value=50_000_000,
    max_value=150_000_000,
    value=75_000_000,
    step=5_000_000,
    format_func=lambda x: f"Rp{x:,.0f}",
)

# Kalkulasi Real-time
gb_event = (selected_photos * 5.0) / 1024.0
cloud_cost_calc = gb_event * (0.025 * 12 + 0.132) * 16500
pg_fee_calc = 0.60 * (selected_price * 0.007) + 0.20 * (selected_price * 0.02) + 0.20 * 4000
cm_b2c_dyn = selected_price - cloud_cost_calc - pg_fee_calc - selected_cac_b2c
bep_b2c_dyn = fixed_opex / cm_b2c_dyn if cm_b2c_dyn > 0 else np.nan

# ----------------- MAIN DASHBOARD -----------------
st.title("📊 Strategic Feasibility & Investment Advisory Dashboard")
st.subheader("Evaluasi Kelayakan Investasi Pre-Seed: QR Event Photo SaaS Indonesia")

st.markdown("""
<div class="verdict-box">
    <h3 style="color: #ef4444; margin-top:0;">🛑 EXECUTIVE VERDICT: NO-GO UNTUK B2C MURNI | PIVOT CONDITIONAL GO KE B2B</h3>
    <p style="margin-bottom:0; color:#cbd5e1; font-size:15px; line-height:1.6;">
        Berdasarkan analisis kuantitatif, model penjualan langsung ke pengantin (B2C) <b>memiliki probabilitas profit 0,0% di tahun ke-2</b> 
        akibat <i>100% Churn (LTV/CAC hanya 1,3x)</i>. Sebaliknya, pivot ke <b>B2B Partnership (Wedding Organizer)</b> menghasilkan 
        <b>LTV/CAC 9,6x</b> dan probabilitas keberhasilan <b>98,8% (J-Curve)</b>. Klien direkomendasikan mengalokasikan modal <b>HANYA JIKA</b> 
        telah mengantongi minimal <b>15 LOI mitra Wedding Organizer</b> sebelum koding dimulai.
    </p>
</div>
""", unsafe_allow_html=True)

# KPI Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        "Margin Kontribusi Unit (B2C)",
        f"Rp{cm_b2c_dyn:,.0f}",
        f"{(cm_b2c_dyn/selected_price)*100:.1f}% dari Harga",
        delta_color="normal" if cm_b2c_dyn > 0 else "inverse",
    )
with col2:
    st.metric(
        "BEP Bulanan Target",
        f"{bep_b2c_dyn:.1f} event/bln" if not np.isnan(bep_b2c_dyn) else "INFINITE (RUGI)",
        f"OpEx: Rp{fixed_opex:,.0f}/bln",
    )
with col3:
    st.metric("Win-Rate B2B (Tahun ke-2)", "98.8%", "J-Curve Scale", delta_color="normal")
with col4:
    st.metric("Rasio LTV / CAC B2B", "9.6x", "B2C hanya 1.3x", delta_color="normal")

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 1. Unit Economics & LTV/CAC",
    "🎲 2. Multi-Horizon Monte Carlo",
    "🏢 3. Ukuran Pasar (TAM/SAM/SOM)",
    "🧭 4. Executive Decision Matrix",
])

# ----------------- TAB 1: UNIT ECONOMICS -----------------
with tab1:
    st.subheader("Analisis Unit Economics & LTV-to-CAC Ratio")
    col_u1, col_u2 = st.columns([1, 1])

    with col_u1:
        st.markdown("#### Waterfall Dekomposisi Biaya per Event B2C")
        fig_waterfall = go.Figure(go.Waterfall(
            name="Waterfall",
            orientation="v",
            measure=["relative", "relative", "relative", "relative", "total"],
            x=["Harga Retail", "AWS S3 & Egress", "Midtrans Fee", "CAC (Ads)", "Net Margin"],
            textposition="outside",
            text=[f"+Rp{selected_price:,.0f}", f"-Rp{cloud_cost_calc:,.0f}", f"-Rp{pg_fee_calc:,.0f}", f"-Rp{selected_cac_b2c:,.0f}", f"Rp{cm_b2c_dyn:,.0f}"],
            y=[selected_price, -cloud_cost_calc, -pg_fee_calc, -selected_cac_b2c, 0],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        ))
        fig_waterfall.update_layout(height=380)
        st.plotly_chart(fig_waterfall, use_container_width=True)

    with col_u2:
        st.markdown("#### Perbandingan Fundamental: LTV-to-CAC")
        fig_ltv = go.Figure()
        fig_ltv.add_trace(go.Bar(
            x=["Model A (B2C Pure)", "Model B (B2B WO Partner)"],
            y=[1.3, 9.6],
            text=["1.3x (Tidak Sehat)", "9.6x (SaaS Standar Dunia)"],
            textposition="outside",
            marker_color=["#f43f5e", "#10b981"],
        ))
        fig_ltv.add_hline(y=3.0, line_dash="dash", line_color="#38bdf8", annotation_text="Batas Minimal SaaS Sehat (3.0x)")
        fig_ltv.update_layout(title="Rasio LTV-to-CAC (Customer Lifetime Value)", yaxis_title="Rasio Multiplier", height=380)
        st.plotly_chart(fig_ltv, use_container_width=True)

# ----------------- TAB 2: MONTE CARLO -----------------
with tab2:
    st.subheader("Simulasi Stokastik Monte Carlo Multi-Horizon (1.000 Iterasi)")

    col_m1, col_m2 = st.columns([1, 1])

    with col_m1:
        fig_dist = px.histogram(
            df_sim,
            x=["b2c_profit_m12", "b2b_profit_m12"],
            barmode="overlay",
            nbins=40,
            title="Distribusi Profit Kumulatif Tahun 1 (M12)",
            labels={"value": "Kumulatif Net Profit (IDR)", "variable": "Model"},
            color_discrete_map={"b2c_profit_m12": "#f43f5e", "b2b_profit_m12": "#10b981"},
        )
        fig_dist.add_vline(x=0, line_dash="dash", line_color="white")
        fig_dist.update_layout(height=380)
        st.plotly_chart(fig_dist, use_container_width=True)

    with col_m2:
        fig_traj = px.line(
            df_traj,
            x="month",
            y="cash_b2b",
            color="simulation_id",
            title="Proyeksi Kas Model B2B 24 Bulan (J-Curve Scale)",
            labels={"month": "Bulan ke-", "cash_b2b": "Saldo Kas (IDR)"},
        )
        fig_traj.add_hline(y=capex_budget, line_dash="dot", line_color="#38bdf8", annotation_text="Modal Awal Rp75jt")
        fig_traj.update_layout(showlegend=False, height=380)
        st.plotly_chart(fig_traj, use_container_width=True)

# ----------------- TAB 3: PASAR INDONESIA -----------------
with tab3:
    st.subheader("Ukuran Pasar (TAM/SAM/SOM) & Benchmarking Kompetitor Indonesia")

    col_p1, col_p2 = st.columns([1, 1])

    with col_p1:
        st.markdown("#### Estimasi Potensi Pasar (TAM / SAM / SOM)")
        fig_tam = px.bar(
            df_market,
            x="tier",
            y="annual_market_value_idr",
            text="annual_market_value_idr",
            title="Nilai Pasar Pernikahan Indonesia (BPS 2024)",
            color="tier",
            color_discrete_sequence=px.colors.sequential.Blues_r,
        )
        fig_tam.update_traces(texttemplate="Rp%{text:,.0f}", textposition="outside")
        fig_tam.update_layout(showlegend=False, height=380)
        st.plotly_chart(fig_tam, use_container_width=True)

    with col_p2:
        st.markdown("#### Peta Posisi Harga Kompetitor Indonesia")
        paid_comp = df_comp[df_comp["price_idr_current"] > 0].dropna(subset=["max_guests"])
        fig_comp = px.scatter(
            paid_comp,
            x="max_guests",
            y="price_idr_current",
            color="competitor",
            size="price_idr_current",
            text="package",
            title="Harga vs Kapasitas Tamu (Platform Lokal IDR)",
            labels={"max_guests": "Kapasitas Tamu", "price_idr_current": "Harga Paket (IDR)"},
        )
        fig_comp.update_traces(textposition="top center")
        fig_comp.update_layout(height=380)
        st.plotly_chart(fig_comp, use_container_width=True)

# ----------------- TAB 4: DECISION MATRIX -----------------
with tab4:
    st.subheader("🧭 Matriks Putusan Investasi & Stage-Gate Action Plan")

    st.markdown("""
    | Dimensi Evaluasi | Model A (B2C Pure: Pengantin) | Model B (B2B Pivot: Wedding Organizer) | Evaluasi Konsultan |
    | :--- | :---: | :---: | :--- |
    | **Struktur Retensi (Churn)** | 100% Churn (Zero Repeat) | Berlangganan / 25–36 event/thn | ✅ B2B Mengunci Volume |
    | **LTV / CAC Ratio** | **1,3x (Tidak Sehat)** | **9,6x (Standar SaaS Global)** | ❌ B2C Kalah Mutlak |
    | **Win-Rate 12 Bulan (Monte Carlo)** | **6,9%** | **27,2%** | B2B Melewati Fase Akuisisi Mitra |
    | **Win-Rate 24 Bulan (Monte Carlo)** | **0,0% (Defisit Pasti)** | **98,8% (Profit Pasti)** | ✅ B2B Menghasilkan J-Curve |
    | **Ketahanan Perang Harga** | Rentan kalah vs Kurinji (Rp79rb)| Tahan banting via integrasi WO | ✅ B2B Melindungi Margin |
    | **Putusan Rekomendasi Konsultan** | **NO-GO MUTLAK (DIBATALKAN)** | **CONDITIONAL GO (SYARAT 15 WO)** | **PIVOT STRATEGIS WAJIB** |
    """)

    st.info("""
    **🎯 Action Plan 90 Hari Sebelum Pencairan Modal CapEx:**
    1. **Bulan 1 (Validasi Kemitraan):** Temui 30 agensi Wedding Organizer. Amankan minimal **15 LOI mitra aktif** pada harga grosir Rp120.000 - Rp150.000 per event. Jika gagal, **proyek wajib ditutup**.
    2. **Bulan 2 (MVP Multi-Tenant B2B):** Alokasikan Rp40.000.000 untuk membangun portal khusus agensi WO. Sisa Rp35.000.000 dicadangkan untuk operasional.
    3. **Bulan 3 (Pilot Testing):** Jalankan uji coba pada 30-45 pernikahan klien dari 15 mitra awal.
    """)

st.caption("Strategic Feasibility Study Platform | Event-Tech SaaS Indonesia | Dibuat dengan Streamlit & Plotly")
