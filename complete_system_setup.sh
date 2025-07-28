#!/bin/bash

echo "🚀 Setting up DocuSynth AI - Complete Multi-Agent System"
echo "========================================================"

# Install all dependencies
echo "📦 Installing Python dependencies..."
pip install fastapi uvicorn python-multipart pydantic langchain langchain-community langchain-core requests beautifulsoup4

# Create demo zip
echo "📁 Creating demo data..."
cd sample_data
zip -r ../demo_codebase.zip .
cd ..

# Start the complete backend
echo "🚀 Starting DocuSynth AI Complete System..."
cd backend
python3 -m uvicorn app.main_complete:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

echo ""
echo "✅ Complete System is ready!"
echo ""
echo "🌐 Access your application:"
echo "   API: http://204.52.27.91:8000"
echo "   Docs: http://204.52.27.91:8000/docs"
echo ""
echo "🎯 Features Available:"
echo "   ✅ Real AI Agents (InternalDocAgent, LibraryDocAgent, ContextManagerAgent)"
echo "   ✅ Nemotron Integration (simulated with sophisticated reasoning)"
echo "   ✅ Real File Parsing (extracts and analyzes actual files)"
echo "   ✅ Agent Status Tracking (real-time progress updates)"
echo "   ✅ Frontend UI (React with drag-and-drop)"
echo ""
echo "📋 Test Commands:"
echo "   curl -X POST http://204.52.27.91:8000/upload -F 'file=@demo_codebase.zip'"
echo "   curl -X POST http://204.52.27.91:8000/analyze/upload_1"
echo "   curl -X GET http://204.52.27.91:8000/analyze/upload_1"
echo ""
echo "🎯 Perfect for your 3-minute presentation!"

# Wait for user to stop
trap "echo '🛑 Stopping complete system...'; kill $BACKEND_PID; exit" INT
wait 