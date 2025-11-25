import os
import shutil
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter(prefix="/template", tags=["Templates"])

TEMPLATE_PATH = os.path.join("templates", "SampleEstimationWorkbook_Template.xlsx")

# DOWNLOAD TEMPLATE WITH PROJECT CODE + NAME
@router.get("/download")
def download_template(project_code: str, project_name: str):
    if not os.path.exists(TEMPLATE_PATH):
        raise HTTPException(500, "Template Excel file not found on server")

    # Create download filename
    output_filename = f"{project_code}_{project_name}_SampleEstimationWorkbook.xlsx"
    output_path = os.path.join("templates", output_filename)

    # Copy template → renamed file
    shutil.copyfile(TEMPLATE_PATH, output_path)

    # Return the file
    return FileResponse(
        path=output_path,
        filename=output_filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
