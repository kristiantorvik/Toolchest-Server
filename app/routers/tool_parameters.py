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

@router.post("/tool_parameters/", response_model=schemas.ToolParameterRead)
def create_tool_parameter(param: schemas.ToolParameterCreate, db: Session = Depends(get_db)):
    db_param = models.ToolParameter(**param.dict())
    db.add(db_param)
    db.commit()
    db.refresh(db_param)
    return db_param

@router.get("/tool_parameters/", response_model=List[schemas.ToolParameterRead])
def read_tool_parameters(db: Session = Depends(get_db)):
    return db.query(models.ToolParameter).all()