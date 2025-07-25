#!/bin/bash

# Build script for Render deployment
echo "Installing Python dependencies with binary wheels only..."

# Install dependencies with flags to prefer/force binary wheels
pip install --upgrade pip
pip install --only-binary=all --find-links https://download.pytorch.org/whl/torch_stable.html -r requirements.txt

echo "Build completed successfully!"
