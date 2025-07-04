from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..db import get_db
from ..auth import verify_api_key

router = APIRouter(
    dependencies=[Depends(verify_api_key)]
)

@router.get("/tool_types/")
def get_tool_types(db: Session = Depends(get_db)):
    tool_types = db.query(models.ToolType).all()
    return [
        {
            "id": tool_type.id,
            "name": tool_type.name
        } for tool_type in tool_types
    ]

@router.post("/tool_types/")
def create_tool_type(tool_type_data: schemas.ToolTypeCreate, db: Session = Depends(get_db)):
    existing = db.query(models.ToolType).filter(models.ToolType.name == tool_type_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Tool type already exists")
    
    tool_type = models.ToolType(name=tool_type_data.name)
    db.add(tool_type)
    db.commit()
    db.refresh(tool_type)

    # Now add the links to tool parameters
    for param_id in tool_type_data.tool_parameter_ids:
        link = models.ToolTypeToolParameterLink(tooltype_id=tool_type.id, parameter_id=param_id)
        db.add(link)

    # Add links to strategies
    for strategy_id in tool_type_data.strategy_ids:
        link = models.ToolTypeStrategyLink(tooltype_id=tool_type.id, strategy_id=strategy_id)
        db.add(link)

    db.commit()

    return {
        "id": tool_type.id,
        "name": tool_type.name
    }

@router.delete("/tool_types/{tool_type_id}")
def delete_tool_type(tool_type_id: int, db: Session = Depends(get_db)):
    tool_type = db.query(models.ToolType).filter(models.ToolType.id == tool_type_id).first()
    if not tool_type:
        raise HTTPException(status_code=404, detail="Tool type not found")
    
    db.delete(tool_type)
    db.commit()

    return {"detail": "Tool type deleted"}
