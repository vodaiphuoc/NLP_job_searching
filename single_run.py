from src.training import Compute_Assign_Score
import json


with open("program_config.json", "r") as f:
    config = json.load(f)

engine = Compute_Assign_Score(**config)

engine.compute_and_assign_score()