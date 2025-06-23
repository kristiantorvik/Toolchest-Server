from app.parameter_sync import sync_parameters_from_config
from app.db import SessionLocal

def main():
    db = SessionLocal()
    sync_parameters_from_config("app/parameter_config.yaml", db)
    db.close()
    print("Parameter sync complete!")

if __name__ == "__main__":
    confirm = input("Are you sure you want to sync parameters? This may alter existing parameter records. (yes/no): ")
    if confirm.lower() == "yes":
        main()
    else:
        print("Cancelled.")
