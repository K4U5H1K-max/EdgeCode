"""
Shared Memory System for Multi-Agent Communication

This module implements a JSON-based shared memory system that allows
all agents to read/write project state and generated artifacts.
"""

import json
import asyncio
from typing import Any, Dict, Optional, List
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class SharedMemory:
    """Thread-safe shared memory for agent coordination"""
    
    def __init__(self):
        self.memory: Dict[str, Any] = {
            "project_id": None,
            "project_spec": {},
            "architecture": {},
            "generated_artifacts": {
                "frontend": [],
                "backend": [],
                "database": [],
                "config": []
            },
            "api_endpoints": [],
            "database_schema": {},
            "errors": [],
            "status": "initializing",
            "agents_status": {},
            "execution_log": []
        }
        self.lock = asyncio.Lock()
    
    async def read(self, key: str, default: Any = None) -> Any:
        """Read value from shared memory"""
        async with self.lock:
            return self.memory.get(key, default)
    
    async def write(self, key: str, value: Any) -> None:
        """Write value to shared memory"""
        async with self.lock:
            self.memory[key] = value
            await self._log_update(key, value)
    
    async def update(self, key: str, updates: Dict[str, Any]) -> None:
        """Update nested dictionary in shared memory"""
        async with self.lock:
            if key in self.memory and isinstance(self.memory[key], dict):
                self.memory[key].update(updates)
                await self._log_update(key, self.memory[key])
    
    async def append(self, key: str, value: Any) -> None:
        """Append to list in shared memory"""
        async with self.lock:
            if key in self.memory and isinstance(self.memory[key], list):
                self.memory[key].append(value)
                await self._log_update(key, self.memory[key])
    
    async def get_all(self) -> Dict[str, Any]:
        """Get entire shared memory state"""
        async with self.lock:
            return dict(self.memory)
    
    async def set_agent_status(self, agent_name: str, status: str, details: Optional[Dict] = None) -> None:
        """Update agent status"""
        async with self.lock:
            self.memory["agents_status"][agent_name] = {
                "status": status,
                "timestamp": datetime.now().isoformat(),
                "details": details or {}
            }
    
    async def add_execution_log(self, agent: str, message: str, level: str = "info") -> None:
        """Add execution log entry"""
        async with self.lock:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "agent": agent,
                "message": message,
                "level": level
            }
            self.memory["execution_log"].append(log_entry)
            logger.log(
                getattr(logging, level.upper(), logging.INFO),
                f"[{agent}] {message}"
            )
    
    async def add_error(self, agent: str, error: str, details: Optional[Dict] = None) -> None:
        """Record error in shared memory"""
        async with self.lock:
            error_entry = {
                "timestamp": datetime.now().isoformat(),
                "agent": agent,
                "error": error,
                "details": details or {}
            }
            self.memory["errors"].append(error_entry)
    
    async def _log_update(self, key: str, value: Any) -> None:
        """Log memory update (called within lock)"""
        logger.debug(f"Memory update: {key}")
    
    async def reset(self) -> None:
        """Reset shared memory"""
        async with self.lock:
            self.memory = {
                "project_id": None,
                "project_spec": {},
                "architecture": {},
                "generated_artifacts": {
                    "frontend": [],
                    "backend": [],
                    "database": [],
                    "config": []
                },
                "api_endpoints": [],
                "database_schema": {},
                "errors": [],
                "status": "initializing",
                "agents_status": {},
                "execution_log": []
            }
    
    async def export_to_file(self, filepath: Path) -> None:
        """Export shared memory to JSON file"""
        async with self.lock:
            with open(filepath, 'w') as f:
                json.dump(self.memory, f, indent=2, default=str)


# Global shared memory instance
shared_memory = SharedMemory()
