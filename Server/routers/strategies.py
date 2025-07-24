from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from db import get_db
import schemas
from auth import verify_api_key

router = APIRouter(
    dependencies=[Depends(verify_api_key)]
)


@router.get("/strategies/")
def get_strategies(db: Session = Depends(get_db)):
    strategies = db.query(models.Strategy).all()
    return [
        {
            "id": strategy.id,
            "name": strategy.name,
            "description": strategy.description
        } for strategy in strategies
    ]


@router.post("/strategies/")
def create_strategy(data: schemas.StrategyCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Strategy).filter(models.Strategy.name == data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Strategy already exists")

    strategy = models.Strategy(name=data.name, description=data.description)
    db.add(strategy)
    db.commit()
    db.refresh(strategy)

    # Now insert into strategy_recipeparameter_link table
    for param_id in data.parameter_ids:
        link = models.StrategyRecipeParameterLink(
            strategy_id=strategy.id,
            parameter_id=param_id
        )
        db.add(link)
    db.commit()

    return {
        "id": strategy.id,
        "name": strategy.name,
        "description": strategy.description
    }


@router.delete("/strategies/{strategy_id}")
def delete_strategy(strategy_id: int, db: Session = Depends(get_db)):
    strategy = db.query(models.Strategy).filter(models.Strategy.id == strategy_id).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")

    db.delete(strategy)
    db.commit()
    return {"detail": "Strategy deleted"}
