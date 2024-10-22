import datetime
import glob
import logging
import os
import time
from logging.handlers import TimedRotatingFileHandler

import config_reader as config
import hikari
import lightbulb


# Initializing Bot
class Bot(lightbulb.BotApp):
    def __init__(self) -> None:
        super().__init__(
            token=config.Bot.token,
            default_enabled_guilds=(config.Bot.server),
            intents=hikari.Intents.ALL,
        )


bot = Bot()

logging.basicConfig(level=logging.DEBUG)  # Set the default logging level
logger = logging.getLogger(__name__)


class Logging:
    """
    A class used for the bots logging.
    """

    class LoggingExcludeFilter(logging.Filter):
        pass
        # def filter(self, record):
        #    # Suppress log message from google-api-python-client
        #    if ("file_cache is only supported with oauth2client<4.0.0" in record.getMessage() or
        #        "ssl.PROTOCOL_TLS is deprecated" in record.getMessage()):
        #        return False
        #    return True

    def configure_logging():
        """
        Setting up logging settings
        """

        # Cleaning up console
        suppressed = [
            "googleapicliet.discovery_cache",
            "lightbulb.internal",
            "hikari.gateway",
            "lightbulb.app",
        ]
        for pack_logger in suppressed:
            logging.getLogger(pack_logger).setLevel(logging.ERROR)

        latest_file_handler = logging.FileHandler(
            os.path.join(config.Paths.logs_folder, "latest.log")
        )
        latest_file_handler.setLevel(logging.DEBUG)

        # Create a TimedRotatingFileHandler to create log files with timestamps (e.g., 2024-05-03_12-00-00.log)
        filename = os.path.join(
            config.Paths.logs_folder,
            f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log",
        )
        time_file_handler = TimedRotatingFileHandler(
            filename=filename, when="midnight", interval=1, backupCount=7
        )
        time_file_handler.setLevel(
            logging.DEBUG
        )  # Set the logging level for the file handler

        # Create a formatter to specify the log message format
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Attach the formatter to each file handler
        latest_file_handler.setFormatter(formatter)
        time_file_handler.setFormatter(formatter)

        # Add the custom filter to the handlers
        exclude_filter = Logging.LoggingExcludeFilter()
        latest_file_handler.addFilter(exclude_filter)
        time_file_handler.addFilter(exclude_filter)

        # Get the root logger and add the file handlers to it
        root_logger = logging.getLogger()
        root_logger.addHandler(latest_file_handler)
        root_logger.addHandler(time_file_handler)

    def purge_old_logs(logs_folder, retention_period):
        """
        A helper function for getting rid of out of date logs
        """
        current_time = time.time()
        for file_path in glob.glob(os.path.join(logs_folder, "*.log")):
            if os.stat(file_path).st_mtime < current_time - retention_period:
                os.remove(file_path)
