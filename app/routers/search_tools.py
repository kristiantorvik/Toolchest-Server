from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas

router = APIRouter(prefix="/search_tools", tags=["Search tools"])

@router.post("/", response_model=list[int])
def search_tools(filters: schemas.SearchTools, db: Session = Depends(get_db)):
    query = db.query(models.Tool).filter_by(tool_type_id=filters.tool_type_id)
    

    # def find_value_type(value):
    #     try:
    #         value = int(value)
    #     except ValueError:
            
    #     else:
    #         return value
    
    #         val = float(value)
        
    #     raise HTTPException(status_code=400, detail=f"Unsupported parameter type: {param_obj.type}")


    for param,value in filters.parameters.items():
        tool_param_query = db.query(models.ToolParameter).filter_by(name=param).first()
        tool_param_id = tool_param_query.id
        param_type = tool_param_query.type

        param_value_query = db.query(models.ToolParameterValue).filter_by(parameter_id=tool_param_id)
        
        if param_type == "int":
            param_value_query = param_value_query.filter(models.ToolParameterValue.value_int.in_(int(value)))
        elif param_type == "int":
            param_value_query = param_value_query.filter(models.ToolParameterValue.value_float.in_(float(value)))
        elif param_type == "int":
            param_value_query = param_value_query.filter(models.ToolParameterValue.value_str.in_(value))

        tool_ids = [r.id for r in param_value_query.all()]

        query = query.filter(models.Tool.id.in_(tool_ids))


    # if filters.tool_type_ids:
    #     tool_ids = [t.id for t in db.query(models.Tool).filter(models.Tool.tool_type_id.in_(filters.tool_type_ids)).all()]
    #     query = query.filter(models.Recipe.tool_id.in_(tool_ids))

    # if filters.tool_ids:
    #     query = query.filter(models.Recipe.tool_id.in_(filters.tool_ids))

    filtered_tool_ids = [r.id for r in query.all()]
    print(filtered_tool_ids)
    return filtered_tool_ids
