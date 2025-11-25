from fastapi import APIRouter, Query
from database import engine
from models import logs_table
from sqlalchemy import select

router = APIRouter(prefix="/logs", tags=["Logs"])

# GET ALL LOGS (optionally filter by project_id)
@router.get("/")
def get_logs(project_id: int = Query(None)):
    with engine.begin() as conn:
        stmt = select(logs_table)
        if project_id:
            stmt = stmt.where(logs_table.c.project_id == project_id)
        rows = conn.execute(stmt).mappings().all()
        return list(rows)
