# Toolchest-Server

An attempt to create a storage bank for manufacturing process recipies.

SQLite server with TKinter application front-end 

The server can be run locally or hosted with Fly.io or similar using docker

The Tkinter application can be built to an .EXE with pyinstaller


## Setup locally
To run the server locally create a file named ".env" in the root directory
'''
# /.env file
API_KEY="YOUR SECRET KEY"
'''

Update the URL and api key in the /TKapp/api.py

Open terminal in the /Toolchest-Server/ directory and create a virtuall environment.
'''
python -m venv venv

.\venv\Scripts\Activate

pip install --upgrade pip

pip install -r requirements.txt
'''

From here you can you can run the 'uvicorn app.main:app --reload' command in the terminal to start the server.

