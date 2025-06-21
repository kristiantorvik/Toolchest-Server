from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship
from .db import Base

tooltype_strategy_link = Table(
    "tooltype_strategy_link",
    Base.metadata,
    Column("tooltype_id", Integer, ForeignKey("tool_types.id"), primary_key=True),
    Column("strategy_id", Integer, ForeignKey("strategies.id"), primary_key=True)
)

tooltype_parameter_link = Table(
    "tooltype_parameter_link",
    Base.metadata,
    Column("tooltype_id", Integer, ForeignKey("tool_types.id"), primary_key=True),
    Column("parameter_name", String, primary_key=True)
)

strategy_parameter_link = Table(
    "strategy_parameter_link",
    Base.metadata,
    Column("strategy_id", Integer, ForeignKey("strategies.id"), primary_key=True),
    Column("parameter_name", String, primary_key=True)
)


class Material(Base):
    __tablename__ = "materials"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)

class Strategy(Base):
    __tablename__ = "strategies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    tool_types = relationship(
        "ToolType",
        secondary=tooltype_strategy_link,
        back_populates="strategies"
    )

class ToolType(Base):
    __tablename__ = "tool_types"
    id = Column(Integer, primary_key=True, index=True)
    type_name = Column(String, unique=True)
    strategies = relationship(
        "Strategy",
        secondary=tooltype_strategy_link,
        back_populates="tool_types"
    )

class Tool(Base):
    __tablename__ = "tools"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    tool_type_id = Column(Integer, ForeignKey("tool_types.id"))
    diameter = Column(Float)
    number_of_flutes = Column(Integer)
    tool_designation = Column(String)
    description = Column(String)

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    tool_id = Column(Integer, ForeignKey("tools.id"))
    material_id = Column(Integer, ForeignKey("materials.id"))
    strategy_id = Column(Integer, ForeignKey("strategies.id"))
    cutting_speed = Column(Float)
    feedrate_fu = Column(Float)
    cut_depth = Column(Float)
    cut_width = Column(Float)
    lifetime = Column(Integer)
    coolant = Column(Boolean)
    airblast = Column(Boolean)



