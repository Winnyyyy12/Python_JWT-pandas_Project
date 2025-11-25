from fastapi import APIRouter, HTTPException
from database import engine
from models import projects_table
from sqlalchemy import select, insert, update, delete

router = APIRouter(prefix="/projects", tags=["Projects"])

# LIST ALL PROJECTS
@router.get("/")
def get_all_projects():
    with engine.begin() as conn:
        rows = conn.execute(select(projects_table)).mappings().all()
        return list(rows)

# GET SINGLE PROJECT
@router.get("/{project_id}")
def get_project(project_id: int):
    with engine.begin() as conn:
        row = conn.execute(
            select(projects_table).where(projects_table.c.id == project_id)
        ).mappings().first()
    if not row:
        raise HTTPException(404, "Project not found")
    return row

# CREATE PROJECT
@router.post("/")
def create_project(data: dict):
    with engine.begin() as conn:
        stmt = insert(projects_table).values(**data).returning(projects_table.c.id)
        new_id = conn.execute(stmt).scalar()
    return {"project_id": new_id, "status": "created"}

# UPDATE PROJECT
@router.put("/{project_id}")
def update_project(project_id: int, data: dict):
    with engine.begin() as conn:
        result = conn.execute(
            update(projects_table)
            .where(projects_table.c.id == project_id)
            .values(**data)
        )
    if result.rowcount == 0:
        raise HTTPException(404, "Project not found")
    return {"project_id": project_id, "status": "updated"}

# DELETE PROJECT
@router.delete("/{project_id}")
def delete_project(project_id: int):
    with engine.begin() as conn:
        result = conn.execute(
            delete(projects_table).where(projects_table.c.id == project_id)
        )
    if result.rowcount == 0:
        raise HTTPException(404, "Project not found")
    return {"project_id": project_id, "status": "deleted"}
