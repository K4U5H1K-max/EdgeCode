"""
API Models for Request/Response handling
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime


class GenerateProjectRequest(BaseModel):
    """Request to generate a new project"""
    prompt: str = Field(..., min_length=10, description="Project description")


class ProjectSpecification(BaseModel):
    """Generated project specification"""
    project_id: str
    project_type: str
    frontend: str
    backend: str
    database: str
    features: List[str]
    pages: List[str]
    components: List[str]
    complexity: str


class ProjectResponse(BaseModel):
    """Response with generated project details"""
    success: bool
    project_id: Optional[str] = None
    project_dir: Optional[str] = None
    project_spec: Optional[ProjectSpecification] = None
    execution_log: Optional[List[Dict[str, Any]]] = None
    agents_status: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    message: Optional[str] = None


class ExecutionLogEntry(BaseModel):
    """Individual execution log entry"""
    timestamp: str
    agent: str
    message: str
    level: str = "info"


class SharedMemorySnapshot(BaseModel):
    """Snapshot of shared memory state"""
    project_id: Optional[str] = None
    project_spec: Dict[str, Any] = {}
    architecture: Dict[str, Any] = {}
    generated_artifacts: Dict[str, Any] = {}
    api_endpoints: List[Dict[str, Any]] = []
    database_schema: Dict[str, Any] = {}
    errors: List[Dict[str, Any]] = []
    status: str
    agents_status: Dict[str, Any] = {}
    execution_log: List[ExecutionLogEntry] = []


class ProjectSummary(BaseModel):
    """Summary of generated project"""
    project_id: str
    project_type: str
    created_at: datetime
    files_generated: int
    status: str
    project_dir: str
