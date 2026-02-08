from dotenv import load_dotenv
import os   

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMINS = os.getenv("ADMINS", "")
if ADMINS:
    ADMINS = [int(admin) for admin in ADMINS.split(",")]
else:
    ADMINS = []

CARD_NUMBER = os.getenv("CARD_NUMBER")
CARD_OWNER = os.getenv("CARD_OWNER")
SUBSCRIPTION_PRICE = int(os.getenv("SUBSCRIPTION_PRICE", 0))