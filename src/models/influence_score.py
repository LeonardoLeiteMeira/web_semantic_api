from pydantic import BaseModel


class InfluenceScore(BaseModel):
    user:str
    influence_score:int|float