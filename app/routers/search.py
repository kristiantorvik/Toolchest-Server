from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas
from ..auth import verify_api_key

router = APIRouter(
    prefix="/search",
    dependencies=[Depends(verify_api_key)],
    tags=["Search"]
)

@router.get("/options/{strategy_id}")
def get_search_options(strategy_id: int, db: Session = Depends(get_db)):
    # Get tool type links for the strategy
    tooltype_links = db.query(models.ToolTypeStrategyLink).filter_by(strategy_id=strategy_id).all()
    tooltype_ids = [link.tooltype_id for link in tooltype_links]

    # Retrieve matching tool types
    tooltypes = db.query(models.ToolType).filter(models.ToolType.id.in_(tooltype_ids)).all()

    # Retrieve tools that match the tool types
    tools = db.query(models.Tool).filter(models.Tool.tool_type_id.in_(tooltype_ids)).all()

    # Retrieve all materials
    materials = db.query(models.Material).all()

    return {
        "materials": [{"id": m.id, "name": m.name} for m in materials],
        "tool_types": [{"id": t.id, "name": t.name} for t in tooltypes],
        "tools": [
            {
                "id": t.id,
                "name": t.name,
                "tool_type_id": t.tool_type_id  # Include tool_type_id for filtering on frontend
            }
            for t in tools
        ],
    }





@router.post("/", response_model=list[int])
def search_recipes(filters: schemas.SearchFilters, db: Session = Depends(get_db)):
    query = db.query(models.Recipe).filter_by(strategy_id=filters.strategy_id)

    if filters.material_ids:
        query = query.filter(models.Recipe.material_id.in_(filters.material_ids))

    if filters.tool_type_ids:
        tool_ids = [t.id for t in db.query(models.Tool).filter(models.Tool.tool_type_id.in_(filters.tool_type_ids)).all()]
        query = query.filter(models.Recipe.tool_id.in_(tool_ids))

    if filters.tool_ids:
        query = query.filter(models.Recipe.tool_id.in_(filters.tool_ids))

    recipe_ids = [r.id for r in query.all()]
    return recipe_ids
