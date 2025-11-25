import re
from io import BytesIO
import pandas as pd
from sqlalchemy import select, insert
from database import engine
from models import projects_table


# -------------------------------------------------------------------
# PARSER: Extract project_code and project_name
# <projectcode>_<projectname>_SampleEstimationWorkbook.xlsx
# projectcode may start with letter or digit (e.g. P001, 001, ABC123)
# -------------------------------------------------------------------

def extract_project_from_filename(file_name: str):
    base = file_name.split(".")[0]
    parts = base.split("_")

    if len(parts) < 3:
        raise ValueError(
            "Filename must follow <projectcode>_<projectname>_SampleEstimationWorkbook.xlsx"
        )

    project_code = parts[0].strip()
    project_name = parts[1].strip()

    return project_code, project_name


# -------------------------------------------------------------------
# Ensure project exists (upsert-like logic)
# -------------------------------------------------------------------

def get_or_create_project(project_code: str, project_name: str):
    with engine.begin() as conn:

        # Check if exists
        stmt = select(projects_table).where(
            projects_table.c.project_code == project_code
        )
        row = conn.execute(stmt).fetchone()

        if row:
            return row.id

        # If not exist → insert
        insert_stmt = insert(projects_table).values(
            project_code=project_code,
            project_name=project_name
        ).returning(projects_table.c.id)

        new_id = conn.execute(insert_stmt).scalar_one()
        return new_id


# -------------------------------------------------------------------
# Sheet imports
# -------------------------------------------------------------------
from sheets.sow_summary import process_sow_summary
from sheets.resource_timeline_plan import ingest_resource_timeline_plan
from sheets.deliverables import ingest_deliverable_sheet
from sheets.infra_cost import ingest_infra_cost


# -------------------------------------------------------------------
# ROUTER
# -------------------------------------------------------------------

def route_excel(file_bytes: bytes, file_name: str, db):
    # Extract project metadata
    project_code, project_name = extract_project_from_filename(file_name)

    # Ensure DB record exists
    project_id = get_or_create_project(project_code, project_name)

    # Load workbook
    excel = pd.ExcelFile(BytesIO(file_bytes))
    results = []

    for sheet in excel.sheet_names:
        sheet_clean = sheet.strip()
        df = excel.parse(sheet_clean, dtype=str).fillna("")

        # SOW SUMMARY
        if sheet_clean.lower() == "sow summary":
            result = process_sow_summary(df, file_name, sheet_clean, project_id)
            results.append(result)
            continue

        # RESOURCE PLAN
        if sheet_clean.lower() == "resource and timeline plan":
            ingest_resource_timeline_plan(db, BytesIO(file_bytes), project_id)
            results.append({"sheet": sheet_clean, "status": "processed"})
            continue

        # INFRA COST
        if sheet_clean.lower() == "infra cost":
            ingest_infra_cost(db, BytesIO(file_bytes), project_id)
            results.append({"sheet": sheet_clean, "status": "processed"})
            continue

        # DELIVERABLE SHEET
        if re.match(r"deliverable\s+\d+", sheet_clean.lower()):
            ingest_deliverable_sheet(db, BytesIO(file_bytes), sheet_clean, project_id)
            results.append({"sheet": sheet_clean, "status": "processed"})
            continue

        # IGNORE
        results.append({"sheet": sheet_clean, "status": "ignored"})

    return {
        "project_code": project_code,
        "project_name": project_name,
        "project_id": project_id,
        "results": results
    }
