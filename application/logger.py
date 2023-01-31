import logging
import logging.handlers
logger = logging.getLogger("")
logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(
    "log_file.log", maxBytes=(1048576*5), backupCount=7
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(logging.StreamHandler())