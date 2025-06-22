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
        if param_obj is None:
            continue
        value_type: str = param_obj.type
        param_value = models.ToolParameterValue(
            tool_id=db_tool.id,
            parameter_id=param_obj.id
        )
        if value_type == "int":
            param_value.value_int = int(val) if val is not None else None
        elif value_type == "float":
            param_value.value_float = float(val) if val is not None else None
        elif value_type == "string":
            param_value.value_str = str(val) if val is not None else None
        db.add(param_value)

    db.commit()
    db.refresh(db_tool)

    return {
        "id": db_tool.id,
        "name": db_tool.name,
        "tool_type_id": db_tool.tool_type_id,
        "parameters": tool.parameters
    }

@router.get("/tools/", response_model=List[schemas.ToolRead])
def read_tools(db: Session = Depends(get_db)):
    tools = db.query(models.Tool).all()
    results = []
    for tool in tools:
        param_values = db.query(models.ToolParameterValue).filter_by(tool_id=tool.id).all()
        parameters = {}
        for pv in param_values:
            param = db.query(models.ToolParameter).filter_by(id=pv.parameter_id).first()
            if param is not None:
                value = None
                for attr in ['value_float', 'value_int', 'value_str']:
                    v = getattr(pv, attr)
                    if v is not None:
                        value = v
                        break
                parameters[param.name] = value
        results.append({
            "id": tool.id,
            "name": tool.name,
            "tool_type_id": tool.tool_type_id,
            "parameters": parameters
        })
    return results

@router.delete("/tools/{tool_id}")
def delete_tool(tool_id: int, db: Session = Depends(get_db)):
    tool = db.query(models.Tool).filter(models.Tool.id == tool_id).first()
    if tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    db.delete(tool)
    db.commit()
    return {"detail": "Deleted"}


@router.get("/tools/by_strategy/{strategy_id}", response_model=List[schemas.ToolRead])
def get_tools_by_strategy(strategy_id: int, db: Session = Depends(get_db)):
    strategy = db.query(models.Strategy).filter(models.Strategy.id == strategy_id).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")

    # Get all tooltypes that support this strategy
    tooltype_ids = [tt.id for tt in strategy.tool_types]

    # Get all tools that belong to these tooltypes
    tools = db.query(models.Tool).filter(models.Tool.tool_type_id.in_(tooltype_ids)).all()

    results = []
    for tool in tools:
        param_values = db.query(models.ToolParameterValue).filter_by(tool_id=tool.id).all()
        parameters = {}
        for pv in param_values:
            param = db.query(models.ToolParameter).filter_by(id=pv.parameter_id).first()
            if param is not None:
                value = None
                for attr in ['value_float', 'value_int', 'value_str']:
                    v = getattr(pv, attr)
                    if v is not None:
                        value = v
                        break
                parameters[param.name] = value
        results.append({
            "id": tool.id,
            "name": tool.name,
            "tool_type_id": tool.tool_type_id,
            "parameters": parameters
        })
    return results
