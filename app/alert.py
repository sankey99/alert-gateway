import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

from dotenv import load_dotenv
import json, os

from dotenv import load_dotenv
import json, os
if os.getenv("FLY_APP_NAME") is None:  # Check if running locally
    load_dotenv()

raw_subscriptions = os.getenv("SUBSCRIPTIONS")
logger.info(f"raw_subscriptions: {raw_subscriptions}")
if raw_subscriptions:
    try:
        unescaped_subscriptions = raw_subscriptions.replace('\\"', '"')
        logger.info(f"unescaped_subscriptions: {unescaped_subscriptions}")
        subscription_map = json.loads(unescaped_subscriptions)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse SUBSCRIPTIONS: {e}")
        subscription_map = {}
else:
    logger.error("SUBSCRIPTIONS environment variable is not set!")
    subscription_map = {}

from fastapi import FastAPI, Request, HTTPException
from twilio.rest import Client

app = FastAPI()


async def send_alert(data):
    subscriber = data.get("id")

    if subscriber not in subscription_map:
        logger.error(f"unknow subscriber : {subscriber}")
        raise HTTPException(status_code=400, detail=f"Unknown client id: {subscriber}")

    print("subscriber: " + str(subscriber))
    account_info = subscription_map[subscriber]
    body = data.get("message", "Default alert triggered.")

    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_phone = account_info["from"]
    to_phone = account_info["to"]
    # print("accoung_sid" + str(account_sid))
    # print("auth_token" + str(auth_token))
    client = Client(account_sid, auth_token)
    logger.info(f"sending alert for subscriber: {subscriber} message: {body}")

    message = client.messages.create(
        from_=from_phone,
        body=body,
        to=to_phone
    )

    print(message.sid)

    # async with httpx.AsyncClient() as client:
    #     response = await client.post(
    #         f"https://api.twilio.com/2010-04-01/Accounts/{os.getenv('TWILIO_ACCOUNT_SID')}/Messages.json",
    #         auth=(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN")),
    #         data={
    #             "To": to,
    #             "From": os.getenv("TWILIO_FROM"),
    #             "Body": body
    #         }
    #     )
    return message.sid  # {"status": response.status_code, "twilio_response": response.text}
