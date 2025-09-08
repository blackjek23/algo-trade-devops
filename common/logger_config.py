import logging
import os

def setup_logging():
    """
    Sets up a central logging configuration for the entire application.
    All loggers in any module will write to this configured file.
    """
    # Navigate up to the project root to create the 'logs' directory
    # Adjust this path based on how many levels up your project root is from common/
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_dir = os.path.join(project_root, 'logs')

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file_path = os.path.join(log_dir, 'trading_bot.log')

    # Basic configuration for file and console logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler()
        ]
    )
    # The 'force=True' argument is available in Python 3.8+ and is useful
    # to reset the configuration if it was already set.
    # logging.basicConfig(..., force=True)