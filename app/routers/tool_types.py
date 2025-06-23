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

@router.post("/tool_types/", response_model=schemas.ToolTypeRead)
def create_tool_type(tool_type: schemas.ToolTypeCreate, db: Session = Depends(get_db)):
    db_tool_type = models.ToolType(type_name=tool_type.type_name)
    db.add(db_tool_type)
    db.commit()
    db.refresh(db_tool_type)

    for param_id in tool_type.tool_parameter_ids:
        link = models.ToolTypeToolParameterLink(tooltype_id=db_tool_type.id, parameter_id=param_id)
        db.add(link)
    for strategy_id in tool_type.strategy_ids:
        link = models.ToolTypeStrategyLink(tooltype_id=db_tool_type.id, strategy_id=strategy_id)
        db.add(link)
    db.commit()
    return db_tool_type

@router.get("/tool_types/", response_model=List[schemas.ToolTypeRead])
def read_tool_types(db: Session = Depends(get_db)):
    return db.query(models.ToolType).all()

@router.get("/tooltype_parameters/{tooltype_id}", response_model=List[schemas.ToolParameterRead])
def get_tooltype_parameters(tooltype_id: int, db: Session = Depends(get_db)):
    tooltype = db.query(models.ToolType).filter(models.ToolType.id == tooltype_id).first()
    if tooltype is None:
        raise HTTPException(status_code=404, detail="ToolType not found")
    links = db.query(models.ToolTypeToolParameterLink).filter_by(tooltype_id=tooltype_id).all()
    parameter_ids = [link.parameter_id for link in links]
    parameters = db.query(models.ToolParameter).filter(models.ToolParameter.id.in_(parameter_ids)).all()
    return parameters