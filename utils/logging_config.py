import logging

def setup_logging(level=logging.INFO):
    """
    Configure logging for the entire project

    Args:
        level: Logging level (default: DEBUG)
    """
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
