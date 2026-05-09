"""
Base Agent Class for Multi-Agent Architecture

Provides common functionality for all agents.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
from app.core.shared_memory import shared_memory
from app.core.llm_client import llm_client

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.start_time: Optional[datetime] = None
    
    @abstractmethod
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent logic. Must be implemented by subclasses."""
        pass
    
    async def initialize(self) -> None:
        """Initialize agent"""
        self.start_time = datetime.now()
        await shared_memory.set_agent_status(self.name, "initializing")
        await shared_memory.add_execution_log(self.name, f"Agent initialized: {self.description}")
    
    async def set_status(self, status: str, details: Optional[Dict] = None) -> None:
        """Update agent status in shared memory"""
        await shared_memory.set_agent_status(self.name, status, details)
    
    async def log(self, message: str, level: str = "info") -> None:
        """Log message to shared memory"""
        await shared_memory.add_execution_log(self.name, message, level)
    
    async def log_error(self, error: str, details: Optional[Dict] = None) -> None:
        """Log error to shared memory"""
        await self.log(error, level="error")
        await shared_memory.add_error(self.name, error, details)
    
    async def read_memory(self, key: str, default: Any = None) -> Any:
        """Read from shared memory"""
        return await shared_memory.read(key, default)
    
    async def write_memory(self, key: str, value: Any) -> None:
        """Write to shared memory"""
        await shared_memory.write(key, value)
    
    async def update_memory(self, key: str, updates: Dict[str, Any]) -> None:
        """Update nested dictionary in shared memory"""
        await shared_memory.update(key, updates)
    
    async def append_memory(self, key: str, value: Any) -> None:
        """Append to list in shared memory"""
        await shared_memory.append(key, value)
    
    async def add_artifact(self, artifact_type: str, artifact_data: Dict[str, Any]) -> None:
        """Add generated artifact to shared memory"""
        if "generated_artifacts" not in (await shared_memory.read("generated_artifacts")):
            await shared_memory.write("generated_artifacts", {
                "frontend": [],
                "backend": [],
                "database": [],
                "config": []
            })
        
        if artifact_type in ["frontend", "backend", "database", "config"]:
            await shared_memory.append(f"generated_artifacts", {
                "type": artifact_type,
                "agent": self.name,
                "timestamp": datetime.now().isoformat(),
                "data": artifact_data
            })
    
    async def finalize(self) -> None:
        """Finalize agent execution"""
        if self.start_time:
            elapsed = (datetime.now() - self.start_time).total_seconds()
            await self.log(f"Agent execution completed in {elapsed:.2f}s")
        await self.set_status("completed")
