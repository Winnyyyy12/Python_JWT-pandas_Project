import pandas as pd
from sqlalchemy import insert, update, text
from models import infra_cost_table, logs_table

def ingest_infra_cost(db, file, project_id=None):
    sheet_name = "Infra cost"

    df = pd.read_excel(file, sheet_name=sheet_name, header=None, dtype=str).fillna("")

    final_rows = []
    header_found = False

    for row in df.itertuples(index=False):
        if str(row[1]).strip().lower() == "service":
            header_found = True
            continue

        if not header_found:
            continue

        service = str(row[1]).strip()
        if service == "" or service.lower() == "total":
            continue

        monthly = str(row[2]).replace(",", "").strip()
        try:
            monthly = float(monthly)
        except:
            monthly = None

        final_rows.append({
            "project_id": project_id,
            "service": service,
            "monthly_cost": monthly,
            "currency": str(row[3]).strip(),
            "configuration_summary": str(row[4]).strip()
        })

    inserted = 0
    updated = 0

    for row in final_rows:
        exists_sql = text("""
            SELECT id FROM infra_cost WHERE
                project_id = :project_id AND
                service = :service
            LIMIT 1
        """)

        existing = db.execute(exists_sql, row).first()

        if existing:
            db.execute(
                update(infra_cost_table)
                .where(infra_cost_table.c.id == existing.id)
                .values(row)
            )
            updated += 1
        else:
            db.execute(insert(infra_cost_table).values(row))
            inserted += 1

    db.commit()

    db.execute(insert(logs_table).values(
        event_type="UPSERT",
        table_name="infra_cost",
        status="SUCCESS",
        rows_inserted=inserted,
        rows_updated=updated,
        rows_deleted=0,
        sheet_name=sheet_name,
        project_id=project_id,
        file_name=getattr(file, "name", None)
    ))
    db.commit()
