# 🧠 DocuSynth AI

> **Multi-agent code intelligence system** that auto-generates internal and external documentation, *proactively* summarizes unfamiliar code, and offers relevant insights across a team codebase — powered by NVIDIA NeMo + LangChain + Nemotron.

## 🎯 Project Overview

DocuSynth AI is a sophisticated multi-agent system that automatically analyzes codebases to generate comprehensive documentation. It combines NVIDIA's NeMo framework with LangChain to create intelligent agents that:

- **InternalDocAgent**: Analyzes code structure and generates function-level documentation
- **LibraryDocAgent**: Identifies external dependencies and fetches relevant documentation
- **ContextManagerAgent**: Maintains cross-file context and usage patterns

## 🏗️ Architecture

```
                      +---------------------------+
                      |   🌐 Frontend (Next.js)   |
                      |  - Upload codebase (.zip) |
                      |  - Show output            |
                      +------------+--------------+
                                   |
                    POST /upload   ↓
                    GET /summary
         +-----------------------------+
         |  🧠 Backend (FastAPI)      |
         |                             |
         |   - NeMo Agent Orchestration|
         |   - LangChain Tools         |
         |   - File parsing / indexing |
         +-----------------------------+
                     ↓
         +------------------------------+
         |     🔀 NeMo Agents System     |
         |                              |
         |  - InternalDocAgent          |
         |  - LibraryDocAgent           |
         |  - ContextMemoryAgent        |
         +------------------------------+
                     ↓
         +------------------------------+
         |  📄 Output JSON / UI Viewer   |
         +------------------------------+
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- NVIDIA GPU (optional, for local NeMo inference)

### Installation

1. **Clone and setup backend:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Setup frontend:**
```bash
cd frontend
npm install
```

3. **Run the application:**
```bash
# Terminal 1 - Backend
cd backend
uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

## 📁 Project Structure

```
docusynth-ai/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── internal_doc_agent.py
│   │   │   ├── library_doc_agent.py
│   │   │   └── context_manager_agent.py
│   │   ├── core/
│   │   │   ├── file_parser.py
│   │   │   └── code_analyzer.py
│   │   ├── models/
│   │   │   └── schemas.py
│   │   └── main.py
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── utils/
│   ├── package.json
│   └── README.md
├── sample_data/
│   └── react-project.zip
└── README.md
```

## 🧰 Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | Next.js + React | Modern UI for file upload and results display |
| **Backend** | FastAPI | High-performance API with automatic docs |
| **AI Agents** | NVIDIA NeMo + LangChain | Multi-agent reasoning and orchestration |
| **LLM** | Nemotron | Code understanding and documentation generation |
| **Code Parsing** | tree-sitter | AST parsing for code structure analysis |
| **Documentation** | requests + BeautifulSoup | Fetching external library docs |
| **Deployment** | Vercel + Railway | Easy deployment and scaling |

## 📊 Output Format

The system generates structured JSON output:

```json
{
  "files": [
    {
      "filename": "SearchBar.js",
      "summary": "Handles user input with debounce. Used in X and Y.",
      "functions": [
        {
          "name": "handleChange",
          "doc": "Updates the query state using a debounced input",
          "parameters": ["event"],
          "returns": "void"
        }
      ],
      "external_libraries": [
        {
          "name": "lodash.debounce",
          "doc_summary": "Delays function execution to limit API calls",
          "link": "https://lodash.com/docs/#debounce"
        }
      ],
      "cross_references": [
        {
          "function": "handleChange",
          "used_in": ["SearchResults.js", "FilterPanel.js"]
        }
      ]
    }
  ],
  "project_summary": "React-based search application with debounced input handling",
  "total_files": 15,
  "libraries_used": ["lodash", "react", "axios"]
}
```

## ⚡ 4-Hour Build Plan

| Time | Task | Status |
|------|------|--------|
| 0:00–0:30 | Frontend: File upload + JSON display | ⏳ |
| 0:30–1:15 | Backend: API + file parsing | ⏳ |
| 1:15–2:00 | InternalDocAgent implementation | ⏳ |
| 2:00–2:30 | LibraryDocAgent implementation | ⏳ |
| 2:30–3:00 | Agent orchestration | ⏳ |
| 3:00–3:30 | UI integration and testing | ⏳ |
| 3:30–4:00 | Deployment and polish | ⏳ |

## 🌟 Features

### ✅ Core Features
- [ ] Multi-file codebase analysis
- [ ] Function-level documentation generation
- [ ] External library documentation fetching
- [ ] Cross-reference detection
- [ ] Structured JSON output
- [ ] Modern web interface

### 🚀 Future Extensions
- [ ] GitHub repository integration
- [ ] Slack/Discord bot integration
- [ ] Inline PR comment generation
- [ ] Markdown export functionality
- [ ] Semantic code Q&A with vector DB
- [ ] Real-time collaboration features

## 🤝 Contributing

This is a hackathon project built for the NVIDIA AI hackathon. Feel free to fork and extend!

## 📄 License

MIT License - see LICENSE file for details.

---

**Built with ❤️ for the NVIDIA AI Hackathon** 