# API Reference

Complete API documentation for AutoCoder backend.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently no authentication required. In production, add:
- API Key authentication
- JWT tokens
- OAuth 2.0

## Response Format

All responses are JSON:

```json
{
  "success": true|false,
  "data": {...},
  "error": "error message if applicable"
}
```

## Endpoints

### 1. Generate Project

Generate a new project from a natural language prompt.

**Endpoint**
```
POST /api/generate
```

**Request**
```json
{
  "prompt": "Create me a jewelry website with shopping cart and checkout"
}
```

**Parameters**
- `prompt` (string, required): Project description. Minimum 10 characters.

**Response** (200 OK)
```json
{
  "success": true,
  "project_id": "550e8400-e29b-41d4-a716-446655440000",
  "project_dir": "/home/user/autocoder/generated_projects/550e8400-e29b-41d4-a716-446655440000",
  "project_spec": {
    "project_id": "550e8400-e29b-41d4-a716-446655440000",
    "project_type": "ecommerce",
    "frontend": "React",
    "backend": "FastAPI",
    "database": "SQLite",
    "features": ["product_catalog", "shopping_cart", "orders", "checkout"],
    "pages": ["Home", "Products", "Cart", "Checkout"],
    "components": ["ProductCard", "ShoppingCart", "Navbar", "Footer"],
    "complexity": "medium"
  },
  "execution_log": [
    {
      "stage": 1,
      "timestamp": "2024-01-15T10:30:45.123456"
    },
    {
      "stage": 2,
      "timestamp": "2024-01-15T10:30:50.234567"
    }
  ],
  "agents_status": {
    "PromptUnderstandingAgent": {
      "status": "completed",
      "timestamp": "2024-01-15T10:30:48.000000",
      "details": {}
    },
    "ArchitectAgent": {
      "status": "completed",
      "timestamp": "2024-01-15T10:30:52.000000",
      "details": {}
    }
  },
  "message": "Project generated successfully at /home/user/autocoder/generated_projects/..."
}
```

**Error Response** (400/500)
```json
{
  "success": false,
  "error": "Prompt must be at least 10 characters"
}
```

**Status Codes**
- `200`: Project generated successfully
- `400`: Invalid request (validation error)
- `500`: Server error during generation

---

### 2. Get Shared Memory

Retrieve the current shared memory state.

**Endpoint**
```
GET /api/memory
```

**Parameters**
None

**Response** (200 OK)
```json
{
  "project_id": "550e8400-e29b-41d4-a716-446655440000",
  "project_spec": {
    "project_type": "ecommerce",
    "frontend": "React",
    "backend": "FastAPI",
    "database": "SQLite",
    "features": [...],
    "pages": [...],
    "components": [...],
    "complexity": "medium"
  },
  "architecture": {
    "name": "...",
    "description": "...",
    "layers": [...],
    "integrations": [...]
  },
  "generated_artifacts": {
    "frontend": [
      {
        "type": "component",
        "agent": "FrontendAgent",
        "timestamp": "2024-01-15T10:31:00.000000",
        "data": {...}
      }
    ],
    "backend": [...],
    "database": [...],
    "config": [...]
  },
  "api_endpoints": [
    {
      "method": "GET",
      "path": "/api/products",
      "description": "Get all products",
      "request_body": {...},
      "response": {...},
      "auth_required": false
    }
  ],
  "database_schema": {
    "tables": [
      {
        "name": "products",
        "fields": [...],
        "relationships": [...]
      }
    ],
    "indexes": [...],
    "constraints": [...]
  },
  "errors": [
    {
      "timestamp": "2024-01-15T10:31:15.000000",
      "agent": "FrontendAgent",
      "error": "Failed to generate component",
      "details": {}
    }
  ],
  "status": "completed",
  "agents_status": {
    "PromptUnderstandingAgent": {
      "status": "completed",
      "timestamp": "2024-01-15T10:30:48.000000",
      "details": {}
    }
  },
  "execution_log": [
    {
      "timestamp": "2024-01-15T10:30:45.123456",
      "agent": "PromptUnderstandingAgent",
      "message": "Agent initialized",
      "level": "info"
    }
  ]
}
```

