import logging
import sys

from bot import Logging, bot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    Logging.configure_logging()

    try:
        logging.info("Loading extensions...")
        bot.load_extensions_from("./ext", recursive=True)
        logging.info("Attempting to run bot")
        bot.run()
    except Exception as e:
        logger.error(f"An error occurred while running the bot: {e}")
        sys.exit(1)
