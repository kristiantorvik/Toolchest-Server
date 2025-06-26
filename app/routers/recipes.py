from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models
from .. import schemas
from ..db import get_db

router = APIRouter()

@router.get("/recipes/")
def get_recipes(db: Session = Depends(get_db)):
    recipes = db.query(models.Recipe).all()
    return [
        {
            "id": recipe.id,
            "material_id": recipe.material_id,
            "strategy_id": recipe.strategy_id,
            "tool_id": recipe.tool_id
        } for recipe in recipes
    ]


@router.post("/recipes/", response_model=dict)
def create_recipe(data: schemas.RecipeCreate, db: Session = Depends(get_db)):
    # Validate material, strategy, tool existence
    material = db.query(models.Material).filter_by(id=data.material_id).first()
    strategy = db.query(models.Strategy).filter_by(id=data.strategy_id).first()
    tool = db.query(models.Tool).filter_by(id=data.tool_id).first()
    if not all([material, strategy, tool]):
        raise HTTPException(status_code=400, detail="Invalid material, strategy, or tool ID")

    # Create the Recipe record
    recipe = models.Recipe(
        material_id=data.material_id,
        strategy_id=data.strategy_id,
        tool_id=data.tool_id
    )
    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    # Get all known parameters
    known_parameters = {
        p.name: p for p in db.query(models.RecipeParameter).all()
    }

    # Create associated RecipeParameterValues
    for param_name, value in data.parameters.items():
        param_obj = known_parameters.get(param_name)
        if not param_obj:
            continue  # Skip unknown parameters

        value_entry = models.RecipeParameterValue(
            recipe_id=recipe.id,
            parameter_id=param_obj.id
        )

        # Assign correct value field
        if param_obj.type == "int":
            value_entry.value_int = int(value)
        elif param_obj.type == "float":
            value_entry.value_float = float(value)
        elif param_obj.type == "string":
            value_entry.value_str = str(value)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported parameter type: {param_obj.type}")

        db.add(value_entry)

    db.commit()

    return {
        "id": recipe.id,
        "material_id": recipe.material_id,
        "strategy_id": recipe.strategy_id,
        "tool_id": recipe.tool_id,
        "parameters_saved": list(data.parameters.keys())
    }

@router.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    db.delete(recipe)
    db.commit()
    return {"detail": "Recipe deleted"}
