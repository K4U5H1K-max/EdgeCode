"""
Tests for Agents
"""

import pytest
import pytest_asyncio
from app.agents import (
    PromptUnderstandingAgent,
    ArchitectAgent,
)
from app.core import shared_memory


@pytest_asyncio.fixture
async def setup_memory():
    """Setup shared memory before test"""
    await shared_memory.reset()
    yield
    await shared_memory.reset()


@pytest.mark.asyncio
async def test_prompt_understanding_agent(setup_memory):
    """Test prompt understanding agent"""
    agent = PromptUnderstandingAgent()
    
    context = {
        "prompt": "Create me a jewelry website with shopping cart and checkout system"
    }
    
    result = await agent.execute(context)
    
    assert result["success"] == True
    assert "project_spec" in result
    assert result["project_spec"]["project_type"] in ["ecommerce", "saas", "blog"]


@pytest.mark.asyncio
async def test_architect_agent(setup_memory):
    """Test architect agent"""
    agent = ArchitectAgent()
    
    # Setup project spec
    project_spec = {
        "project_type": "ecommerce",
        "frontend": "React",
        "backend": "FastAPI",
        "database": "SQLite",
        "features": ["products", "cart", "checkout"]
    }
    await shared_memory.write("project_spec", project_spec)
    
    context = {"project_spec": project_spec}
    result = await agent.execute(context)
    
    assert result["success"] == True
    assert "architecture_plan" in result
