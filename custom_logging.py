import logging


def get_process_logger():
    PROCESS_FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
    PROCESS_LOG_FILE = "./info/process.log"

    process_handler = logging.FileHandler(PROCESS_LOG_FILE)
    process_handler.setFormatter(PROCESS_FORMATTER)

    process_logger = logging.getLogger('process_logger')
    process_logger.setLevel(logging.INFO)
    process_logger.addHandler(process_handler)

    return process_logger
