from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas
from ..auth import verify_api_key

router = APIRouter(
    prefix="/search_tools",
    dependencies=[Depends(verify_api_key)],
    tags=["Search tools"]
)

@router.post("/", response_model=list[int])
def search_tools(filters: schemas.SearchTools, db: Session = Depends(get_db)):
    query = db.query(models.Tool).filter_by(tool_type_id=filters.tool_type_id)

    for param,value in filters.parameters.items():

        tool_param_query = db.query(models.ToolParameter).filter_by(name=param).first()
        tool_param_id = tool_param_query.id
        param_type = tool_param_query.type

        param_value_query = db.query(models.ToolParameterValue).filter_by(parameter_id=tool_param_id)
        
        if param_type == "int":
            param_value_query = param_value_query.filter_by(value_int=int(value))
        elif param_type == "float":
            param_value_query = param_value_query.filter_by(value_float=float(value))
        elif param_type == "string":
            param_value_query = param_value_query.filter_by(value_str=value)

        tool_ids = [r.tool_id for r in param_value_query.all()]
        query = query.filter(models.Tool.id.in_(tool_ids))


    filtered_tool_ids = [r.id for r in query.all()]
    return filtered_tool_ids
