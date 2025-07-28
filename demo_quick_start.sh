#!/bin/bash

echo "🚀 DocuSynth AI - Quick Demo Setup"
echo "=================================="

# Install minimal dependencies
echo "📦 Installing dependencies..."
pip install fastapi uvicorn python-multipart

# Create demo zip
echo "📁 Creating demo data..."
cd sample_data
zip -r ../demo_codebase.zip .
cd ..

# Start the simplified backend
echo "🚀 Starting DocuSynth AI backend..."
cd backend
python -m uvicorn app.main_simple:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

echo ""
echo "✅ Demo is ready!"
echo ""
echo "🌐 Access your API:"
echo "   API: http://localhost:8000"
echo "   Docs: http://localhost:8000/docs"
echo ""
echo "📋 Demo steps:"
echo "   1. Open http://localhost:8000/docs"
echo "   2. Upload demo_codebase.zip"
echo "   3. Start analysis"
echo "   4. Get results!"
echo ""
echo "🎯 Perfect for your 3-minute presentation!"

# Wait for user to stop
trap "echo '🛑 Stopping demo...'; kill $BACKEND_PID; exit" INT
wait 