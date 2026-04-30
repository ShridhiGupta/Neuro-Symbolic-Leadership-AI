from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import os
import fitz  # PyMuPDF
import io
from pathlib import Path

from app.models.schemas import FileUploadResponse
from app.core.config import settings

router = APIRouter()

@router.post("/resume", response_model=FileUploadResponse)
async def upload_resume(file: UploadFile = File(...), user_id: Optional[str] = None):
    """
    Upload and extract text from resume file
    
    - **file**: Resume file (PDF, TXT, DOCX)
    - **user_id**: Optional user identifier
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        file_extension = Path(file.filename).suffix.lower()
        if file_extension not in settings.allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type. Allowed: {settings.allowed_extensions}"
            )
        
        # Check file size
        file_content = await file.read()
        if len(file_content) > settings.max_file_size:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {settings.max_file_size // (1024*1024)}MB"
            )
        
        # Extract text based on file type
        extracted_text = await extract_text_from_file(file_content, file_extension)
        
        # Save file (optional)
        upload_dir = Path(settings.upload_dir)
        upload_dir.mkdir(exist_ok=True)
        
        file_path = upload_dir / file.filename
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        # Save to database
        from app.services.database_service import DatabaseService
        db_service = DatabaseService()
        await db_service.save_file_upload(
            user_id or "anonymous", 
            file.filename, 
            len(file_content), 
            extracted_text
        )
        
        return FileUploadResponse(
            filename=file.filename,
            file_size=len(file_content),
            extracted_text=extracted_text,
            text_length=len(extracted_text),
            status="success",
            message="File uploaded and text extracted successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

@router.post("/text")
async def upload_text(text: str, user_id: Optional[str] = None, filename: Optional[str] = None):
    """
    Upload text directly without file
    
    - **text**: Text content to upload
    - **user_id**: Optional user identifier
    - **filename**: Optional filename for reference
    """
    try:
        if not text.strip():
            raise HTTPException(status_code=400, detail="Empty text provided")
        
        # Save to database
        from app.services.database_service import DatabaseService
        db_service = DatabaseService()
        await db_service.save_file_upload(
            user_id or "anonymous",
            filename or "direct_text_input",
            len(text.encode('utf-8')),
            text
        )
        
        return FileUploadResponse(
            filename=filename or "direct_text_input",
            file_size=len(text.encode('utf-8')),
            extracted_text=text,
            text_length=len(text),
            status="success",
            message="Text uploaded successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text upload failed: {str(e)}")

@router.get("/supported-formats")
async def get_supported_formats():
    """Get list of supported file formats"""
    return {
        "supported_formats": settings.allowed_extensions,
        "max_file_size_mb": settings.max_file_size // (1024 * 1024),
        "upload_directory": settings.upload_dir
    }

async def extract_text_from_file(file_content: bytes, file_extension: str) -> str:
    """Extract text from uploaded file based on its type"""
    try:
        if file_extension == ".pdf":
            return extract_text_from_pdf(file_content)
        elif file_extension == ".txt":
            return file_content.decode('utf-8', errors='ignore')
        elif file_extension == ".docx":
            return extract_text_from_docx(file_content)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Text extraction failed: {str(e)}")

def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF file using PyMuPDF"""
    try:
        # Create a PDF document from bytes
        pdf_document = fitz.open(stream=file_content, filetype="pdf")
        
        extracted_text = ""
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            extracted_text += page.get_text()
        
        pdf_document.close()
        
        # Clean up the text
        extracted_text = clean_extracted_text(extracted_text)
        
        return extracted_text
        
    except Exception as e:
        raise Exception(f"PDF text extraction failed: {str(e)}")

def extract_text_from_docx(file_content: bytes) -> str:
    """Extract text from DOCX file (basic implementation)"""
    try:
        # This is a simplified implementation
        # For production, you might want to use python-docx library
        import zipfile
        import xml.etree.ElementTree as ET
        
        # DOCX files are ZIP archives
        with zipfile.ZipFile(io.BytesIO(file_content)) as docx_zip:
            # Extract the main document
            document_xml = docx_zip.read('word/document.xml')
            
        # Parse XML and extract text
        root = ET.fromstring(document_xml)
        
        # Define namespace
        namespaces = {
            'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
        }
        
        # Extract all text nodes
        text_elements = root.findall('.//w:t', namespaces)
        extracted_text = ''.join([element.text or '' for element in text_elements])
        
        return clean_extracted_text(extracted_text)
        
    except Exception as e:
        raise Exception(f"DOCX text extraction failed: {str(e)}")

def clean_extracted_text(text: str) -> str:
    """Clean and normalize extracted text"""
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = ' '.join(text.split())
    
    # Remove common PDF artifacts
    artifacts = [
        '\x0c',  # Form feed
        '\x0b',  # Vertical tab
        '\f',    # Form feed character
    ]
    
    for artifact in artifacts:
        text = text.replace(artifact, '')
    
    # Remove multiple newlines
    while '\n\n\n' in text:
        text = text.replace('\n\n\n', '\n\n')
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text

@router.delete("/{filename}")
async def delete_uploaded_file(filename: str):
    """Delete an uploaded file"""
    try:
        file_path = Path(settings.upload_dir) / filename
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        # Remove file
        file_path.unlink()
        
        return {
            "status": "success",
            "message": f"File {filename} deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File deletion failed: {str(e)}")

@router.get("/")
async def list_uploaded_files():
    """List all uploaded files"""
    try:
        upload_dir = Path(settings.upload_dir)
        
        if not upload_dir.exists():
            return {"files": [], "total_files": 0}
        
        files = []
        for file_path in upload_dir.iterdir():
            if file_path.is_file():
                files.append({
                    "filename": file_path.name,
                    "size": file_path.stat().st_size,
                    "modified": file_path.stat().st_mtime
                })
        
        return {
            "files": files,
            "total_files": len(files),
            "upload_directory": str(upload_dir)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list files: {str(e)}")
