#!/usr/bin/env bash

# ✅ Universal script is fully compatible:
# (Works in zsh AND bash, macOS AND Ubuntu) without modification.
# create_cineescape.sh 

# nano create_cineescape.sh
# chmod 700 create_cineescape.sh
# ./create_cineescape.sh

# Root folder
PROJECT="CineEscapeApp"

# Create directory structure
mkdir -p "$PROJECT"/instance "$PROJECT"/static "$PROJECT"/templates
touch "$PROJECT"/app.py "$PROJECT"/models.py "$PROJECT"/data_manager.py "$PROJECT"/requirements.txt "$PROJECT"/config.py

# Create files inside subfolders
touch "$PROJECT"/static/style.css
touch "$PROJECT"/templates/base.html "$PROJECT"/templates/index.html "$PROJECT"/templates/movies.html "$PROJECT"/templates/404.html

# Create empty SQLite DB
touch "$PROJECT"/instance/movies.db

# Determine Python version
# Prefer python3.12 if installed, otherwise fall back to python3
if command -v python3.12 >/dev/null 2>&1; then
    PYTHON_BIN="python3.12"
else
    PYTHON_BIN="python3"
fi

# Create virtual environment
cd "$PROJECT" || exit 1
$PYTHON_BIN -m venv .venv

# Optional: upgrade pip inside venv
# Works in both bash and zsh
. .venv/bin/activate
pip install --upgrade pip
deactivate

echo "CineEscapeApp structure created successfully."
