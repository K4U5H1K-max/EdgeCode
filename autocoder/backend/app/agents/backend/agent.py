"""
Backend Generation Agent

Generates FastAPI backend code and endpoints.
"""

from typing import Dict, Any
from app.core.base_agent import BaseAgent
from app.core.llm_client import llm_client


class BackendAgent(BaseAgent):
    """Generates FastAPI backend code"""
    
    def __init__(self):
        super().__init__(
            name="BackendAgent",
            description="Generates FastAPI routes, models, and business logic"
        )
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate backend code.
        
        Returns:
        - models: Dict - Pydantic models
        - routes: Dict - API routes
        - services: Dict - Business logic
        """
        await self.initialize()
        
        try:
            project_spec = await self.read_memory("project_spec")
            api_endpoints = await self.read_memory("api_endpoints", [])
            database_schema = await self.read_memory("database_schema", {})
            
            if not project_spec:
                await self.log_error("No project specification")
                return {"error": "No project specification"}
            
            await self.log("Generating backend code")
            await self.set_status("generating", {"type": "backend"})
            
            models = await self._generate_models(database_schema)
            routes = await self._generate_routes(api_endpoints)
            services = await self._generate_services(project_spec)
            
            backend_code = {
                "models": models,
                "routes": routes,
                "services": services
            }
            
            await self.log("Backend code generated")
            await self.finalize()
            
            return {
                "success": True,
                "backend_code": backend_code
            }
        
        except Exception as e:
            await self.log_error(f"Error generating backend: {str(e)}", {"error": str(e)})
            return {"success": False, "error": str(e)}
    
    async def _generate_models(self, database_schema: Dict[str, Any]) -> Dict[str, str]:
        """Generate Pydantic models"""
        models_code = {}
        
        prompt = f"""
Generate SQLAlchemy ORM models and Pydantic schemas based on this database schema:
{database_schema}

Requirements:
- Use SQLAlchemy with TypeDecorators
- Generate Pydantic BaseModel for each table
- Include validation
- Use Python type hints
- Add __tablename__ for each model

Return complete Python code with all models and schemas.
Only code, no markdown.
"""
        
        code = await llm_client.generate_code(
            prompt,
            language="python",
            max_tokens=3000
        )
        
        models_code["all_models"] = code
        await self.log("Generated database models")
        
        return models_code
    
    async def _generate_routes(self, api_endpoints: list) -> Dict[str, str]:
        """Generate FastAPI routes"""
        routes_code = {}
        
        # Generate main routes file
        prompt = f"""
Generate FastAPI router code for these endpoints:
{api_endpoints}

Requirements:
- Use FastAPI with async/await
- Include input validation with Pydantic
- Add error handling with HTTPException
- Include docstrings for each endpoint
- Add OpenAPI documentation
- Return appropriate status codes

Generate a complete router module with @router.get, @router.post, etc.
Only Python code, no markdown.
"""
        
        code = await llm_client.generate_code(
            prompt,
            language="python",
            max_tokens=4000
        )
        
        routes_code["main_router"] = code
        await self.log("Generated API routes")
        
        return routes_code
    
    async def _generate_services(self, project_spec: Dict[str, Any]) -> Dict[str, str]:
        """Generate service layer with business logic"""
        services_code = {}
        
        features = project_spec.get("features", [])
        
        for feature in features:
            prompt = f"""
Generate a FastAPI service class for: {feature}

Requirements:
- Use async/await
- Include CRUD operations
- Add business logic
- Include error handling
- Use dependency injection where needed
- Add proper type hints

Return complete Python service class code.
Only code, no markdown.
"""
            
            code = await llm_client.generate_code(
                prompt,
                language="python",
                max_tokens=2000
            )
            
            service_name = f"{feature}_service"
            services_code[service_name] = code
            await self.log(f"Generated {feature} service")
        
        return services_code
