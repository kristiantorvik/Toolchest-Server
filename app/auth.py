from fastapi import Header, HTTPException, status
from fastapi import Request


API_KEY = "mysupersecretpasscode"  # Ideally store in environment variable!

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )