#!/bin/bash

# Install dependencies
pip install --no-cache-dir -r requirements.txt

# Use Render's assigned PORT (default is 10000 but Render may assign a different one)
uvicorn app:app --host=0.0.0.0 --port=${PORT:-10000}
