from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import status
from contextlib import asynccontextmanager
from database.session import engine, base
from core.logger import logger

from core.exception_handler import setup_exception_handlers
from fastapi.exceptions import RequestValidationError

from modules.auth.controller import router as auth_router
from modules.project.controller import router as project_router
from modules.scene.controller import router as scene_router

from app.database.init_db import init_models

@asynccontextmanager
async def startup_event(app: FastAPI):
    try:
        with engine.connect() as conn:
            logger.info("✅ Database connected successfully!")
        init_models()
        base.metadata.create_all(bind=engine)
        yield
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")


app = FastAPI(lifespan=startup_event, title="Animatic-Vision")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_exception_handlers(app)
app.include_router(auth_router)
app.include_router(project_router)
app.include_router(scene_router)


@app.get("/test")
def home():
    return {"status": "Server is running"}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error = exc.errors()[0]
    print(error)
    field = error.get("loc")[-1] if error.get("loc") else "field"
    message = error.get("msg", "Invalid input")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": f"{field.capitalize()} {message}.", "status_code": 422},
    )
