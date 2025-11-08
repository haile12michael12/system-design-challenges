import os
import mimetypes
from typing import Optional

def validate_file_extension(file_path: str, allowed_extensions: list) -> bool:
    """
    Validate that a file has an allowed extension
    """
    _, ext = os.path.splitext(file_path)
    return ext.lower() in [e.lower() for e in allowed_extensions]

def validate_file_size(file_path: str, max_size_mb: int) -> bool:
    """
    Validate that a file size is within limits
    """
    file_size = os.path.getsize(file_path)
    return file_size <= max_size_mb * 1024 * 1024

def get_file_type(file_path: str) -> Optional[str]:
    """
    Get the MIME type of a file
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type

def is_image_file(file_path: str) -> bool:
    """
    Check if a file is an image
    """
    mime_type = get_file_type(file_path)
    return bool(mime_type and mime_type.startswith('image/'))

def is_pdf_file(file_path: str) -> bool:
    """
    Check if a file is a PDF
    """
    mime_type = get_file_type(file_path)
    return mime_type == 'application/pdf'

def safe_filename(filename: str) -> str:
    """
    Sanitize a filename to prevent directory traversal attacks
    """
    # Remove path separators and other dangerous characters
    filename = filename.replace('/', '_').replace('\\', '_').replace('..', '_')
    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255-len(ext)] + ext
    return filename