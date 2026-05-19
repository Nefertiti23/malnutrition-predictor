#!/bin/bash
# Detect and run the right start command for your project

if [ -f "package.json" ]; then
    # Node.js project
    npm start
elif [ -f "app.py" ] || [ -f "main.py" ]; then
    # Python project
    python app.py || python main.py
elif [ -f "requirements.txt" ]; then
    # Python with requirements but no main file
    pip install -r requirements.txt
    python app.py 2>/dev/null || python main.py 2>/dev/null
else
    echo "No recognized project type found"
    exit 1
fi