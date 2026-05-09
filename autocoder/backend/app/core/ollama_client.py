"""
Ollama LLM Client

Wrapper for local Ollama models.
"""

import httpx
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class OllamaClient:
    """Client for local Ollama models"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "mistral:latest"):
        """
        Initialize Ollama client
        
        Args:
            base_url: Ollama API base URL (default: localhost:11434)
            model: Model name to use (default: mistral:latest)
        """
        self.base_url = base_url
        self.model = model
        # No request timeout for local models; generation can take longer on CPU/GPU.
        self.client = httpx.Client(timeout=None)
    
    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """
        Generate text using Ollama
        
        Args:
            prompt: User prompt
            system_prompt: System context
            temperature: Temperature for generation (0-1)
            max_tokens: Maximum tokens to generate
        
        Returns:
            Generated text
        """
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "temperature": temperature,
            "num_predict": max_tokens,
        }
        
        try:
            response = self.client.post(url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "").strip()
        
        except Exception as e:
            logger.error(f"Ollama error: {str(e)}")
            raise Exception(f"Ollama generation failed: {str(e)}")
    
    async def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 3000
    ) -> Dict[str, Any]:
        """
        Generate JSON response using Ollama
        
        Args:
            prompt: User prompt
            system_prompt: System context
            temperature: Temperature (lower for JSON consistency)
            max_tokens: Maximum tokens
        
        Returns:
            Parsed JSON dictionary
        """
        json_prompt = f"""{prompt}

Return ONLY valid JSON, no markdown, no explanation."""
        
        text = await self.generate_text(
            json_prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        # Clean up markdown code blocks if present
        text = text.replace("```json", "").replace("```", "").strip()
        
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse JSON: {text}")
            # Return empty dict on parse error
            return {}
    
    async def generate_code(
        self,
        prompt: str,
        language: str = "python",
        max_tokens: int = 3000
    ) -> str:
        """
        Generate code using Ollama
        
        Args:
            prompt: Code generation prompt
            language: Programming language
            max_tokens: Maximum tokens
        
        Returns:
            Generated code (without markdown fences)
        """
        code_prompt = f"""{prompt}

Return ONLY the {language} code, no markdown fences, no explanation."""
        
        code = await self.generate_text(
            code_prompt,
            system_prompt=f"You are an expert {language} developer. Generate production-quality code.",
            temperature=0.2,
            max_tokens=max_tokens
        )
        
        # Remove markdown code blocks if present
        code = code.replace(f"```{language}", "").replace("```", "").strip()
        
        return code
    
    def __del__(self):
        """Cleanup HTTP client"""
        try:
            self.client.close()
        except:
            pass
