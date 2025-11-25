from sqlalchemy import insert
from database import engine
from models import logs_table

def log_event(
    event_type,
    table_name,
    status,
    rows_inserted=0,
    rows_updated=0,
    rows_deleted=0,
    file_name=None,
    sheet_name=None,
    project_id=None,
    error=None
):
    with engine.begin() as conn:
        conn.execute(
            insert(logs_table).values(
                event_type=event_type,
                table_name=table_name,
                status=status,
                error=error,
                rows_inserted=rows_inserted,
                rows_updated=rows_updated,
                rows_deleted=rows_deleted,
                file_name=file_name,
                sheet_name=sheet_name,
                project_id=project_id
            )
        )