---

### 3. Get Generation Status

Get current generation status and agent statuses.

**Endpoint**
```
GET /api/status
```

**Parameters**
None

**Response** (200 OK)
```json
{
  "status": "generating",
  "agents_status": {
    "PromptUnderstandingAgent": {
      "status": "completed",
      "timestamp": "2024-01-15T10:30:48.000000",
      "details": {}
    },
    "ArchitectAgent": {
      "status": "in_progress",
      "timestamp": "2024-01-15T10:30:50.000000",
      "details": {
        "current_step": "Generating API endpoints"
      }
    },
    "FrontendAgent": {
      "status": "pending",
      "timestamp": null,
      "details": {}
    }
  },
  "error_count": 0,
  "errors": []
}
```

---

### 4. Get Execution Logs

Retrieve execution logs with filtering and pagination.

**Endpoint**
```
GET /api/logs
```

**Query Parameters**
- `limit` (integer, optional): Maximum number of logs to return. Default: 50. Max: 1000.

**Response** (200 OK)
```json
{
  "total": 127,
  "logs": [
    {
      "timestamp": "2024-01-15T10:30:45.123456",
      "agent": "PromptUnderstandingAgent",
      "message": "Agent initialized: Parses user prompts and extracts project requirements",
      "level": "info"
    },
    {
      "timestamp": "2024-01-15T10:30:46.234567",
      "agent": "PromptUnderstandingAgent",
      "message": "Analyzing prompt: Create me a jewelry website...",
      "level": "info"
    },
    {
      "timestamp": "2024-01-15T10:30:48.345678",
      "agent": "PromptUnderstandingAgent",
      "message": "Project specification created: ecommerce",
      "level": "info"
    },
    {
      "timestamp": "2024-01-15T10:30:52.456789",
      "agent": "ArchitectAgent",
      "message": "Creating architecture for ecommerce",
      "level": "info"
    },
    {
      "timestamp": "2024-01-15T10:30:53.567890",
      "agent": "ArchitectAgent",
      "message": "Architecture plan created successfully",
      "level": "success"
    }
  ]
}
```

**Log Levels**
- `info`: Information message
- `success`: Successful operation
- `warning`: Warning message
- `error`: Error message

---

### 5. Reset Memory

Reset shared memory to initial state. Useful for testing.

**Endpoint**
```
POST /api/reset
```

**Parameters**
None

**Request Body**
None

**Response** (200 OK)
```json
{
  "message": "Memory reset successfully"
}
```

**Warning**: This will clear all current state. Only use in development.

---

### 6. List Projects

List all generated projects.

**Endpoint**
```
GET /api/projects
```

**Query Parameters**
- `limit` (integer, optional): Maximum number of projects to return. Default: 50.
- `offset` (integer, optional): Number of projects to skip. Default: 0.

**Response** (200 OK)
```json
{
  "projects": [
    {
      "project_id": "550e8400-e29b-41d4-a716-446655440000",
      "project_type": "ecommerce",
      "status": "completed",
      "created_at": "2024-01-15T10:30:45.123456",
      "project_dir": "/home/user/autocoder/generated_projects/550e8400-e29b-41d4-a716-446655440000"
    },
    {
      "project_id": "550e8400-e29b-41d4-a716-446655440001",
      "project_type": "blog",
      "status": "completed",
      "created_at": "2024-01-15T11:45:30.234567",
      "project_dir": "/home/user/autocoder/generated_projects/550e8400-e29b-41d4-a716-446655440001"
    }
  ],
  "total": 2
}
```

---

### 7. Get Project Files

Get file tree structure of a generated project.

**Endpoint**
```
GET /api/projects/{project_id}/files
```

**Path Parameters**
- `project_id` (string, required): UUID of the project

