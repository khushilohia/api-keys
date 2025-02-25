#!/bin/bash

#!/bin/bash

# Install dependencies (if not already installed)
pip install --no-cache-dir -r requirements.txt

# Start the FastAPI server
uvicorn app:app --host=0.0.0.0 --port=10000

