# Module 2: Cross-Sector Workforce Mobility Forecasting
import numpy as np
import pandas as pd
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity

class CrossSectorMobilityForecaster:
    """
    Module 2: Cross-Sector Workforce Mobility Forecasting
    Implements interpretable NLP skill-matching, career pathway graph construction,
    and macroeconomic ROI projections for targeted national reskilling.
    """
    
    def __init__(self):
        # Initialize a Directed Graph to map occupational transition networks
        self.mobility_graph = nx.DiGraph()
        
    def calculate_skill_similarity(self, vec_a, vec_b):
        """
        Calculates transparent skill similarity scoring using Cosine Similarity.
        Ensures explainable AI (XAI) standards by outputting clear directional features.
        """
        # Reshape for sklearn compatibility
        v_a = np.array(vec_a).reshape(1, -1)
        v_b = np.array(vec_b).reshape(1, -1)
        
        score = cosine_similarity(v_a, v_b)[0][0]
        return round(float(score), 4)

    def build_mobility_network(self, occupations_dict, threshold=0.50):
        """
        Constructs a career mobility network where nodes are occupations 
        and edges indicate viable transition vectors exceeding the similarity threshold.
        """
        self.mobility_graph.clear()
        
        # Add occupational nodes
        for job_name, skill_vector in occupations_dict.items():
            self.mobility_graph.add_node(job_name, skill_vector=skill_vector)
            
        # Add directed transitions based on skill adjacencies
        jobs = list(occupations_dict.keys())
        for i in range(len(jobs)):
            for j in range(len(jobs)):
                if i != j:
                    job_a = jobs[i]
                    job_b = jobs[j]
                    
                    similarity = self.calculate_skill_similarity(
                        occupations_dict[job_a], occupations_dict[job_b]
                    )
                    
                    if similarity >= threshold:
                        # Edge weight is inverse to similarity (lower distance = easier transition)
                        transition_friction = round(1.0 - similarity, 4)
                        self.mobility_graph.add_edge(
                            job_a, job_b, weight=transition_friction, similarity=similarity
                        )

    def find_mobility_pathway(self, source_job, target_job):
        """
        Algorithmically discovers optimal workforce pathways. 
        If the skill gap is too vast, utilizes Shortest Path logic via NetworkX 
        to discover intermediate 'stepping stone' occupations to minimize friction.
        """
        if not self.mobility_graph.has_node(source_job) or not self.mobility_graph.has_node(target_job):
            return {"status": "ERROR", "message": "Source or Target occupation not found in matrix."}
            
        try:
            # Shortest weighted path handles the transition with the lowest overall skill friction
            path = nx.shortest_path(self.mobility_graph, source=source_job, target=target_job, weight='weight')
            path_edges = list(zip(path[:-1], path[1:]))
            
            steps = []
            for u, v in path_edges:
                steps.append({
                    "from": u,
                    "to": v,
                    "similarity_match": self.mobility_graph[u][v]['similarity']
                })
                
            return {
                "status": "SUCCESS",
                "optimal_pathway": path,
                "transition_steps": steps
            }
        except nx.NetworkXNoPath:
            return {
                "status": "BLOCKED",
                "message": f"Direct or intermediate pathway from {source_job} to {target_job} is unfeasible given current skill matrix definitions."
            }

    def estimate_retraining_efficiency(self, skill_similarity, target_job_zone):
        """
        Quantifies the retraining friction by estimating the estimated months of upskilling 
        required based on the O*NET Job Zone profile and measured skill deficit.
        """
        # Baseline preparation months maps roughly to federal O*NET Specific Vocational Preparation (SVP) tiers
        job_zone_baseline_months = {1: 3, 2: 6, 3: 12, 4: 24, 5: 48}
        baseline = job_zone_baseline_months.get(target_job_zone, 12)
        
        # Skill gap acts as a linear multiplier on training duration requirements
        skill_gap = 1.0 - skill_similarity
        estimated_months = baseline * (1 + skill_gap)
        return round(estimated_months, 1)

    def project_macro_reskilling_roi(self, cohort_volume, wage_delta, annual_unemployment_savings, total_program_cost):
        """
        Calculates the Macroeconomic Return on Investment for the U.S. Economy.
        Measures public funds saved and localized GDP value-add variations against training program expenditures.
        """
        if total_program_cost <= 0:
            return 0.0
            
        # Economic benefits = wage additions + public assistance expenditures averted
        annual_economic_benefit = cohort_volume * (wage_delta + annual_unemployment_savings)
        
        # Calculate 3-year structural impact projection
        total_3yr_benefit = annual_economic_benefit * 3
        macro_roi = (total_3yr_benefit - total_program_cost) / total_program_cost
        
        return round(macro_roi, 2)


# Module self-validation block
if __name__ == "__main__":
    print("Testing Module 2 Architecture Elements...")
    forecaster = CrossSectorMobilityForecaster()
    
    # High-dimensional mock skill profile arrays representing standardized competency indices
    # Index representations: [Data Analytics, Advanced Math, Physical Metallurgy, Automation Engineering, Manual Dexterity]
    mock_profiles = {
        "Displaced Insurance Underwriter":  [0.80, 0.60, 0.00, 0.20, 0.10],
        "Intermediate Industrial Analyst":  [0.75, 0.70, 0.30, 0.50, 0.20],
        "Microelectronics Manufacturing Tech": [0.60, 0.75, 0.70, 0.85, 0.60]
    }
    
    # Build graph with a low similarity filter to allow multi-hop path testing
    forecaster.build_mobility_network(mock_profiles, threshold=0.40)
    
    print("\n--- Career Transition Graph Nodes ---")
    print("Mapped Positions:", list(forecaster.mobility_graph.nodes))
    
    # Attempt a multi-hop pathway search from a displaced office role to a technical microelectronics semiconductor role
    pathway_results = forecaster.find_mobility_pathway(
        source_job="Displaced Insurance Underwriter", 
        target_job="Microelectronics Manufacturing Tech"
    )
    
    print("\n--- Pathway Discovery Verification ---")
    if pathway_results["status"] == "SUCCESS":
        print(" -> ".join(pathway_results["optimal_pathway"]))
        
    # Calculate a sample macro ROI projection
    sample_roi = forecaster.project_macro_reskilling_roi(
        cohort_volume=500,                    # 500 workers transitioned
        wage_delta=15000,                      # $15k average salary increase in strategic tech sector
        annual_unemployment_savings=9000,      # $9k saved per worker in state unemployment assistance
        total_program_cost=4500000             # $4.5M comprehensive training grant funding
    )
    print(f"\nProjected Macroeconomic 3-Year Return on Investment: {sample_roi}x")