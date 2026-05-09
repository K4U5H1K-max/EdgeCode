"""
Backend Application Package
"""

__version__ = "1.0.0"
__author__ = "AutoCoder Team"

from app.core import get_settings, shared_memory, llm_client
from app.services import ProjectOrchestrator

__all__ = [
    "get_settings",
    "shared_memory",
    "llm_client",
    "ProjectOrchestrator",
]
