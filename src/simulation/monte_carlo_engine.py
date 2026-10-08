"""Monte Carlo Predictive Simulation Engine (Milestone 3) - Enhanced 24-Month Horizon
Menjalankan 1.000 skenario stokastik selama horizon 12 bulan dan 24 bulan
untuk membedah kurva J-Curve profitabilitas Model B2B dan pembuktian LTV/CAC.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
ANALYTICS_DIR = ROOT / "data" / "03_analytics_marts"


def run_monte_carlo_simulation_multi_horizon(
    n_simulations: int = 1000,
    initial_cash_capex: float = 75_000_000.0,
    monthly_fixed_opex: float = 5_000_000.0,
    seed: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    np.random.seed(seed)
    sim_results = []
    monthly_trajectories = []

    for sim_id in range(1, n_simulations + 1):
        cash_b2c = initial_cash_capex
        net_profit_b2c_cum = 0.0
        profit_b2c_m12 = 0.0

        cash_b2b = initial_cash_capex
        net_profit_b2b_cum = 0.0
        profit_b2b_m12 = 0.0
        wo_partners = 3  # Start dengan 3 mitra pilot

        b2c_bankrupt_m = None
        b2b_bankrupt_m = None

        for m in range(1, 25):  # 24 Bulan
            aov = np.random.triangular(199_000, 299_000, 439_000)
            photos = np.random.uniform(300, 1000)
            cloud_cost_unit = (photos * 5.0 / 1024.0) * (0.025 * 12 + 0.132) * 16500
            pg_fee_unit = 0.60 * (aov * 0.007) + 0.20 * (aov * 0.02) + 0.20 * 4000

            # --- MODEL A (B2C) ---
            # Fluktuasi volume B2C (terbatas oleh budget ads bulanan)
            vol_b2c = max(3, int(np.random.normal(12 + (m * 0.8), 5)))
            cac_b2c = np.clip(np.random.normal(120_000, 25_000), 75_000, 190_000)
            rev_b2c = vol_b2c * aov
            var_b2c = vol_b2c * (cloud_cost_unit + pg_fee_unit + cac_b2c)
            ebitda_b2c = rev_b2c - var_b2c - monthly_fixed_opex
            cash_b2c += ebitda_b2c
            net_profit_b2c_cum += ebitda_b2c
            if cash_b2c < 0 and b2c_bankrupt_m is None:
                b2c_bankrupt_m = m

            # --- MODEL B (B2B Partner) ---
            # Pertumbuhan jaringan WO: Efek word-of-mouth & direct sales
            new_wo = np.random.poisson(1.2 if m <= 12 else 1.8)
            churn_wo = int(wo_partners * 0.04)  # Churn WO rendah 4%
            wo_partners = max(1, wo_partners + new_wo - churn_wo)
            events_per_wo = np.random.uniform(2.2, 3.5)
            vol_b2b = int(wo_partners * events_per_wo)
            wholesale_aov = aov * 0.60
            cac_b2b_unit = 15_000

            rev_b2b = vol_b2b * wholesale_aov
            var_b2b = vol_b2b * (cloud_cost_unit + pg_fee_unit + cac_b2b_unit)
            ebitda_b2b = rev_b2b - var_b2b - monthly_fixed_opex
            cash_b2b += ebitda_b2b
            net_profit_b2b_cum += ebitda_b2b
            if cash_b2b < 0 and b2b_bankrupt_m is None:
                b2b_bankrupt_m = m

            if m == 12:
                profit_b2c_m12 = net_profit_b2c_cum
                profit_b2b_m12 = net_profit_b2b_cum

            if sim_id <= 50:
                monthly_trajectories.append({
                    "simulation_id": sim_id,
                    "month": m,
                    "cash_b2c": cash_b2c,
                    "cash_b2b": cash_b2b,
                    "volume_b2c": vol_b2c,
                    "volume_b2b": vol_b2b,
                    "wo_partners": wo_partners,
                    "ebitda_b2b": ebitda_b2b,
                })

        sim_results.append({
            "simulation_id": sim_id,
            "b2c_profit_m12": profit_b2c_m12,
            "b2b_profit_m12": profit_b2b_m12,
            "b2c_profit_m24": net_profit_b2c_cum,
            "b2b_profit_m24": net_profit_b2b_cum,
            "b2c_profitable_m12": profit_b2c_m12 > 0,
            "b2b_profitable_m12": profit_b2b_m12 > 0,
            "b2c_profitable_m24": net_profit_b2c_cum > 0,
            "b2b_profitable_m24": net_profit_b2b_cum > 0,
            "b2c_depleted": b2c_bankrupt_m is not None,
            "b2b_depleted": b2b_bankrupt_m is not None,
        })

    df_sim = pd.DataFrame(sim_results)
    df_traj = pd.DataFrame(monthly_trajectories)
    return df_sim, df_traj


if __name__ == "__main__":
    ANALYTICS_DIR.mkdir(parents=True, exist_ok=True)
    df_sim, df_traj = run_monte_carlo_simulation_multi_horizon()
    out_sim = ANALYTICS_DIR / "monte_carlo_simulation_results.csv"
    out_traj = ANALYTICS_DIR / "monte_carlo_monthly_trajectories.csv"
    df_sim.round(2).to_csv(out_sim, index=False)
    df_traj.round(2).to_csv(out_traj, index=False)
    print(f"[OK] Multi-Horizon Monte Carlo complete -> {out_sim}")
    print(f"Win-Rate B2B M12: {(df_sim['b2b_profitable_m12'].mean())*100:.1f}%")
    print(f"Win-Rate B2B M24: {(df_sim['b2b_profitable_m24'].mean())*100:.1f}%")
    print(f"Win-Rate B2C M24: {(df_sim['b2c_profitable_m24'].mean())*100:.1f}%")
