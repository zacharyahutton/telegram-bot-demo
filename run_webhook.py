import uvicorn

from api.webhook_server import app
from bot.config import settings

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.port)
