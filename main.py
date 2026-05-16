import os
import pandas as pd
import numpy as np
from src.resilience_index import NationalWorkforceResilienceIndex
from src.mobility_forecasting import CrossSectorMobilityForecaster
from src.geo_analyzer import GeographicLaborAnalyzer
from src.simulation_engine import MacroScenarioSimulationEngine

def execute_complete_national_intelligence_pipeline(csv_path):
    print("=======================================================================")
    print("RUNNING NATIONAL SKILLS GAP & WORKFORCE FORECASTING PLATFORM")
    print("=======================================================================\n")
    
    # -------------------------------------------------------------------------
    # DATA INGESTION & FEATURE ENGINEERING
    # -------------------------------------------------------------------------
    print(f"[Data Pipeline] Loading synthetic workforce data from: {csv_path}")
    df = pd.read_csv(csv_path)
    
    # Group by occupation to find the mean macroeconomic markers from your dataset
    grouped = df.groupby('occupation_name')[['retirement_velocity', 'skill_transferability', 'pipeline_replacement']].mean().reset_index()
    
    # Dynamically inject unique SOC codes to simulate formal federal tracking standards
    soc_mapping = {
        "Nursing Assistants": "31-1131",
        "Medical Assistants": "31-9092",
        "Semiconductor Wafer Fabrication Operators": "51-9141",
        "Microelectronics Materials Engineers": "17-2131",
        "Industrial Engineers": "17-2112"
    }
    grouped['soc_code'] = grouped['occupation_name'].map(lambda x: soc_mapping.get(x, "99-9999"))
    print(f"Loaded {len(grouped)} unique occupational vectors from database.\n")
    print("-" * 75)

    # -------------------------------------------------------------------------
    # MODULE 1: NATIONAL WORKFORCE RESILIENCE INDEX & EARLY WARNING
    # -------------------------------------------------------------------------
    print("\n[MODULE 1] RUNNING NATIONAL WORKFORCE RESILIENCE ASSESSMENT")
    resilience_engine = NationalWorkforceResilienceIndex(alpha=0.75, beta=0.25)
    
    # Evaluate baseline stability across all occupations found in the CSV
    stability_df = resilience_engine.evaluate_semiconductor_stability(grouped)
    alerts_df = resilience_engine.run_early_warning_system(stability_df, critical_threshold=0.45)
    
    print("\n--- Diagnostic Pipeline Status & Early Warning Directives ---")
    print(alerts_df[['occupation_name', 'vulnerability_score', 'system_status']].to_string(index=False))
    print("\n" + "-" * 75)

    # -------------------------------------------------------------------------
    # MODULE 2: CROSS-SECTOR WORKFORCE MOBILITY FORECASTING
    # -------------------------------------------------------------------------
    print("\n[MODULE 2] MODELING TRANSPARENT LABOR MOBILITY VECTORS")
    mobility_engine = CrossSectorMobilityForecaster()
    
    # Convert dataframe data to standard dictionary arrays for vector comparisons
    occupations_dict = {}
    for _, row in grouped.iterrows():
        # Using metrics directly to form 3D competency arrays
        occupations_dict[row['occupation_name']] = [row['retirement_velocity'], row['skill_transferability'], row['pipeline_replacement']]
    
    # Construct directed graph networks using a loose similarity threshold to allow transition routing
    mobility_engine.build_mobility_network(occupations_dict, threshold=0.70)
    
    source_job = "Nursing Assistants"
    target_job = "Semiconductor Wafer Fabrication Operators"
    
    print(f"\nSearching for optimal structural career pathway: [{source_job}] -> [{target_job}]")
    path_results = mobility_engine.find_mobility_pathway(source_job, target_job)
    
    if path_results["status"] == "SUCCESS":
        print(f"  Optimal Vector Discovered: {' -> '.join(path_results['optimal_pathway'])}")
        # Calculate retraining duration based on similarity of transition steps
        avg_similarity = np.mean([step['similarity_match'] for step in path_results['transition_steps']])
        months_required = mobility_engine.estimate_retraining_efficiency(avg_similarity, target_job_zone=3)
        print(f"  Estimated Upskilling Transition Timeline: {months_required} months.")
    else:
        print(f"  Pathway Alert: {path_results['message']}")
        
    # Project macroeconomic Return on Investment for policy planners
    macro_roi = mobility_engine.project_macro_reskilling_roi(
        cohort_volume=750, 
        wage_delta=16500, 
        annual_unemployment_savings=11000, 
        total_program_cost=4200000
    )
    print(f"  Projected 3-Year Macroeconomic ROI on Training Grant: {macro_roi}x Return.")
    print("\n" + "-" * 75)

    # -------------------------------------------------------------------------
    # MODULE 3: GEOSPATIAL VULNERABILITY & REGIONAL MAPPING
    # -------------------------------------------------------------------------
    print("\n[MODULE 3] CALCULATING REGIONAL INDUSTRIAL DEPENDENCIES (MSAs)")
    geo_engine = GeographicLaborAnalyzer()
    
    # Create sample reference baseline representing national workforce averages
    mock_national_baseline = pd.DataFrame([
        {"soc_code": "51-9141", "nat_occ_emp": 45000, "total_nat_emp": 160000000}, # Fab operators
        {"soc_code": "31-1131", "nat_occ_emp": 1300000, "total_nat_emp": 160000000} # Nursing assistants
    ])
    
    # Build a regional model representing diverse U.S. labor hubs (Austin urban vs Vermont semi-rural)
    mock_msa_data = pd.DataFrame([
        {"msa_code": "12420", "msa_name": "Austin-Round Rock, TX", "soc_code": "51-9141", "occupation_name": "Semiconductor Wafer Fabrication Operators", "local_occ_emp": 3800, "total_local_emp": 1100000, "rucc_code": 1},
        {"msa_code": "42200", "msa_name": "Rural Micro Cluster, VT", "soc_code": "51-9141", "occupation_name": "Semiconductor Wafer Fabrication Operators", "local_occ_emp": 450, "total_local_emp": 32000, "rucc_code": 5}
    ])
    
    # Identify localized monocultures using Location Quotients
    lq_df = geo_engine.analyze_regional_industrial_dependency(mock_msa_data, mock_national_baseline)
    hotspot_df = geo_engine.forecast_msa_level_vulnerability(lq_df, stability_df)
    
    print("\n--- Geo-Vulnerability Hotspot Ranking ---")
    print(hotspot_df[['msa_name', 'location_quotient', 'localized_vulnerability_index']].to_string(index=False))
    print("\n" + "-" * 75)

    # -------------------------------------------------------------------------
    # MODULE 4: MACRO-SCENARIO SIMULATION ENGINE
    # -------------------------------------------------------------------------
    print("\n[MODULE 4] EXECUTING FORWARD-LOOKING POLICY SIMULATION")
    sim_engine = MacroScenarioSimulationEngine(planning_years=5)
    
    # Target a 5-year structural projection for Semiconductor operators
    df_base_trend = sim_engine.generate_baseline_trajectory(
        initial_demand=18000, 
        initial_supply=12000, 
        growth_rate_demand=0.07, # 7% industry annual growth
        growth_rate_supply=0.015 # 1.5% baseline training pipeline growth
    )
    
    # Simulate a federal intervention policy (e.g., CHIPS Act upskilling + workforce incentives)
    chips_act_policy_config = {
        'ai_acceleration': 0.01,
        'recession_impact': 0.00,
        'immigration_policy_shift': 0.03,
        'federal_funding_initiative': 0.20  # 20% increase in funded vocational pipelines
    }
    
    df_simulated_outcome = sim_engine.apply_scenario_shocks(df_base_trend, chips_act_policy_config)
    policy_efficiency = sim_engine.evaluate_policy_mitigation_efficiency(df_simulated_outcome)
    
    print("\n--- 60-Month Strategic Simulation Model Summary ---")
    print(f"  Unmitigated Status-Quo Terminal Deficit: {policy_efficiency['unmitigated_terminal_shortage']} open positions.")
    print(f"  Simulated Post-Intervention Terminal Deficit: {policy_efficiency['simulated_terminal_shortage']} open positions.")
    print(f"  🚀 Net Labor Deficit Averted via Policy: {policy_efficiency['net_talent_shortage_averted']} vacancies ({policy_efficiency['mitigation_efficiency_percentage']}% efficiency).")
    print("=======================================================================")
    print("END-TO-END WORKFLOW RUN SUCCESSFUL")
    print("=======================================================================")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(script_dir, "data", "simulated", "synthetic_workforce_data.csv")
    
    if os.path.exists(csv_file):
        execute_complete_national_intelligence_pipeline(csv_file)
    else:
        print(f"CRITICAL ERROR: Synthetic data file not found at {csv_file}.")
        print("Please ensure your Gemini Code Assist Agent has generated the dataset.")