from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """Application configuration"""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )
    
    # LLM Provider
    llm_provider: str = "groq"  # "groq" or "ollama"
    
    # Groq API (when using Groq provider)
    groq_api_key: str = ""
    groq_model: str = "llama-3.1-8b-instant"
    groq_request_interval_seconds: float = 30.0
    
    # Ollama (when using Ollama provider)
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "mistral:latest"
    
    # Server
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    debug: bool = False
    
    # Frontend
    frontend_url: str = "http://localhost:5173"
    
    # Projects
    projects_base_dir: str = "./generated_projects"
    max_project_size_mb: int = 500
    
    # For backward compatibility
    @property
    def llm_model(self) -> str:
        """Get the current LLM model based on provider"""
        if self.llm_provider == "groq":
            return self.groq_model
        return self.ollama_model
    
    # Logging
    log_level: str = "INFO"
    
@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
