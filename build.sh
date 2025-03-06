#!/usr/bin/env bash
# Exit on first error
set -o errexit

# Install system dependencies if needed
if ! command -v cargo &> /dev/null
then
    echo "Installing Rust..."
    curl https://sh.rustup.rs -sSf | sh -s -- -y
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
