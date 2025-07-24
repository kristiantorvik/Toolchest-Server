import yaml
from sqlalchemy.orm import Session
from models import ToolParameter, RecipeParameter


def sync_parameters_from_config(tool_param_path: str, recipe_param_path: str, db: Session):
    sync_tool_parameters_from_yaml(db, tool_param_path)
    sync_recipe_parameters_from_yaml(db, recipe_param_path)


def sync_tool_parameters_from_yaml(db: Session, yaml_path: str):
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f) or {}

    for param in data.get("tool_parameters", []):
        name = param["name"]
        param_type = param["type"]
        description = param.get("description", "")

        existing = db.query(ToolParameter).filter_by(name=name).first()
        if existing:
            if existing.type != param_type or existing.description != description:
                existing.type = param_type
                existing.description = description
                print(f"Updated ToolParameter: {name}")
        else:
            new_param = ToolParameter(name=name, type=param_type, description=description)
            db.add(new_param)
            print(f"Added ToolParameter: {name}")

    db.commit()


def sync_recipe_parameters_from_yaml(db: Session, yaml_path: str):
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f) or {}

    for param in data.get("recipe_parameters", []):
        name = param["name"]
        param_type = param["type"]
        description = param.get("description", "")

        existing = db.query(RecipeParameter).filter_by(name=name).first()
        if existing:
            if existing.type != param_type or existing.description != description:
                existing.type = param_type
                existing.description = description
                print(f"Updated RecipeParameter: {name}")
        else:
            new_param = RecipeParameter(name=name, type=param_type, description=description)
            db.add(new_param)
            print(f"Added RecipeParameter: {name}")

    db.commit()
