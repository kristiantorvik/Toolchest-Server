from pydantic import BaseModel
from typing import Optional, List, Union, Dict

# ------------------- Tool Parameters -------------------

class ToolParameterBase(BaseModel):
    name: str
    type: str  # "int", "float", "string"
    description: Optional[str] = None

class ToolParameterCreate(ToolParameterBase):
    pass

class ToolParameterRead(ToolParameterBase):
    id: int

# ------------------- Tool Parameter Values -------------------

class ToolParameterValueBase(BaseModel):
    parameter_id: int
    value_int: Optional[int]
    value_float: Optional[float]
    value_str: Optional[str]

class ToolParameterValueCreate(ToolParameterValueBase):
    tool_id: int

class ToolParameterValueRead(ToolParameterValueBase):
    id: int
    tool_id: int

# ------------------- Recipe Parameters -------------------

class RecipeParameterBase(BaseModel):
    name: str
    type: str  # "int", "float", "string"
    description: Optional[str] = None

class RecipeParameterCreate(RecipeParameterBase):
    pass

class RecipeParameterRead(RecipeParameterBase):
    id: int


# ------------------- Recipe Parameter Values -------------------

class RecipeParameterValueBase(BaseModel):
    parameter_id: int
    value_int: Optional[int]
    value_float: Optional[float]
    value_str: Optional[str]

class RecipeParameterValueCreate(RecipeParameterValueBase):
    recipe_id: int

class RecipeParameterValueRead(RecipeParameterValueBase):
    recipe_id: int

# ------------------- Materials -------------------

class MaterialBase(BaseModel):
    name: str
    comment: Optional[str]

class MaterialCreate(MaterialBase):
    pass

class MaterialRead(MaterialBase):
    id: int

# ------------------- Tool Types -------------------

class ToolTypeBase(BaseModel):
    name: str
    tool_parameter_ids: List[int]
    strategy_ids: List[int]

class ToolTypeCreate(ToolTypeBase):
    pass

class ToolTypeRead(ToolTypeBase):
    id: int

# ------------------- Strategies -------------------

class StrategyBase(BaseModel):
    name: str
    description: Optional[str]
    parameter_ids: List[int]

class StrategyCreate(StrategyBase):
    pass

class StrategyRead(StrategyBase):
    id: int

# ------------------- Tools -------------------

class ToolBase(BaseModel):
    name: str
    tool_type_id: int
    parameters: Dict[str, Union[float, int, str]]

class ToolCreate(ToolBase):
    pass

class ToolRead(ToolBase):
    id: int

# ------------------- Recipes -------------------

class RecipeBase(BaseModel):
    material_id: int
    strategy_id: int
    tool_id: int

class RecipeCreate(RecipeBase):
    parameters: Dict[str, Union[int, float, str]]

class RecipeRead(RecipeBase):
    id: int

# ------------------- Linking Tables -------------------

class ToolTypeStrategyLinkCreate(BaseModel):
    tooltype_id: int
    strategy_id: int

class ToolTypeToolParameterLinkCreate(BaseModel):
    tooltype_id: int
    toolparameter_id: int

class StrategyRecipeParameterLinkCreate(BaseModel):
    strategy_id: int
    parameter_id: int



# ------------------- Search -------------------

class SearchFilters(BaseModel):
    strategy_id: int
    material_ids: List[int]
    tool_type_ids: List[int]
    tool_ids: List[int]