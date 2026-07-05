from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.missions import router as missions_router
from app.api.learning_sessions import router as learning_sessions_router
from app.api.attempts import router as attempts_router

app = FastAPI(
    title="Orion SLE API",
    version="0.2.0",
    description="Speech Learning / Mastery Engine API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(missions_router)
app.include_router(learning_sessions_router)
app.include_router(attempts_router)

@app.get("/")
def root():
    return {
        "product": "Orion",
        "service": "sle-api",
        "version": "0.2.0",
    }