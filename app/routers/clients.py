from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models, database, auth

router = APIRouter(
    prefix="/clients",
    tags=["clients"],
)

def _format_client(client: models.Client):
    return {
        "id": client.id,
        "client_name": client.client_name,
        "created_at": client.created_at,
        "created_by": client.created_by.name if client.created_by else "Unknown"
    }

@router.post("/", response_model=schemas.ClientResponseSimple)
def create_client(
    client: schemas.ClientCreate, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_client = models.Client(client_name=client.client_name, created_by_id=current_user.id)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return _format_client(db_client)

@router.get("/", response_model=List[schemas.ClientResponseSimple])
def list_clients(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    clients = db.query(models.Client).offset(skip).limit(limit).all()
    return [_format_client(c) for c in clients]

@router.get("/{id}", response_model=schemas.ClientResponse)
def get_client(id: int, db: Session = Depends(database.get_db)):
    client = db.query(models.Client).filter(models.Client.id == id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # We need to construct projects properly including client_name
    projects = []
    for p in client.projects:
        projects.append({
            "id": p.id,
            "project_name": p.project_name,
            "client_name": client.client_name,
            "users": p.users
        })

    response = _format_client(client)
    response["projects"] = projects
    return response

@router.put("/{id}", response_model=schemas.ClientResponseSimple)
@router.patch("/{id}", response_model=schemas.ClientResponseSimple)
def update_client(
    id: int, 
    client_update: schemas.ClientCreate, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    client = db.query(models.Client).filter(models.Client.id == id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    client.client_name = client_update.client_name
    db.commit()
    db.refresh(client)
    return _format_client(client)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(
    id: int, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    client = db.query(models.Client).filter(models.Client.id == id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    db.delete(client)
    db.commit()
    return None
