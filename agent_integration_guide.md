# 🚀 DocuSynth AI - NVIDIA Agent Integration Guide

## **Quick Setup for 2-Hour Hackathon**

### **Step 1: Access Your Deployed Agent Environment**
- Navigate to your deployed instance on `brev.nvidia.com`
- Access Jupyter notebook on port 8888
- You'll have the "build-an-agent" environment ready

### **Step 2: Clone Your Repository**
```bash
git clone https://github.com/rmahesh2003/nvidiahackathon.git
cd nvidiahackathon
```

### **Step 3: Install Dependencies**
```bash
# Backend dependencies
pip install -r backend/requirements.txt

# Frontend dependencies (if needed)
npm install --prefix frontend
```

### **Step 4: Configure Nemotron Integration**

Replace the mock LLM in `backend/app/agents/internal_doc_agent.py`:

```python
# Replace MockNeMoLLM with real Nemotron
from nemo.collections.nlp.models import get_pretrained_model

class NemotronLLM:
    def __init__(self):
        self.model = get_pretrained_model("llama-3.3-nemotron-super-49b-v1")
    
    def generate(self, prompt):
        # Use your model endpoint from build.nvidia.com/models
        return self.model.generate(prompt)
```

### **Step 5: Update Agent Configuration**

In `backend/app/agents/internal_doc_agent.py`:
```python
# Replace MockNeMoLLM with NemotronLLM
self.llm = NemotronLLM()
```

### **Step 6: Test Your Agent**

```bash
# Start the backend
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000

# In another terminal, start frontend
cd frontend
npm run dev
```

### **Step 7: Demo Your Agent**

1. **Upload a codebase** (zip file)
2. **Watch agents analyze**:
   - InternalDocAgent generates documentation
   - LibraryDocAgent fetches external docs
   - ContextManagerAgent builds cross-references
3. **Export results** as JSON

## **Key Features to Highlight:**

### **✅ Agent Intelligence**
- **Multi-agent orchestration** with LangChain
- **Nemotron reasoning** for code understanding
- **Proactive documentation** generation

### **✅ Real-World Application**
- **Team onboarding** - New developers understand codebase instantly
- **Documentation automation** - No more manual doc writing
- **Knowledge persistence** - Exportable insights

### **✅ Technical Innovation**
- **NVIDIA NeMo Agent Toolkit** integration
- **GPU-accelerated** code analysis
- **Cross-language support** (Python, JavaScript, TypeScript)

## **Presentation Script (3 minutes):**

### **"What Problem Does This Solve?"**
"Developers spend 40% of their time understanding code. DocuSynth AI eliminates this with AI agents that automatically document and explain any codebase."

### **"How Does It Work?"**
"Upload any codebase, and our three AI agents work together: one analyzes code structure, another fetches library documentation, and a third builds cross-references."

### **"What Makes It Special?"**
"Unlike existing tools, this creates a complete knowledge base - not just code help, but team-wide understanding that persists and scales."

### **"Technical Innovation?"**
"Leverages NVIDIA's Nemotron for reasoning, NeMo Agent Toolkit for orchestration, and GPU acceleration for real-time analysis."

## **Judging Criteria Alignment:**

### **✅ Creativity (5/5)**
- Multi-agent approach for code intelligence
- Proactive documentation vs reactive help

### **✅ Functionality (5/5)**
- Live demo with real codebases
- Exportable JSON results
- Cross-language support

### **✅ Scope of Completion (5/5)**
- Full-stack application
- Beautiful UI with Tailwind CSS
- Complete API with FastAPI

### **✅ Presentation (5/5)**
- Clear problem statement
- Live demonstration
- Technical depth explanation

### **✅ NVIDIA Tools (5/5)**
- Nemotron reasoning model
- NeMo Agent Toolkit
- GPU-accelerated processing

## **Quick Commands for Demo:**

```bash
# Create sample zip for demo
cd sample_data
zip -r ../demo_codebase.zip .
cd ..

# Start the full stack
./quick-start.sh

# Access the app
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

## **Submission Checklist:**

- [ ] Agent deployed and running
- [ ] Live demo working
- [ ] Code uploaded to GitHub
- [ ] Presentation script ready
- [ ] Shareable project link created

**Time Remaining: Focus on the demo and presentation!** ⏰ 