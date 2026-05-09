"""
Validation and Repair Agent

Validates generated code and fixes errors.
"""

from typing import Dict, Any
from app.core.base_agent import BaseAgent
from app.core.llm_client import llm_client


class ValidationAgent(BaseAgent):
    """Validates and repairs generated code"""
    
    def __init__(self):
        super().__init__(
            name="ValidationAgent",
            description="Validates generated code and fixes errors"
        )
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate generated code and fix errors.
        
        Expected context:
        - build_output: str - Build/test output with errors
        - generated_code: Dict - Generated code files
        
        Returns:
        - validation_report: Dict
        - fixed_code: Dict - Corrected code
        """
        await self.initialize()
        
        try:
            await self.log("Starting validation")
            await self.set_status("validating")
            
            # Get generated artifacts
            all_memory = await self.read_memory("", {})
            
            errors = await self.read_memory("errors", [])
            
            if errors:
                await self.log(f"Found {len(errors)} errors to fix")
                
                # Fix errors
                fixed_code = await self._fix_errors(errors)
                
                validation_report = {
                    "status": "errors_fixed",
                    "errors_found": len(errors),
                    "errors_fixed": len(fixed_code)
                }
            else:
                validation_report = {
                    "status": "passed",
                    "errors_found": 0
                }
                fixed_code = {}
            
            await self.log("Validation complete")
            await self.finalize()
            
            return {
                "success": True,
                "validation_report": validation_report,
                "fixed_code": fixed_code
            }
        
        except Exception as e:
            await self.log_error(f"Validation error: {str(e)}", {"error": str(e)})
            return {"success": False, "error": str(e)}
    
    async def _fix_errors(self, errors: list) -> Dict[str, str]:
        """Fix identified errors"""
        fixed_code = {}
        
        for error in errors:
            agent_name = error.get("agent", "unknown")
            error_msg = error.get("error", "")
            
            prompt = f"""
This generated code has an error:

Error: {error_msg}

Please fix the error and return corrected code.
Ensure it's production-quality and handles edge cases.

Return only corrected code, no markdown.
"""
            
            fixed = await llm_client.generate_code(prompt, language="python")
            fixed_code[f"{agent_name}_fixed"] = fixed
            await self.log(f"Fixed error from {agent_name}")
        
        return fixed_code
