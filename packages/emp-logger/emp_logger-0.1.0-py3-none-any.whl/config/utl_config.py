# Importing necessary modules
import os
from typing import Dict, List

# Importing necessary 3rd party modules
import logging
from config import ConfigClient
from requests.auth import HTTPBasicAuth

# Function to dynamically retrieve nested keys
def get_nested_config(config: Dict[str, str], key_parts: List[str]) -> str:
    """
    Retrieve a nested configuration value from a dictionary using a list of keys.

    Args:
        config (Dict[str, str]): The nested dictionary which contains environment variables and configurations
        key_parts (List[str]): List of strings representing the hierarchy of keys needed to access the desired values

    Returns:
        str: The retrieved value from configurations
    """
    
    # If key_parts is empty, return None immediately
    if not key_parts:
        return None

    value: Dict[str, str] = config
    
    # Looping through all items in list 'key_parts'
    for part in key_parts:
        
        # Ensuring each level is a dictionary
        if isinstance(value, dict):
            value = value.get(part)
        else:
            return None
        if value is None:
            break
    return value

# Function to loead environment variables from Spring Cloud Config Server or local OS / Profile
def load_cnf(service_name: str,
             required_keys: List[str],
             logger:logging.Logger) -> Dict[str, str]:
    """Load environment variables from the Spring Cloud Config Server or fall back to local OS profile.

    This function attempts to retrieve configuration values from a Spring Cloud Config Server
    for a specified service. If the server is unavailable, it loads the environment variables
    directly from the local OS profile.

    Args:
        service_name (str): Name of the service whose configuration is being retrieved.
        required_keys (List[str]): List of environment variable keys to retrieve.
        logger (logging.Logger): Logger instance used for logging status, warnings, and errors.

    Returns:
        Dict[str, str]: Dictionary containing the loaded environment variables with their values.

    Raises:
        None directly, but logs any exceptions encountered when loading from either source.

    Notes:
        - If the Spring Cloud Config Server is unreachable, environment variables are loaded
          from the local OS profile as a fallback.
        - If an environment variable is not found, it is logged and skipped in the final dictionary.
    """
    
    # Final variables
    ENVIRONMENT: str = os.getenv(key = 'ENVIRONMENT', default = 'dev')
    BASE_URL: str = os.getenv(key = 'BASE_URL')
    USERNAME: str = os.getenv(key = 'EMP_CONFIG_USERNAME')
    PASSWORD: str = os.getenv(key = 'EMP_ENCRYPT_KEY')

    # Dictionary to store environment variables
    env_vars: Dict[str, str] = {'ENVIRONMENT' : ENVIRONMENT}
    
    # Establishing connection to Spring Cloud Config Server 'CNF-S'
    try:
        cc: ConfigClient = ConfigClient(address = f'{BASE_URL}:8888',
                          label = ENVIRONMENT,
                          app_name = service_name,
                          profile = ENVIRONMENT)
        cc.get_config(auth = HTTPBasicAuth(username = USERNAME, password = PASSWORD))
    except SystemExit:
        logger.warning(msg = f'Spring Cloud Config Server \'(CNF-S)\' is currently not available on environment \'{ENVIRONMENT}\'')
        
        # Fallback: Loading environment variables from local OS into dictionary 'env_vars' if 'CNF-S' is not available
        try:
            for key in required_keys:
                if key not in env_vars.keys():
                    env_vars[key] = os.getenv(key = key)
            logger.info(msg = f'Environment variables loaded successfully from local OS \'(Profile)\' on environment \'{ENVIRONMENT}\'')
        except Exception as e:
            logger.error(msg = f'Error occurred in loading environment variables from local OS \'(Profile)\' on environment \'{ENVIRONMENT}\': {repr(e)} - Trace: {traceback.print_exc()}')
            raise
    else:
        
        # Loading environment variables from Spring Cloud Config Server 'CNF-S' into dictionary 'env_vars'
        try:
            for key in required_keys:
                if key not in env_vars.keys():
                    key_parts: List[str] = [part.lower() for part in key.split(sep = '_')]
                    value: str = get_nested_config(config = cc.config, key_parts = key_parts)
                    env_vars[key] = value
            logger.info(msg = f'Environment variables loaded successfully from Spring Cloud Config Server \'(CNF-S)\' on environment \'{ENVIRONMENT}\'')
        except Exception as e:
            logger.error(msg = f'Error occurred in loading environment variables from Spring Cloud Config Server \'(CNF-S)\' on environment \'{ENVIRONMENT}\': {repr(e)} - Trace: {traceback.print_exc()}')
            raise
    finally:
        
        # Returning dictionary 'env_vars'
        return env_vars