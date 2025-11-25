from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from database import engine
from models import (
    sow_summary_table,
    deliverables_table,
    infra_cost_table,
    resource_timeline_plan_table,
)

# Allowed tables (write-enabled)
TABLE_MAP = {
    "sow_summary": sow_summary_table,
    "deliverables": deliverables_table,
    "infra_cost": infra_cost_table,
    "resource_timeline_plan": resource_timeline_plan_table,
}

def get_table(table_name: str):
    if table_name not in TABLE_MAP:
        raise HTTPException(status_code=404, detail="Invalid table name")
    return TABLE_MAP[table_name]

def list_rows(project_id: int, table_name: str):
    table = get_table(table_name)
    stmt = select(table).where(table.c.project_id == project_id)

    with engine.begin() as conn:
        rows = conn.execute(stmt).mappings().all()

    return list(rows)

def get_row(project_id: int, table_name: str, row_id: int):
    table = get_table(table_name)

    stmt = (
        select(table)
        .where(table.c.id == row_id)
        .where(table.c.project_id == project_id)
    )

    with engine.begin() as conn:
        row = conn.execute(stmt).mappings().first()

    if not row:
        raise HTTPException(status_code=404, detail="Record not found")

    return row

def create_row(project_id: int, table_name: str, data: dict):
    table = get_table(table_name)

    data["project_id"] = project_id

    with engine.begin() as conn:
        result = conn.execute(insert(table).values(data).returning(table.c.id))
        new_id = result.scalar()

    return {"id": new_id, "message": "Created"}

def update_row(project_id: int, table_name: str, row_id: int, data: dict):
    table = get_table(table_name)

    stmt = (
        update(table)
        .where(table.c.id == row_id)
        .where(table.c.project_id == project_id)
        .values(data)
        .returning(table.c.id)
    )

    with engine.begin() as conn:
        result = conn.execute(stmt).scalar()

    if not result:
        raise HTTPException(status_code=404, detail="Record not found")

    return {"id": row_id, "message": "Updated"}

def delete_row(project_id: int, table_name: str, row_id: int):
    table = get_table(table_name)

    stmt = (
        delete(table)
        .where(table.c.id == row_id)
        .where(table.c.project_id == project_id)
        .returning(table.c.id)
    )

    with engine.begin() as conn:
        result = conn.execute(stmt).scalar()

    if not result:
        raise HTTPException(status_code=404, detail="Record not found")

    return {"id": row_id, "message": "Deleted"}
