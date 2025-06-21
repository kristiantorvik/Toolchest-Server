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

@router.post("/tools/", response_model=schemas.ToolRead)
def create_tool(tool: schemas.ToolCreate, db: Session = Depends(get_db)):
    db_tool = models.Tool(**tool.dict())
    db.add(db_tool)
    db.commit()
    db.refresh(db_tool)
    return db_tool

@router.get("/tools/", response_model=list[schemas.ToolRead])
def read_tools(db: Session = Depends(get_db)):
    return db.query(models.Tool).all()

@router.delete("/tools/{tool_id}")
def delete_tool(tool_id: int, db: Session = Depends(get_db)):
    tool = db.query(models.Tool).filter(models.Tool.id == tool_id).first()
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    db.delete(tool)
    db.commit()
    return {"detail": "Deleted"}