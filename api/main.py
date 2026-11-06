
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.tasks import router as tasks_router

app = FastAPI(
    title="TaskPilot API",
    description="REST API for the TaskPilot AI Productivity Assistant",
    version="1.0.0",
)

# Allow the React development server to communicate with FastAPI.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(tasks_router)

@app.get("/health")
async def health_check():
    """Check whether the TaskPilot API is running."""
    return {
        "status": "healthy",
        "application": "TaskPilot API",
        "version": "1.0.0",
    }


@app.get("/")
async def root():
    return {
        "message": "Welcome to TaskPilot API",
        "documentation": "/docs",
    }
