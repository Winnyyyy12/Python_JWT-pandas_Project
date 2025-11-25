from sqlalchemy import (
    Table, Column, Integer, String, Text, Float, TIMESTAMP, Boolean,
    MetaData, func, ForeignKey
)

metadata = MetaData()

# --- PROJECTS TABLE ---
projects_table = Table(
    "projects",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("project_name", Text, nullable=False),
    Column("project_code", String(50), unique=True),
    Column("client_name", Text, nullable=True)
)

# --- SOW SUMMARY TABLE ---
sow_summary_table = Table(
    "sow_summary",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("project_id", Integer, ForeignKey("projects.id", ondelete="SET NULL")),
    Column("client_deliverables", Text),
    Column("deliverables", Text),
    Column("total_hours", Float),
    Column("retail_price", Float),
    Column("discount", Float),
    Column("sales_investment", Float),
    Column("discounted_price", Float)
)

# --- LOGS TABLE ---
logs_table = Table(
    "logs",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("timestamp", TIMESTAMP, default=func.now()),
    Column("event_type", Text),
    Column("table_name", Text),
    Column("status", Text),
    Column("error", Text),

    # NEW COLUMNS
    Column("rows_inserted", Integer),
    Column("rows_updated", Integer),
    Column("rows_deleted", Integer),

    Column("file_name", String(255)),
    Column("sheet_name", Text),
    Column("project_id", Integer, ForeignKey("projects.id", ondelete="SET NULL"))
)

# --- RESOURCE & TIMELINE PLAN TABLE ---
resource_timeline_plan_table = Table(
    "resource_timeline_plan",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("project_id", Integer, ForeignKey("projects.id", ondelete="SET NULL")),
    Column("deliverable_name", Text),
    Column("resource_name", Text),
    Column("week_label", Text),
    Column("week_date", Text),
    Column("phase", Text),
    Column("hours", Float),
    Column("total_hours", Float),
    Column("standard_rate", Float),
    Column("discounted_rate", Float),
    Column("total_cost", Float)
)

# --- DELIVERABLES TABLE ---
deliverables_table = Table(
    "deliverables",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("project_id", Integer, ForeignKey("projects.id", ondelete="SET NULL")),
    Column("deliverable_number", Integer),
    Column("deliverable_name", Text),
    Column("feature_module", Text),
    Column("subtask_description", Text),
    Column("estimated_hours", Float)
)

# --- INFRA COST TABLE ---
infra_cost_table = Table(
    "infra_cost",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("project_id", Integer, ForeignKey("projects.id", ondelete="SET NULL")),
    Column("service", Text),
    Column("monthly_cost", Float),
    Column("currency", Text),
    Column("configuration_summary", Text)
)

# --- EMPLOYEES TABLE ---
employees_table = Table(
    "employees",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=True),
    Column("department", String(50)),
    Column("join_date", TIMESTAMP),
    Column("is_active", Integer, default=1)  # Using Integer for Boolean representation
)

# --- USERS TABLE (AUTH) ---
users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(50), unique=True, nullable=False),
    Column("email", String(255), unique=True, nullable=False),
    Column("password", String(255), nullable=False),
    Column("is_online", Integer, default=0)  # 0 = offline, 1 = online
)
