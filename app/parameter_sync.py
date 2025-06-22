import yaml
from sqlalchemy.orm import Session
from app.models import ToolParameter, RecipeParameter



def sync_parameters_from_config(config_path: str, db: Session):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    # Sync Tool Parameters
    for param in config.get("tool_parameters", []):
        existing = db.query(ToolParameter).filter_by(name=param["name"]).first()
        if existing:
            existing.type = param["type"]
            existing.description = param["description"]
        else:
            new_param = ToolParameter(
                name=param["name"],
                type=param["type"],
                description=param["description"]
            )
            db.add(new_param)

    # Sync Recipe Parameters
    for param in config.get("recipe_parameters", []):
        existing = db.query(RecipeParameter).filter_by(name=param["name"]).first()
        if existing:
            existing.type = param["type"]
            existing.description = param["description"]
        else:
            new_param = RecipeParameter(
                name=param["name"],
                type=param["type"],
                description=param["description"]
            )
            db.add(new_param)

    db.commit()