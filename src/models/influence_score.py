from pydantic import BaseModel

class InfluenceScore(BaseModel):
    user:int
    influence_score:int|float