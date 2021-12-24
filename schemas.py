# from enum import Enum
from pydantic import BaseModel

class QueryOptions(BaseModel):
    id: str = "3y5zzb"
    get_players: bool= False
    get_resources: bool= False