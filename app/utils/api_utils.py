from typing import Optional

from fastapi.responses import StreamingResponse

from app.core.configs import settings


def make_response(
    content: Optional[str] = None,
    file_path: Optional[str] = None,
) -> StreamingResponse:
    """The function creates a StreamingResponse object.

    Args:
        content (Optional[str], optional): Text content. Defaults to None.
        file_path (Optional[str], optional): File path, if response is Audio, PPT,...\
            Defaults to None.

    Raises:
        ValueError: If neither content nor file_path is provided.

    Returns:
        StreamingResponse: StreamingResponse object.
    """
    if file_path is None and content is not None:
        return StreamingResponse(
            content=content,
            media_type="application/octet-stream",
        )
    if file_path is not None:
        file_name = file_path.split("/")[-1]
        media_url = f"{settings.media_base_url}/{file_name}"
        return StreamingResponse(
            content=media_url,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={file_name}"},
        )
    raise ValueError("Either content or file_path must be provided.")
