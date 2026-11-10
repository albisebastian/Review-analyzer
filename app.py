"""Start the Customer Review Analyzer:  python app.py

Opens the web app at http://127.0.0.1:8000
Options (environment variables):  HOST, PORT, MODEL_PATH, LEXICON_BLEND
"""
import os

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", "8000")),
        log_level="info",
    )
