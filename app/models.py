from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

# Materials
class Material(Base):
    __tablename__ = "materials"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)

# Tool Parameters
class ToolParameter(Base):
    __tablename__ = "tool_parameters"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    type = Column(String)
    description = Column(String)
    
    tooltype_links = relationship("ToolTypeToolParameterLink", back_populates="parameter")

# Tool Types
class ToolType(Base):
    __tablename__ = "tool_types"
    id = Column(Integer, primary_key=True)
    type_name = Column(String, unique=True)

    parameters = relationship("ToolTypeToolParameterLink", back_populates="tool_type")
    strategies = relationship("ToolTypeStrategyLink", back_populates="tool_type")

# Tools
class Tool(Base):
    __tablename__ = "tools"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    tool_type_id = Column(Integer, ForeignKey("tool_types.id"))

    parameter_values = relationship("ToolParameterValue", back_populates="tool")

# Tool Parameter Values
class ToolParameterValue(Base):
    __tablename__ = "tool_parameter_values"
    id = Column(Integer, primary_key=True)
    tool_id = Column(Integer, ForeignKey("tools.id"))
    parameter_id = Column(Integer, ForeignKey("tool_parameters.id"))
    value_float = Column(Float, nullable=True)
    value_int = Column(Integer, nullable=True)
    value_str = Column(String, nullable=True)

    tool = relationship("Tool", back_populates="parameter_values")
    parameter = relationship("ToolParameter")

# ToolType <-> ToolParameter association object
class ToolTypeToolParameterLink(Base):
    __tablename__ = "tooltype_toolparameter_link"
    id = Column(Integer, primary_key=True)
    tooltype_id = Column(Integer, ForeignKey("tool_types.id"))
    parameter_id = Column(Integer, ForeignKey("tool_parameters.id"))

    tool_type = relationship("ToolType", back_populates="parameters")
    parameter = relationship("ToolParameter", back_populates="tooltype_links")

# Strategies
class Strategy(Base):
    __tablename__ = "strategies"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)

    tooltype_links = relationship("ToolTypeStrategyLink", back_populates="strategy")
    recipeparameter_links = relationship("StrategyRecipeParameterLink", back_populates="strategy")

# ToolType <-> Strategy association object
class ToolTypeStrategyLink(Base):
    __tablename__ = "tooltype_strategy_link"
    id = Column(Integer, primary_key=True)
    tooltype_id = Column(Integer, ForeignKey("tool_types.id"))
    strategy_id = Column(Integer, ForeignKey("strategies.id"))

    tool_type = relationship("ToolType", back_populates="strategies")
    strategy = relationship("Strategy", back_populates="tooltype_links")

# Recipe Parameters
class RecipeParameter(Base):
    __tablename__ = "recipe_parameters"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    type = Column(String)
    description = Column(String)

    strategy_links = relationship("StrategyRecipeParameterLink", back_populates="recipe_parameter")

# Strategy <-> RecipeParameter association object
class StrategyRecipeParameterLink(Base):
    __tablename__ = "strategy_recipeparameter_link"
    id = Column(Integer, primary_key=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"))
    parameter_id = Column(Integer, ForeignKey("recipe_parameters.id"))

    strategy = relationship("Strategy", back_populates="recipeparameter_links")
    recipe_parameter = relationship("RecipeParameter", back_populates="strategy_links")

# Recipes
class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True)
    material_id = Column(Integer, ForeignKey("materials.id"))
    strategy_id = Column(Integer, ForeignKey("strategies.id"))
    tool_id = Column(Integer, ForeignKey("tools.id"))

    parameter_values = relationship("RecipeParameterValue", back_populates="recipe")

# Recipe Parameter Values
class RecipeParameterValue(Base):
    __tablename__ = "recipe_parameter_values"
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    parameter_id = Column(Integer, ForeignKey("recipe_parameters.id"))
    value_float = Column(Float, nullable=True)
    value_int = Column(Integer, nullable=True)
    value_str = Column(String, nullable=True)

    recipe = relationship("Recipe", back_populates="parameter_values")
    parameter = relationship("RecipeParameter")
