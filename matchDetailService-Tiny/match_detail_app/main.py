
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .config import settings
from .routes import router, manager, broadcaster


@asynccontextmanager
async def lifespan(app: FastAPI):
	await broadcaster.start(manager)
	yield
	await broadcaster.stop()


app = FastAPI(title=settings.service_name, lifespan=lifespan)
app.add_middleware(
	CORSMiddleware,
	allow_origins=settings.cors_origins,
	allow_methods=["*"],
	allow_headers=["*"],
)
app.include_router(router)
