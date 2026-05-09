"""
Database Agent

Generates SQLite schema and migrations.
"""

from typing import Dict, Any
from app.core.base_agent import BaseAgent
from app.core.llm_client import llm_client


class DatabaseAgent(BaseAgent):
    """Generates database schema and migrations"""
    
    def __init__(self):
        super().__init__(
            name="DatabaseAgent",
            description="Generates SQLite schema and migrations"
        )
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate database schema and migrations.
        
        Returns:
        - schema_sql: str - SQL schema definition
        - migrations: Dict - Migration scripts
        - seeds: Dict - Seed data
        """
        await self.initialize()
        
        try:
            database_schema = await self.read_memory("database_schema", {})
            
            if not database_schema:
                await self.log_error("No database schema available")
                return {"error": "No database schema"}
            
            await self.log("Generating database schema")
            await self.set_status("generating", {"type": "database"})
            
            schema_sql = await self._generate_schema_sql(database_schema)
            migrations = await self._generate_migrations(database_schema)
            seeds = await self._generate_seeds(database_schema)
            
            database_code = {
                "schema_sql": schema_sql,
                "migrations": migrations,
                "seeds": seeds
            }
            
            await self.log("Database schema generated")
            await self.finalize()
            
            return {
                "success": True,
                "database_code": database_code
            }
        
        except Exception as e:
            await self.log_error(f"Error generating database: {str(e)}", {"error": str(e)})
            return {"success": False, "error": str(e)}
    
    async def _generate_schema_sql(self, schema: Dict[str, Any]) -> str:
        """Generate SQL schema"""
        prompt = f"""
Generate SQLite CREATE TABLE statements for this schema:
{schema}

Requirements:
- Use SQLite syntax
- Include primary keys
- Include foreign keys
- Add indexes
- Add constraints
- Include timestamps

Return only SQL code, no markdown.
"""
        
        sql = await llm_client.generate_code(
            prompt,
            language="sql",
            max_tokens=2000
        )
        
        return sql
    
    async def _generate_migrations(self, schema: Dict[str, Any]) -> Dict[str, str]:
        """Generate migration files"""
        migrations = {}
        
        prompt = f"""
Generate an Alembic migration script for this schema:
{schema}

Requirements:
- Use SQLAlchemy migration syntax
- Create all tables
- Add relationships
- Add constraints
- Be reversible

Return Python code for migration file.
Only code, no markdown.
"""
        
        code = await llm_client.generate_code(
            prompt,
            language="python",
            max_tokens=2000
        )
        
        migrations["001_initial_schema"] = code
        
        return migrations
    
    async def _generate_seeds(self, schema: Dict[str, Any]) -> Dict[str, str]:
        """Generate seed data"""
        seeds = {}
        
        prompt = f"""
Generate Python seeding script with sample data for these tables:
{schema}

Requirements:
- Use SQLAlchemy ORM
- Create realistic sample data
- Include relationships
- Include timestamps
- Be idempotent

Return Python script code.
Only code, no markdown.
"""
        
        code = await llm_client.generate_code(
            prompt,
            language="python",
            max_tokens=2000
        )
        
        seeds["seed_data"] = code
        
        return seeds
