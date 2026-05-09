"""
LLM Client Factory

Provides unified interface for LLM calls across all agents.
Supports both Groq and Ollama providers.
"""

import asyncio
import json
import logging
import time
from typing import Optional, Dict, Any
from groq import Groq
from app.core.config import get_settings

logger = logging.getLogger(__name__)


class GroqLLMClient:
    """Groq LLM client wrapper"""
    
    def __init__(self, api_key: str, model: str):
        self.client = Groq(api_key=api_key)
        self.model = model
        settings = get_settings()
        self.min_request_interval_seconds = max(0.0, float(settings.groq_request_interval_seconds))
        self._request_lock = asyncio.Lock()
    
    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> str:
        """Generate text using Groq API"""
        async with self._request_lock:
            try:
                messages = []
                
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                
                messages.append({"role": "user", "content": prompt})
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                return response.choices[0].message.content
            
            except Exception as e:
                logger.error(f"Groq generation error: {e}")
                raise
            finally:
                if self.min_request_interval_seconds > 0:
                    await asyncio.sleep(self.min_request_interval_seconds)
    
    async def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 4096
    ) -> Dict[str, Any]:
        """Generate JSON using Groq API"""
        try:
            json_system = (system_prompt or "") + "\nRespond with valid JSON only, no markdown, no code blocks."
            
            response_text = await self.generate_text(
                prompt,
                json_system,
                temperature,
                max_tokens
            )
            
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            return json.loads(response_text)
        
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {e}")
            return {}
    
    async def generate_code(
        self,
        prompt: str,
        language: str = "python",
        max_tokens: int = 4096
    ) -> str:
        """Generate code using Groq API"""
        code_prompt = f"{prompt}\n\nReturn ONLY the code, no markdown fences."
        
        code = await self.generate_text(
            code_prompt,
            system_prompt=f"You are an expert {language} developer. Generate production-quality code.",
            temperature=0.2,
            max_tokens=max_tokens
        )
        
        code = code.strip()
        if code.startswith(f"```{language}"):
            code = code[len(f"```{language}"):]
        if code.startswith("```"):
            code = code[3:]
        if code.endswith("```"):
            code = code[:-3]
        
        return code.strip()


class OllamaLLMClient:
    """Ollama LLM client wrapper"""
    
    def __init__(self, base_url: str, model: str):
        import httpx
        self.base_url = base_url
        self.model = model
        # No request timeout for local models; generation can take longer on CPU/GPU.
        self.client = httpx.Client(timeout=None)
    
    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> str:
        """Generate text using Ollama"""
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
            raise
    
    async def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 4096
    ) -> Dict[str, Any]:
        """Generate JSON using Ollama"""
        json_prompt = f"""{prompt}

Return ONLY valid JSON, no markdown, no explanation."""
        
        text = await self.generate_text(
            json_prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        text = text.replace("```json", "").replace("```", "").strip()
        
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse JSON from Ollama: {text}")
            return {}
    
    async def generate_code(
        self,
        prompt: str,
        language: str = "python",
        max_tokens: int = 4096
    ) -> str:
        """Generate code using Ollama"""
        code_prompt = f"""{prompt}

Return ONLY the {language} code, no markdown fences, no explanation."""
        
        code = await self.generate_text(
            code_prompt,
            system_prompt=f"You are an expert {language} developer. Generate production-quality code.",
            temperature=0.2,
            max_tokens=max_tokens
        )
        
        code = code.replace(f"```{language}", "").replace("```", "").strip()
        return code
    
    def __del__(self):
        """Cleanup HTTP client"""
        try:
            self.client.close()
        except:
            pass


def create_llm_client():
    """Factory function to create appropriate LLM client based on settings"""
    settings = get_settings()
    
    if settings.llm_provider == "groq":
        if not settings.groq_api_key:
            raise ValueError("GROQ_API_KEY not set in .env")
        logger.info(f"Using Groq provider with model {settings.groq_model}")
        return GroqLLMClient(settings.groq_api_key, settings.groq_model)
    
    elif settings.llm_provider == "ollama":
        logger.info(f"Using Ollama provider with model {settings.ollama_model} at {settings.ollama_base_url}")
        return OllamaLLMClient(settings.ollama_base_url, settings.ollama_model)
    
    else:
        raise ValueError(f"Unknown LLM_PROVIDER: {settings.llm_provider}")


# Global LLM client instance
llm_client = create_llm_client()
