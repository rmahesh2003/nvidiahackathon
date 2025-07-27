#!/bin/bash

echo "🚀 Setting up DocuSynth AI..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3.8+"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed. Please install Node.js 16+"
    exit 1
fi

echo "📦 Installing backend dependencies..."
cd backend
python3 -m pip install -r requirements.txt
cd ..

echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo "✅ Dependencies installed successfully!"

echo ""
echo "🎯 To start the application:"
echo ""
echo "1. Start the backend server:"
echo "   cd backend && python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "2. In a new terminal, start the frontend:"
echo "   cd frontend && npm run dev"
echo ""
echo "3. Open your browser to:"
echo "   http://localhost:3000"
echo ""
echo "4. API documentation available at:"
echo "   http://localhost:8000/docs"
echo ""
echo "🧪 To test with sample data:"
echo "   Create a zip file containing the sample_data/ files and upload it through the web interface"
echo ""
echo "🎉 Happy coding!" 