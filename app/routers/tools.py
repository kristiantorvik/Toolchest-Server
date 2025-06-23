from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..db import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/tools/", response_model=schemas.ToolRead)
def create_tool(tool: schemas.ToolCreate, db: Session = Depends(get_db)):
    db_tool = models.Tool(name=tool.name, tool_type_id=tool.tool_type_id)
    db.add(db_tool)
    db.commit()
    db.refresh(db_tool)

    # Save parameter values
    for pname, val in tool.parameters.items():
        param_obj = db.query(models.ToolParameter).filter(models.ToolParameter.name == pname).first()
        if not param_obj:
            continue
        value_type = param_obj.type
        param_value = models.ToolParameterValue(
            tool_id=db_tool.id,
            parameter_id=param_obj.id
        )
        if value_type == "int":
            param_value.value_int = int(val)
        elif value_type == "float":
            param_value.value_float = float(val)
        elif value_type == "string":
            param_value.value_str = str(val)
        db.add(param_value)

    db.commit()

    # Build parameters dict for response
    param_values = db.query(models.ToolParameterValue).filter_by(tool_id=db_tool.id).all()
    parameters = {}
    for pv in param_values:
        param = db.query(models.ToolParameter).filter_by(id=pv.parameter_id).first()
        value = pv.value_float or pv.value_int or pv.value_str
        parameters[param.name] = value

    return {
        "id": db_tool.id,
        "name": db_tool.name,
        "tool_type_id": db_tool.tool_type_id,
        "parameters": parameters
    }


    # Build parameters dict for response
    param_values = db.query(models.ToolParameterValue).filter_by(tool_id=db_tool.id).all()
    parameters = {}
    for pv in param_values:
        param = db.query(models.ToolParameter).filter_by(id=pv.parameter_id).first()
        value = pv.value_float or pv.value_int or pv.value_str
        parameters[param.name] = value

    return {
        "id": db_tool.id,
        "name": db_tool.name,
        "tool_type_id": db_tool.tool_type_id,
        "parameters": parameters
    }



@router.get("/tools/", response_model=List[schemas.ToolRead])
def read_tools(db: Session = Depends(get_db)):
    return db.query(models.Tool).all()

@router.get("/tools/by_strategy/{strategy_id}", response_model=List[schemas.ToolRead])
def get_tools_by_strategy(strategy_id: int, db: Session = Depends(get_db)):
    # First, get tool type ids for this strategy
    strategy = db.query(models.Strategy).filter(models.Strategy.id == strategy_id).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")

    tooltype_links = db.query(models.ToolTypeStrategyLink).filter_by(strategy_id=strategy_id).all()
    tooltype_ids = [link.tooltype_id for link in tooltype_links]

    # Now, get tools for those tool types
    tools = db.query(models.Tool).filter(models.Tool.tool_type_id.in_(tooltype_ids)).all()

    results = []
    for tool in tools:
        param_values = db.query(models.ToolParameterValue).filter_by(tool_id=tool.id).all()
        parameters = {}
        for pv in param_values:
            param = db.query(models.ToolParameter).filter_by(id=pv.parameter_id).first()
            value = None
            if pv.value_float is not None:
                value = pv.value_float
            elif pv.value_int is not None:
                value = pv.value_int
            elif pv.value_str is not None:
                value = pv.value_str
            parameters[param.name] = value

        results.append({
            "id": tool.id,
            "name": tool.name,
            "tool_type_id": tool.tool_type_id,
            "parameters": parameters
        })

    return results
