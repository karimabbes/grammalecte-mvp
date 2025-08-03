#!/usr/bin/env python3
"""
Render startup script for the Grammalecte FastAPI application
"""

import os
import uvicorn

if __name__ == "__main__":
    # Get port from Render environment variable, default to 8000
    port = int(os.environ.get("PORT", 8000))
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",  # Bind to all interfaces for Render
        port=port,
        reload=False,  # Disable reload in production
        log_level="info"
    ) 