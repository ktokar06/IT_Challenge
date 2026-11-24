import uvicorn
from fastapi import FastAPI

from app.controllers.controller import router
from app.exceptions.handlers import register_handlers
from app.utils.logger import setup_logging
from app.utils.parameter_provider import ParameterProvider

setup_logging()

app = FastAPI(title="IT Challenge")
app.include_router(router)
register_handlers(app)

if __name__ == "__main__":
    uvicorn.run("app.main:app", port=ParameterProvider.get_int("server.port", 8001),
                reload=True, reload_excludes=["*.log"])