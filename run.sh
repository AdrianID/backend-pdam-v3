#!/bin/bash

echo "🧹 Cleaning Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
find . -type f -name "*.pyo" -delete 2>/dev/null
find . -type f -name "*.pyd" -delete 2>/dev/null

echo "🚀 Setting Python path and starting server..."
export PYTHONPATH="${PWD}"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 