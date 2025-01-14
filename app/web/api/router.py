from fastapi.responses import StreamingResponse
from fastapi.routing import APIRouter
from fastapi import  HTTPException
from app.web.api import echo
import uuid
import os
import datetime
from fastapi.responses import JSONResponse
from fastapi import  HTTPException
from app.core.configs import settings
from app.repositories.generate_text import  GenOutline
from app.mdtree.tree2ppt import Tree2PPT
from app.schemas.request_schema import (

    PPTRequest,
    PPTReq,PPTRequestTopic
)

from app.utils.extract_file import download_file_from_google_drive,load_pdf
api_router = APIRouter()
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])



@api_router.get("/auto-ppt/gen-uuid")
async def get_uuid():
    random_uuid = str(uuid.uuid4())
    return random_uuid
@api_router.post("/generate_outline_topic")
async def generate_outline_topic(request:PPTRequestTopic):
    """Nhận topic và tạo phác thảo"""
    if not request.topic or not request.topic:
        raise HTTPException(status_code=400, detail="topic must be provided")
    session_id = request.session.strip('"')
    
    outline_generator = GenOutline(session_id)
    outline = outline_generator.generate_outline_from_topic(request.topic)
    
    return JSONResponse(outline)



@api_router.post("/generate_outline")
async def generate_outline(request:PPTRequest):
    """Nhận file PDF và topic để tạo phác thảo."""
    file_id = request.file_url.split("/d/")[1].split("/")[0]
    # if not topic:
    #     raise HTTPException(status_code=400, detail="Topic must be provided")
    if not request.session_id or not request.topic:
        raise HTTPException(status_code=400, detail="session_id and topic must be provided")
    
    session_id = request.session_id.strip('"')
    # Lưu file PDF và tách nội dung
    pdf_path = settings.pdf_dir + f"/{session_id}.pdf"
    
    download_file_from_google_drive(file_id,pdf_path)
    
    pdf_chunks = load_pdf(pdf_path, max_chunks=5)
    
   
    outline_generator = GenOutline(request.session_id)
  
    # Tạo phác thảo từ nội dung PDF và topic
    outline = outline_generator.generate_outline_from_pdf(pdf_chunks, request.topic)
    print(outline)
    return JSONResponse(outline)



@api_router.post("/generate_ppt")
async def generate_ppt_endpoint(request: PPTReq):
    """Generate a PowerPoint file from markdown input."""
    
    markdown_data = request.phac_thao.replace("\"","").replace("\\n","\n\n")
    if not markdown_data:
        raise HTTPException(status_code=400, detail="No data provided")
    print(markdown_data)
    markdown_str = markdown_data.replace("\r", "\n").lstrip('*').rstrip('*')  # Ensure proper line endings
    
    print(markdown_data)
    ppt = Tree2PPT(markdown_str)  # Generate PowerPoint file using Tree2PPT
    stream = ppt.save_stream()  # Get the PowerPoint file as a byte stream
    
    # Prepare filename for the downloaded PowerPoint file
    now = datetime.datetime.now().timestamp()
    filename = f"generated_ppt_{now}.pptx"
    file_path = os.path.join(settings.media_dir, filename)
    
    # Kiểm tra đường dẫn
    print("File saved at:", file_path)
    
    # Lưu file PPTX vào thư mục upload
    try:
        with open(file_path, "wb") as f:
            f.write(stream.getvalue())
    except OSError as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")
    
    # Tạo đường dẫn tải về
    download_url =  settings.host_server + f"/static/media/{filename}"  # Thay your-server-domain bằng domain của bạn
    
    # Trả về đường dẫn tải về
    return JSONResponse(
        content=download_url,
        status_code=200,
    )


                




