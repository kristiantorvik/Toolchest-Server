from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..db import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/recipes/", response_model=schemas.RecipeRead)
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    # Create Recipe entry
    db_recipe = models.Recipe(
        material_id=recipe.material_id,
        strategy_id=recipe.strategy_id,
        tool_id=recipe.tool_id
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)

    # Save parameter values
    for pname, val in recipe.parameters.items():
        param_obj = db.query(models.RecipeParameter).filter(models.RecipeParameter.name == pname).first()
        if param_obj is None:
            continue

        param_value = models.RecipeParameterValue(
            recipe_id=db_recipe.id,
            parameter_id=param_obj.id
        )

        param_type: str = str(param_obj.type)  # Cast for Pylance happiness

        if param_type == "int":
            param_value.value_int = int(val) if val is not None else None
        elif param_type == "float":
            param_value.value_float = float(val) if val is not None else None
        elif param_type == "string":
            param_value.value_str = str(val) if val is not None else None

        db.add(param_value)

    db.commit()
    db.refresh(db_recipe)
    return build_recipe_read(db_recipe, db)

@router.get("/recipes/", response_model=List[schemas.RecipeRead])
def read_recipes(db: Session = Depends(get_db)):
    recipes = db.query(models.Recipe).all()
    return [build_recipe_read(recipe, db) for recipe in recipes]

@router.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db.delete(recipe)
    db.commit()
    return {"detail": "Deleted"}

def build_recipe_read(recipe: models.Recipe, db: Session) -> schemas.RecipeRead:
    param_values = db.query(models.RecipeParameterValue).filter_by(recipe_id=recipe.id).all()
    parameters = {}
    for pv in param_values:
        param = db.query(models.RecipeParameter).filter_by(id=pv.parameter_id).first()
        if param is None:
            continue

        value = None
        if pv.value_float is not None:
            value = pv.value_float
        elif pv.value_int is not None:
            value = pv.value_int
        elif pv.value_str is not None:
            value = pv.value_str

        parameters[param.name] = value

    return schemas.RecipeRead(
        id=recipe.id,
        material_id=recipe.material_id,
        strategy_id=recipe.strategy_id,
        tool_id=recipe.tool_id,
        parameters=parameters
    )
