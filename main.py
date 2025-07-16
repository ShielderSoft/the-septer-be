from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.db import Base, engine
from api import auth, hunter, logs, guardian

# Initialize FastAPI app
app = FastAPI(title="Septer Backend")

# Enable CORS (adjust allowed origins in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create DB tables (auto-migrate if not using Alembic)
Base.metadata.create_all(bind=engine)

# Register route groups
app.include_router(guardian.router, prefix="/api/guardian", tags=["Guardian"])
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(auth.router, prefix="/api/g-login-rntinfosec", tags=["Guardian-login"])
app.include_router(hunter.router, prefix="/api/hunter", tags=["Hunter"])
app.include_router(logs.router, prefix="/api/logs", tags=["Logs"])