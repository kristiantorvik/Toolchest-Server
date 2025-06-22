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
    db_tool_type = models.ToolType(type_name=tool_type.type_name)

    # Link strategies
    db_tool_type.strategies = db.query(models.Strategy).filter(models.Strategy.id.in_(tool_type.strategy_ids)).all()

    # Link tool parameters
    db_tool_type.tool_parameters = db.query(models.ToolParameter).filter(models.ToolParameter.id.in_(tool_type.tool_parameter_ids)).all()

    db.add(db_tool_type)
    db.commit()
    db.refresh(db_tool_type)
    return db_tool_type


@router.get("/tool_types/", response_model=list[schemas.ToolTypeRead])
def read_tool_types(db: Session = Depends(get_db)):
    return db.query(models.ToolType).all()

@router.get("/tooltype_parameters/{tooltype_id}")
def get_tooltype_parameters(tooltype_id: int, db: Session = Depends(get_db)):
    tooltype = db.query(models.ToolType).filter(models.ToolType.id == tooltype_id).first()
    if not tooltype:
        raise HTTPException(status_code=404, detail="ToolType not found")
    return [
        {"name": param.name, "type": param.type}
        for param in tooltype.tool_parameters
    ]

@router.delete("/tool_types/{tool_types_id}")
def delete_tool_types(tool_typer_id: int, db: Session = Depends(get_db)):
    tool_type = db.query(models.ToolType).filter(models.ToolType.id == tool_typer_id).first()
    if not tool_type:
        raise HTTPException(status_code=404, detail="Tool type not found")
    db.delete(tool_type)
    db.commit()
    return {"detail": "Deleted"}