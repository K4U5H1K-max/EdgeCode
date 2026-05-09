# Architecture Documentation

Comprehensive guide to the AutoCoder architecture and design decisions.

## System Overview

AutoCoder is a multi-agent system that autonomously generates complete, production-ready web applications. The system follows a modular architecture with clear separation of concerns.

```
┌─────────────────────────────────────────────────────────────────┐
│                        Web Application                          │
│  ┌─────────────────┐                    ┌──────────────────┐   │
│  │  React Frontend │◄──────HTTP API────►│  FastAPI Backend │   │
│  │   (Vite Build)  │                    │  (Async/Await)   │   │
│  └─────────────────┘                    └──────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
         │                                         │
         │ User Input                              │ Project Request
         ▼                                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Orchestration Layer                          │
│                 (ProjectOrchestrator)                           │
│  - Coordinates agent execution                                 │
│  - Manages agent workflow stages                               │
│  - Writes generated code to disk                               │
└─────────────────────────────────────────────────────────────────┘
         │
         │ Orchestrates Agents
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Multi-Agent System                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Shared Memory Store (Thread-Safe State)                │  │
│  │  - Project Specifications                               │  │
│  │  - Architecture Definitions                             │  │
│  │  - Generated Artifacts                                  │  │
│  │  - Execution Logs & Errors                              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           ▲                                      │
│                           │ Read/Write                           │
│                           │                                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Agents (7 Total)                       │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ 1. Prompt Understanding ► 2. Architect                   │  │
│  │ 3. Frontend ── (Parallel) ── 4. Backend                  │  │
│  │ 5. Database ─────────────── 6. DevOps                    │  │
│  │ 7. Validation                                             │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           │                                      │
│                           ▼                                      │
│                      LLM Client                                  │
│                   (Groq API Wrapper)                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Shared Memory System (`shared_memory.py`)

**Purpose**: Centralized state management for all agents

**Features**:
- Thread-safe read/write operations using `asyncio.Lock`
- Nested dictionary updates
- List append operations
- Agent status tracking
- Execution logging
- Error recording

**Key Methods**:
```python
async def read(key, default)        # Read value
async def write(key, value)         # Write value
async def update(key, updates)      # Update nested dict
async def append(key, value)        # Append to list
async def get_all()                 # Get entire state
async def export_to_file(path)      # Export as JSON
```

**Memory Structure**:
```json
{
  "project_id": "uuid",
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
  "status": "completed",
  "agents_status": {
    "AgentName": {
      "status": "completed",
      "timestamp": "2024-01-01T00:00:00",
      "details": {}
    }
  },
  "execution_log": []
}
```

### 2. LLM Client (`llm_client.py`)

**Purpose**: Unified interface for Groq API with rate limiting

**Features**:
- Text generation with custom prompts
- JSON generation with parsing
- Code generation with language-specific formatting
- **Request Rate Limiting** via asyncio.Lock + configurable interval
- Support for both Groq and Ollama providers
- Token optimization

**Methods**:
```python
async def generate_text(prompt, system_prompt, temperature, max_tokens)
async def generate_json(prompt, system_prompt, temperature, max_tokens)
async def generate_code(prompt, language, max_tokens)
```

**Rate Limiting Implementation**:
```python
# Single lock serializes all API requests
self._request_lock = asyncio.Lock()

# Each request waits for interval before next
await asyncio.sleep(min_request_interval_seconds)

# Default: 30 seconds (configurable via GROQ_REQUEST_INTERVAL_SECONDS)
```

### 3. Base Agent (`base_agent.py`)

**Purpose**: Foundation class for all specialized agents

**Features**:
- Lifecycle management (initialize, execute, finalize)
- Shared memory access
- Logging and error handling
- Status tracking
- Artifact recording

**Key Methods**:
```python
async def execute(context)          # Override in subclasses
async def initialize()              # Setup
async def set_status(status, details)
async def log(message, level)
async def log_error(error, details)
async def add_artifact(type, data)
```

### 4. Orchestrator (`orchestrator.py`)

**Purpose**: Coordinates entire project generation workflow

**Responsibilities**:
- Agent instantiation
- Workflow orchestration
- Parallel execution management
- File writing and project persistence
- Error recovery

**Flow** (6 Main Stages):
```
Stage 1: Reset & Initialize
   ↓
