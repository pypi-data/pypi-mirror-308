# Logging class
import logging


def logger(
    name=None,
    handler="console",
    filepath=None,
    level=logging.DEBUG,
):
    """
    This is a simple logger to save logs locally or print to console

    :param name: name of logging file
    :param handler: logging handler selection.  Values should be 'file','console' or 'both'
    :param filepath: file path for the logging file, should contain ending '/'
    :param level: logging level. Default is logging.INFO

    :returns: Python logger
    """
    # Set Handler
    file = f"{filepath}/{name}.log"
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    if handler == "file":
        fh = logging.FileHandler(file)
        fh.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.setLevel(level)
        if not logger.handlers:
            logger.addHandler(fh)

    elif handler == "console":
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.setLevel(level)
        if logger.hasHandlers():
            logger.handlers.clear()

        logger.addHandler(ch)

    elif handler == "both":
        fh = logging.FileHandler(file)
        fh.setFormatter(formatter)
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(fh)
        logger.addHandler(ch)

    else:
        print("Please select an appropriate handler list: file, console or both")
        return
    logger.propagate = False
    return logger
