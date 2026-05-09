"""
DevOps/Config Agent

Generates configuration files and deployment setup.
"""

from typing import Dict, Any
from app.core.base_agent import BaseAgent
from app.core.llm_client import llm_client


class DevOpsAgent(BaseAgent):
    """Generates configuration and DevOps files"""
    
    def __init__(self):
        super().__init__(
            name="DevOpsAgent",
            description="Generates configs, setup scripts, and deployment files"
        )
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate configuration and DevOps files.
        
        Returns:
        - package_json: str
        - requirements_txt: str
        - env_files: Dict
        - docker_files: Dict
        - scripts: Dict
        """
        await self.initialize()
        
        try:
            project_spec = await self.read_memory("project_spec")
            
            if not project_spec:
                await self.log_error("No project specification")
                return {"error": "No project specification"}
            
            await self.log("Generating configuration files")
            await self.set_status("generating", {"type": "devops"})
            
            configs = {
                "package_json": self._generate_package_json(project_spec),
                "requirements_txt": self._generate_requirements_txt(),
                "env_files": self._generate_env_files(),
                "docker_files": await self._generate_docker_files(project_spec),
                "scripts": self._generate_scripts()
            }
            
            await self.log("Configuration files generated")
            await self.finalize()
            
            return {
                "success": True,
                "configs": configs
            }
        
        except Exception as e:
            await self.log_error(f"Error generating configs: {str(e)}", {"error": str(e)})
            return {"success": False, "error": str(e)}
    
    def _generate_package_json(self, project_spec: Dict[str, Any]) -> str:
        """Generate package.json for frontend"""
        return """{
  "name": "autocoder-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext .js,.jsx,.ts,.tsx",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.0",
    "lucide-react": "^0.309.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.2.0",
    "vite": "^5.0.0",
    "tailwindcss": "^3.4.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0",
    "typescript": "^5.3.0",
    "eslint": "^8.55.0"
  }
}"""
    
    def _generate_requirements_txt(self) -> str:
        """Generate requirements.txt for backend"""
        return """fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
groq==0.4.1
aiofiles==23.2.1
python-multipart==0.0.6
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
alembic==1.12.1"""
    
    def _generate_env_files(self) -> Dict[str, str]:
        """Generate environment configuration files"""
        return {
            ".env.development": """GROQ_API_KEY=your_development_key
BACKEND_URL=http://localhost:8000
DATABASE_URL=sqlite:///./app.db
DEBUG=true
LOG_LEVEL=DEBUG""",
            
            ".env.production": """GROQ_API_KEY=your_production_key
BACKEND_URL=https://api.example.com
DATABASE_URL=sqlite:///./prod.db
DEBUG=false
LOG_LEVEL=INFO""",
            
            ".env.example": """GROQ_API_KEY=your_groq_api_key
BACKEND_URL=http://localhost:8000
DATABASE_URL=sqlite:///./app.db
DEBUG=true
LOG_LEVEL=DEBUG"""
        }
    
    async def _generate_docker_files(self, project_spec: Dict[str, Any]) -> Dict[str, str]:
        """Generate Docker configuration"""
        return {
            "Dockerfile.frontend": """FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "preview"]""",
            
            "Dockerfile.backend": """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]""",
            
            "docker-compose.yml": """version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.frontend
    ports:
      - "5173:3000"
    environment:
      - VITE_API_URL=http://localhost:8000
    depends_on:
      - backend

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./app.db
      - GROQ_API_KEY=${GROQ_API_KEY}
    volumes:
      - ./backend:/app
    depends_on:
      - db

  db:
    image: sqlite
    volumes:
      - db_data:/data

volumes:
  db_data:"""
        }
    
    def _generate_scripts(self) -> Dict[str, str]:
        """Generate startup and utility scripts"""
        return {
            "setup.sh": """#!/bin/bash
set -e

echo "Setting up AutoCoder..."

# Backend setup
echo "Setting up backend..."
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
echo "Backend setup complete"

# Frontend setup
echo "Setting up frontend..."
cd ../frontend
npm install
echo "Frontend setup complete"

echo "Setup complete! Run ./start.sh to start the application"
""",
            
            "start.sh": """#!/bin/bash

echo "Starting AutoCoder..."

# Start backend
cd backend
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
uvicorn app.main:app --reload --port 8000 &

# Start frontend
cd ../frontend
npm run dev

echo "AutoCoder is running!"
"""
        }
