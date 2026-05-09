"""
Frontend Generation Agent

Generates React components and pages for the frontend.
"""

from typing import Dict, Any
from app.core.base_agent import BaseAgent
from app.core.llm_client import llm_client


class FrontendAgent(BaseAgent):
    """Generates React frontend code"""
    
    def __init__(self):
        super().__init__(
            name="FrontendAgent",
            description="Generates React components, pages, and UI"
        )
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate frontend code.
        
        Expected context:
        - project_spec: Dict
        - architecture: Dict
        - api_endpoints: List
        
        Returns:
        - pages: Dict - Generated pages
        - components: Dict - Generated components
        - hooks: Dict - Generated hooks
        """
        await self.initialize()
        
        try:
            project_spec = await self.read_memory("project_spec")
            api_endpoints = await self.read_memory("api_endpoints", [])
            
            if not project_spec:
                await self.log_error("No project specification")
                return {"error": "No project specification"}
            
            await self.log("Generating frontend code")
            await self.set_status("generating", {"type": "frontend"})
            
            pages = await self._generate_pages(project_spec)
            components = await self._generate_components(project_spec)
            hooks = await self._generate_hooks(project_spec, api_endpoints)
            
            frontend_code = {
                "pages": pages,
                "components": components,
                "hooks": hooks
            }
            
            await self.log("Frontend code generated")
            await self.finalize()
            
            return {
                "success": True,
                "frontend_code": frontend_code
            }
        
        except Exception as e:
            await self.log_error(f"Error generating frontend: {str(e)}", {"error": str(e)})
            return {"success": False, "error": str(e)}
    
    async def _generate_pages(self, project_spec: Dict[str, Any]) -> Dict[str, str]:
        """Generate page components"""
        pages = project_spec.get("pages", ["Home", "Products", "Cart", "Checkout"])
        
        pages_code = {}
        
        for page in pages:
            prompt = f"""
Generate a production-quality React page component for: {page}

Requirements:
- Use TypeScript
- Use React hooks
- Import from 'lucide-react' for icons
- Use TailwindCSS for styling
- Include error states and loading states
- Make it responsive
- Add proper JSDoc comments

Return the complete TSX code for a page component named: {page}Page
Only return code, no markdown.
"""
            
            code = await llm_client.generate_code(
                prompt,
                language="typescript",
                max_tokens=3000
            )
            
            pages_code[page] = code
            await self.log(f"Generated {page} page")
        
        return pages_code
    
    async def _generate_components(self, project_spec: Dict[str, Any]) -> Dict[str, str]:
        """Generate reusable components"""
        components = project_spec.get("components", [
            "ProductCard",
            "ShoppingCart",
            "Navbar",
            "Footer",
            "ProductFilter",
            "SearchBar"
        ])
        
        components_code = {}
        
        for component in components:
            prompt = f"""
Generate a production-quality React component: {component}

Requirements:
- Use TypeScript
- Use React hooks
- Import icons from 'lucide-react'
- Use TailwindCSS
- Accept props with proper typing
- Include JSDoc comments
- Make it reusable and composable

Return complete TSX code for {component} component.
Only return code, no markdown.
"""
            
            code = await llm_client.generate_code(
                prompt,
                language="typescript",
                max_tokens=2000
            )
            
            components_code[component] = code
            await self.log(f"Generated {component} component")
        
        return components_code
    
    async def _generate_hooks(self, project_spec: Dict[str, Any], api_endpoints: list) -> Dict[str, str]:
        """Generate custom React hooks"""
        hooks_code = {}
        
        # useAPI hook
        hooks_code["useAPI"] = await llm_client.generate_code(
            """
Generate a TypeScript React hook called useAPI for making API calls.

Requirements:
- Handle loading, error, and success states
- Support GET, POST, PUT, DELETE
- Handle authentication token
- Include error handling
- Use TypeScript
- Return { data, loading, error, execute }

Return complete hook code. Only code, no markdown.
""",
            language="typescript",
            max_tokens=1500
        )
        
        # useCart hook
        hooks_code["useCart"] = await llm_client.generate_code(
            """
Generate a TypeScript React hook called useCart for cart management.

Requirements:
- Manage cart items in state
- Add/remove/update items
- Calculate totals
- Persist to localStorage
- Use TypeScript

Return complete hook code. Only code, no markdown.
""",
            language="typescript",
            max_tokens=1500
        )
        
        # useAuth hook
        hooks_code["useAuth"] = await llm_client.generate_code(
            """
Generate a TypeScript React hook called useAuth for authentication.

Requirements:
- Manage user auth state
- Handle login/logout
- Store token in localStorage
- Validate token expiry
- Use TypeScript

Return complete hook code. Only code, no markdown.
""",
            language="typescript",
            max_tokens=1500
        )
        
        await self.log(f"Generated {len(hooks_code)} hooks")
        
        return hooks_code