Stage 2: Prompt Understanding (Sequential)
   ├─ Parse user prompt
   └─ Create project specification
   ↓
Stage 3: Architect (Sequential)
   ├─ Design system architecture
   ├─ Define API endpoints
   └─ Plan database schema
   ↓
Stage 4: Parallel Code Generation
   ├─ Frontend Agent → React components
   ├─ Backend Agent → FastAPI routes
   └─ Database Agent → SQL schema
   ↓
Stage 5: DevOps (Sequential)
   ├─ Generate configurations
   ├─ Create Docker setup
   └─ Generate scripts
   ↓
Stage 6: Validation (Sequential)
   ├─ Detect errors
   └─ Regenerate as needed
   ↓
Stage 7: Write Project Files
   └─ Persist to disk with structure
```

## Agent Design

### 7 Specialized Agents

#### 1. Prompt Understanding Agent
- **Input**: User prompt
- **Output**: Structured project specification
- **Process**: 
  1. Parse prompt with LLM
  2. Extract project type, features, pages
  3. Set defaults for stack choices
  4. Store in shared memory

#### 2. Architect Agent
- **Input**: Project specification
- **Output**: Architecture, APIs, schema, folder structure
- **Process**:
  1. Generate high-level architecture
  2. Define REST API endpoints
  3. Design database schema
  4. Create folder structure plan

#### 3. Frontend Agent
- **Input**: Project spec, architecture
- **Output**: React pages, components, hooks
- **Process**:
  1. Generate page components
  2. Generate reusable components
  3. Generate custom React hooks
  4. All with TypeScript + TailwindCSS

#### 4. Backend Agent
- **Input**: Project spec, architecture
- **Output**: FastAPI routes, models, services
- **Process**:
  1. Generate Pydantic/SQLAlchemy models
  2. Generate API routes
  3. Generate business logic services
  4. Include validation and error handling

#### 5. Database Agent
- **Input**: Database schema from architect
- **Output**: SQL schema, migrations, seed data
- **Process**:
  1. Generate SQLite CREATE TABLE statements
  2. Generate Alembic migration scripts
  3. Generate seed data scripts

#### 6. DevOps Agent
- **Input**: Project spec
- **Output**: Config files, Dockerfiles, scripts
- **Process**:
  1. Generate package.json
  2. Generate requirements.txt
  3. Generate .env files
  4. Generate Dockerfiles
  5. Generate startup scripts

#### 7. Validation Agent
- **Input**: Generated code, errors
- **Output**: Validation report, fixed code
- **Process**:
  1. Check for syntax errors
  2. Validate imports and dependencies
  3. Fix errors by regenerating
  4. Report fixes applied

## Data Flow

### Generation Request

```
User Prompt (min 10 characters)
    ↓
Frontend sends: POST /api/generate
    ↓
Backend: orchestrator.orchestrate(prompt)
    ↓
STAGE 1: Reset shared_memory
    ↓
STAGE 2: prompt_understanding_agent.execute()
    ├─ LLM parses prompt → project_spec
    ├─ shared_memory.write("project_spec", spec)
    └─ shared_memory.write("project_id", id)
    ↓
STAGE 3: architect_agent.execute()
    ├─ Read project_spec from memory
    ├─ LLM designs architecture
    ├─ shared_memory.write("architecture", arch)
    ├─ shared_memory.write("api_endpoints", endpoints)
    └─ shared_memory.write("database_schema", schema)
    ↓
STAGE 4: Parallel Execution (Rate-Limited)
    ├─ frontend_agent.execute() → React code
    ├─ backend_agent.execute() → FastAPI code
    └─ database_agent.execute() → SQL code
    └─ (Groq API calls throttled by _request_lock)
    ↓
STAGE 5: devops_agent.execute()
    ├─ Generate package.json, requirements.txt
    ├─ Generate Dockerfiles
    └─ Generate startup scripts
    ↓
STAGE 6: validation_agent.execute()
    ├─ Check generated code
    ├─ Detect syntax/import errors
    └─ Regenerate if needed
    ↓
STAGE 7: orchestrator._write_project_files()
    ├─ Create: frontend/src/{pages,components,hooks}/
    ├─ Create: backend/app/{models,routes,services}/
    ├─ Create: database/{schema.sql,migrations,seeds}/
    ├─ Write all files to disk
    └─ Export shared_memory → project_memory.json
    ↓
