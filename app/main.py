from fastapi import FastAPI
from .db import engine, Base, SessionLocal
from .routers import materials, tools, strategies, recipes, tool_types, tool_parameters, recipe_parameters

import sys
import os
from .parameter_sync import sync_parameters_from_config

# Check if database exists
db_path = "params.db"
if not os.path.exists(db_path):
    print("Database not found. Creating database and syncing parameters...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    sync_parameters_from_config("app/parameter_config.yaml", db)
    db.close()
else:
    Base.metadata.create_all(bind=engine)  # This can always be run safely

app = FastAPI()

app.include_router(materials.router)
app.include_router(tools.router)
app.include_router(strategies.router)
app.include_router(recipes.router)
app.include_router(tool_types.router)
app.include_router(tool_parameters.router)
app.include_router(recipe_parameters.router)
