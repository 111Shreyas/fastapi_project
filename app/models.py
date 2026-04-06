from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

# Association table for Many-to-Many relationship between Users and Projects
project_user_association = Table(
    "project_users",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("project_id", Integer, ForeignKey("projects.id")),
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    # Relationship to projects
    projects = relationship("Project", secondary=project_user_association, back_populates="users")


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by_id = Column(Integer, ForeignKey("users.id"))

    created_by = relationship("User")
    projects = relationship("Project", back_populates="client", cascade="all, delete-orphan")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))

    client = relationship("Client", back_populates="projects")
    users = relationship("User", secondary=project_user_association, back_populates="projects")
