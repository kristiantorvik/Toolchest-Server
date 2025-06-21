from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..db import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.post("/tool_types/", response_model=schemas.ToolTypeRead)
def create_tool(tool_type: schemas.ToolTypeCreate, db: Session = Depends(get_db)):
    db_tool_type = models.ToolType(**tool_type.dict())
    db.add(db_tool_type)
    db.commit()
    db.refresh(db_tool_type)
    return db_tool_type

@router.get("/tool_types/", response_model=list[schemas.ToolTypeRead])
def read_tool_types(db: Session = Depends(get_db)):
    return db.query(models.ToolType).all()

@router.delete("/tool_types/{tool_types_id}")
def delete_tool_types(tool_typer_id: int, db: Session = Depends(get_db)):
    tool_type = db.query(models.ToolType).filter(models.ToolType.id == tool_typer_id).first()
    if not tool_type:
        raise HTTPException(status_code=404, detail="Tool type not found")
    db.delete(tool_type)
    db.commit()
    return {"detail": "Deleted"}