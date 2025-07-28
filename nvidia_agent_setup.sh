#!/bin/bash

# 🚀 NVIDIA Agent Setup Script for DocuSynth AI
# Run this in your deployed NVIDIA agent environment

echo "🚀 Setting up DocuSynth AI in NVIDIA Agent Environment..."

# Step 1: Clone the repository
echo "📥 Cloning DocuSynth AI repository..."
git clone https://github.com/rmahesh2003/nvidiahackathon.git
cd nvidiahackathon

# Step 2: Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r backend/requirements.txt

# Step 3: Install Node.js dependencies (if needed)
echo "📦 Installing Node.js dependencies..."
cd frontend
npm install
cd ..

# Step 4: Create demo data
echo "📁 Creating demo data..."
cd sample_data
zip -r ../demo_codebase.zip .
cd ..

# Step 5: Start the application
echo "🚀 Starting DocuSynth AI..."
echo ""
echo "✅ Setup complete!"
echo ""
echo "🌐 Access your application:"
echo "   Backend API: http://localhost:8000"
echo "   Frontend UI: http://localhost:3000"
echo ""
echo "📋 Demo steps:"
echo "   1. Open http://localhost:3000"
echo "   2. Upload demo_codebase.zip"
echo "   3. Watch the AI agents analyze your code!"
echo ""
echo "🎯 Ready for your 3-minute presentation!"

# Start the backend in background
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Start the frontend in background
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo "🔄 Services started! Press Ctrl+C to stop."
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"

# Wait for user to stop
trap "echo '🛑 Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait 