from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from db import Base


# --- Materials ---
class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    comment = Column(String)


# --- Tool Types ---
class ToolType(Base):
    __tablename__ = "tool_types"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    strategies = relationship("ToolTypeStrategyLink", back_populates="tool_type", passive_deletes=True)
    parameters = relationship("ToolTypeToolParameterLink", back_populates="tool_type", passive_deletes=True)


# --- Strategies ---
class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

    recipe_parameters = relationship("StrategyRecipeParameterLink", back_populates="strategy", passive_deletes=True)


# --- Tools ---
class Tool(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    tool_type_id = Column(Integer, ForeignKey("tool_types.id", ondelete="CASCADE"), nullable=False)

    parameter_values = relationship("ToolParameterValue", back_populates="tool", passive_deletes=True)


# --- Recipes ---
class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)
    material_id = Column(Integer, ForeignKey("materials.id", ondelete="CASCADE"), nullable=False)
    strategy_id = Column(Integer, ForeignKey("strategies.id", ondelete="CASCADE"), nullable=False)
    tool_id = Column(Integer, ForeignKey("tools.id", ondelete="CASCADE"), nullable=False)

    parameter_values = relationship("RecipeParameterValue", back_populates="recipe", passive_deletes=True)


# --- Recipe Parameters ---
class RecipeParameter(Base):
    __tablename__ = "recipe_parameters"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)  # 'int', 'float', 'string'
    description = Column(String)


class RecipeParameterValue(Base):
    __tablename__ = "recipe_parameter_values"

    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False)
    parameter_id = Column(Integer, ForeignKey("recipe_parameters.id", ondelete="RESTRICT"), nullable=False)

    value_float = Column(Float, nullable=True)
    value_int = Column(Integer, nullable=True)
    value_str = Column(String, nullable=True)

    recipe = relationship("Recipe", back_populates="parameter_values", passive_deletes=True)
    parameter = relationship("RecipeParameter", passive_deletes=True)


class StrategyRecipeParameterLink(Base):
    __tablename__ = "strategy_recipeparameter_link"

    id = Column(Integer, primary_key=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id", ondelete="CASCADE"), nullable=False)
    parameter_id = Column(Integer, ForeignKey("recipe_parameters.id", ondelete="RESTRICT"), nullable=False)

    strategy = relationship("Strategy", back_populates="recipe_parameters", passive_deletes=True)
    recipe_parameter = relationship("RecipeParameter", passive_deletes=True)


# --- Tool Parameters ---
class ToolParameter(Base):
    __tablename__ = "tool_parameters"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)
    description = Column(String)


class ToolParameterValue(Base):
    __tablename__ = "tool_parameter_values"

    id = Column(Integer, primary_key=True)
    tool_id = Column(Integer, ForeignKey("tools.id", ondelete="CASCADE"), nullable=False)
    parameter_id = Column(Integer, ForeignKey("tool_parameters.id", ondelete="CASCADE"), nullable=False)

    value_float = Column(Float, nullable=True)
    value_int = Column(Integer, nullable=True)
    value_str = Column(String, nullable=True)

    tool = relationship("Tool", back_populates="parameter_values", passive_deletes=True)
    parameter = relationship("ToolParameter", passive_deletes=True)


class ToolTypeStrategyLink(Base):
    __tablename__ = "tooltype_strategy_link"

    id = Column(Integer, primary_key=True)
    tooltype_id = Column(Integer, ForeignKey("tool_types.id", ondelete="CASCADE"), nullable=False)
    strategy_id = Column(Integer, ForeignKey("strategies.id", ondelete="CASCADE"), nullable=False)

    tool_type = relationship("ToolType", back_populates="strategies", passive_deletes=True)
    strategy = relationship("Strategy", passive_deletes=True)


class ToolTypeToolParameterLink(Base):
    __tablename__ = "tooltype_toolparameter_link"

    id = Column(Integer, primary_key=True)
    tooltype_id = Column(Integer, ForeignKey("tool_types.id", ondelete="CASCADE"), nullable=False)
    parameter_id = Column(Integer, ForeignKey("tool_parameters.id", ondelete="CASCADE"), nullable=False)

    tool_type = relationship("ToolType", back_populates="parameters", passive_deletes=True)
    parameter = relationship("ToolParameter", passive_deletes=True)