**Response** (200 OK)
```json
{
  "project_id": "550e8400-e29b-41d4-a716-446655440000",
  "files": [
    {
      "path": "frontend",
      "type": "directory",
      "children": [
        {
          "path": "frontend/src",
          "type": "directory",
          "children": [
            {
              "path": "frontend/src/App.tsx",
              "type": "file",
              "size": 2048
            },
            {
              "path": "frontend/src/main.tsx",
              "type": "file",
              "size": 512
            }
          ]
        }
      ]
    },
    {
      "path": "backend",
      "type": "directory",
      "children": [
        {
          "path": "backend/app",
          "type": "directory"
        }
      ]
    }
  ]
}
```

---

### 8. Get File Content

Get the content of a specific file from a generated project.

**Endpoint**
```
GET /api/projects/{project_id}/file
```

**Path Parameters**
- `project_id` (string, required): UUID of the project

**Query Parameters**
- `path` (string, required): Relative path to the file within the project

**Response** (200 OK)
```json
{
  "project_id": "550e8400-e29b-41d4-a716-446655440000",
  "path": "frontend/src/App.tsx",
  "content": "export default function App() {\n  return (\n    <div>\n      <h1>Hello World</h1>\n    </div>\n  );\n}",
  "size": 2048,
  "language": "typescript"
}
```

**Error Response** (404 Not Found)
```json
{
  "detail": "File not found"
}
```

---

### 9. Health Check

Check if API is running.

**Endpoint**
```
GET /health
```

**Response** (200 OK)
```json
{
  "status": "ok",
  "service": "autocoder-api",
  "version": "1.0.0"
}
```

---

### 10. Root Endpoint

Get API information.

**Endpoint**
```
GET /
```

**Response** (200 OK)
```json
{
  "message": "AutoCoder API",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health"
}
```

---

## OpenAPI Documentation

Interactive API documentation available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Rate Limiting

The Groq API client implements built-in rate limiting:

```python
# Configuration in .env
GROQ_REQUEST_INTERVAL_SECONDS=30.0  # Delay between API requests
```

This prevents hitting Groq API rate limits during agent execution.

For HTTP API endpoints, add rate limiting as needed:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/generate")
@limiter.limit("5/minute")
async def generate_project(request):
    ...
```

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/generate")
@limiter.limit("5/minute")
async def generate_project(request):
    ...
```

## CORS Configuration

Current CORS allowed origins:
- http://localhost:5173 (frontend dev)
- http://localhost:3000
- Environment variable: FRONTEND_URL

## Error Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Project generated |
| 400 | Bad Request | Invalid prompt |
| 401 | Unauthorized | No API key |
| 403 | Forbidden | Access denied |
| 404 | Not Found | Project not found |
| 429 | Too Many Requests | Rate limited |
| 500 | Server Error | LLM API failure |
| 503 | Service Unavailable | Database down |

## Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

## Request/Response Examples

### Generate Project Example

**cURL**
```bash
curl -X POST "http://localhost:8000/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a jewelry website with products and shopping cart"
  }'
```

**Python**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/generate",
    json={"prompt": "Create a jewelry website with products and shopping cart"}
)
result = response.json()
print(f"Project ID: {result['project_id']}")
```

**JavaScript**
```javascript
const response = await fetch('http://localhost:8000/api/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    prompt: "Create a jewelry website with products and shopping cart"
  })
});
const result = await response.json();
console.log(`Project ID: ${result.project_id}`);
```

## Webhooks (Future)

Planned webhook support for:
- Generation started
- Generation completed
- Generation failed
- Error occurred

---

## Pagination (Future)

Planned pagination support for:
- Project history
- Execution logs
- Generated artifacts

---

## Batch Operations (Future)

Planned batch endpoints:
- Generate multiple projects
- Batch error recovery
- Bulk exports

---

## Version History

### v1.0.0 (Current)
- Basic project generation
- Shared memory API
- Status and logs endpoints
- No authentication
- No rate limiting

### v1.1.0 (Planned)
- Authentication
- Rate limiting
- Webhook support
- Better error messages
- Project history

### v2.0.0 (Planned)
- Multi-tenancy
- Advanced caching
- Project versioning
- Collaborative editing
- Custom agent support

---

**Note**: This is a beta API. Breaking changes may occur in future versions.
