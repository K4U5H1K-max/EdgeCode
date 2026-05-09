"""
Project Generation API Routes
"""

import asyncio
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any

from app.core.shared_memory import shared_memory
from app.services.orchestrator import ProjectOrchestrator
from app.models.schemas import (
    GenerateProjectRequest,
    ProjectResponse,
    SharedMemorySnapshot
)

router = APIRouter(prefix="/api", tags=["projects"])

# Global orchestrator instance
orchestrator = ProjectOrchestrator()

# Background tasks
background_tasks = {}


@router.post("/generate", response_model=ProjectResponse)
async def generate_project(request: GenerateProjectRequest, background_tasks: BackgroundTasks) -> ProjectResponse:
    """
    Generate a new project from user prompt.
    
    This endpoint starts the autonomous project generation workflow.
    
    Args:
        request: Project generation request with user prompt
        background_tasks: FastAPI background tasks
    
    Returns:
        Project response with generation status and details
    """
    
    try:
        # Validate prompt
        if not request.prompt or len(request.prompt.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail="Prompt must be at least 10 characters"
            )
        
        # Start orchestration
        result = await orchestrator.orchestrate(request.prompt)
        
        if not result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Generation failed")
            )
        
        return ProjectResponse(
            success=True,
            project_id=result.get("project_id"),
            project_dir=result.get("project_dir"),
            project_spec=result.get("project_spec"),
            execution_log=result.get("execution_log"),
            agents_status=result.get("agents_status"),
            message=result.get("message")
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Generation failed: {str(e)}"
        )


@router.get("/memory")
async def get_shared_memory() -> SharedMemorySnapshot:
    """
    Get current shared memory state.
    
    Used for monitoring generation progress and debugging.
    """
    
    try:
        memory = await shared_memory.get_all()
        
        return SharedMemorySnapshot(
            project_id=memory.get("project_id"),
            project_spec=memory.get("project_spec", {}),
            architecture=memory.get("architecture", {}),
            generated_artifacts=memory.get("generated_artifacts", {}),
            api_endpoints=memory.get("api_endpoints", []),
            database_schema=memory.get("database_schema", {}),
            errors=memory.get("errors", []),
            status=memory.get("status", "unknown"),
            agents_status=memory.get("agents_status", {}),
            execution_log=memory.get("execution_log", [])
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve memory: {str(e)}"
        )


@router.get("/status")
async def get_generation_status() -> Dict[str, Any]:
    """Get current generation status"""
    
    try:
        status = await shared_memory.read("status", "unknown")
        agents_status = await shared_memory.read("agents_status", {})
        errors = await shared_memory.read("errors", [])
        
        return {
            "status": status,
            "agents_status": agents_status,
            "error_count": len(errors),
            "errors": errors[-5:] if errors else []  # Last 5 errors
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get status: {str(e)}"
        )


@router.get("/logs")
async def get_execution_logs(limit: int = 50) -> Dict[str, Any]:
    """Get execution logs"""
    
    try:
        execution_log = await shared_memory.read("execution_log", [])
        
        return {
            "total": len(execution_log),
            "logs": execution_log[-limit:]
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get logs: {str(e)}"
        )


@router.post("/reset")
async def reset_memory() -> Dict[str, str]:
    """Reset shared memory (for testing)"""
    
    try:
        await shared_memory.reset()
        return {"message": "Memory reset successfully"}
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to reset: {str(e)}"
        )


# Project files browsing endpoints
from pathlib import Path


def _get_generated_projects_dir() -> Path:
    # Try to locate the 'backend' folder in the file's parents reliably.
    p = Path(__file__).resolve()
    backend_root = None
    for parent in p.parents:
        if parent.name == 'backend':
            backend_root = parent
            break

    if backend_root is None:
        # fallback to current working directory if running in different context
        backend_root = Path.cwd()

    gen_dir = backend_root / "generated_projects"
    gen_dir.mkdir(parents=True, exist_ok=True)
    return gen_dir


@router.get("/projects")
async def list_projects():
    """List generated project folders"""
    try:
        base = _get_generated_projects_dir()
        projects = []
        for p in sorted(base.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
            if p.is_dir():
                projects.append({"project_id": p.name, "name": p.name})

        return {"projects": projects}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list projects: {e}")


@router.get("/projects/{project_id}/files")
async def list_project_files(project_id: str, path: str = ""):
    """List files and folders within a project path"""
    try:
        base = _get_generated_projects_dir() / project_id
        if not base.exists() or not base.is_dir():
            raise HTTPException(status_code=404, detail="Project not found")

        target = (base / path).resolve()
        # prevent path traversal
        if not str(target).startswith(str(base.resolve())):
            raise HTTPException(status_code=400, detail="Invalid path")

        items = []
        if target.is_dir():
            for child in sorted(target.iterdir(), key=lambda x: (not x.is_dir(), x.name)):
                items.append({
                    "name": child.name,
                    "path": str(child.relative_to(base)).replace('\\', '/'),
                    "is_dir": child.is_dir(),
                })
        else:
            raise HTTPException(status_code=400, detail="Path is not a directory")

        return {"items": items}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list files: {e}")


@router.get("/projects/{project_id}/file")
async def get_project_file(project_id: str, path: str):
    """Get file contents (text)"""
    try:
        base = _get_generated_projects_dir() / project_id
        if not base.exists() or not base.is_dir():
            raise HTTPException(status_code=404, detail="Project not found")

        target = (base / path).resolve()
        if not str(target).startswith(str(base.resolve())):
            raise HTTPException(status_code=400, detail="Invalid path")

        if not target.exists() or not target.is_file():
            raise HTTPException(status_code=404, detail="File not found")

        # read text
        try:
            text = target.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="Binary file or unsupported encoding")

        return {"path": str(target.relative_to(base)).replace('\\', '/'), "content": text}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read file: {e}")
