# Importing necessary modules
import os
import logging

# Function to find root of project
def find_project_root(start_path: os.PathLike[str] = None):
    """
    Finds the root directory of a project by searching for specific marker files or folders, 
    such as a `.git` folder or `setup.py` file, which commonly indicate the root of a repository.

    Args:
        start_path (os.PathLike[str], optional): The starting path for the search. Defaults to the current working 
            directory if not specified.

    Returns:
        Optional[os.PathLike[str]]: The absolute path to the project root if found, otherwise None.
    """
    
    if start_path is None:
        start_path: os.PathLike[str] = os.getcwd()
        
    current_path: os.PathLike[str] = start_path
    while current_path != os.path.dirname(current_path):
        if os.path.isdir(os.path.join(current_path, '.git')):
            return current_path
        if os.path.isfile(os.path.join(current_path, 'setup.py')):
            return current_path
        current_path = os.path.dirname(current_path)
    
    return None

# Function to setup custom logger for EMP - Microservices
def setup_logger(
    SERVICE: str,
    ENVIRONMENT: str = os.getenv(key = 'ENVIRONMENT', default = 'dev'),
    module: str = 'Serverless') -> logging.Logger:
    """
    Setting up and configuring the logger for all the datapreparation function and python modules.

    This function initializes and configures a logger named '<service>_logger' for use within the Serverless Function.
    The logger is set to log messages with INFO level by default. It ensures that AWS CloudWatch Logs handler is added to stream logs to AWS CloudWatch in case of deploying to AWS Lambda Function.

    Example:
    logger = setup_logger(ENVIRONMENT = 'dev', SERVICE = 'location', module = 'Serverless')
    logger.info('Logging information message')

    Note:
    - The logger is configured to format the log entries to JSON Format for easy integration with AWS CloudWatch and other applications for monitoring (Splunk, New Relic, etc.)
    - The log filename is set according it's environment -> i.e.: EMP-Location-Service-Serverless_dev.log and exported to local 'logs' directory
    - The logfile write mode is set to overwrite for environments (dev and int) while for environments (stg and prd) to append
    - The custom attribute 'handler_set' is used to track if the handler has been added

    Returns:
        logging.Logger: The configured logger instance for logging within the Serverless Function
    """
    
    # Using dynamic name from parameters
    logger_name: str = f'{SERVICE}-{module}'
    if logger_name in logging.root.manager.loggerDict:
        return logging.getLogger(name = logger_name)
    
    # Setting up environment variable (dev, int, stg or prd)
    if not ENVIRONMENT:
        ENVIRONMENT: str = os.getenv(key = 'ENVIRONMENT', default = 'dev')
        
    # Initializing the logger
    logger: logging.Logger = logging.getLogger(name = logger_name)
    logger.setLevel(level = logging.INFO)
    
    # Defining log file path and mode
    log_dir: os.PathLike[str] = find_project_root() + '/logs'
    log_file_path: os.PathLike[str] = (
        log_dir + f'/EMP-{SERVICE}-{module}_{ENVIRONMENT}.log'
    )
    os.makedirs(name = log_dir, exist_ok = True)
    log_mode: str = 'a' if ENVIRONMENT in ('stg' or 'prd') else 'w'
    
    # Setting up the format
    formatter: str = logging.Formatter(
        fmt = '{"Timestamp" : "%(asctime)s", "Filename" : "%(filename)s", "Line" : "%(lineno)d", "Level" : "%(levelname)s", "Message" : "%(message)s"}'
    )
    
    # Filehandler
    file_handler = logging.FileHandler(
        filename = log_file_path, mode = log_mode, delay = True
    )
    
    file_handler.setFormatter(fmt = formatter)
    logger.addHandler(hdlr = file_handler)
    
    # Disabling propagating to avoid duplicate logging
    logger.propagate = False
    
    # Returning logger
    return logger