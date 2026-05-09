# AutoCoder - GenAI Based Autonomous Code Generation Platform

A sophisticated web-based AI coding platform that generates complete, production-ready projects (frontend, backend, database) from high-level natural language prompts. Inspired by Bolt.new, Lovable, and V0, but with a focus on autonomous multi-agent orchestration.

## 🎯 Features

- **Autonomous Project Generation**: Generate complete projects from simple text prompts
- **Multi-Agent Architecture**: 7 specialized agents collaborating via shared memory
- **Production-Quality Code**: Real, runnable projects with proper architecture
- **Real-time Monitoring**: Live logs, agent status, and shared memory visualization
- **Complete Stack**: Frontend (React), Backend (FastAPI), Database (SQLite)
- **Validation & Repair**: Automatic error detection and fixing
- **Professional UI**: Modern, responsive web interface
- **Rate-Limited LLM Access**: Built-in Groq API request throttling to prevent rate limits

## 🏗️ Architecture

### Multi-Agent System

1. **Prompt Understanding Agent**
   - Parses user prompts
   - Extracts project requirements
   - Creates structured specifications

2. **Architect Agent**
   - Designs project structure
   - Defines APIs and contracts
   - Creates database schema

3. **Frontend Agent**
   - Generates React components
   - Creates pages and UI
   - Implements routing and state management

4. **Backend Agent**
   - Generates FastAPI endpoints
   - Creates business logic
   - Implements validation

5. **Database Agent**
   - Generates SQLite schema
   - Creates migrations
   - Generates seed data

6. **DevOps Agent**
   - Generates configuration files
   - Creates Docker setup
   - Generates deployment scripts

7. **Validation Agent**
   - Validates generated code
   - Detects and fixes errors
   - Ensures consistency

### Shared Memory System

All agents communicate via a thread-safe shared memory store:

```json
{
  "project_id": "uuid",
  "project_spec": {},
  "architecture": {},
  "generated_artifacts": {},
  "api_endpoints": [],
  "database_schema": {},
  "errors": [],
  "status": "generating",
  "agents_status": {},
  "execution_log": []
}
```

### Orchestration Flow (6 Stages)

```
1. User Prompt
         ↓
2. Prompt Understanding Agent (Sequential)
         ↓
3. Architect Agent (Sequential)
         ↓
4. Frontend/Backend/Database Agents (Parallel Execution)
         ↓
5. DevOps Agent (Sequential)
         ↓
6. Validation Agent (Sequential)
         ↓
7. Write Project Files to Disk (Sequential)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- Groq API key (https://console.groq.com)

### Setup

#### 1. Clone and Navigate

```bash
cd autocoder
```

#### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

#### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install
```

#### 4. Run Development

```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

Access the application at:
- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📝 Project Structure

```
autocoder/
├── backend/
│   ├── app/
│   │   ├── agents/                    # Multi-agent implementations
│   │   │   ├── prompt_understanding/
│   │   │   ├── architect/
│   │   │   ├── frontend/
│   │   │   ├── backend/
│   │   │   ├── database/
│   │   │   ├── devops/
│   │   │   └── validation/
│   │   ├── core/                      # Core infrastructure
│   │   │   ├── config.py             # Configuration
│   │   │   ├── shared_memory.py      # Shared memory system
│   │   │   ├── llm_client.py         # Groq API client
│   │   │   └── base_agent.py         # Base agent class
│   │   ├── services/
│   │   │   └── orchestrator.py       # Agent orchestration
│   │   ├── models/
│   │   │   └── schemas.py            # Pydantic schemas
│   │   ├── api/
│   │   │   └── projects.py           # FastAPI routes
│   │   └── main.py                   # FastAPI app
│   ├── requirements.txt
│   ├── .env.example
│   └── generated_projects/           # Generated project output
│
├── frontend/
│   ├── src/
│   │   ├── components/               # React components
│   │   ├── pages/                    # React pages
│   │   ├── hooks/                    # Custom React hooks
│   │   ├── store/                    # Zustand state management
│   │   ├── utils/                    # Utilities
│   │   ├── styles/                   # TailwindCSS styles
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── index.html
│
└── README.md (this file)
```

## 🔌 API Endpoints (8 Total)

### Generate Project

```bash
POST /api/generate
Content-Type: application/json

{
  "prompt": "Create me a jewelry website with product catalog and shopping cart"
}

Response:
{
  "success": true,
  "project_id": "uuid",
  "project_dir": "/path/to/generated/project",
  "project_spec": { ... },
  "execution_log": [ ... ]
}
```

### Get Shared Memory

```bash
GET /api/memory

Response: Complete shared memory state
```

### Get Status

```bash
GET /api/status

Response: Current generation status and agent statuses
```

### Get Logs

```bash
GET /api/logs?limit=50

Response: Execution logs
```

### Reset Memory

```bash
POST /api/reset

Response: Confirmation of memory reset
```

### List Projects

```bash
GET /api/projects

Response: List of all generated projects
```

### Get Project Files

```bash
GET /api/projects/{project_id}/files

