#!/bin/bash

echo "🚀 Deploying DocuSynth AI to NVIDIA Brev with GPU Acceleration"
echo "💰 Using your $20 GPU credits for optimal performance"
echo "=" * 60

# Check if brev CLI is installed
if ! command -v brev &> /dev/null; then
    echo "❌ Brev CLI not found. Installing..."
    curl -fsSL https://brev.sh/install.sh | bash
    source ~/.bashrc
fi

# Check if user is logged in
if ! brev whoami &> /dev/null; then
    echo "🔐 Please log in to Brev:"
    brev login
fi

echo "📊 Current Brev balance:"
brev billing

echo ""
echo "🎯 Deploying with GPU configuration:"
echo "   - GPU: NVIDIA L40S (48GB VRAM)"
echo "   - RAM: 294GB"
echo "   - CPUs: 16"
echo "   - Cost: ~$3.48/hour"
echo "   - Estimated runtime: ~5-6 hours with $20 credits"

echo ""
echo "🚀 Starting deployment..."
echo "   This will create a launchable that others can deploy too!"

# Deploy the project
brev deploy

echo ""
echo "✅ Deployment initiated!"
echo ""
echo "📋 Next steps:"
echo "   1. Wait for deployment to complete (2-3 minutes)"
echo "   2. Access your app at the provided URL"
echo "   3. Upload code files to test the AI documentation"
echo "   4. Share the launchable URL with others"
echo ""
echo "💡 Tips for demo:"
echo "   - Upload a Python/JavaScript project"
echo "   - Show the intelligent documentation generation"
echo "   - Highlight the multi-agent architecture"
echo "   - Demonstrate the GPU-accelerated AI responses" 