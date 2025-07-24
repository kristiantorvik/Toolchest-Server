from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from db import get_db
from auth import verify_api_key

router = APIRouter(
    dependencies=[Depends(verify_api_key)]
)


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



@router.post("/recipes/")
def create_recipe(data: schemas.RecipeCreate, db: Session = Depends(get_db)):

    check_recipe(data, db)

    # Create the Recipe record
    recipe = models.Recipe(
        material_id=data.material_id,
        strategy_id=data.strategy_id,
        tool_id=data.tool_id
    )
    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    # Set parameter values
    for param_id, value in data.parameters.items():
        param_obj = db.query(models.RecipeParameter).filter_by(id=param_id).first()
        if not param_obj:
            raise HTTPException(status_code=400, detail=f"Tool parameter ID:{param_id} not found")

        value_entry = models.RecipeParameterValue(
            recipe_id=recipe.id,
            parameter_id=param_obj.id
        )

        if value == "":
            continue
        try:
            if param_obj.type == "int":
                value_entry.value_int = int(value)
            elif param_obj.type == "float":
                value_entry.value_float = float(value)
            elif param_obj.type == "string":
                value_entry.value_str = str(value)
            else:
                raise HTTPException(status_code=400, detail=f"Unsupported parameter type: {param_obj.type}")
        except ValueError:
            raise HTTPException(status_code=422, detail=f"Could not convert value: '{value}' to correct type: {param_obj.type}")
        except Exception:
            raise HTTPException(status_code=500, detail="Unexpected error while converting values")

        db.add(value_entry)

    db.commit()

    return {"detail": "Recipe Succesfully added"}


@router.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    db.delete(recipe)
    db.commit()
    return {"detail": "Recipe deleted"}


@router.get("/recipes_by_tool/{tool_id}")
def recipe_by_tool(tool_id: int, db: Session = Depends(get_db)):
    tool = db.query(models.Tool).filter(models.Tool.id == tool_id).first()
    if not tool:
        return None
    recipes = db.query(models.Recipe).filter(models.Recipe.tool_id == tool.id)
    if not recipes:
        return None
    recipe_ids = [r.id for r in recipes.all()]
    return recipe_ids


@router.get("/recipes_by_material/{material_id}")
def recipe_by_material(material_id: int, db: Session = Depends(get_db)):
    material = db.query(models.Material).filter(models.Material.id == material_id).first()
    if not material:
        return None
    recipes = db.query(models.Recipe).filter(models.Recipe.material_id_id == material.id)
    if not recipes:
        return None
    recipe_ids = [r.id for r in recipes.all()]
    return recipe_ids


@router.patch("/recipe/")
def update_recipe(update: schemas.RecipePatch, db: Session = Depends(get_db)):
    recipe = db.query(models.Recipe).filter_by(id=update.id).first()
    if not recipe:
        raise HTTPException(status_code=400, detail="Recipe not found")

    check_recipe(update, db)

    # Update parameter values
    for param_id, value in update.parameters.items():
        param_obj = db.query(models.RecipeParameter).filter_by(id=param_id).first()
        if not param_obj:
            raise HTTPException(status_code=400, detail=f"Tool parameter ID:{param_id} not found")

        # Checking if parameter was used
        used_param = db.query(models.RecipeParameterValue).filter_by(recipe_id=update.id, parameter_id=param_id).first()
        if used_param:
            if value == "":
                db.delete(used_param)

            p_type = param_obj.type
            try:
                if p_type == "string":
                    used_param.value_str = value
                    used_param.value_int = None
                    used_param.value_float = None

                elif p_type == "int":
                    used_param.value_str = None
                    used_param.value_int = value
                    used_param.value_float = None

                elif p_type == "float":
                    used_param.value_str = None
                    used_param.value_int = None
                    used_param.value_float = value
                else:
                    raise HTTPException(status_code=400, detail=f"Unsupported parameter type: {param_obj.type}")
            except ValueError:
                raise HTTPException(status_code=422, detail=f"Could not convert value: '{value}' to correct type: {param_obj.type}")
            except Exception:
                raise HTTPException(status_code=500, detail="Unexpected error while converting values")

        else:
            if value == "":
                pass
            else:
                param_value = models.RecipeParameterValue(
                    recipe_id=recipe.id,
                    parameter_id=param_obj.id,
                    value_float=value if param_obj.type == "float" else None,
                    value_int=value if param_obj.type == "int" else None,
                    value_str=value if param_obj.type == "string" else None
                )
                db.add(param_value)

    db.commit()
    return {"detail": "Recipe Succsessfully updated"}


def check_recipe(recipe, db):
    # Checking if parameters match strategy
    parameter_keys = recipe.parameters.keys()
    try:
        parameter_ids = [int(k) for k in parameter_keys]
    except ValueError:
        raise HTTPException(status_code=422, detail="Parameter id's is not valid")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unknown error while processing parameter ids. Error: {e}")


    strat_param_link = db.query(models.StrategyRecipeParameterLink).filter_by(strategy_id=recipe.strategy_id).all()
    allowed_parameter_ids = [item.parameter_id for item in strat_param_link]

    if not parameter_ids == allowed_parameter_ids:
        raise HTTPException(status_code=403, detail=f"Invalid parameter types for recipe with strategy: {recipe.strategy_id}")

    # Checking if tool allows strategy
    tool = db.query(models.Tool).filter_by(id=recipe.tool_id).first()
    if not tool:
        raise HTTPException(status_code=400, detail="Tool not found")

    link = db.query(models.ToolTypeStrategyLink).filter_by(tooltype_id=tool.tool_type_id, strategy_id=recipe.strategy_id).first()
    if not link:
        raise HTTPException(status_code=403, detail=f"Invalid tool for selected strategy: {recipe.strategy_id}")

    # Checking if material exists
    material = db.query(models.Material).filter_by(id=recipe.material_id).first()
    if not material:
        raise HTTPException(status_code=400, detail="Material not found")

    return True


@router.get("/recipe_detail/{recipe_id}")
def get_recipe_detail(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(models.Recipe).filter_by(id=recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    material = db.query(models.Material).filter_by(id=recipe.material_id).first()
    tool = db.query(models.Tool).filter_by(id=recipe.tool_id).first()
    strategy = db.query(models.Strategy).filter_by(id=recipe.strategy_id).first()

    values = db.query(models.RecipeParameterValue).filter_by(recipe_id=recipe.id).all()
    parameter_map = {}
    for v in values:
        param = db.query(models.RecipeParameter).filter_by(id=v.parameter_id).first()
        if param.type == 'float':
            val = v.value_float
        elif param.type == 'int':
            val = v.value_int
        elif param.type == 'string':
            val = v.value_str
        parameter_map[param.name] = val

    return {
        "id": recipe.id,
        "material": material.name,
        "strategy": strategy.name,
        "tool": tool.name,
        "strategy_id": recipe.strategy_id,
        "parameters": parameter_map,
    }