Response: File tree structure of project
```

### Get File Content

```bash
GET /api/projects/{project_id}/file?path=frontend/src/App.tsx

Response: File content
```

**Plus**: Automatic Swagger UI at `/docs` and ReDoc at `/redoc`

## 🎨 Frontend Features

- **Prompt Input**: Rich text area for project descriptions
- **Live Generation Status**: Real-time status with agent updates
- **Execution Logs**: Color-coded logs with timestamps
- **Shared Memory Inspector**: View complete memory state
- **Agent Dashboard**: Monitor all agent statuses
- **Project Specification Display**: View parsed project details

## 🛠️ Technology Stack

### Backend

- **Framework**: FastAPI
- **LLM Integration**: Groq API
- **Orchestration**: Asyncio + Custom Pipeline
- **Rate Limiting**: Groq Request Throttling
- **Database ORM**: SQLAlchemy
- **Database**: SQLite
- **Async**: asyncio
- **Type Hints**: Pydantic

### Frontend

- **Framework**: React 18
- **Build Tool**: Vite
- **Language**: TypeScript
- **State Management**: Zustand
- **Styling**: TailwindCSS
- **HTTP Client**: Axios
- **Icons**: lucide-react

## 🔑 Configuration

### Environment Variables

```bash
# Backend (.env)
GROQ_API_KEY=your_groq_api_key
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:5173
DEBUG=True
LOG_LEVEL=INFO
GROQ_MODEL=llama-3.1-8b-instant
GROQ_REQUEST_INTERVAL_SECONDS=30.0
PROJECTS_BASE_DIR=./generated_projects
```

## 📦 Generated Project Output

Generated projects follow this structure:

```
project-{id}/
├── frontend/
│   ├── src/
│   │   ├── pages/          # React pages
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom hooks
│   │   └── styles/         # Stylesheets
│   ├── package.json
│   └── Dockerfile
├── backend/
│   ├── app/
│   │   ├── models/         # SQLAlchemy models
│   │   ├── routers/        # FastAPI routers
│   │   ├── services/       # Business logic
│   │   └── main.py         # FastAPI app
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
├── database/
│   ├── schema.sql
│   ├── migrations/
│   └── seeds/
├── docker-compose.yml
├── .env.example
├── README.md
└── project_memory.json
```

## 🧪 Testing

### Run Backend Tests

```bash
cd backend
pytest tests/ -v
```

### Run Frontend Tests

```bash
cd frontend
npm run test
```

## 🐳 Docker Deployment

Generate and run the project with Docker:

```bash
cd generated_projects/{project-id}
docker-compose up
```

## 📊 Monitoring and Debugging

### View Logs in Real-time

The frontend provides a live log viewer showing all agent activities.

### Shared Memory Inspector

View the complete internal state of all agents at `/api/memory` (also accessible from frontend Memory tab).

### Agent Status Dashboard

Monitor individual agent progress and errors from the Status panel.

## 🔒 Error Handling

The system implements a robust error handling and repair loop:

1. **Error Detection**: Validation agent detects issues
2. **Error Logging**: Errors recorded in shared memory
3. **Auto-Repair**: Relevant agents regenerate with error context
4. **Retry Logic**: Failed sections are regenerated up to 3 times
5. **User Notification**: Errors displayed in UI with details

## 🚦 Production Considerations

For production deployment:

1. **Security**
   - Validate all user inputs
   - Implement rate limiting
   - Add authentication/authorization
   - Use HTTPS

2. **Performance**
   - Cache agent responses
   - Implement project queuing
   - Use async processing
   - Monitor resource usage

3. **Scalability**
   - Run multiple backend instances
   - Use load balancing
   - Separate agent workers
   - Implement job scheduling

4. **Monitoring**
   - Add APM (Application Performance Monitoring)
   - Implement error tracking (Sentry)
   - Add metrics collection (Prometheus)
   - Set up alerting

## 🎓 Learning Resources

### Agent Implementation

See [Agent Development Guide](docs/AGENT_DEVELOPMENT.md)

### Architecture Details

See [Architecture Documentation](docs/ARCHITECTURE.md)

### API Reference

See [API Documentation](docs/API.md)

## 📝 Example Projects

Try these prompts to test the system:

```
"Create me a jewelry website with product catalog, shopping cart, and checkout"

"Build a fitness tracking application with workout logging and progress analytics"

"Create an AI chatbot application with conversation history and multi-language support"

"Build a todo list application with task management and team collaboration"
```

## 🤝 Contributing

This is a prototype/internship project. For contributions, please:

1. Follow the existing code structure
2. Add comprehensive docstrings
3. Include error handling
4. Write tests for new features
5. Update documentation

## 📄 License

MIT License

## 👨‍💻 Author

Built as a GenAI-powered autonomous coding system demonstrating:
- Multi-agent architecture
- LLM integration
- Autonomous code generation
- Shared state management
- Production-quality scaffolding

---

**Note**: This is a simplified implementation for demonstration/internship purposes. For production use, additional features like user authentication, data persistence, advanced error recovery, and comprehensive testing would be required.
