# Setup Guide - AutoCoder

Complete step-by-step setup instructions for AutoCoder development environment.

## Prerequisites

### System Requirements

- OS: Windows, macOS, or Linux
- Python: 3.11 or higher
- Node.js: 20 or higher
- npm: 10 or higher
- RAM: 8GB minimum, 16GB recommended

### API Keys

1. **Groq API Key**
   - Create account at https://console.groq.com
   - Get API key from dashboard
   - Keep it secure

## Windows Setup

### 1. Install Python

```powershell
# Check if Python is installed
python --version

# Download and install from: https://www.python.org/downloads/
# During installation, ensure "Add Python to PATH" is checked
```

### 2. Install Node.js

```powershell
# Download and install from: https://nodejs.org/
# Recommended: LTS version

# Verify installation
node --version
npm --version
```

### 3. Clone Repository

```powershell
cd C:\Users\YourName\Documents
git clone https://github.com/yourusername/EdgeCode.git
cd EdgeCode\autocoder
```

### 4. Backend Setup

```powershell
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env

# Edit .env with your GROQ_API_KEY
# Use Notepad or VS Code
notepad .env
```

### 5. Frontend Setup

```powershell
# In a new terminal
cd ..\frontend

# Install dependencies
npm install
```

### 6. Run Development Server

```powershell
# Terminal 1: Backend
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend (new terminal)
cd frontend
npm run dev
```

### 7. Access Application

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## macOS Setup

### 1. Install Python

```bash
# Using Homebrew
brew install python@3.11

# Verify
python3 --version

# Create alias for convenience
alias python=python3
```

### 2. Install Node.js

```bash
# Using Homebrew
brew install node

# Verify
node --version
npm --version
```

### 3. Clone Repository

```bash
cd ~/Documents
git clone https://github.com/yourusername/EdgeCode.git
cd EdgeCode/autocoder
```

### 4. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env

# Edit .env
nano .env
# Add your GROQ_API_KEY
```

### 5. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install
```

### 6. Run Development Server

```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend (new terminal)
cd frontend
npm run dev
```

### 7. Access Application

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Linux Setup

### Ubuntu/Debian

```bash
# Update packages
sudo apt update && sudo apt upgrade

# Install Python
sudo apt install python3.11 python3.11-venv python3-pip

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install nodejs

# Verify
python3 --version
node --version
npm --version
```

### Clone and Setup

```bash
cd ~/projects
git clone https://github.com/yourusername/EdgeCode.git
cd EdgeCode/autocoder

# Backend
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your GROQ_API_KEY

# Frontend
cd ../frontend
npm install

# Run backend
cd ../backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000

# Run frontend (new terminal)
cd frontend
npm run dev
```

---

## Environment Configuration

### Backend (.env)

```bash
# Required
GROQ_API_KEY=your_actual_groq_api_key

# Optional (defaults provided)
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:5173
DEBUG=True
LOG_LEVEL=INFO
GROQ_MODEL=llama-3.1-8b-instant
GROQ_REQUEST_INTERVAL_SECONDS=30.0
PROJECTS_BASE_DIR=./generated_projects
```

### Frontend Environment

Create `frontend/.env.local`:

```bash
VITE_API_URL=http://localhost:8000
VITE_DEBUG=true
```

---

## Testing Setup

### Backend Tests

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_agents.py -v

# With coverage
pytest tests/ --cov=app
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm run test

# Watch mode
npm run test:watch
```

---

## IDE Setup

### VS Code

1. Install extensions:
   - Python (ms-python.python)
   - Pylance (ms-python.vscode-pylance)
   - FastAPI (ms-maturin.fastapi)
   - ES7+ React/Redux/React-Native snippets (dsznajder.es7-react-js-snippets)
   - Tailwind CSS IntelliSense (bradlc.vscode-tailwindcss)

2. Create workspace settings (`.vscode/settings.json`):

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/backend/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "[python]": {
    "editor.formatOnSave": true
  },
  "[typescript]": {
    "editor.formatOnSave": true
  }
}
```

### PyCharm

1. Open project in PyCharm
2. Configure Python interpreter: Settings → Project → Python Interpreter → Add
3. Select venv path: `backend/venv`
4. Mark `backend/app` as Sources Root

---

## Docker Setup (Alternative)

### Using Docker Compose

```bash
cd backend

# Build images
docker-compose build

# Run services
docker-compose up

# Services will be available at:
# Frontend: http://localhost:5173
# Backend: http://localhost:8000
```

---

## Troubleshooting

### Port Already in Use

```bash
# Find process using port
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

### Python Module Not Found

```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### CORS Issues

- Ensure `FRONTEND_URL` in backend `.env` matches frontend URL
- Backend should be on `http://localhost:8000`
- Frontend should be on `http://localhost:5173`

### Groq API Errors

1. Verify API key is correct
2. Check API key has permissions
3. Monitor API rate limits
4. Check network connectivity

### Node Modules Issues

```bash
cd frontend

# Clear cache
npm cache clean --force

# Reinstall
rm -rf node_modules package-lock.json
npm install
```

---

## First Run Checklist

- [ ] Python 3.11+ installed
- [ ] Node.js 20+ installed
- [ ] Repository cloned
- [ ] Backend virtual environment created and activated
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] `.env` files configured with Groq API key
- [ ] Backend running on localhost:8000
- [ ] Frontend running on localhost:5173
- [ ] Can access http://localhost:5173
- [ ] Can generate a project

---

## Next Steps

1. **Try a Project Generation**
   - Go to http://localhost:5173
   - Enter prompt: "Create me a jewelry website"
   - Watch agents work in real-time

2. **Explore the API**
   - Visit http://localhost:8000/docs
   - Try generating a project via OpenAPI UI

3. **Check Generated Projects**
   - Look in `backend/generated_projects/`
   - Each project has its own README

4. **Read Documentation**
   - [Architecture Guide](./docs/ARCHITECTURE.md)
   - [Agent Development](./docs/AGENT_DEVELOPMENT.md)
   - [API Reference](./docs/API.md)

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review error logs in the UI
3. Check backend console output
4. Verify environment configuration

---

**Last Updated**: 2024
