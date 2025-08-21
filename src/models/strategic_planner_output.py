from pydantic import BaseModel
from typing import List

class StrategicPlannerOutput(BaseModel):
    """Output schema for strategic planner. Returns a list of tool names in sequence"""
    plan: List[str]