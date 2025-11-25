import pandas as pd
from sqlalchemy import insert, update, text
from database import engine
from models import sow_summary_table
from utils.logger import log_event
import numpy as np

COLUMN_MAP = {
    "Client Deliverables": "client_deliverables",
    "Deliverables": "deliverables",
    "Total Hours": "total_hours",
    "Retail Price $": "retail_price",
    "Discount %": "discount",
    "Sales Investment $": "sales_investment",
    "Discounted Price $": "discounted_price",
}

NUMERIC_COLUMNS = [
    "total_hours",
    "retail_price",
    "discount",
    "sales_investment",
    "discounted_price",
]

def clean_number(value):
    if value is None or value is np.nan:
        return None
    s = str(value).strip()
    if s.lower() in ("", "-", "—", "nan", "none"):
        return None
    for c in [",", "$", "₹", "€", "%", " "]:
        s = s.replace(c, "")
    try:
        return float(s)
    except:
        return None

def process_sow_summary(df, file_name, sheet_name, project_id):
    df = df.rename(columns=COLUMN_MAP)
    df = df[list(COLUMN_MAP.values())]

    df["deliverables"] = df["deliverables"].astype(str)

    for col in NUMERIC_COLUMNS:
        df[col] = df[col].apply(clean_number)

    records = df.to_dict(orient="records")

    inserted = 0
    updated = 0

    with engine.begin() as conn:
        for row in records:
            row["project_id"] = project_id

            exists_sql = text("""
                SELECT id FROM sow_summary WHERE
                    project_id = :project_id AND
                    client_deliverables = :client_deliverables AND
                    deliverables = :deliverables
                LIMIT 1
            """)

            existing = conn.execute(exists_sql, row).first()

            if existing:
                conn.execute(
                    update(sow_summary_table)
                    .where(sow_summary_table.c.id == existing.id)
                    .values(row)
                )
                updated += 1
            else:
                conn.execute(insert(sow_summary_table), row)
                inserted += 1

    log_event(
        event_type="UPSERT",
        table_name="sow_summary",
        status="success",
        rows_inserted=inserted,
        rows_updated=updated,
        rows_deleted=0,
        file_name=file_name,
        sheet_name=sheet_name,
        project_id=project_id
    )

    return {
        "sheet": sheet_name,
        "inserted": inserted,
        "updated": updated,
        "deleted": 0,
        "status": "success",
    }
