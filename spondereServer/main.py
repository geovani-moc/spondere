import uvicorn
from uvicorn.config import LOGGING_CONFIG

if __name__ == '__main__':
    LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(levelprefix)s [%(asctime)s] %(message)s"
    uvicorn.run('app:app', host="0.0.0.0", port=8000, reload=True)