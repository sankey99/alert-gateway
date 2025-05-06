import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


from fastapi import FastAPI, Request, HTTPException

app = FastAPI()
from app.alert import send_alert


@app.post("/alert")
async def alert_proxy(request: Request):
    data = await request.json()
    logger.info(f"Received alert data: {data}")
    try:
        response = await send_alert(data)
        logger.info(f"Alert sent successfully: {response}")
        return {"status": "success"}
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Failed to send alert")


@app.get("/health")
def health():
    return {"status": "ok"}
