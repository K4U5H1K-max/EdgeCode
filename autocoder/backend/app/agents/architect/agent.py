"""
Architect Agent

Defines project structure, APIs, and database schema.
"""

from typing import Dict, Any, List
from app.core.base_agent import BaseAgent
from app.core.llm_client import llm_client


class ArchitectAgent(BaseAgent):
    """Creates project architecture and design specifications"""
    
    def __init__(self):
        super().__init__(
            name="ArchitectAgent",
            description="Defines project structure, APIs, DB schema, and contracts"
        )
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create comprehensive architecture plan.
        
        Expected context:
        - project_spec: Dict - Project specification from PromptUnderstandingAgent
        
        Returns:
        - architecture: Dict - Complete architecture plan
        - api_endpoints: List - API endpoint definitions
        - database_schema: Dict - Database schema
        - folder_structure: Dict - Project folder structure
        """
        await self.initialize()
        
        try:
            project_spec = context.get("project_spec") or await self.read_memory("project_spec")
            
            if not project_spec:
                await self.log_error("No project specification available")
                return {"error": "No project specification"}
            
            await self.log(f"Creating architecture for {project_spec['project_type']}")
            await self.set_status("architecting", {"project_type": project_spec["project_type"]})
            
            # Generate architecture
            architecture = await self._generate_architecture(project_spec)
            api_endpoints = await self._generate_api_endpoints(project_spec)
            database_schema = await self._generate_database_schema(project_spec)
            folder_structure = await self._generate_folder_structure(project_spec)
            
            architecture_plan = {
                "architecture": architecture,
                "api_endpoints": api_endpoints,
                "database_schema": database_schema,
                "folder_structure": folder_structure
            }
            
            # Store in shared memory
            await self.write_memory("architecture", architecture)
            await self.write_memory("api_endpoints", api_endpoints)
            await self.write_memory("database_schema", database_schema)
            
            await self.log("Architecture plan created successfully")
            await self.finalize()
            
            return {
                "success": True,
                "architecture_plan": architecture_plan
            }
        
        except Exception as e:
            await self.log_error(f"Error creating architecture: {str(e)}", {"error": str(e)})
            return {"success": False, "error": str(e)}
    
    async def _generate_architecture(self, project_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Generate high-level architecture"""
        prompt = f"""
Based on this project specification:
{project_spec}

Generate a JSON architecture document with:
{{
    "name": "Architecture Name",
    "description": "Architecture description",
    "layers": [
        {{"name": "Frontend", "components": [], "technologies": []}},
        {{"name": "Backend", "components": [], "technologies": []}},
        {{"name": "Database", "components": [], "technologies": []}}
    ],
    "integrations": [list of system integrations]
}}
"""
        return await llm_client.generate_json(
            prompt,
            system_prompt="You are a senior software architect. Generate detailed architecture."
        )
    
    async def _generate_api_endpoints(self, project_spec: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate API endpoint specifications"""
        features = project_spec.get("features", [])
        project_type = project_spec.get("project_type", "")
        
        prompt = f"""
Generate REST API endpoints for a {project_type} with features: {features}

Return a JSON array of endpoints:
[
    {{
        "method": "GET|POST|PUT|DELETE",
        "path": "/api/endpoint",
        "description": "What it does",
        "request_body": {{schema}},
        "response": {{schema}},
        "auth_required": true|false
    }}
]

Include at least 10 essential endpoints.
"""
        return await llm_client.generate_json(
            prompt,
            system_prompt="You are a REST API designer. Generate production-quality API specifications."
        )
    
    async def _generate_database_schema(self, project_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Generate database schema"""
        features = project_spec.get("features", [])
        
        prompt = f"""
Design SQLite database schema for a project with features: {features}

Return JSON:
{{
    "tables": [
        {{
            "name": "table_name",
            "fields": [
                {{"name": "id", "type": "INTEGER", "primary_key": true}},
                {{"name": "field", "type": "TEXT", "required": true}}
            ],
            "relationships": [
                {{"table": "other_table", "field": "foreign_key"}}
            ]
        }}
    ],
    "indexes": [list of indexes],
    "constraints": [list of constraints]
}}
"""
        return await llm_client.generate_json(
            prompt,
            system_prompt="You are a database architect. Design efficient, normalized schemas."
        )
    
    async def _generate_folder_structure(self, project_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Generate project folder structure"""
        return {
            "frontend": {
                "description": "React + Vite frontend",
                "structure": [
                    "src/pages",
                    "src/components",
                    "src/hooks",
                    "src/store",
                    "src/utils",
                    "src/styles",
                    "public"
                ]
            },
            "backend": {
                "description": "FastAPI backend",
                "structure": [
                    "app/api/routes",
                    "app/models",
                    "app/services",
                    "app/core",
                    "app/db",
                    "tests"
                ]
            },
            "database": {
                "description": "Database migrations",
                "structure": [
                    "migrations",
                    "seeds"
                ]
            },
            "root": [
                ".env",
                "docker-compose.yml",
                "README.md"
            ]
        }
