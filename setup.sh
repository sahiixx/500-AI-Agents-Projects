#!/bin/bash
# Setup script for 500-AI-Agents-Projects
# Compatible with Python 3.11.14+

set -e

echo "================================================"
echo "500-AI-Agents-Projects Setup Script"
echo "================================================"
echo ""

# Check Python version
echo "1. Checking Python version..."
PYTHON_CMD=""
if command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
    echo "✓ Found Python 3.11: $(python3.11 --version)"
elif command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | grep -oP '\d+\.\d+')
    if [[ $(echo "$PYTHON_VERSION >= 3.11" | bc) -eq 1 ]]; then
        PYTHON_CMD="python3"
        echo "✓ Found Python 3: $(python3 --version)"
    else
        echo "✗ Python 3.11+ is required, found $PYTHON_VERSION"
        exit 1
    fi
else
    echo "✗ Python 3.11+ not found"
    exit 1
fi

# Verify pip is available
echo ""
echo "2. Checking pip..."
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    echo "Installing pip..."
    $PYTHON_CMD -m ensurepip --default-pip
fi
echo "✓ pip is available: $($PYTHON_CMD -m pip --version)"

# Install dependencies
echo ""
echo "3. Installing dependencies from requirements.txt..."
$PYTHON_CMD -m pip install -r requirements.txt --quiet
echo "✓ All dependencies installed successfully"

# Verify key packages
echo ""
echo "4. Verifying key packages..."
$PYTHON_CMD -c "
import crewai
import langchain
import pandas
import numpy
import pytest
print('✓ CrewAI')
print('✓ LangChain')
print('✓ Pandas')
print('✓ NumPy')
print('✓ Pytest')
"

# Verify project modules
echo ""
echo "5. Verifying project modules..."
$PYTHON_CMD -c "
import sys
sys.path.insert(0, '.')
from dubai_real_estate_workflow.tools import (
    LinkedInScraperTool,
    ContactVerificationTool,
    GoogleSheetsTool
)
print('✓ Dubai workflow tools import successfully')
" 2>&1 | grep -v "UserWarning" | grep -v "pkg_resources" | grep -v "Mixing V1" || true

# Run tests
echo ""
echo "6. Running test suite..."
$PYTHON_CMD -m pytest tests/ -q --tb=no
echo "✓ All tests passed"

echo ""
echo "================================================"
echo "Setup completed successfully!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Copy .env.example files and configure with your API keys"
echo "2. Run tests: $PYTHON_CMD -m pytest tests/ -v"
echo "3. Run with coverage: $PYTHON_CMD -m pytest tests/ --cov=. --cov-report=term-missing"
echo ""
