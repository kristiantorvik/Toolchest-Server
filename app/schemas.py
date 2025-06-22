from pydantic import BaseModel
from typing import Optional,List, Dict, Union

class MaterialCreate(BaseModel):
    name: str
    description: Optional[str] = None
class MaterialRead(MaterialCreate):
    id: int
    class Config:
        from_attributes = True

class StrategyCreate(BaseModel):
    name: str
    description: Optional[str] = None
    recipe_parameter_ids: list[int] = []

class StrategyRead(StrategyCreate):
    id: int
    class Config:
        from_attributes = True

class ToolTypeCreate(BaseModel):
    type_name: str
    strategy_ids: list[int] = []
    tool_parameter_ids: list[int] = []



class ToolTypeRead(ToolTypeCreate):
    id: int
    class Config:
        from_attributes = True


from pydantic import BaseModel
from typing import List, Dict, Union

class ToolParameterValueCreate(BaseModel):
    parameter_id: int
    value: float

class ToolCreate(BaseModel):
    name: str
    tool_type_id: int
    parameters: Dict[str, Union[int, float, str]]

class ToolRead(BaseModel):
    id: int
    name: str
    tool_type_id: int
    parameters: Dict[str, Union[int, float, str]]
    
    class Config:
        orm_mode = True

class RecipeCreate(BaseModel):
    tool_id: int
    material_id: int
    strategy_id: int
    cutting_speed: float
    feedrate_fu: float
    cut_depth: float
    cut_width: float
    lifetime: int
    coolant: bool
    airblast: bool
class RecipeRead(RecipeCreate):
    id: int
    class Config:
        from_attributes = True




class RecipeParameterBase(BaseModel):
    name: str
    type: str
    description: str

class RecipeParameterCreate(RecipeParameterBase):
    pass

class RecipeParameterRead(RecipeParameterBase):
    id: int

    class Config:
        from_attributes = True  # for Pydantic V2
