# DocuSynth AI Backend

The backend service for DocuSynth AI, providing a FastAPI-based REST API with multi-agent code analysis capabilities.

## 🏗️ Architecture

The backend consists of three main agents:

### 1. InternalDocAgent
- Analyzes code structure and generates function-level documentation
- Uses AST parsing for Python and regex patterns for JavaScript/React
- Generates natural language descriptions of functions and files

### 2. LibraryDocAgent
- Identifies external dependencies and fetches documentation
- Supports npm, PyPI, and browser APIs
- Provides links to official documentation

### 3. ContextManagerAgent
- Maintains cross-file context and usage patterns
- Tracks function usage across files
- Generates project summaries and statistics

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Start the server:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

3. **Access the API:**
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## 📡 API Endpoints

### POST /upload
Upload a zip file containing codebase for analysis.

**Request:**
- Content-Type: multipart/form-data
- Body: zip file

**Response:**
```json
{
  "message": "File uploaded successfully",
  "upload_id": "uuid-string",
  "file_count": 15
}
```

### POST /analyze/{upload_id}
Start analysis of uploaded codebase.

**Response:**
```json
{
  "status": "started",
  "progress": 0.0,
  "result": null
}
```

### GET /analyze/{upload_id}
Get analysis results.

**Response:**
```json
{
  "status": "completed",
  "progress": 1.0,
  "result": {
    "files": [...],
    "project_summary": "...",
    "total_files": 15,
    "libraries_used": ["react", "lodash"],
    "analysis_time": 2.5
  }
}
```

### GET /status/{upload_id}
Get current agent status and progress.

**Response:**
```json
{
  "internal_doc_agent": "completed",
  "library_doc_agent": "active",
  "context_manager_agent": "active",
  "overall_progress": 0.75
}
```

### GET /health
Health check endpoint.

## 🧪 Testing

### Using Sample Data

1. Create a zip file containing the sample files:
```bash
cd sample_data
zip -r ../test-project.zip .
cd ..
```

2. Upload the zip file through the web interface or using curl:
```bash
curl -X POST "http://localhost:8000/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test-project.zip"
```

3. Start analysis:
```bash
curl -X POST "http://localhost:8000/analyze/{upload_id}"
```

4. Check results:
```bash
curl "http://localhost:8000/analyze/{upload_id}"
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true

# NeMo Configuration (for production)
NEMO_MODEL_PATH=/path/to/nemo/model
NEMO_DEVICE=cuda  # or cpu

# LangChain Configuration
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your-api-key
```

## 🏗️ Development

### Project Structure
```
backend/
├── app/
│   ├── agents/
│   │   ├── internal_doc_agent.py
│   │   ├── library_doc_agent.py
│   │   └── context_manager_agent.py
│   ├── core/
│   │   └── file_parser.py
│   ├── models/
│   │   └── schemas.py
│   └── main.py
├── requirements.txt
└── README.md
```

### Adding New Agents

1. Create a new agent class in `app/agents/`
2. Implement the required methods
3. Add the agent to the main analysis pipeline in `main.py`
4. Update the agent status tracking

### Extending File Support

1. Add new file extensions to `FileParser.supported_extensions`
2. Implement parsing logic in `FileParser.parse_file()`
3. Update the `get_file_type()` method

## 🚀 Production Deployment

### Using Docker

1. Create a Dockerfile:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. Build and run:
```bash
docker build -t docusynth-backend .
docker run -p 8000:8000 docusynth-backend
```

### Using Railway/Heroku

1. Add a `Procfile`:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

2. Deploy to your preferred platform

## 🔍 Monitoring

### Health Checks
The `/health` endpoint provides basic health information:
```json
{
  "status": "healthy",
  "timestamp": 1234567890.123,
  "active_uploads": 5
}
```

### Logging
Enable detailed logging by setting the log level:
```bash
uvicorn app.main:app --log-level debug
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details. 