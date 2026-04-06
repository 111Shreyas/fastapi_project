from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models, database, auth

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)

def _format_project(project: models.Project):
    return {
        "id": project.id,
        "project_name": project.project_name,
        "client_name": project.client.client_name if project.client else "Unknown",
        "users": project.users
    }

@router.post("/", response_model=schemas.ProjectResponse)
def create_project(
    project: schemas.ProjectCreate, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Verify Client exists
    client = db.query(models.Client).filter(models.Client.id == project.client_id).first()
    if not client:
        raise HTTPException(status_code=400, detail="Client does not exist")
    
    # Process project creation
    db_project = models.Project(project_name=project.project_name, client_id=project.client_id)
    
    # Verify and associate users
    if project.users:
        users = db.query(models.User).filter(models.User.id.in_(project.users)).all()
        # The requirements ask: "Users assigned must already exist"
        if len(users) != len(set(project.users)):
            raise HTTPException(status_code=400, detail="One or more specified users do not exist")
        db_project.users = users

    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    return _format_project(db_project)

@router.get("/", response_model=List[schemas.ProjectResponse])
def get_user_projects(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Fetch projects assigned to the logged-in user
    projects = []
    for p in current_user.projects:
        projects.append(_format_project(p))
    return projects

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    id: int, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    project = db.query(models.Project).filter(models.Project.id == id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(project)
    db.commit()
    return None
