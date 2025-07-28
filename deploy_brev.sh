#!/bin/bash

echo "🚀 Deploying DocuSynth AI to NVIDIA Brev"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Check if brev CLI is installed
if ! command -v brev &> /dev/null; then
    print_error "Brev CLI is not installed. Please install it first:"
    echo "  npm install -g @brev/cli"
    echo "  brev login"
    exit 1
fi

# Check if user is logged in to Brev
if ! brev whoami &> /dev/null; then
    print_error "Not logged in to Brev. Please run:"
    echo "  brev login"
    exit 1
fi

print_status "Checking GPU availability..."
gpu_info=$(brev gpu list 2>/dev/null)
if [ $? -eq 0 ]; then
    print_success "GPU resources available"
else
    print_warning "GPU resources may not be available. Check your Brev account."
fi

print_status "Preparing deployment..."
print_status "Model: NVIDIA Nemotron Super 49B"
print_status "GPU: A100 with 24GB memory"
print_status "Port: 8000"

# Deploy the launchable
print_status "Deploying to Brev..."
if brev deploy; then
    print_success "Deployment successful!"
    echo ""
    echo "🎉 DocuSynth AI is now deployed on NVIDIA Brev!"
    echo ""
    echo "📱 Access your application:"
    echo "  - Frontend: https://your-deployment-url.brev.dev"
    echo "  - API Docs: https://your-deployment-url.brev.dev/docs"
    echo "  - Health Check: https://your-deployment-url.brev.dev/health"
    echo ""
    echo "🧠 AI Model: NVIDIA Nemotron Super 49B"
    echo "⚡ GPU: A100 with 24GB memory"
    echo "🚀 Ready for hackathon demo!"
    echo ""
    echo "💡 Tips:"
    echo "  - Upload a zip file with your codebase"
    echo "  - Watch real-time AI analysis"
    echo "  - Explore intelligent documentation"
    echo "  - Share the launchable with others"
else
    print_error "Deployment failed. Check your Brev account and try again."
    exit 1
fi 