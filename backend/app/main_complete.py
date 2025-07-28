from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import zipfile
import os
import json
import tempfile
from typing import Dict, Any
import asyncio

# Import our real agents
from app.agents.real_internal_doc_agent import RealInternalDocAgent
from app.agents.real_library_doc_agent import RealLibraryDocAgent
from app.agents.real_context_manager_agent import RealContextManagerAgent
from app.core.real_file_parser import RealFileParser

app = FastAPI(title="DocuSynth AI - Complete Multi-Agent System")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize our real agents
internal_doc_agent = RealInternalDocAgent()
library_doc_agent = RealLibraryDocAgent()
context_manager_agent = RealContextManagerAgent()
file_parser = RealFileParser()

# In-memory storage for uploads
uploads = {}

@app.get("/")
async def root():
    return {"message": "DocuSynth AI - Complete Multi-Agent Code Intelligence System"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a zip file for analysis"""
    if not file.filename.endswith('.zip'):
        return JSONResponse(
            status_code=400,
            content={"error": "Please upload a zip file"}
        )
    
    # Generate upload ID
    upload_id = f"upload_{len(uploads) + 1}"
    
    # Save uploaded file temporarily
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
    try:
        content = await file.read()
        temp_file.write(content)
        temp_file.close()
        
        # Store file info
        uploads[upload_id] = {
            "filename": file.filename,
            "temp_path": temp_file.name,
            "status": "uploaded",
            "analysis": None
        }
        
        # Initialize context manager
        context_manager_agent.update_status(upload_id, "uploaded", 0, "File uploaded successfully")
        
        return {
            "upload_id": upload_id,
            "message": "File uploaded successfully",
            "status": "ready_for_analysis"
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error processing file: {str(e)}"}
        )

@app.post("/analyze/{upload_id}")
async def analyze_code(upload_id: str, background_tasks: BackgroundTasks):
    """Start analysis of uploaded code"""
    if upload_id not in uploads:
        return JSONResponse(
            status_code=404,
            content={"error": "Upload not found"}
        )
    
    # Start real analysis in background
    background_tasks.add_task(perform_real_analysis, upload_id)
    
    return {
        "message": "Analysis started",
        "upload_id": upload_id,
        "status": "analyzing"
    }

@app.get("/analyze/{upload_id}")
async def get_analysis(upload_id: str):
    """Get analysis results"""
    if upload_id not in uploads:
        return JSONResponse(
            status_code=404,
            content={"error": "Upload not found"}
        )
    
    upload = uploads[upload_id]
    
    if upload["analysis"] is None:
        status = context_manager_agent.get_status(upload_id)
        return {
            "status": "analyzing",
            "message": status.get("message", "Analysis in progress..."),
            "progress": status.get("progress", 0)
        }
    
    return upload["analysis"]

@app.get("/status/{upload_id}")
async def get_status(upload_id: str):
    """Get detailed analysis status"""
    if upload_id not in uploads:
        return JSONResponse(
            status_code=404,
            content={"error": "Upload not found"}
        )
    
    status = context_manager_agent.get_status(upload_id)
    return {
        "upload_id": upload_id,
        "filename": uploads[upload_id]["filename"],
        **status
    }

async def perform_real_analysis(upload_id: str):
    """Perform real analysis using all 3 AI agents"""
    try:
        upload = uploads[upload_id]
        temp_path = upload["temp_path"]
        
        # Step 1: Extract and parse files
        context_manager_agent.update_status(upload_id, "extracting", 10, "Extracting files from zip")
        extracted_files = file_parser.extract_zip(temp_path)
        
        if not extracted_files:
            context_manager_agent.update_status(upload_id, "error", 0, "No supported files found")
            return
        
        # Step 2: Parse all files
        context_manager_agent.update_status(upload_id, "parsing", 20, "Parsing file structure")
        parsed_files = file_parser.parse_all_files(extracted_files)
        
        # Step 3: Store file contents for cross-reference analysis
        for filename, content in extracted_files.items():
            context_manager_agent.store_file_content(filename, content)
        
        # Step 4: InternalDocAgent analysis
        context_manager_agent.update_status(upload_id, "analyzing", 40, "InternalDocAgent analyzing code structure")
        analyzed_files = []
        
        for parsed_file in parsed_files:
            filename = parsed_file["filename"]
            content = parsed_file["content"]
            
            # Analyze file with InternalDocAgent
            file_analysis = internal_doc_agent.analyze_file(filename, content)
            
            # Analyze libraries with LibraryDocAgent
            libraries = library_doc_agent.analyze_libraries(content)
            file_analysis["external_libraries"] = libraries
            
            analyzed_files.append(file_analysis)
        
        # Step 5: ContextManagerAgent analysis
        context_manager_agent.update_status(upload_id, "context", 70, "ContextManagerAgent building cross-references")
        
        # Find cross-references
        cross_references = context_manager_agent.find_cross_references()
        
        # Generate project summary
        project_summary = context_manager_agent.generate_project_summary(analyzed_files)
        
        # Get library summary
        all_libraries = []
        for file_analysis in analyzed_files:
            all_libraries.extend(file_analysis.get("external_libraries", []))
        
        library_summary = library_doc_agent.get_library_summary(all_libraries)
        
        # Step 6: Compile final results
        context_manager_agent.update_status(upload_id, "compiling", 90, "Compiling analysis results")
        
        final_analysis = {
            "project_summary": project_summary,
            "files": analyzed_files,
            "cross_references": cross_references,
            "external_libraries_summary": library_summary,
            "analysis_metadata": {
                "total_files": len(analyzed_files),
                "total_functions": sum(len(f.get("functions", [])) for f in analyzed_files),
                "total_libraries": len(library_summary),
                "analysis_timestamp": context_manager_agent.get_status(upload_id)["timestamp"]
            }
        }
        
        # Store results
        uploads[upload_id]["analysis"] = final_analysis
        context_manager_agent.update_status(upload_id, "completed", 100, "Analysis completed successfully")
        
        # Clean up temp file
        try:
            os.unlink(temp_path)
        except:
            pass
            
    except Exception as e:
        context_manager_agent.update_status(upload_id, "error", 0, f"Analysis failed: {str(e)}")
        print(f"Analysis error: {e}")

# Serve static files for frontend
app.mount("/static", StaticFiles(directory="frontend/out"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 