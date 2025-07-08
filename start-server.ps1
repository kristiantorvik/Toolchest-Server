# Navigate to project directory
Set-Location -LiteralPath $PSScriptRoot

# Activate virtual environment
& .\venv\Scripts\Activate.ps1

# Run the FastAPI server
uvicorn app.main:app --reload
