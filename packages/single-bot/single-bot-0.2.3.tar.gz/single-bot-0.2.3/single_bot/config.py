from dotenv import load_dotenv, find_dotenv
import os


load_dotenv(find_dotenv(), override=True)

# SINGLE_BOT_DATABASE_URL = os.getenv("SINGLE_BOT_DATABASE_URL")

SINGLE_BOT_DATABASE_PATH = os.getenv("SINGLE_BOT_DATABASE_PATH")
