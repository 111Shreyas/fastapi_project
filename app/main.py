from fastapi import FastAPI
from . import models, database
from .routers import users, clients, projects

# Create all database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Assignment FastAPI Service",
    description="A very simple REST API covering the assignment requirements.",
    version="1.0.0"
)

app.include_router(users.auth_router)
app.include_router(users.router)
app.include_router(clients.router)
app.include_router(projects.router)

@app.get("/")
def read_root():
    return {"message": "Service is up and running. Visit /docs for Swagger UI."}