Return ProjectResponse with project_id
    ↓
Frontend polls: GET /api/memory (real-time status)
    ↓
User downloads/accesses: /api/projects/{project_id}/files
```

### Memory State Transitions

```
Initialize → Analyzing → Architecting → Generating → Validating → Writing → Completed
             (Agent 1)    (Agent 2)     (Agents 3-6) (Agent 7)   (File I/O)
```

## Rate Limiting Strategy

### Groq API Rate Limiting

The system implements request throttling to prevent Groq API rate limit errors:

**Implementation**:
- **asyncio.Lock**: Mutual exclusion ensures serial requests (only 1 concurrent Groq call)
- **Interval Delay**: Configurable delay between requests (default: 30 seconds)
- **Location**: `GroqLLMClient._request_lock` in `llm_client.py`

**Configuration** (.env):
```bash
GROQ_REQUEST_INTERVAL_SECONDS=30.0  # Adjust based on your Groq plan
```

**How It Works**:
```
Request 1 (locked) → Wait 30s → Request 2 (locked) → Wait 30s → Request 3
```

Even during parallel agent execution (Stage 4), all Groq calls are serialized by the lock.

## Error Handling Strategy

### Error Detection

Errors recorded in shared memory during:
- Agent execution failures
- LLM API failures
- File I/O errors
- Validation failures

### Error Recovery

```
Error Detected
    ↓
Log to shared_memory["errors"]
    ↓
Validation Agent
    ├─ Read errors
    ├─ Regenerate failed modules
    └─ Fix and retry (up to 3 attempts)
    ↓
Continue or Abort
```

### Error Reporting

- UI displays errors in real-time
- Frontend fetches `/api/status` every 1 second
- Frontend displays last 5 errors
- Full error history in `/api/logs`

## Scalability Considerations

### Current Design
- Single-instance backend
- In-memory shared memory (lost on restart)
- Synchronous file I/O
- Sequential agent execution with parallel code generation

### For Production Scale

1. **Persistence**
   - Replace in-memory with Redis
   - Add database for project history
   - Implement project versioning

2. **Distribution**
   - Run agents as separate services
   - Use message queue (RabbitMQ/Kafka)
   - Load balance backend instances

3. **Caching**
   - Cache LLM responses
   - Cache project templates
   - Cache generated snippets

4. **Monitoring**
   - Add APM (New Relic/Datadog)
   - Implement error tracking (Sentry)
   - Add metrics (Prometheus)
   - Set up alerting

## Security Considerations

### Current Implementation
- Basic CORS setup
- No authentication
- No rate limiting
- No input validation

### Production Security

1. **Authentication**
   - Add JWT tokens
   - Implement API key management
   - Add user authentication

2. **Authorization**
   - Implement role-based access control
   - Project ownership validation
   - Resource quotas per user

3. **Input Validation**
   - Validate prompts for malicious content
   - Sanitize generated code
   - Check file paths for traversal attacks

4. **Secrets Management**
   - Use environment variables
   - Implement secret rotation
   - Add secret scanning in code

## Performance Optimization

### Current Bottlenecks
- LLM API calls (largest latency)
- File I/O for large projects
- JSON parsing of LLM responses

### Optimization Strategies
- Implement result caching
- Use streaming responses
- Parallel LLM calls where possible
- Optimize JSON parsing
- Implement request batching

---

## Technology Rationale

### Why These Choices?

**FastAPI**
- Native async support
- Automatic OpenAPI documentation
- Fast development
- Type safety with Pydantic

**React + Vite**
- Fast development server
- Small bundle size
- Modern JavaScript ecosystem
- Great TypeScript support

**SQLite**
- Single file database
- No server setup required
- Good for prototype/demo
- Easy to distribute

**Groq API**
- Fast inference
- Good code generation
- Reasonable pricing
- REST API

**Zustand**
- Simple state management
- No boilerplate
- Small bundle size
- Easy to understand

---

This architecture prioritizes:
- **Modularity**: Each agent is independent
- **Scalability**: Easy to add new agents
- **Maintainability**: Clear separation of concerns
- **Debuggability**: Shared memory provides visibility
- **Extensibility**: Open to modifications and additions
