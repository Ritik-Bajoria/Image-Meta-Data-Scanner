from app import app
import os
from utils.logger import Logger

logger=Logger()
if __name__ == "__main__":
    port = os.getenv('PORT',5000)
    host = os.getenv('HOST','0.0.0.0')
    app.run(host=host,port=port)
    logger.info(f"server is listenting at {host}:{port}")