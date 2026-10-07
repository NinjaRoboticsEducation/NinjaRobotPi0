import logging

def get_logger(name, level=logging.INFO):
    """
    Initializes and returns a logger with a specified name and level.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent adding duplicate handlers to the logger
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(level)
        
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        formatter = logging.Formatter(log_format)
        ch.setFormatter(formatter)
        
        logger.addHandler(ch)
    
    return logger

if __name__ == "__main__":
    # Example usage
    logger = get_logger(__name__)
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
