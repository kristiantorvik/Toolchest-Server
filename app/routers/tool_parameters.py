from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..db import get_db
from typing import List

router = APIRouter()

@router.get("/tool_parameters/")
def get_tool_parameters(db: Session = Depends(get_db)):
    parameters = db.query(models.ToolParameter).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "type": p.type,
            "description": p.description
        } for p in parameters
    ]

@router.get("/tooltype_parameters/{tooltype_id}", response_model=List[schemas.ToolParameterRead])
def get_tooltype_parameters(tooltype_id: int, db: Session = Depends(get_db)):
    tooltype = db.query(models.ToolType).filter(models.ToolType.id == tooltype_id).first()
    if tooltype is None:
        raise HTTPException(status_code=404, detail="ToolType not found")
    links = db.query(models.ToolTypeToolParameterLink).filter_by(tooltype_id=tooltype_id).all()
    parameter_ids = [link.parameter_id for link in links]
    parameters = db.query(models.ToolParameter).filter(models.ToolParameter.id.in_(parameter_ids)).all()
    return parameters