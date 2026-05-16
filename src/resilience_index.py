# Module 1: National Workforce Resilience Index & Early Warning System
import numpy as np
import pandas as pd

class NationalWorkforceResilienceIndex:
    """
    Module 1: National Workforce Resilience Index & Early Warning System
    Designed to monitor structural labor health in federally designated strategic sectors
    and generate early-warning indicators for public policy planning.
    """
    
    def __init__(self, alpha=0.75, beta=0.25):
        # Alpha represents the sensitivity weight for long-term structural threats (demographics)
        # Beta represents the weight for skill isolation / low transferability
        self.alpha = alpha
        self.beta = beta
        
    def calculate_structural_vulnerability(self, retirement_velocity, skill_transferability, pipeline_replacement):
        """
        Calculates the Structural Vulnerability Score (Sv) for a given occupation or sector.
        High values indicate high risk of talent depletion.
        """
        # Ensure input boundaries are constrained between 0 and 1
        v_r = np.clip(retirement_velocity, 0, 1)
        t_s = np.clip(skill_transferability, 0, 1)
        r_p = np.clip(pipeline_replacement, 0, 1)
        
        # Base structural vulnerability model
        base_vulnerability = (self.alpha * v_r) + (self.beta * (1 - t_s))
        
        # Net score adjusted by incoming talent pipeline mitigation capacity
        structural_vulnerability_score = base_vulnerability * (1 - r_p)
        return round(float(structural_vulnerability_score), 4)

    def evaluate_semiconductor_stability(self, df_sector_data):
        """
        Computes the Semiconductor Labor Stability Index.
        Expects a DataFrame containing historical and simulated labor data for microelectronics.
        """
        results = []
        for _, row in df_sector_data.iterrows():
            sv_score = self.calculate_structural_vulnerability(
                retirement_velocity=row['retirement_velocity'],
                skill_transferability=row['skill_transferability'],
                pipeline_replacement=row['pipeline_replacement']
            )
            
            # Index is inverse to vulnerability: higher score means a more stable workforce
            stability_index = 1.0 - sv_score
            results.append({
                "soc_code": row['soc_code'],
                "occupation_name": row['occupation_name'],
                "structural_vulnerability": sv_score,
                "labor_stability_index": round(stability_index, 4)
            })
            
        return pd.DataFrame(results)

    def run_early_warning_system(self, df_stability_results, critical_threshold=0.40):
        """
        Monitors structural resilience scores and triggers proactive policy alert status markers 
        before severe talent shortage crisis thresholds are breached.
        """
        alerts = []
        for _, row in df_stability_results.iterrows():
            vulnerability = row['structural_vulnerability']
            
            if vulnerability >= 0.75:
                status = "CRITICAL_RISK_ALERT"
                recommendation = "Immediate federal pipeline funding and fast-track vocational training expansion recommended."
            elif vulnerability >= critical_threshold:
                status = "ELEVATED_VULNERABILITY_WARNING"
                recommendation = "Strategic workforce planning intervention required. Target cross-sector upskilling pathways."
            else:
                status = "STABLE"
                recommendation = "Routine talent pipeline maintenance monitoring."
                
            alerts.append({
                "occupation_name": row['occupation_name'],
                "vulnerability_score": vulnerability,
                "system_status": status,
                "policy_action_directive": recommendation
            })
            
        return pd.DataFrame(alerts)

# Self-test logic to verify module stability
if __name__ == "__main__":
    print("Testing Module 1 Architecture Components...")
    evaluator = NationalWorkforceResilienceIndex()
    
    # Mock data structure matching expected BLS / O*NET integrated data
    mock_semi_data = pd.DataFrame([
        {"soc_code": "17-2131", "occupation_name": "Microelectronics Materials Engineers", "retirement_velocity": 0.85, "skill_transferability": 0.15, "pipeline_replacement": 0.10},
        {"soc_code": "51-9141", "occupation_name": "Semiconductor Wafer Fabrication Operators", "retirement_velocity": 0.70, "skill_transferability": 0.30, "pipeline_replacement": 0.25}
    ])
    
    stability_df = evaluator.evaluate_semiconductor_stability(mock_semi_data)
    alerts_df = evaluator.run_early_warning_system(stability_df)
    
    print("\n--- Model Output Baseline Verification Success ---")
    print(alerts_df[['occupation_name', 'vulnerability_score', 'system_status']].to_string())