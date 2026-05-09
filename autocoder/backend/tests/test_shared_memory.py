"""
Tests for Shared Memory
"""

import pytest
import pytest_asyncio
from app.core.shared_memory import SharedMemory


@pytest_asyncio.fixture
async def memory():
    """Create shared memory for testing"""
    mem = SharedMemory()
    yield mem


@pytest.mark.asyncio
async def test_write_read(memory):
    """Test write and read operations"""
    await memory.write("test_key", "test_value")
    value = await memory.read("test_key")
    assert value == "test_value"


@pytest.mark.asyncio
async def test_read_default(memory):
    """Test read with default value"""
    value = await memory.read("nonexistent", "default")
    assert value == "default"


@pytest.mark.asyncio
async def test_update(memory):
    """Test update nested dictionary"""
    await memory.write("test_dict", {"a": 1})
    await memory.update("test_dict", {"b": 2})
    value = await memory.read("test_dict")
    assert value == {"a": 1, "b": 2}


@pytest.mark.asyncio
async def test_append(memory):
    """Test append to list"""
    await memory.write("test_list", [])
    await memory.append("test_list", "item1")
    await memory.append("test_list", "item2")
    value = await memory.read("test_list")
    assert value == ["item1", "item2"]


@pytest.mark.asyncio
async def test_reset(memory):
    """Test memory reset"""
    await memory.write("test_key", "test_value")
    await memory.reset()
    value = await memory.read("test_key")
    assert value is None
