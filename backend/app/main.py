from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.missions import router as missions_router

app = FastAPI(
    title="Orion SLE API",
    version="0.2.0",
    description="Speech Learning / Mastery Engine API",
)

app.include_router(health_router)
app.include_router(missions_router)


@app.get("/")
def root():
    return {
        "product": "Orion",
        "service": "sle-api",
        "version": "0.2.0",
        "framework": "FastAPI",
        "goal": "Learner completes one Mission end-to-end",
    }
