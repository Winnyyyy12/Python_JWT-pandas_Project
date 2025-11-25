from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from database import create_all_tables, get_db
from utils.excel_router import route_excel

# Routers
from routers.auth_router import router as auth_router
from routers.crud_router import router as crud_router
from routers.projects_router import router as projects_router
from routers.logs_router import router as logs_router
from routers.template_router import router as template_router

app = FastAPI(
    title="Excel to DB Importer",
    openapi_tags=[
        {"name": "Upload", "description": "Excel upload API"},
        {"name": "Projects", "description": "CRUD for projects"},
        {"name": "Logs", "description": "System logs"},x
        {"name": "Templates", "description": "Download Excel templates"},
        {"name": "Dynamic CRUD", "description": "CRUD for all project-linked tables"},
    ]
)

# -----------------------------------------------------
# CORS CONFIGURATION
# -----------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------
# ROOT ROUTE
# -----------------------------------------------------
@app.get("/", tags=["Upload"])
async def root():
    return {"message": "Hello There."}

# -----------------------------------------------------
# ENSURE TABLES ARE CREATED
# -----------------------------------------------------
create_all_tables()

# -----------------------------------------------------
# FILE UPLOAD ENDPOINT
# -----------------------------------------------------
@app.post("/upload", tags=["Upload"])
async def upload_excel(file: UploadFile = File(...)):
    content = await file.read()
    db = get_db()
    result = route_excel(content, file.filename, db)
    return {"file": file.filename, "results": result}

# -----------------------------------------------------
# ATTACH ROUTERS
# -----------------------------------------------------
app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(logs_router)
app.include_router(template_router)
app.include_router(crud_router)
