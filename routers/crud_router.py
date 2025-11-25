from fastapi import APIRouter, HTTPException
from utils.crud_service import (
    list_rows,
    get_row,
    create_row,
    update_row,
    delete_row,
)

router = APIRouter()

@router.get("/{project_id}/{table_name}")
def list_records(project_id: int, table_name: str):
    return list_rows(project_id, table_name)

@router.get("/{project_id}/{table_name}/{row_id}")
def fetch_single(project_id: int, table_name: str, row_id: int):
    return get_row(project_id, table_name, row_id)

@router.post("/{project_id}/{table_name}")
def create_record(project_id: int, table_name: str, data: dict):
    return create_row(project_id, table_name, data)

@router.put("/{project_id}/{table_name}/{row_id}")
def update_record(project_id: int, table_name: str, row_id: int, data: dict):
    return update_row(project_id, table_name, row_id, data)

@router.delete("/{project_id}/{table_name}/{row_id}")
def delete_record(project_id: int, table_name: str, row_id: int):
    return delete_row(project_id, table_name, row_id)
