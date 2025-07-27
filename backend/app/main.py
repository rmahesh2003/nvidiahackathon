from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import tempfile
import shutil
import uuid
import time
from typing import Dict, Any, List

from app.models.schemas import (
    UploadResponse, AnalysisRequest, AnalysisResponse, 
    ProjectAnalysis, FileAnalysis, AgentStatus
)
from app.core.file_parser import FileParser
from app.agents.internal_doc_agent import InternalDocAgent
from app.agents.library_doc_agent import LibraryDocAgent
from app.agents.context_manager_agent import ContextManagerAgent

app = FastAPI(
    title="DocuSynth AI API",
    description="Multi-agent code intelligence system for automatic documentation generation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
file_parser = FileParser()
internal_doc_agent = InternalDocAgent()
library_doc_agent = LibraryDocAgent()
context_manager_agent = ContextManagerAgent()

# In-memory storage for uploads (in production, use a database)
uploads = {}

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "DocuSynth AI API",
        "version": "1.0.0",
        "description": "Multi-agent code intelligence system",
        "endpoints": {
            "upload": "/upload",
            "analyze": "/analyze/{upload_id}",
            "status": "/status/{upload_id}",
            "docs": "/docs"
        }
    }

@app.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """Upload a zip file containing codebase for analysis."""
    
    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="Only .zip files are supported")
    
    # Create unique upload ID
    upload_id = str(uuid.uuid4())
    
    # Create temporary directory for extraction
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Save uploaded file
        file_path = os.path.join(temp_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Extract and count files
        code_files = file_parser.extract_zip(file_path, temp_dir)
        
        # Store upload information
        uploads[upload_id] = {
            "temp_dir": temp_dir,
            "file_count": len(code_files),
            "code_files": code_files,
            "upload_time": time.time(),
            "status": "uploaded"
        }
        
        return UploadResponse(
            message="File uploaded successfully",
            upload_id=upload_id,
            file_count=len(code_files)
        )
        
    except Exception as e:
        # Cleanup on error
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/analyze/{upload_id}", response_model=AnalysisResponse)
async def analyze_codebase(upload_id: str, background_tasks: BackgroundTasks):
    """Start analysis of uploaded codebase."""
    
    if upload_id not in uploads:
        raise HTTPException(status_code=404, detail="Upload not found")
    
    upload_info = uploads[upload_id]
    
    # Start background analysis
    background_tasks.add_task(perform_analysis, upload_id)
    
    return AnalysisResponse(
        status="started",
        progress=0.0,
        result=None
    )

@app.get("/analyze/{upload_id}", response_model=AnalysisResponse)
async def get_analysis_result(upload_id: str):
    """Get analysis results for an upload."""
    
    if upload_id not in uploads:
        raise HTTPException(status_code=404, detail="Upload not found")
    
    upload_info = uploads[upload_id]
    
    if upload_info.get("status") == "completed":
        return AnalysisResponse(
            status="completed",
            progress=1.0,
            result=upload_info.get("result")
        )
    elif upload_info.get("status") == "failed":
        return AnalysisResponse(
            status="failed",
            progress=0.0,
            error=upload_info.get("error")
        )
    else:
        return AnalysisResponse(
            status="processing",
            progress=upload_info.get("progress", 0.0),
            result=None
        )

@app.get("/status/{upload_id}", response_model=AgentStatus)
async def get_agent_status(upload_id: str):
    """Get current status of all agents for an upload."""
    
    if upload_id not in uploads:
        raise HTTPException(status_code=404, detail="Upload not found")
    
    upload_info = uploads[upload_id]
    agent_status = upload_info.get("agent_status", {
        'internal_doc_agent': 'idle',
        'library_doc_agent': 'idle',
        'context_manager_agent': 'idle'
    })
    
    return AgentStatus(
        internal_doc_agent=agent_status.get('internal_doc_agent', 'idle'),
        library_doc_agent=agent_status.get('library_doc_agent', 'idle'),
        context_manager_agent=agent_status.get('context_manager_agent', 'idle'),
        overall_progress=upload_info.get("progress", 0.0)
    )

async def perform_analysis(upload_id: str):
    """Perform the complete analysis pipeline."""
    
    upload_info = uploads[upload_id]
    upload_info["status"] = "processing"
    upload_info["progress"] = 0.0
    
    try:
        # Update agent status
        context_manager_agent.update_agent_status('context_manager_agent', 'active')
        upload_info["agent_status"] = context_manager_agent.agent_status
        
        # Stage 1: Parse all files
        upload_info["progress"] = 0.1
        parsed_files = []
        
        for file_path in upload_info["code_files"]:
            parsed_data = file_parser.parse_file(file_path)
            parsed_files.append({
                'file_path': file_path,
                'parsed_data': parsed_data
            })
        
        upload_info["progress"] = 0.3
        
        # Stage 2: Internal documentation analysis
        context_manager_agent.update_agent_status('internal_doc_agent', 'active')
        upload_info["agent_status"] = context_manager_agent.agent_status
        
        analyzed_files = []
        for parsed_file in parsed_files:
            file_analysis = internal_doc_agent.analyze_file(
                parsed_file['file_path'], 
                parsed_file['parsed_data']
            )
            analyzed_files.append(file_analysis)
            
            # Track context
            context_manager_agent.track_analysis_context(
                parsed_file['file_path'], 
                file_analysis
            )
        
        upload_info["progress"] = 0.6
        
        # Stage 3: Library documentation analysis
        context_manager_agent.update_agent_status('library_doc_agent', 'active')
        upload_info["agent_status"] = context_manager_agent.agent_status
        
        libraries = library_doc_agent.analyze_libraries(analyzed_files)
        
        # Add library information to files
        for file_analysis in analyzed_files:
            file_imports = parsed_files[0]['parsed_data'].get('imports', [])
            file_libraries = []
            
            for import_name in file_imports:
                clean_name = library_doc_agent._clean_import_name(import_name)
                if clean_name:
                    for lib in libraries:
                        if lib['name'].lower() == clean_name.lower():
                            file_libraries.append(lib)
                            break
            
            file_analysis['external_libraries'] = file_libraries
        
        upload_info["progress"] = 0.8
        
        # Stage 4: Cross-reference analysis
        context_manager_agent.update_agent_status('context_manager_agent', 'active')
        upload_info["agent_status"] = context_manager_agent.agent_status
        
        cross_refs = context_manager_agent.find_cross_references(analyzed_files)
        
        # Add cross-references to files
        for file_analysis in analyzed_files:
            file_cross_refs = []
            for func in file_analysis.get('functions', []):
                func_name = func['name']
                for cross_ref in cross_refs:
                    if cross_ref['function'] == func_name:
                        file_cross_refs.append(cross_ref)
            
            file_analysis['cross_references'] = file_cross_refs
        
        upload_info["progress"] = 0.9
        
        # Stage 5: Generate final project summary
        project_summary = context_manager_agent.generate_project_summary(
            analyzed_files, libraries
        )
        
        # Create final result
        result = ProjectAnalysis(
            files=analyzed_files,
            project_summary=project_summary,
            total_files=len(analyzed_files),
            libraries_used=[lib['name'] for lib in libraries],
            analysis_time=time.time() - upload_info["upload_time"]
        )
        
        upload_info["result"] = result
        upload_info["status"] = "completed"
        upload_info["progress"] = 1.0
        
        # Update final agent status
        context_manager_agent.update_agent_status('internal_doc_agent', 'completed')
        context_manager_agent.update_agent_status('library_doc_agent', 'completed')
        context_manager_agent.update_agent_status('context_manager_agent', 'completed')
        upload_info["agent_status"] = context_manager_agent.agent_status
        
    except Exception as e:
        upload_info["status"] = "failed"
        upload_info["error"] = str(e)
        upload_info["progress"] = 0.0
        
        # Update agent status on error
        context_manager_agent.update_agent_status('internal_doc_agent', 'error')
        context_manager_agent.update_agent_status('library_doc_agent', 'error')
        context_manager_agent.update_agent_status('context_manager_agent', 'error')
        upload_info["agent_status"] = context_manager_agent.agent_status

@app.delete("/uploads/{upload_id}")
async def delete_upload(upload_id: str):
    """Delete an upload and clean up temporary files."""
    
    if upload_id not in uploads:
        raise HTTPException(status_code=404, detail="Upload not found")
    
    upload_info = uploads[upload_id]
    
    # Clean up temporary directory
    if os.path.exists(upload_info["temp_dir"]):
        shutil.rmtree(upload_info["temp_dir"])
    
    # Remove from storage
    del uploads[upload_id]
    
    return {"message": "Upload deleted successfully"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "active_uploads": len(uploads)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 