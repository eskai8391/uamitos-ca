import uvicorn
import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/api_server.log", mode="a")
    ]
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting API server on http://localhost:8000")
    logger.info("Press Ctrl+C to stop the server")
    uvicorn.run(
        "main:api", 
        host="0.0.0.0", 
        port=8000, 
        reload=True, 
        log_level="info"
    )