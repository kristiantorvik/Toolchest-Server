from fastapi import FastAPI
from . import models
from .db import engine, Base
from .routers import materials, tools, strategies, recipes, tool_types

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(materials.router)
app.include_router(tools.router)
app.include_router(strategies.router)
app.include_router(recipes.router)
app.include_router(tool_types.router)

