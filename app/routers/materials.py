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

@router.post("/materials/", response_model=schemas.MaterialRead)
def create_material(material: schemas.MaterialCreate, db: Session = Depends(get_db)):
    db_material = models.Material(**material.dict())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material

@router.get("/materials/", response_model=list[schemas.MaterialRead])
def read_materials(db: Session = Depends(get_db)):
    return db.query(models.Material).all()

@router.delete("/materials/{material_id}")
def delete_material(material_id: int, db: Session = Depends(get_db)):
    material = db.query(models.Material).filter(models.Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    db.delete(material)
    db.commit()
    return {"detail": "Deleted"}