from pydantic import BaseModel
from typing import Optional, Dict

# MATERIALS
class MaterialCreate(BaseModel):
    name: str
    description: Optional[str] = ""

class MaterialRead(MaterialCreate):
    id: int
    class Config:
        from_attributes = True

# TOOL PARAMETERS
class ToolParameterCreate(BaseModel):
    name: str
    type: str
    description: Optional[str] = ""

class ToolParameterRead(ToolParameterCreate):
    id: int
    class Config:
        from_attributes = True

# RECIPE PARAMETERS
class RecipeParameterCreate(BaseModel):
    name: str
    type: str
    description: Optional[str] = ""

class RecipeParameterRead(RecipeParameterCreate):
    id: int
    class Config:
        from_attributes = True

# TOOL TYPES
class ToolTypeCreate(BaseModel):
    type_name: str
    tool_parameter_ids: list[int] = []
    strategy_ids: list[int] = []

class ToolTypeRead(ToolTypeCreate):
    id: int
    class Config:
        from_attributes = True

# STRATEGIES
class StrategyCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    recipe_parameter_ids: list[int] = []

class StrategyRead(StrategyCreate):
    id: int
    class Config:
        from_attributes = True

# TOOLS
class ToolCreate(BaseModel):
    name: str
    tool_type_id: int
    parameters: Dict[str, str | int | float]

class ToolRead(ToolCreate):
    id: int

# RECIPES
class RecipeCreate(BaseModel):
    material_id: int
    strategy_id: int
    tool_id: int
    parameters: Dict[str, str | int | float]

class RecipeRead(RecipeCreate):
    id: int
