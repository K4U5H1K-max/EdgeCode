"""
Prompt Understanding Agent

Parses user prompts and generates structured project specifications.
"""

from typing import Dict, Any
from app.core.base_agent import BaseAgent
from app.core.llm_client import llm_client
import uuid


class PromptUnderstandingAgent(BaseAgent):
    """Analyzes user prompts and creates project specifications"""
    
    def __init__(self):
        super().__init__(
            name="PromptUnderstandingAgent",
            description="Parses user prompts and extracts project requirements"
        )
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse user prompt and generate project specification.
        
        Expected context:
        - prompt: str - User's project description
        
        Returns:
        - project_spec: Dict - Structured project specification
        """
        await self.initialize()
        
        try:
            prompt = context.get("prompt", "")
            
            if not prompt:
                await self.log_error("No prompt provided")
                return {"error": "No prompt provided"}
            
            await self.log(f"Analyzing prompt: {prompt[:100]}...")
            await self.set_status("analyzing", {"prompt_length": len(prompt)})
            
            # Use LLM to analyze prompt
            analysis_prompt = f"""
Analyze this user prompt and extract project requirements. Return a JSON object with:
{{
    "project_type": "ecommerce|saas|blog|portfolio|other",
    "frontend": "React|Vue|Angular",
    "backend": "FastAPI|Django|Flask",
    "database": "SQLite|PostgreSQL|MongoDB",
    "features": [list of features],
    "pages": [list of pages to create],
    "components": [list of UI components],
    "complexity": "simple|medium|complex"
}}

User Prompt: {prompt}

Respond with JSON only.
"""
            
            project_spec = await llm_client.generate_json(
                analysis_prompt,
                system_prompt="You are an expert software architect. Analyze requirements and return structured JSON."
            )
            
            # Add metadata
            project_spec["project_id"] = str(uuid.uuid4())
            project_spec["created_at"] = None  # Will be set by response handler
            
            # Set defaults
            project_spec.setdefault("frontend", "React")
            project_spec.setdefault("backend", "FastAPI")
            project_spec.setdefault("database", "SQLite")
            project_spec.setdefault("features", [])
            project_spec.setdefault("pages", [])
            project_spec.setdefault("components", [])
            project_spec.setdefault("complexity", "medium")
            
            await self.log(f"Project specification created: {project_spec['project_type']}")
            await self.write_memory("project_spec", project_spec)
            await self.write_memory("project_id", project_spec["project_id"])
            
            await self.finalize()
            
            return {
                "success": True,
                "project_spec": project_spec
            }
        
        except Exception as e:
            await self.log_error(f"Error analyzing prompt: {str(e)}", {"error": str(e)})
            return {
                "success": False,
                "error": str(e)
            }
