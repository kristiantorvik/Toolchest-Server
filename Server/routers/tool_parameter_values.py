from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from db import get_db
from auth import verify_api_key

router = APIRouter(
    dependencies=[Depends(verify_api_key)]
)


@router.post("/tools/{tool_id}/parameters")
def update_tool_parameter_values(tool_id: int, parameters: dict, db: Session = Depends(get_db)):
    tool = db.query(models.Tool).filter(models.Tool.id == tool_id).first()
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")

    for param_name, param_value in parameters.items():
        param = db.query(models.ToolParameter).filter_by(name=param_name).first()
        if not param:
            continue  # skip unknown parameters

        # check if value already exists
        param_value_record = (
            db.query(models.ToolParameterValue)
            .filter_by(tool_id=tool_id, parameter_id=param.id)
            .first()
        )

        if not param_value_record:
            param_value_record = models.ToolParameterValue(
                tool_id=tool_id,
                parameter_id=param.id
            )

        # assign value according to type
        param_value_record.value_int = None
        param_value_record.value_float = None
        param_value_record.value_str = None

        if param.type == "int":
            param_value_record.value_int = int(param_value)
        elif param.type == "float":
            param_value_record.value_float = float(param_value)
        elif param.type == "string":
            param_value_record.value_str = str(param_value)

        db.add(param_value_record)

    db.commit()

    return {"detail": "Parameter values updated"}



@router.get("/tool_detail/{tool_id}")
def get_tool_detail(tool_id: int, db: Session = Depends(get_db)):
    tool = db.query(models.Tool).filter_by(id=tool_id).first()
    if not tool:
        raise HTTPException(status_code=404, detail="tool not found")

    values = db.query(models.ToolParameterValue).filter_by(tool_id=tool.id).all()
    parameter_map = {}
    for v in values:
        param = db.query(models.ToolParameter).filter_by(id=v.parameter_id).first()
        val = v.value_float or v.value_int or v.value_str
        parameter_map[param.name] = val

    return {
        "id": tool.id,
        "name": tool.name,
        "tool_type_id": tool.tool_type_id,
        "parameters": parameter_map,
    }


@router.get("/tools/{tool_id}/parameters")
def get_tool_parameter_values(tool_id: int, db: Session = Depends(get_db)):
    tool = db.query(models.Tool).filter(models.Tool.id == tool_id).first()
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")

    param_values = db.query(models.ToolParameterValue).filter_by(tool_id=tool_id).all()

    result = []
    for pv in param_values:
        param = pv.parameter
        value = None
        if pv.value_int is not None:
            value = pv.value_int
        elif pv.value_float is not None:
            value = pv.value_float
        elif pv.value_str is not None:
            value = pv.value_str

        result.append({
            "parameter_id": param.id,
            "name": param.name,
            "type": param.type,
            "value": value
        })

    return result
