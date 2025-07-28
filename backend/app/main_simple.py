from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import zipfile
import os
import json
from typing import Dict, Any

app = FastAPI(title="DocuSynth AI - Demo Version")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for demo
uploads = {}

@app.get("/")
async def root():
    return {"message": "DocuSynth AI - Multi-agent Code Intelligence System"}

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
    
    # Store file info (for demo, we'll simulate analysis)
    uploads[upload_id] = {
        "filename": file.filename,
        "status": "uploaded",
        "analysis": None
    }
    
    return {
        "upload_id": upload_id,
        "message": "File uploaded successfully",
        "status": "ready_for_analysis"
    }

@app.post("/analyze/{upload_id}")
async def analyze_code(upload_id: str, background_tasks: BackgroundTasks):
    """Start analysis of uploaded code"""
    if upload_id not in uploads:
        return JSONResponse(
            status_code=404,
            content={"error": "Upload not found"}
        )
    
    # Simulate analysis for demo
    background_tasks.add_task(simulate_analysis, upload_id)
    
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
        return {
            "status": "analyzing",
            "message": "Analysis in progress..."
        }
    
    return upload["analysis"]

@app.get("/status/{upload_id}")
async def get_status(upload_id: str):
    """Get analysis status"""
    if upload_id not in uploads:
        return JSONResponse(
            status_code=404,
            content={"error": "Upload not found"}
        )
    
    return {
        "upload_id": upload_id,
        "status": uploads[upload_id]["status"],
        "filename": uploads[upload_id]["filename"]
    }

async def simulate_analysis(upload_id: str):
    """Simulate AI agent analysis for demo"""
    import time
    
    # Simulate processing time
    time.sleep(2)
    
    # Demo analysis results
    analysis_result = {
        "project_summary": "React search application with debounced API calls",
        "files": [
            {
                "filename": "SearchBar.js",
                "summary": "React component with debounced search functionality",
                "functions": [
                    {
                        "name": "handleChange",
                        "summary": "Handles input changes with debounced search"
                    },
                    {
                        "name": "handleSubmit", 
                        "summary": "Handles form submission"
                    }
                ],
                "external_libraries": [
                    {
                        "name": "lodash.debounce",
                        "link": "https://lodash.com/docs/#debounce"
                    },
                    {
                        "name": "axios",
                        "link": "https://axios-http.com/"
                    }
                ]
            },
            {
                "filename": "SearchResults.js",
                "summary": "Component that displays search results",
                "functions": [
                    {
                        "name": "handleSearch",
                        "summary": "Updates search results state"
                    },
                    {
                        "name": "renderResult",
                        "summary": "Renders individual search result items"
                    }
                ],
                "external_libraries": [
                    {
                        "name": "react",
                        "link": "https://reactjs.org/"
                    }
                ]
            },
            {
                "filename": "utils.js",
                "summary": "Utility functions for search and data processing",
                "functions": [
                    {
                        "name": "formatDate",
                        "summary": "Formats date strings into readable format"
                    },
                    {
                        "name": "truncateText",
                        "summary": "Truncates text to specified length"
                    },
                    {
                        "name": "validateSearchQuery",
                        "summary": "Validates search query input"
                    },
                    {
                        "name": "filterResults",
                        "summary": "Filters search results based on query"
                    },
                    {
                        "name": "sortByRelevance",
                        "summary": "Sorts results by relevance and date"
                    }
                ],
                "external_libraries": []
            }
        ],
        "cross_references": [
            {
                "from": "SearchResults.js",
                "to": "SearchBar.js",
                "type": "import",
                "description": "SearchResults imports SearchBar component"
            }
        ],
        "external_libraries_summary": [
            {
                "name": "lodash",
                "usage": "Debouncing search input",
                "link": "https://lodash.com/"
            },
            {
                "name": "axios",
                "usage": "HTTP requests for search API",
                "link": "https://axios-http.com/"
            },
            {
                "name": "react",
                "usage": "React components and hooks",
                "link": "https://reactjs.org/"
            }
        ]
    }
    
    uploads[upload_id]["analysis"] = analysis_result
    uploads[upload_id]["status"] = "completed"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 