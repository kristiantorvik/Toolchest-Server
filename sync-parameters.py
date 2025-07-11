import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, ToolParameter, RecipeParameter


# Load YAML configs
def load_yaml(filename):
    with open(filename, 'r') as f:
        return yaml.safe_load(f)


def sync_parameters(session):
    # --- Tool Parameters ---
    tool_params = load_yaml("app/tool_parameter_config.yaml")
    for param in tool_params['tool_parameters']:
        existing = session.query(ToolParameter).filter_by(name=param['name']).first()
        if not existing:
            new_param = ToolParameter(
                name=param['name'],
                type=param['type'],
                description=param.get('description', '')
            )
            session.add(new_param)
            print(f"Added tool parameter: {param['name']}")

    # --- Recipe Parameters ---
    recipe_params = load_yaml("app/recipe_parameter_config.yaml")
    for param in recipe_params['recipe_parameters']:
        existing = session.query(RecipeParameter).filter_by(name=param['name']).first()
        if not existing:
            new_param = RecipeParameter(
                name=param['name'],
                type=param['type'],
                description=param.get('description', '')
            )
            session.add(new_param)
            print(f"Added recipe parameter: {param['name']}")

    session.commit()


if __name__ == "__main__":
    DATABASE_URL = "sqlite:///toolchest.db"

    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)  # Create tables if not exist

    Session = sessionmaker(bind=engine)
    session = Session()

    sync_parameters(session)

    session.close()
