import uuid
from typing import Optional
from pydantic import BaseModel, Field 

class AugmentModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str
    tier: int
    desc: str
    tooltip: str


class FlowchartInstanceModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4,alias="_id")
    name : str = Field(...)
    current_round : int = 0
    completed: bool = False

    class Config:
        allow_population_by_field_name = True 
        schema_extra = {
            "example":{
                "id": "12345",
                "name": "aatrox_123",
                "progress" : {"item1": 1, "item2" : 2}
            }
        }



    
