import pandas as pd
import numpy as np
import random
import os

def generate_mock_data(num_rows=50, output_path="synthetic_workforce_data.csv"):
    np.random.seed(42)
    random.seed(42)
    
    sectors = ["Healthcare", "Semiconductor"]
    
    occupations = {
        "Healthcare": [
            ("29-1141", "Registered Nurses"),
            ("29-1062", "Family Medicine Physicians"),
            ("31-1131", "Nursing Assistants"),
            ("29-2061", "Licensed Practical Nurses"),
            ("29-1123", "Physical Therapists"),
            ("29-2010", "Clinical Laboratory Technologists and Technicians"),
            ("21-1094", "Community Health Workers"),
            ("31-9092", "Medical Assistants")
        ],
        "Semiconductor": [
            ("17-2131", "Microelectronics Materials Engineers"),
            ("51-9141", "Semiconductor Wafer Fabrication Operators"),
            ("17-2072", "Electronics Engineering Technicians"),
            ("17-2071", "Electrical Engineers"),
            ("51-2022", "Electrical and Electronic Equipment Assemblers"),
            ("17-2112", "Industrial Engineers"),
            ("19-2031", "Chemists"),
            ("11-9041", "Architectural and Engineering Managers")
        ]
    }
    
    data = []
    
    for _ in range(num_rows):
        sector = random.choice(sectors)
        soc_code, occ_name = random.choice(occupations[sector])
        
        # Generating diverse metrics representing different workforce realities
        if sector == "Healthcare":
            ret_vel = np.clip(np.random.normal(loc=0.5, scale=0.2), 0.1, 0.9)
            skill_trans = np.clip(np.random.normal(loc=0.4, scale=0.2), 0.1, 0.8)
            pipe_repl = np.clip(np.random.normal(loc=0.4, scale=0.2), 0.1, 0.9)
        else:
            # Semiconductor sector typically has higher retirement velocity and lower skill transferability
            ret_vel = np.clip(np.random.normal(loc=0.7, scale=0.15), 0.2, 0.95)
            skill_trans = np.clip(np.random.normal(loc=0.25, scale=0.15), 0.05, 0.6)
            pipe_repl = np.clip(np.random.normal(loc=0.2, scale=0.15), 0.05, 0.5)
            
        data.append({
            "sector": sector,
            "soc_code": soc_code,
            "occupation_name": occ_name,
            "retirement_velocity": round(float(ret_vel), 4),
            "skill_transferability": round(float(skill_trans), 4),
            "pipeline_replacement": round(float(pipe_repl), 4)
        })
        
    df = pd.DataFrame(data)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    df.to_csv(output_path, index=False)
    print(f"Successfully generated {num_rows} rows of mock workforce data at {output_path}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, "synthetic_workforce_data.csv")
    generate_mock_data(num_rows=50, output_path=output_file)
