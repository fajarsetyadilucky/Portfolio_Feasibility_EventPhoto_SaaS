"""
Consolidates all analytical marts and benchmark datasets into a single 
Power BI Master Data Model Excel file (.xlsx) for seamless 1-click import.
"""

import os
import pandas as pd

def build_powerbi_master_excel():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    marts_dir = os.path.join(base_dir, "data", "03_analytics_marts")
    processed_dir = os.path.join(base_dir, "data", "02_processed")
    output_path = os.path.join(base_dir, "power_bi", "Feasibility_Study_DataModel_Master.xlsx")

    writer = pd.ExcelWriter(output_path, engine="openpyxl")

    # 1. Fact Unit Economics & BEP
    unit_bep_path = os.path.join(marts_dir, "unit_economics_bep_scenarios.csv")
    if os.path.exists(unit_bep_path):
        df_bep = pd.read_csv(unit_bep_path)
        df_bep.to_excel(writer, sheet_name="Fact_UnitEconomics_BEP", index=False)
        print("Loaded Fact_UnitEconomics_BEP")

    # 2. Fact Monte Carlo Results
    mc_res_path = os.path.join(marts_dir, "monte_carlo_simulation_results.csv")
    if os.path.exists(mc_res_path):
        df_mc = pd.read_csv(mc_res_path)
        df_mc.to_excel(writer, sheet_name="Fact_MonteCarlo_Simulations", index=False)
        print("Loaded Fact_MonteCarlo_Simulations")

    # 3. Fact Monte Carlo Trajectories (Monthly Cash Flow)
    mc_traj_path = os.path.join(marts_dir, "monte_carlo_monthly_trajectories.csv")
    if os.path.exists(mc_traj_path):
        df_traj = pd.read_csv(mc_traj_path)
        df_traj.to_excel(writer, sheet_name="Fact_Monthly_Cashflow_Paths", index=False)
        print("Loaded Fact_Monthly_Cashflow_Paths")

    # 4. Dim Competitor Benchmark
    comp_path = os.path.join(processed_dir, "processed_competitor_benchmark.csv")
    if os.path.exists(comp_path):
        df_comp = pd.read_csv(comp_path)
        df_comp.to_excel(writer, sheet_name="Dim_Competitor_Benchmark", index=False)
        print("Loaded Dim_Competitor_Benchmark")

    # 5. Dim Wedding Demographics (BPS)
    demo_path = os.path.join(processed_dir, "processed_wedding_demographics.csv")
    if os.path.exists(demo_path):
        df_demo = pd.read_csv(demo_path)
        df_demo.to_excel(writer, sheet_name="Dim_Wedding_Demographics", index=False)
        print("Loaded Dim_Wedding_Demographics")

    # 6. Dim Market Sizing (TAM SAM SOM)
    market_path = os.path.join(marts_dir, "tam_sam_som_market_sizing.csv")
    if os.path.exists(market_path):
        df_market = pd.read_csv(market_path)
        df_market.to_excel(writer, sheet_name="Dim_Market_Sizing", index=False)
        print("Loaded Dim_Market_Sizing")

    # 7. Dim CAC Sensitivity
    cac_path = os.path.join(marts_dir, "cac_sensitivity_matrix.csv")
    if os.path.exists(cac_path):
        df_cac = pd.read_csv(cac_path)
        df_cac.to_excel(writer, sheet_name="Dim_CAC_Sensitivity", index=False)
        print("Loaded Dim_CAC_Sensitivity")

    writer.close()
    print(f"Master Power BI Data Model successfully created at: {output_path}")

if __name__ == "__main__":
    build_powerbi_master_excel()
