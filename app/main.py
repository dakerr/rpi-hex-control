import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from pydantic import ValidationError

from app.core.config import Settings
from app.core.settings import get_settings
from app.core.events import create_start_app_handler, create_stop_app_handler
from app.api.errors.http_error import http_error_handler
from app.api.errors.validation_error import http422_error_handler
from app.api.routes.api import router as api_router

def get_application(settings: Settings = get_settings()) -> FastAPI:
  application = FastAPI(
    title=settings.app_name, debug=settings.debug, version=settings.version
  )

  application.add_event_handler("startup", create_start_app_handler(application))
  application.add_event_handler("shutdown", create_stop_app_handler(application))

  application.add_exception_handler(HTTPException, http_error_handler)
  application.add_exception_handler(RequestValidationError, http422_error_handler)
  application.add_exception_handler(ValidationError, http422_error_handler)

  application.include_router(api_router, prefix=settings.api_prefix)

  return application

app = get_application()

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=get_settings().app_port)
