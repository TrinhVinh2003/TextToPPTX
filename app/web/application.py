from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import UJSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, FileResponse
from app.core.configs import settings
from app.utils.log_utils import configure_logging
from app.web.api.router import api_router
from fastapi.responses import FileResponse
import os

def get_app() -> FastAPI:
    """Create and configure FastAPI application."""
    configure_logging()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.APP_VERSION,
        description=settings.PROJECT_DESCRIPTION,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
        servers=[
            {
                "url": "",
                "description": "Deployed server",
            },
        ],
    )

    app.include_router(router=api_router, prefix="/api")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Update for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
 
    
    @app.route('/static/media/<filename>')
    def serve_media(filename):
        # Đường dẫn đến file
        file_path = os.path.join(settings.media_dir, filename)
        
        # Trả về file với header Content-Disposition để tải về
        return FileResponse(
            file_path,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    app.mount(
        "/static/media",
        StaticFiles(directory=settings.media_dir  ),
        name="media",
    )
 
    return app


# Main Entry Point
app = get_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)