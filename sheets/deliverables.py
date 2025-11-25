import pandas as pd
from sqlalchemy import insert, update, text
from models import deliverables_table, logs_table

def ingest_deliverable_sheet(db, file, sheet_name, project_id=None):
    parts = sheet_name.split()
    deliverable_number = next((int(p) for p in parts if p.isdigit()), None)

    df = pd.read_excel(file, sheet_name=sheet_name, header=None, dtype=str).fillna("")

    deliverable_name = df.iloc[0, 1].strip()

    final_rows = []
    hit_data = False

    for row in df.itertuples(index=False):
        if str(row[0]).strip().lower() == "feature / module":
            hit_data = True
            continue

        if not hit_data:
            continue

        feature = str(row[0]).strip()
        subtask = str(row[1]).strip()
        est = str(row[2]).strip()

        if feature == "":
            continue

        try:
            est = float(est)
        except:
            est = None

        final_rows.append({
            "project_id": project_id,
            "deliverable_number": deliverable_number,
            "deliverable_name": deliverable_name,
            "feature_module": feature,
            "subtask_description": subtask,
            "estimated_hours": est
        })

    inserted = 0
    updated = 0

    for row in final_rows:
        exists_sql = text("""
            SELECT id FROM deliverables WHERE
                project_id = :project_id AND
                deliverable_number = :deliverable_number AND
                feature_module = :feature_module AND
                subtask_description = :subtask_description
            LIMIT 1
        """)

        existing = db.execute(exists_sql, row).first()

        if existing:
            db.execute(
                update(deliverables_table)
                .where(deliverables_table.c.id == existing.id)
                .values(row)
            )
            updated += 1
        else:
            db.execute(insert(deliverables_table).values(row))
            inserted += 1

    db.commit()

    db.execute(insert(logs_table).values(
        event_type="UPSERT",
        table_name="deliverables",
        status="SUCCESS",
        rows_inserted=inserted,
        rows_updated=updated,
        rows_deleted=0,
        file_name=getattr(file, "name", None),
        sheet_name=sheet_name,
        project_id=project_id
    ))
    db.commit()
