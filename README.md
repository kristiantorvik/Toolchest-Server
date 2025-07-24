# Toolchest-Server

An attempt to create a storage bank for manufacturing process recipies.

SQLite server with TKinter application front-end 

The server can be run locally or hosted with Fly.io or similar using docker

The Tkinter application can be built to an .EXE with pyinstaller

The server lies under /Server and the frontend application under /TKapp

## Setup server locally
To run the server locally create a file named ".env" in the /Server directory
```
# Server/.env
API_KEY="YOUR SECRET KEY"
```
Ofcourse set the API_KEY to something else.
This is the key you need to access the server later.

Then create the virtuall environment where the server will run.

Move to the /Server directory in your terminal and setup the (venv) using these commands:
```
python -m venv venv_Server

.\venv_server\Scripts\Activate

pip install --upgrade pip

pip install -r requirements.txt
```

From here you can you can run the command: `uvicorn main:app --reload` command in the terminal to start the server.


## Setup for using and building the TKinter application
Update the URL and api key in the `/TKapp/api.py` to you server's key and URL

Then create the virtuall environment for the app.

Move the /TKapp directory in a terminal and run these commands to build and set up the (venv_TKapp)
```
python -m venv venv_TKapp

.\venv_TKapp\Scripts\Activate

pip install --upgrade pip

pip install -r requirements.txt
```

From here you can run it with: `.\main.py`

To build the TKinter app to an .EXE install pyinstaller with:

`pip install pyinstaller`

Then run this command: `pyinstaller --onefile --windowed --icon=ICON.ico main.py`

