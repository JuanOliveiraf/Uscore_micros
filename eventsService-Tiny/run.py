import uvicorn
from events_app.config import PORT

if __name__ == "__main__":
    uvicorn.run("events_app.main:app", host="0.0.0.0", port=PORT, reload=True)
