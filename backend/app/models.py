from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class UploadResponse(BaseModel):
    message: str
    upload_id: str
    file_count: int

class AnalysisResponse(BaseModel):
    status: str
    progress: float
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class AgentStatus(BaseModel):
    internal_doc_agent: str
    library_doc_agent: str
    context_manager_agent: str
    overall_progress: float

class FileAnalysis(BaseModel):
    filename: str
    summary: str
    functions: List[Dict[str, Any]]
    external_libraries: List[Dict[str, Any]]
    cross_references: List[Dict[str, Any]]
    file_type: str
    line_count: int

class ProjectAnalysis(BaseModel):
    files: List[FileAnalysis]
    project_summary: str
    total_files: int
    libraries_used: List[str]
    analysis_time: float 