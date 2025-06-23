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


@router.post("/recipes/", response_model=schemas.RecipeRead)
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    # First create the recipe base object
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
        if not param_obj:
            continue
        param_value = models.RecipeParameterValue(
            recipe_id=db_recipe.id,
            parameter_id=param_obj.id
        )
        if param_obj.type == "int":
            param_value.value_int = int(val)
        elif param_obj.type == "float":
            param_value.value_float = float(val)
        elif param_obj.type == "string":
            param_value.value_str = str(val)
        db.add(param_value)

    db.commit()

    # Now build response
    param_values = db.query(models.RecipeParameterValue).filter_by(recipe_id=db_recipe.id).all()
    parameters = {}
    for pv in param_values:
        param = db.query(models.RecipeParameter).filter_by(id=pv.parameter_id).first()
        value = None
        if pv.value_float is not None:
            value = pv.value_float
        elif pv.value_int is not None:
            value = pv.value_int
        elif pv.value_str is not None:
            value = pv.value_str
        parameters[param.name] = value

    return {
        "id": db_recipe.id,
        "material_id": db_recipe.material_id,
        "strategy_id": db_recipe.strategy_id,
        "tool_id": db_recipe.tool_id,
        "parameters": parameters
    }


@router.get("/recipes/", response_model=List[schemas.RecipeRead])
def read_recipes(db: Session = Depends(get_db)):
    return db.query(models.Recipe).all()

@router.get("/strategy_recipe_parameters/{strategy_id}", response_model=List[schemas.RecipeParameterRead])
def get_recipe_parameters_for_strategy(strategy_id: int, db: Session = Depends(get_db)):
    links = db.query(models.StrategyRecipeParameterLink).filter_by(strategy_id=strategy_id).all()
    parameter_ids = [link.parameter_id for link in links]
    parameters = db.query(models.RecipeParameter).filter(models.RecipeParameter.id.in_(parameter_ids)).all()
    return parameters
