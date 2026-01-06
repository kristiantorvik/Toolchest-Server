from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from db import get_db
from auth import verify_api_key

router = APIRouter(
    dependencies=[Depends(verify_api_key)]
)


@router.get("/tool_types/")
def get_tool_types(db: Session = Depends(get_db)):
    tool_types = db.query(models.ToolType).all()
    return [
        {
            "id": tool_type.id,
            "name": tool_type.name
        } for tool_type in tool_types
    ]


@router.post("/tool_types/")
def create_tool_type(tool_type_data: schemas.ToolTypeCreate, db: Session = Depends(get_db)):
    existing = db.query(models.ToolType).filter(models.ToolType.name == tool_type_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Tool type already exists")

    tool_type = models.ToolType(name=tool_type_data.name)
    db.add(tool_type)
    db.commit()
    db.refresh(tool_type)

    # Now add the links to tool parameters
    for param_id in tool_type_data.tool_parameter_ids:
        link = models.ToolTypeToolParameterLink(tooltype_id=tool_type.id, parameter_id=param_id)
        db.add(link)

    # Add links to strategies
    for strategy_id in tool_type_data.strategy_ids:
        link = models.ToolTypeStrategyLink(tooltype_id=tool_type.id, strategy_id=strategy_id)
        db.add(link)

    db.commit()

    return {
        "id": tool_type.id,
        "name": tool_type.name
    }


@router.delete("/tooltypes/{tool_type_id}")
def delete_tool_type(tool_type_id: int, db: Session = Depends(get_db)):
    tool_type = db.query(models.ToolType).filter(models.ToolType.id == tool_type_id).first()
    if not tool_type:
        raise HTTPException(status_code=404, detail="Tool type not found")

    db.delete(tool_type)
    db.commit()

    return {"detail": "Tool type deleted"}


@router.get("/tooltype/detail/{tooltype_id}")
def get_tool_type_detail(tooltype_id: int, db: Session = Depends(get_db)):
    tool_type = db.query(models.ToolType).filter(models.ToolType.id == tooltype_id).first()
    if not tool_type:
        raise HTTPException(status_code=404, detail="Tool type not found")

    strategy_link = db.query(models.ToolTypeStrategyLink).filter_by(tooltype_id=tooltype_id).all()
    used_strategies = [link.strategy_id for link in strategy_link]

    tool_parameter_link = db.query(models.ToolTypeToolParameterLink).filter_by(tooltype_id=tooltype_id).all()
    used_tool_parameters = [link.parameter_id for link in tool_parameter_link]

    return {
        "id": tooltype_id,
        "name": tool_type.name,
        "strategy_ids": used_strategies,
        "tool_parameter_ids": used_tool_parameters
    }


@router.patch("/tooltype/")
def patch_tooltype(update: schemas.ToolTypePatch, db: Session = Depends(get_db)):
    print("hello Debug")
    tooltype = db.query(models.ToolType).filter_by(id=update.id).first()
    if not tooltype:
        raise HTTPException(status_code=404, detail="Tool type not found")

    all_params = db.query(models.ToolParameter).all()
    all_params_ids = {param.id for param in all_params}

    existing_param_links = db.query(models.ToolTypeToolParameterLink).filter_by(tooltype_id=update.id).all()
    existing_param_ids = {link.parameter_id for link in existing_param_links}

    new_param_ids = set(update.tool_parameter_ids)

    if not new_param_ids.issubset(all_params_ids):
        raise HTTPException(status_code=400, detail="Illegal tool param_id")

    tools = db.query(models.Tool).filter_by(tool_type_id=update.id)
    affected_tools = []

    # paramvalues that should be removed
    for id in existing_param_ids - new_param_ids:
        for tool in tools:
            affected_tools.append(tool.id)
            db.query(models.ToolParameterValue).filter_by(tool_id=tool.id, parameter_id=id).delete()

        param_to_delete = db.query(models.ToolTypeToolParameterLink).filter_by(tooltype_id=update.id, parameter_id=id).first()
        db.delete(param_to_delete)

    # Parametervalues that should be added
    for id in new_param_ids - existing_param_ids:
        add = models.ToolTypeToolParameterLink(tooltype_id=update.id, parameter_id=id)
        db.add(add)

    all_strats = db.query(models.Strategy).all()
    all_strat_ids = {strat.id for strat in all_strats}

    existing_strat_links = db.query(models.ToolTypeStrategyLink).filter_by(tooltype_id=update.id).all()
    existing_strat_ids = {link.strategy_id for link in existing_strat_links}

    new_strat_ids = set(update.strategy_ids)

    if not new_strat_ids.issubset(all_strat_ids):
        raise HTTPException(status_code=400, detail="Illegal strategy id")

    # Strategylinks that should be removed
    for id in existing_strat_ids - new_strat_ids:
        for tool in tools:
            recipes = db.query(models.Recipe).filter_by(tool_id=tool.id, strategy_id=id).all()
            if recipes:
                if update.force:
                    print("force removing recipes")
                    for recipe in recipes:
                        db.delete(recipe)
                else:
                    raise HTTPException(status_code=403, detail=f"Cannot remove strategy:{id} because it is used by recipes,\nUse force=true to overide and delete recipes")

        strat_to_delete = db.query(models.ToolTypeStrategyLink).filter_by(tooltype_id=update.id, strategy_id=id).first()
        db.delete(strat_to_delete)

    # Strategies to add
    for id in new_strat_ids - existing_strat_ids:
        add = models.ToolTypeStrategyLink(tooltype_id=update.id, strategy_id=id)
        db.add(add)

    db.commit()
    return
