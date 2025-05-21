import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to the path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Determine which framework to use based on environment variable
# Default to FastAPI if not specified
FRAMEWORK = os.getenv("FRAMEWORK", "fastapi").lower()

if FRAMEWORK == "nicegui":
    from app.frontend.nicegui_app import ui
    
    if __name__ == "__main__":
        ui.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
else:
    # Default to FastAPI
    from app import app
    import uvicorn

    if __name__ == "__main__":
        uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)