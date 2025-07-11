from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import Material
from ..db import get_db
from .. import schemas
from ..auth import verify_api_key

router = APIRouter(
    prefix="/materials",
    dependencies=[Depends(verify_api_key)]
)


# Get all materials
@router.get("/")
def get_materials(db: Session = Depends(get_db)):
    materials = db.query(Material).all()
    return [
        {"id": m.id, "name": m.name, "comment": m.comment}
        for m in materials
    ]


# Get single material
@router.get("/by_id/{material_id}")
def get_materials_by_id(material_id: int, db: Session = Depends(get_db)):
    material = db.query(Material).filter_by(id=material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return {"id": material.id, "name": material.name, "comment": material.comment}


# Create new material
@router.post("/")
def create_material(material: schemas.MaterialCreate, db: Session = Depends(get_db)):
    existing = db.query(Material).filter_by(name=material.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Material already exists.")

    new_material = Material(name=material.name, comment=material.comment)
    db.add(new_material)
    db.commit()
    db.refresh(new_material)
    return {"id": new_material.id, "name": new_material.name, "comment": new_material.comment}


# Delete material
@router.delete("/{material_id}")
def delete_material(material_id: int, db: Session = Depends(get_db)):
    material = db.query(Material).filter_by(id=material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found.")

    db.delete(material)
    db.commit()
    return {"detail": "Material deleted."}


# Patch material
@router.patch("/")
def update_material(update: schemas.MaterialPatch, db: Session = Depends(get_db)):
    material = db.query(Material).filter(Material.id == update.id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found.")

    material.name = update.name
    material.comment = update.comment

    db.commit()
    return {"detail": "Material updated."}
