# Navigate to project directory
cd "C:\Users\Kristian\Documents\Toolchest-server"

# Activate virtual environment
& .\venv\Scripts\Activate.ps1

# Run the FastAPI server
uvicorn app.main:app --reload
