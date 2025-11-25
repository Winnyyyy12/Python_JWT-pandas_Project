import pandas as pd
from sqlalchemy import insert, text
from models import resource_timeline_plan_table, logs_table

def ingest_resource_timeline_plan(db, file, project_id=None):
    """
    Process Resource & Timeline Plan sheet with duplicate protection.
    """

    sheet_name = "Resource and Timeline Plan"

    # Read raw excel
    df = pd.read_excel(
        file,
        sheet_name=sheet_name,
        header=None,
        dtype=str
    ).fillna("")

    final_rows = []
    current_deliverable = None
    week_labels = []
    phase_labels = []

    def to_num(val):
        val = str(val).strip()
        if val in ["", None]:
            return None
        try:
            return float(val.replace(",", "").replace("$", ""))
        except:
            return None

    # ----------------------------
    # Identify rows
    # ----------------------------
    i = 0
    while i < len(df):

        row = df.iloc[i]

        # Detect deliverable header
        if str(row[0]).startswith("Deliverable"):
            current_deliverable = str(row[0]).strip()

            i += 1
            week_labels = [str(x).strip() for x in df.iloc[i][1:].tolist()]

            i += 1
            phase_labels = [str(x).strip() for x in df.iloc[i][1:].tolist()]

            i += 1
            continue

        # Skip non-data
        if row[0].strip() in ["", "resource", "Resource"]:
            i += 1
            continue
        if "subtotal" in row[0].strip().lower():
            i += 1
            continue

        # Parse resource row
        resource_name = row[0].strip()
        week_values = row[1:1 + len(week_labels)]
        trailing = row[1 + len(week_labels):].tolist()

        total_hours     = to_num(trailing[0]) if len(trailing) > 0 else None
        standard_rate   = to_num(trailing[1]) if len(trailing) > 1 else None
        discounted_rate = to_num(trailing[2]) if len(trailing) > 2 else None
        total_cost      = to_num(trailing[3]) if len(trailing) > 3 else None

        for idx, w in enumerate(week_labels):
            phase = phase_labels[idx] if idx < len(phase_labels) else None
            hours = to_num(week_values.iloc[idx])

            final_rows.append({
                "project_id": project_id,
                "deliverable_name": current_deliverable,
                "resource_name": resource_name,
                "week_label": w,
                "phase": phase,
                "hours": hours,
                "total_hours": total_hours,
                "standard_rate": standard_rate,
                "discounted_rate": discounted_rate,
                "total_cost": total_cost
            })

        i += 1

    # ---------------------------------------------------
    # DEDUPE: check before insert
    # ---------------------------------------------------

    def row_exists(db, row):
        sql = text("""
            SELECT 1 FROM resource_timeline_plan
            WHERE project_id = :project_id
              AND deliverable_name = :deliverable_name
              AND resource_name = :resource_name
              AND week_label = :week_label
              AND phase = :phase
            LIMIT 1
        """)
        return db.execute(sql, row).first() is not None

    rows_inserted = 0
    rows_skipped = 0

    for row in final_rows:
        if row_exists(db, row):
            rows_skipped += 1
            continue

        stmt = insert(resource_timeline_plan_table).values(**row)
        db.execute(stmt)
        rows_inserted += 1

    db.commit()

    # Log the import
    log_stmt = insert(logs_table).values(
        event_type="INSERT",
        table_name="resource_timeline_plan",
        status="SUCCESS",
        rows_inserted=rows_inserted,
        rows_updated=0,
        rows_deleted=0,
        file_name=getattr(file, "name", None),
        sheet_name=sheet_name,
        project_id=project_id,
        error=f"skipped_duplicates={rows_skipped}"
    )
    db.execute(log_stmt)
    db.commit()
