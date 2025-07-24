from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from db import get_db
from auth import verify_api_key

router = APIRouter(
    dependencies=[Depends(verify_api_key)]
)


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
            raise HTTPException(status_code=400, detail="Tool parameter not found")

        param_value = models.ToolParameterValue(
            tool_id=tool.id,
            parameter_id=param_obj.id,
            value_float=value if param_obj.type == "float" else None,
            value_int=value if param_obj.type == "int" else None,
            value_str=value if param_obj.type == "string" else None
        )
        db.add(param_value)

    db.commit()

    return {
        "id": tool.id,
        "name": tool.name,
        "tool_type_id": tool.tool_type_id
    }


@router.delete("/tool/{tool_id}")
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


@router.patch("/tool/")
def edit_tool(update: schemas.ToolPatch, db: Session = Depends(get_db)):
    # Validate tool exists
    tool = db.query(models.Tool).filter_by(id=update.id).first()
    if not tool:
        raise HTTPException(status_code=400, detail="Tool not found")


    # Update name of tool
    tool.name = update.name

    # Update parameter values
    for param_id, value in update.parameters.items():
        param_obj = db.query(models.ToolParameter).filter_by(id=param_id).first()
        if not param_obj:
            raise HTTPException(status_code=400, detail=f"Tool parameter ID:{param_id} not found")

        # Checking if parameter was used
        used_param = db.query(models.ToolParameterValue).filter_by(tool_id=update.id, parameter_id=param_id).first()
        if used_param:
            if value == "":
                db.delete(used_param)

            p_type = param_obj.type
            if p_type == "string":
                used_param.value_str = value
                used_param.value_int = None
                used_param.value_float = None

            elif p_type == "int":
                used_param.value_str = None
                used_param.value_int = value
                used_param.value_float = None

            elif p_type == "float":
                used_param.value_str = None
                used_param.value_int = None
                used_param.value_float = value

            else:
                raise HTTPException(status_code=426, detail=f"Invalid parameter type:{param_obj.type}")

        else:
            if value == "":
                print(f"passing {param_id}")
                pass
            else:
                param_value = models.ToolParameterValue(
                    tool_id=tool.id,
                    parameter_id=param_obj.id,
                    value_float=value if param_obj.type == "float" else None,
                    value_int=value if param_obj.type == "int" else None,
                    value_str=value if param_obj.type == "string" else None
                )
                db.add(param_value)

    db.commit()

    return
