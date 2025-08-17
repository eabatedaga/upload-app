#!/bin/bash

# AWS Amplify File Upload Application - Deployment Script
# This script automates the deployment process

set -e  # Exit on any error

echo "🚀 AWS Amplify File Upload Application Deployment"
echo "=================================================="

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "   python3 -m venv .venv"
    echo "   source .venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Check if AWS CLI is configured
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo "❌ AWS CLI not configured. Please run 'aws configure' first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Activate virtual environment
source .venv/bin/activate

echo "📦 Installing frontend dependencies..."
cd file-upload-frontend
if command -v pnpm &> /dev/null; then
    pnpm install
else
    npm install
fi
cd ..

echo "🔨 Synthesizing CDK template..."
cdk synth

echo "🚀 Deploying CDK stack..."
cdk deploy --require-approval never

echo "⚙️  Setting up environment variables..."
python3 setup-env.py

echo "🧪 Testing local build..."
cd file-upload-frontend
if command -v pnpm &> /dev/null; then
    pnpm run build
else
    npm run build
fi
cd ..

echo ""
echo "✅ Deployment completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Test locally: cd file-upload-frontend && npm run dev"
echo "2. Open http://localhost:5173 in your browser"
echo "3. Create an account and test file uploads"
echo ""
echo "📚 For production deployment, see README.md"
echo ""

