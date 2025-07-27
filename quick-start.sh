#!/bin/bash

echo "🧠 DocuSynth AI - NVIDIA Hackathon Quick Start"
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
print_status "Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is required but not installed"
    exit 1
fi

if ! command -v node &> /dev/null; then
    print_error "Node.js is required but not installed"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    print_error "npm is required but not installed"
    exit 1
fi

print_success "Prerequisites check passed"

# Create sample zip file
print_status "Creating sample data zip file..."
cd sample_data
if command -v zip &> /dev/null; then
    zip -r ../test-project.zip . > /dev/null 2>&1
    print_success "Created test-project.zip"
else
    print_warning "zip command not found, please create test-project.zip manually"
fi
cd ..

# Install backend dependencies
print_status "Installing backend dependencies..."
cd backend
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1
print_success "Backend dependencies installed"
cd ..

# Install frontend dependencies
print_status "Installing frontend dependencies..."
cd frontend
npm install > /dev/null 2>&1
print_success "Frontend dependencies installed"
cd ..

# Start services
print_status "Starting services..."

# Start backend in background
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend in background
cd frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Wait a moment for frontend to start
sleep 5

# Check if services are running
if curl -s http://localhost:8000/health > /dev/null; then
    print_success "Backend is running at http://localhost:8000"
else
    print_error "Backend failed to start"
    exit 1
fi

if curl -s http://localhost:3000 > /dev/null; then
    print_success "Frontend is running at http://localhost:3000"
else
    print_error "Frontend failed to start"
    exit 1
fi

echo ""
echo "🎉 DocuSynth AI is now running!"
echo ""
echo "📱 Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   API Docs: http://localhost:8000/docs"
echo "   Health Check: http://localhost:8000/health"
echo ""
echo "🧪 Demo Instructions:"
echo "   1. Open http://localhost:3000 in your browser"
echo "   2. Upload the test-project.zip file"
echo "   3. Watch the real-time analysis"
echo "   4. Explore the generated documentation"
echo ""
echo "🛑 To stop the services:"
echo "   Press Ctrl+C or run: kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "📋 Logs:"
echo "   Backend: backend.log"
echo "   Frontend: frontend.log"
echo ""

# Function to cleanup on exit
cleanup() {
    print_status "Stopping services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    print_success "Services stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Keep script running
print_status "Services are running. Press Ctrl+C to stop."
while true; do
    sleep 1
done 