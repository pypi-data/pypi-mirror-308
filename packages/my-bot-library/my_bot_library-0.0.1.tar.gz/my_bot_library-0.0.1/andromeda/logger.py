import inspect
import logging

def get_logger(name):
    # Create a logger instance
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create a console handler (StreamHandler)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)

    # Create a file handler (FileHandler)
    file_handler = logging.FileHandler("andromeda_app.logs")
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter that includes the function name
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s"
    )

    # Set the formatter for both handlers
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add the handlers to the logger (if not already added)
    if not logger.handlers:
        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

    return logger


async def get_current_function_name():
    return inspect.currentframe().f_code.co_name
