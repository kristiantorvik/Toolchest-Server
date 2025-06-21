from pydantic import BaseModel
from typing import Optional

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
class StrategyRead(StrategyCreate):
    id: int
    class Config:
        from_attributes = True

class ToolTypeCreate(BaseModel):
    type_name: str
class ToolTypeRead(ToolTypeCreate):
    id: int
    class Config:
        from_attributes = True

class ToolCreate(BaseModel):
    name: str
    tool_type_id: int
    diameter: float
    number_of_flutes: int
    tool_designation: Optional[str] = None
    description: Optional[str] = None
class ToolRead(ToolCreate):
    id: int
    class Config:
        from_attributes = True

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
