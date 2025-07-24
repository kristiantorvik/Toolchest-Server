import os
from dotenv import load_dotenv
load_dotenv()  # noqa: E402
from parameter_sync import sync_parameters_from_config
from routers import materials, recipe_parameters, recipes, strategies, tool_parameter_values, tool_parameters, tool_types, tools, search, search_tools
from db import engine, Base, SessionLocal
from fastapi import FastAPI

DB_PATH = "data/toolchest.db"
TOOL_PARAM_CONFIG = "tool_parameter_config.yaml"
RECIPE_PARAM_CONFIG = "recipe_parameter_config.yaml"

# Create database if it doesn't exist
if not os.path.exists(DB_PATH):
    print("Database not found. Creating database and syncing parameters...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    sync_parameters_from_config(TOOL_PARAM_CONFIG, RECIPE_PARAM_CONFIG, db)
    db.close()
else:
    # Always safe to run to create missing tables
    Base.metadata.create_all(bind=engine)

app = FastAPI()

# Register routers
app.include_router(materials.router)
app.include_router(recipe_parameters.router)
app.include_router(recipes.router)
app.include_router(strategies.router)
app.include_router(tool_parameter_values.router)
app.include_router(tool_parameters.router)
app.include_router(tool_types.router)
app.include_router(tools.router)
app.include_router(search.router)
app.include_router(search_tools.router)
