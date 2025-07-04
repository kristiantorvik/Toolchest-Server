from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from ..db import get_db
from ..auth import verify_api_key

router = APIRouter(
    dependencies=[Depends(verify_api_key)]
)



@router.post("/recipes/{recipe_id}/parameters/")
def set_recipe_parameter_value(recipe_id: int, parameter_id: int, value: str, db: Session = Depends(get_db)):
    recipe = db.query(models.Recipe).filter_by(id=recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    parameter = db.query(models.RecipeParameter).filter_by(id=parameter_id).first()
    if not parameter:
        raise HTTPException(status_code=404, detail="Parameter not found")

    # See if value already exists for this recipe and parameter
    param_value = db.query(models.RecipeParameterValue).filter_by(recipe_id=recipe_id, parameter_id=parameter_id).first()
    if not param_value:
        param_value = models.RecipeParameterValue(recipe_id=recipe_id, parameter_id=parameter_id)
        db.add(param_value)

    # Set correct value based on type
    if parameter.type == "int":
        param_value.value_int = int(value)
        param_value.value_float = None
        param_value.value_str = None
    elif parameter.type == "float":
        param_value.value_float = float(value)
        param_value.value_int = None
        param_value.value_str = None
    elif parameter.type == "string":
        param_value.value_str = str(value)
        param_value.value_int = None
        param_value.value_float = None
    else:
        raise HTTPException(status_code=400, detail="Unknown parameter type")

    db.commit()

    return {"detail": "Parameter value saved"}


@router.get("/recipe_detail/{recipe_id}")
def get_recipe_detail(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(models.Recipe).filter_by(id=recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    material = db.query(models.Material).filter_by(id=recipe.material_id).first()
    tool = db.query(models.Tool).filter_by(id=recipe.tool_id).first()

    values = db.query(models.RecipeParameterValue).filter_by(recipe_id=recipe.id).all()
    parameter_map = {}
    for v in values:
        param = db.query(models.RecipeParameter).filter_by(id=v.parameter_id).first()
        val = v.value_float or v.value_int or v.value_str
        parameter_map[param.name] = val

    return {
        "id": recipe.id,
        "material": material.name,
        "tool": tool.name,
        "parameters": parameter_map,
    }

