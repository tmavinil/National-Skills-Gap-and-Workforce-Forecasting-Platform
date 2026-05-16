# Module 4: Macro-Scenario Simulation Engine
import numpy as np
import pandas as pd

class MacroScenarioSimulationEngine:
    """
    Module 4: Macro-Scenario Simulation Engine
    Simulates national macroeconomic shocks, policy shifts, and funding impacts 
    on structural labor gaps over a 5-year planning horizon.
    """
    
    def __init__(self, planning_years=5):
        self.planning_years = planning_years
        self.months = planning_years * 12
        
    def generate_baseline_trajectory(self, initial_demand, initial_supply, growth_rate_demand, growth_rate_supply):
        """
        Creates a 60-month linear/exponential trend baseline for talent supply and demand 
        under status quo conditions.
        """
        timeline = np.arange(self.months)
        
        # Simulating rolling monthly compounding growth
        demand_trend = initial_demand * (1 + (growth_rate_demand / 12)) ** timeline
        supply_trend = initial_supply * (1 + (growth_rate_supply / 12)) ** timeline
        
        df_trajectory = pd.DataFrame({
            "month": timeline + 1,
            "baseline_demand": np.round(demand_trend, 0),
            "baseline_supply": np.round(supply_trend, 0),
            "baseline_gap": np.round(demand_trend - supply_trend, 0)
        })
        return df_trajectory

    def apply_scenario_shocks(self, df_baseline, scenario_config):
        """
        Applies macroeconomic policy and technology shocks to the baseline trajectory.
        
        Supported scenario variables in configuration:
        - 'ai_acceleration': Spikes demand automation or displaces specific roles.
        - 'recession_impact': Temporary downward demand contraction, drops training input.
        - 'immigration_policy_shift': Multiplies international talent supply inflows.
        - 'federal_funding_initiative': Accelerates localized pipeline replacement.
        """
        df_simulated = df_baseline.copy()
        
        # Extract shock multipliers from configuration (defaulting to 1.0 = neutral/no shock)
        ai_shock = scenario_config.get('ai_acceleration', 0.0)
        recession_shock = scenario_config.get('recession_impact', 0.0)
        immigration_modifier = scenario_config.get('immigration_policy_shift', 0.0)
        funding_infusion = scenario_config.get('federal_funding_initiative', 0.0)
        
        simulated_demand = []
        simulated_supply = []
        
        for idx, row in df_simulated.iterrows():
            m = row['month']
            
            # 1. Demand shocks compound over the timeline
            # AI might reduce manual demand or spike specialized engineering demand
            demand_modifier = 1.0 + (ai_shock * (m / self.months)) - (recession_shock * 0.05 if m <= 18 else 0)
            sim_d = row['baseline_demand'] * demand_modifier
            
            # 2. Supply shocks react to policy changes (e.g., funding takes 12 months to yield graduates)
            pipeline_delay_multiplier = (m - 12) / (self.months - 12) if m > 12 else 0.0
            supply_modifier = 1.0 + (immigration_modifier * (m / self.months)) + (funding_infusion * pipeline_delay_multiplier)
            sim_s = row['baseline_supply'] * supply_modifier
            
            simulated_demand.append(np.round(sim_d, 0))
            simulated_supply.append(np.round(sim_s, 0))
            
        df_simulated['simulated_demand'] = simulated_demand
        df_simulated['simulated_supply'] = simulated_supply
        df_simulated['simulated_gap'] = df_simulated['simulated_demand'] - df_simulated['simulated_supply']
        
        return df_simulated

    def evaluate_policy_mitigation_efficiency(self, df_simulated):
        """
        Quantifies the effectiveness of simulated public sector or policy interventions
        by comparing baseline structural shortages against optimized scenario paths.
        """
        final_month = self.months - 1
        
        base_terminal_gap = df_simulated.iloc[final_month]['baseline_gap']
        sim_terminal_gap = df_simulated.iloc[final_month]['simulated_gap']
        
        gap_reduction = base_terminal_gap - sim_terminal_gap
        pct_improvement = (gap_reduction / base_terminal_gap) * 100 if base_terminal_gap > 0 else 0.0
        
        return {
            "horizon_months": self.months,
            "unmitigated_terminal_shortage": int(base_terminal_gap),
            "simulated_terminal_shortage": int(sim_terminal_gap),
            "net_talent_shortage_averted": int(gap_reduction),
            "mitigation_efficiency_percentage": round(pct_improvement, 2)
        }


# Module self-validation block
if __name__ == "__main__":
    print("Testing Module 4 Scenario Simulation Pipeline...")
    engine = MacroScenarioSimulationEngine(planning_years=5)
    
    # Baseline: Microelectronics engineering gap expands over 5 years
    df_base = engine.generate_baseline_trajectory(
        initial_demand=15000, 
        initial_supply=11000, 
        growth_rate_demand=0.06,  # 6% annual expansion
        growth_rate_supply=0.01   # 1% annual organic graduation growth
    )
    
    # Define a Policy Simulation: "CHIPS Act Influx - 15% increase in dedicated training programs"
    # alongside a 5% increase in domestic high-skilled immigration pipelines
    chips_act_scenario = {
        'ai_acceleration': 0.02,            # AI increases complexity/demand for advanced chips slightly
        'recession_impact': 0.00,           # Stable economic expansion assumed
        'immigration_policy_shift': 0.05,   # Moderate high-skilled visa expansion
        'federal_funding_initiative': 0.15  # 15% training/apprenticeship expansion
    }
    
    df_results = engine.apply_scenario_shocks(df_base, chips_act_scenario)
    metrics = engine.evaluate_policy_mitigation_efficiency(df_results)
    
    print("\n--- Year 5 Baseline vs. Policy Intervention Simulation ---")
    print(f"Initial Unmitigated Shortage Trend (Month 60): {metrics['unmitigated_terminal_shortage']} vacancies.")
    print(f"Simulated Shortage After Federal Funding Intervention: {metrics['simulated_terminal_shortage']} vacancies.")
    print(f"✅ Structural Deficit Averted: {metrics['net_talent_shortage_averted']} roles ({metrics['mitigation_efficiency_percentage']}% Gap Reduction).")