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


@router.post("/strategies/", response_model=schemas.StrategyRead)
def create_strategy(strategy: schemas.StrategyCreate, db: Session = Depends(get_db)):
    db_strategy = models.Strategy(name=strategy.name, description=strategy.description)
    db.add(db_strategy)
    db.commit()
    db.refresh(db_strategy)

    # Create recipe parameter links
    for param_id in strategy.recipe_parameter_ids:
        link = models.StrategyRecipeParameterLink(strategy_id=db_strategy.id, parameter_id=param_id)
        db.add(link)
    db.commit()
    return db_strategy

@router.get("/strategies/", response_model=List[schemas.StrategyRead])
def read_strategies(db: Session = Depends(get_db)):
    return db.query(models.Strategy).all()

