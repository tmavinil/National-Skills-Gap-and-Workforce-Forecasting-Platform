# Module 3: Geospatial Vulnerability & Regional Mapping
import numpy as np
import pandas as pd

class GeographicLaborAnalyzer:
    """
    Module 3: Geospatial Vulnerability & Regional Mapping
    Executes MSA-level trend parsing, rural-urban dichotomy mapping, and
    industry concentration modeling using standard macroeconomic indicators.
    """
    
    def __init__(self):
        pass

    def calculate_location_quotient(self, local_occ_emp, total_local_emp, nat_occ_emp, total_nat_emp):
        """
        Calculates the Location Quotient (LQ) for an occupation within a specific region.
        LQ > 1.2 indicates a significant regional specialization and concentration.
        
        Formula:
        LQ = (Regional Occ Employment / Total Regional Employment) / 
             (National Occ Employment / Total National Employment)
        """
        if total_local_emp <= 0 or total_nat_emp <= 0 or nat_occ_emp <= 0:
            return 0.0
            
        local_ratio = local_occ_emp / total_local_emp
        national_ratio = nat_occ_emp / total_nat_emp
        
        lq = local_ratio / national_ratio
        return round(float(lq), 4)

    def analyze_regional_industrial_dependency(self, df_regional_data, df_national_baselines):
        """
        Evaluates regional industrial dependencies by blending MSA employment metrics 
        with baseline national employment metrics to identify fragile monoculture areas.
        """
        # Map national baselines for rapid lookup
        nat_map = df_national_baselines.set_index('soc_code').to_dict('index')
        
        results = []
        for _, row in df_regional_data.iterrows():
            soc = row['soc_code']
            nat_info = nat_map.get(soc, {"nat_occ_emp": 0, "total_nat_emp": 1})
            
            lq = self.calculate_location_quotient(
                local_occ_emp=row['local_occ_emp'],
                total_local_emp=row['total_local_emp'],
                nat_occ_emp=nat_info['nat_occ_emp'],
                total_nat_emp=nat_info['total_nat_emp']
            )
            
            # Determine concentration risk status based on standard BLS interpretive tiers
            dependency_risk = "HIGH_SPECIALIZATION" if lq >= 1.2 else "DIVERSIFIED"
            if lq < 0.8:
                dependency_risk = "UNDER_REPRESENTED"
                
            results.append({
                "msa_code": row['msa_code'],
                "msa_name": row['msa_name'],
                "soc_code": soc,
                "occupation_name": row['occupation_name'],
                "location_quotient": lq,
                "dependency_status": dependency_risk
            })
            
        return pd.DataFrame(results)

    def evaluate_rural_vs_urban_dynamics(self, df_geo_combined, rural_continuum_col='rucc_code'):
        """
        Differentiates labor migration and upskilling friction across urban hubs 
        versus non-MSA rural environments using standard USDA/OMB classifications.
        """
        # Higher RUCC codes indicate smaller, nonmetropolitan areas adjacent to rural zones
        df_processed = df_geo_combined.copy()
        
        conditions = [
            (df_processed[rural_continuum_col] <= 3),  # Urban/Metro
            (df_processed[rural_continuum_col] <= 6),  # Semi-Rural/Micro
        ]
        choices = ['METROPOLITAN_HUB', 'RELIANT_MICRO_AREA', 'ISOLATED_RURAL_ZONE']
        
        df_processed['geographic_tier'] = np.select(conditions, choices, default='ISOLATED_RURAL_ZONE')
        return df_processed

    def forecast_msa_level_vulnerability(self, df_lq_results, df_structural_vulnerability):
        """
        Blends localized concentration data (Location Quotients) with long-term 
        structural vulnerabilities to pinpoint regional economic instability hotspots.
        """
        vuln_map = df_structural_vulnerability.set_index('soc_code')['structural_vulnerability'].to_dict()
        
        forecast_results = []
        for _, row in df_lq_results.iterrows():
            soc = row['soc_code']
            sv_score = vuln_map.get(soc, 0.0)
            lq = row['location_quotient']
            
            # Hotspot multiplier combines local industry over-reliance with high structural retirement velocities
            localized_vulnerability_index = round(float(lq * sv_score), 4)
            
            forecast_results.append({
                "msa_name": row['msa_name'],
                "occupation_name": row['occupation_name'],
                "location_quotient": lq,
                "structural_vulnerability_baseline": sv_score,
                "localized_vulnerability_index": localized_vulnerability_index
            })
            
        return pd.DataFrame(forecast_results).sort_values(by='localized_vulnerability_index', ascending=False)


# Module self-validation block
if __name__ == "__main__":
    print("Testing Module 3 Geographic Analysis Engines...")
    analyzer = GeographicLaborAnalyzer()
    
    # 1. Setup sample national reference layers
    mock_national_baselines = pd.DataFrame([
        {"soc_code": "17-2131", "nat_occ_emp": 80000, "total_nat_emp": 150000000},  # Microelectronics
    ])
    
    # 2. Setup sample regional data reflecting different MSAs
    mock_regional_data = pd.DataFrame([
        # Austin MSA: High concentration of semiconductor engineers
        {"msa_code": "12420", "msa_name": "Austin-Round Rock, TX", "soc_code": "17-2131", "occupation_name": "Microelectronics Materials Engineers", "local_occ_emp": 4500, "total_local_emp": 1200000, "rucc_code": 1},
        # Isolated micro area with small manufacturing fab presence
        {"msa_code": "42200", "msa_name": "Rural Micro Cluster, VT", "soc_code": "17-2131", "occupation_name": "Microelectronics Materials Engineers", "local_occ_emp": 120, "total_local_emp": 15000, "rucc_code": 6}
    ])
    
    # 3. Setup mock vulnerability data from Module 1
    mock_vuln_data = pd.DataFrame([
        {"soc_code": "17-2131", "structural_vulnerability": 0.785} # Flagged as critical due to aging demographics
    ])
    
    # Execute pipelines
    lq_df = analyzer.analyze_regional_industrial_dependency(mock_regional_data, mock_national_baselines)
    geo_dynamic_df = analyzer.evaluate_rural_vs_urban_dynamics(mock_regional_data)
    hotspot_df = analyzer.forecast_msa_level_vulnerability(lq_df, mock_vuln_data)
    
    print("\n--- Regional Specialization Detection (Location Quotients) ---")
    print(lq_df[['msa_name', 'location_quotient', 'dependency_status']].to_string())
    
    print("\n--- Geographic Labor Vulnerability Hotspot Forecasting ---")
    print(hotspot_df[['msa_name', 'occupation_name', 'localized_vulnerability_index']].to_string())