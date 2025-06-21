from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..db import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.post("/strategies/", response_model=schemas.StrategyRead)
def create_strategy(strategy: schemas.StrategyCreate, db: Session = Depends(get_db)):
    db_strategy = models.Strategy(**strategy.dict())
    db.add(db_strategy)
    db.commit()
    db.refresh(db_strategy)
    return db_strategy

@router.get("/strategies/", response_model=list[schemas.StrategyRead])
def read_strategies(db: Session = Depends(get_db)):
    return db.query(models.Strategy).all()

@router.delete("/strategies/{strategy_id}")
def delete_strategy(strategy_id: int, db: Session = Depends(get_db)):
    strategy = db.query(models.Strategy).filter(models.Strategy.id == strategy_id).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    db.delete(strategy)
    db.commit()
    return {"detail": "Deleted"}
