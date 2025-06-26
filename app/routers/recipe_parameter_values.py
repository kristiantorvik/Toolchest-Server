from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models
from ..db import get_db

router = APIRouter()



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

@router.get("/recipes/{recipe_id}/parameters/")
def get_recipe_parameter_values(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(models.Recipe).filter_by(id=recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    values = []
    for value in recipe.parameter_values:
        param = value.parameter
        if param.type == "int":
            val = value.value_int
        elif param.type == "float":
            val = value.value_float
        elif param.type == "string":
            val = value.value_str
        else:
            val = None
        values.append({
            "parameter_id": param.id,
            "parameter_name": param.name,
            "value": val
        })

    return values
