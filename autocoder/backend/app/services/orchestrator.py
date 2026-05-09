"""
LangGraph Orchestration

Coordinates all agents in a multi-stage workflow.
"""

from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import json
import asyncio

from app.core.shared_memory import shared_memory
from app.agents import (
    PromptUnderstandingAgent,
    ArchitectAgent,
    FrontendAgent,
    BackendAgent,
    DatabaseAgent,
    DevOpsAgent,
    ValidationAgent
)


class ProjectOrchestrator:
    """Orchestrates agent execution for autonomous project generation"""
    
    def __init__(self, projects_base_dir: str = "./generated_projects"):
        self.projects_base_dir = Path(projects_base_dir)
        self.projects_base_dir.mkdir(exist_ok=True)
        
        # Initialize agents
        self.agents = {
            "prompt_understanding": PromptUnderstandingAgent(),
            "architect": ArchitectAgent(),
            "frontend": FrontendAgent(),
            "backend": BackendAgent(),
            "database": DatabaseAgent(),
            "devops": DevOpsAgent(),
            "validation": ValidationAgent(),
        }
    
    async def orchestrate(self, user_prompt: str) -> Dict[str, Any]:
        """
        Orchestrate autonomous project generation.
        
        Flow:
        1. Prompt Understanding Agent - Parse requirements
        2. Architect Agent - Design structure and APIs
        3. Frontend/Backend/Database Agents - Generate code (parallel)
        4. DevOps Agent - Generate configs
        5. Validation Agent - Validate and fix
        6. Write files to project directory
        
        Args:
            user_prompt: User's project description
        
        Returns:
            Project metadata and status
        """
        
        await shared_memory.reset()
        await shared_memory.write("status", "starting")
        
        project_id = None
        execution_log = []
        
        try:
            # Stage 1: Understand Prompt
            await shared_memory.write("status", "analyzing_prompt")
            execution_log.append({"stage": 1, "timestamp": datetime.now().isoformat()})
            
            prompt_result = await self.agents["prompt_understanding"].execute(
                {"prompt": user_prompt}
            )
            
            if not prompt_result.get("success"):
                return self._create_failure_response("Failed to analyze prompt", prompt_result)
            
            project_spec = prompt_result["project_spec"]
            project_id = project_spec.get("project_id")
            
            # Stage 2: Create Architecture
            await shared_memory.write("status", "architecting")
            execution_log.append({"stage": 2, "timestamp": datetime.now().isoformat()})
            
            arch_result = await self.agents["architect"].execute(
                {"project_spec": project_spec}
            )
            
            if not arch_result.get("success"):
                return self._create_failure_response("Failed to create architecture", arch_result)
            
            # Stage 3: Generate Code (Parallel)
            await shared_memory.write("status", "generating_code")
            execution_log.append({"stage": 3, "timestamp": datetime.now().isoformat()})
            
            # Run frontend, backend, database in parallel
            frontend_task = self.agents["frontend"].execute({})
            backend_task = self.agents["backend"].execute({})
            database_task = self.agents["database"].execute({})
            
            frontend_result, backend_result, database_result = await asyncio.gather(
                frontend_task, backend_task, database_task,
                return_exceptions=True
            )
            
            # Check for errors
            for result in [frontend_result, backend_result, database_result]:
                if isinstance(result, Exception):
                    raise result
                if not result.get("success"):
                    return self._create_failure_response("Failed to generate code", result)
            
            # Stage 4: Generate Configs
            await shared_memory.write("status", "generating_configs")
            execution_log.append({"stage": 4, "timestamp": datetime.now().isoformat()})
            
            devops_result = await self.agents["devops"].execute({})
            
            if not devops_result.get("success"):
                return self._create_failure_response("Failed to generate configs", devops_result)
            
            # Stage 5: Validation
            await shared_memory.write("status", "validating")
            execution_log.append({"stage": 5, "timestamp": datetime.now().isoformat()})
            
            validation_result = await self.agents["validation"].execute({})
            
            # Stage 6: Write Files
            await shared_memory.write("status", "writing_files")
            execution_log.append({"stage": 6, "timestamp": datetime.now().isoformat()})
            
            project_dir = await self._write_project_files(
                project_id,
                frontend_result,
                backend_result,
                database_result,
                devops_result
            )
            
            # Final Status
            await shared_memory.write("status", "completed")
            
            execution_log.append({
                "stage": "completed",
                "timestamp": datetime.now().isoformat()
            })
            
            return {
                "success": True,
                "project_id": project_id,
                "project_spec": project_spec,
                "project_dir": str(project_dir),
                "execution_log": execution_log,
                "agents_status": await shared_memory.read("agents_status", {}),
                "message": f"Project generated successfully at {project_dir}"
            }
        
        except Exception as e:
            await shared_memory.write("status", "error")
            return self._create_failure_response(str(e), {"exception": str(e)})
    
    async def _write_project_files(
        self,
        project_id: str,
        frontend_result: Dict,
        backend_result: Dict,
        database_result: Dict,
        devops_result: Dict
    ) -> Path:
        """Write generated code to project directory"""
        
        project_dir = self.projects_base_dir / project_id
        project_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (project_dir / "frontend" / "src" / "pages").mkdir(parents=True, exist_ok=True)
        (project_dir / "frontend" / "src" / "components").mkdir(parents=True, exist_ok=True)
        (project_dir / "frontend" / "src" / "hooks").mkdir(parents=True, exist_ok=True)
        (project_dir / "backend" / "app" / "models").mkdir(parents=True, exist_ok=True)
        (project_dir / "backend" / "app" / "routes").mkdir(parents=True, exist_ok=True)
        (project_dir / "backend" / "app" / "services").mkdir(parents=True, exist_ok=True)
        (project_dir / "database" / "migrations").mkdir(parents=True, exist_ok=True)
        (project_dir / "database" / "seeds").mkdir(parents=True, exist_ok=True)
        
        # Write frontend code
        frontend_code = frontend_result.get("frontend_code", {})
        frontend_dir = project_dir / "frontend" / "src"
        
        # Write pages
        for page_name, page_code in frontend_code.get("pages", {}).items():
            with open(frontend_dir / "pages" / f"{page_name}.tsx", "w") as f:
                f.write(page_code)
        
        # Write components
        for component_name, component_code in frontend_code.get("components", {}).items():
            with open(frontend_dir / "components" / f"{component_name}.tsx", "w") as f:
                f.write(component_code)
        
        # Write hooks
        for hook_name, hook_code in frontend_code.get("hooks", {}).items():
            with open(frontend_dir / "hooks" / f"use{hook_name}.ts", "w") as f:
                f.write(hook_code)
        
        # Write backend code
        backend_code = backend_result.get("backend_code", {})
        backend_dir = project_dir / "backend" / "app"
        
        # Write models
        for model_name, model_code in backend_code.get("models", {}).items():
            with open(backend_dir / "models" / f"{model_name}.py", "w") as f:
                f.write(model_code)
        
        # Write routes
        for route_name, route_code in backend_code.get("routes", {}).items():
            with open(backend_dir / "routes" / f"{route_name}.py", "w") as f:
                f.write(route_code)
        
        # Write services
        for service_name, service_code in backend_code.get("services", {}).items():
            with open(backend_dir / "services" / f"{service_name}.py", "w") as f:
                f.write(service_code)
        
        # Write database files
        database_code = database_result.get("database_code", {})
        
        if "schema_sql" in database_code:
            with open(project_dir / "database" / "schema.sql", "w") as f:
                f.write(database_code["schema_sql"])
        
        for migration_name, migration_code in database_code.get("migrations", {}).items():
            with open(project_dir / "database" / "migrations" / f"{migration_name}.py", "w") as f:
                f.write(migration_code)
        
        for seed_name, seed_code in database_code.get("seeds", {}).items():
            with open(project_dir / "database" / "seeds" / f"{seed_name}.py", "w") as f:
                f.write(seed_code)
        
        # Write configs
        configs = devops_result.get("configs", {})
        
        if "package_json" in configs:
            with open(project_dir / "frontend" / "package.json", "w") as f:
                f.write(configs["package_json"])
        
        if "requirements_txt" in configs:
            with open(project_dir / "backend" / "requirements.txt", "w") as f:
                f.write(configs["requirements_txt"])
        
        for env_name, env_content in configs.get("env_files", {}).items():
            with open(project_dir / env_name, "w") as f:
                f.write(env_content)
        
        for docker_name, docker_content in configs.get("docker_files", {}).items():
            with open(project_dir / docker_name, "w") as f:
                f.write(docker_content)
        
        for script_name, script_content in configs.get("scripts", {}).items():
            script_path = project_dir / script_name
            with open(script_path, "w") as f:
                f.write(script_content)
            script_path.chmod(0o755)  # Make executable on Unix
        
        # Write shared memory and metadata
        await shared_memory.export_to_file(project_dir / "project_memory.json")
        
        # Create README
        readme_content = self._generate_readme()
        with open(project_dir / "README.md", "w") as f:
            f.write(readme_content)
        
        return project_dir
    
    def _generate_readme(self) -> str:
        """Generate project README"""
        return """# AutoCoder Generated Project

This is a production-style web application generated by AutoCoder.

## Project Structure

```
frontend/          - React + Vite frontend application
backend/           - FastAPI backend server
database/          - Database schemas and migrations
```

## Quick Start

### Setup

```bash
./setup.sh          # On Windows: run setup.bat
```

### Development

```bash
./start.sh          # On Windows: run start.bat
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Docker

```bash
docker-compose up
```

## Environment Variables

Copy `.env.example` to `.env` and fill in your Groq API key and other configuration.

## Development

- **Frontend**: React + TypeScript + TailwindCSS + Vite
- **Backend**: FastAPI + SQLAlchemy + SQLite
- **Orchestration**: LangGraph + Groq

## API Documentation

See `http://localhost:8000/docs` when backend is running.

## Building for Production

```bash
# Frontend
cd frontend
npm run build

# Backend
cd backend
pip install -r requirements.txt
# Set up your production database
```

## Support

Generated by AutoCoder - GenAI Based Autonomous Code Generation Platform
"""
    
    def _create_failure_response(self, error: str, details: Dict) -> Dict[str, Any]:
        """Create standardized failure response"""
        return {
            "success": False,
            "error": error,
            "details": details,
            "status": "failed"
        }
