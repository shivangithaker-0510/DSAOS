from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import create_tables
from routes.auth import router as auth_router
from routes.codeforces import router as codeforces_router

app = FastAPI(title="DSAOS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(codeforces_router)


@app.on_event("startup")
def on_startup() -> None:
    create_tables()


@app.get("/")
def root() -> dict:
    return {"message": "Welcome to DSAOS - Codeforces Tracker API"}


@app.get("/api/health")
def health() -> dict:
    return {"status": "healthy"}
