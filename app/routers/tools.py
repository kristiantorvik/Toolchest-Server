from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..db import get_db

router = APIRouter()


@router.get("/tools/")
def get_tools(db: Session = Depends(get_db)):
    tools = db.query(models.Tool).all()
    return [
        {
            "id": tool.id,
            "name": tool.name,
            "tool_type_id": tool.tool_type_id
        } for tool in tools
    ]

@router.post("/tools/")
def create_tool(tool_data: schemas.ToolCreate, db: Session = Depends(get_db)):
    # Validate tool type exists
    tool_type = db.query(models.ToolType).filter(models.ToolType.id == tool_data.tool_type_id).first()
    if not tool_type:
        raise HTTPException(status_code=400, detail="ToolType not found")

    tool = models.Tool(name=tool_data.name, tool_type_id=tool_data.tool_type_id)
    db.add(tool)
    db.commit()
    db.refresh(tool)

    # Add parameter values
    for param_name, value in tool_data.parameters.items():
        param_obj = db.query(models.ToolParameter).filter_by(name=param_name).first()
        if not param_obj:
            continue  # Optionally raise an error if parameter is not found

        param_value = models.ToolParameterValue(
            tool_id=tool.id,
            parameter_id=param_obj.id,
            value_float=value if param_obj.type == "float" else None,
            value_int=value if param_obj.type == "int" else None,
            value_str=value if param_obj.type == "str" else None
        )
        db.add(param_value)

    db.commit()

    return {
        "id": tool.id,
        "name": tool.name,
        "tool_type_id": tool.tool_type_id
    }

@router.delete("/tools/{tool_id}")
def delete_tool(tool_id: int, db: Session = Depends(get_db)):
    tool = db.query(models.Tool).filter(models.Tool.id == tool_id).first()
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")

    db.delete(tool)
    db.commit()
    return {"detail": "Tool deleted"}


@router.get("/tools/by_strategy/{strategy_id}", response_model=List[schemas.ToolRead])
def get_tools_by_strategy(strategy_id: int, db: Session = Depends(get_db)):
    # Validate strategy exists
    strategy = db.query(models.Strategy).filter(models.Strategy.id == strategy_id).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")

    # Find all tool types linked to this strategy
    tooltype_ids = db.query(models.ToolTypeStrategyLink.tooltype_id).filter_by(strategy_id=strategy_id).all()
    tooltype_ids = [tid[0] for tid in tooltype_ids]

    # Get tools with tool types supporting the strategy
    tools = db.query(models.Tool).filter(models.Tool.tool_type_id.in_(tooltype_ids)).all()
    result = []

    for tool in tools:
        parameters = {}
        param_values = db.query(models.ToolParameterValue).filter_by(tool_id=tool.id).all()

        for pv in param_values:
            param = db.query(models.ToolParameter).filter_by(id=pv.parameter_id).first()
            if not param:
                continue
            if pv.value_float is not None:
                parameters[param.name] = pv.value_float
            elif pv.value_int is not None:
                parameters[param.name] = pv.value_int
            elif pv.value_str is not None:
                parameters[param.name] = pv.value_str

        result.append({
            "id": tool.id,
            "name": tool.name,
            "tool_type_id": tool.tool_type_id,
            "parameters": parameters
        })

    return result
