import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


file_handler = logging.FileHandler("./single_bot.log", encoding="utf-8")
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
