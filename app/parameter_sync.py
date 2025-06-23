import yaml
from . import models

def sync_parameters_from_config(config_path: str, db):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # Tool Parameters
    for param in config.get("tool_parameters", []):
        existing = db.query(models.ToolParameter).filter_by(name=param["name"]).first()
        if not existing:
            db.add(models.ToolParameter(
                name=param["name"],
                type=param["type"],
                description=param.get("description", "")
            ))
    
    # Recipe Parameters
    for param in config.get("recipe_parameters", []):
        existing = db.query(models.RecipeParameter).filter_by(name=param["name"]).first()
        if not existing:
            db.add(models.RecipeParameter(
                name=param["name"],
                type=param["type"],
                description=param.get("description", "")
            ))
    
    db.commit()
