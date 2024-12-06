
import logging
import queue
import atexit
from logging.handlers import QueueHandler
from typing import Optional, List

from watchtower_logging import utils, config
from watchtower_logging.loggers import WatchtowerLogger
from watchtower_logging.handlers import WatchtowerHandler, CustomQueueListener

def getLogger(beam_id: str,
              host: str,
              name: Optional[str] = None, 
              execution_id: Optional[str] = None, 
              token: Optional[str] = None, 
              protocol: str = 'https', 
              dev: bool = False, 
              default_data: Optional[dict] = None,
              level: int = utils.logLevels.START, 
              debug: bool = False, 
              path: Optional[str] = None, 
              console: bool = False, 
              send: bool = True, 
              use_threading: bool = True, 
              dedup: bool = True,
              dedup_keys: Optional[List] = None, 
              retry_count: int = config.DEFAULT_RETRY_COUNT,
              backoff_factor: float = config.DEFAULT_BACKOFF_FACTOR,
              catch_all: bool = True, 
              dedup_id_key: Optional[str] = None, 
              use_fallback: bool = True,
              fallback_host: Optional[str] = None,
              lvl_frame_info: int = 0,
              env_interval: int = config.DEFAULT_ENV_INTERVAL) -> logging.Logger:
    
    """
    Create and configure a Watchtower logger.

    Args:
        beam_id (str): Unique identifier for the beam.
        host (str): Host for sending log data.
        name (Optional[str]): Name of the logger. Defaults to a cloud function name (if available) and 'watchtower-logging' otherwise.
        execution_id (Optional[str]): Execution Id for the logger. Will default to a random string of x characters, x being specified in config.py
        token (Optional[str]): Authentication token. Defaults to None.
        protocol (str): Protocol to use ('http' or 'https'). Defaults to 'https'.
        dev (bool): Flag to indicate development environment. Defaults to False.
        default_data (Optional[dict]): Default data to include in each log entry. Defaults to None.
        level (int): Logging level. Defaults to utils.logLevels.START.
        debug (bool): Flag to enable debug mode. Defaults to False.
        path (Optional[str]): File path for logging (not supported). Defaults to None.
        console (bool): Flag to add console handler. Defaults to False.
        send (bool): Flag to send logs to the endpoint. Defaults to True.
        use_threading (bool): Flag to enable threading for logging. Defaults to True.
        dedup (bool): Flag to enable deduplication. Defaults to True.
        dedup_keys (Optional[List]): Keys to use for deduplication. Defaults to None.
        retry_count (int): Number of retries for sending logs. Defaults to config.DEFAULT_RETRY_COUNT.
        backoff_factor (float): Backoff factor for retries. Defaults to config.DEFAULT_BACKOFF_FACTOR.
        catch_all (bool): Flag to catch uncaught exceptions. Defaults to True.
        dedup_id_key (Optional[str]): Key for deduplication ID (not supported). Defaults to None.
        use_fallback (bool): Flag to use fallback host. Defaults to True.
        fallback_host (Optional[str]): Fallback host. Defaults to None.
        lvl_frame_info (int): Logging level for frame information (not supported). Defaults to 0.
        env_interval (int): Interval for environment updates. Defaults to config.DEFAULT_ENV_INTERVAL.

    Returns:
        logging.Logger: Configured Watchtower logger.
    """
    
    # raise implementation errors when arguments are specified that are no longer supported.
    if not path is None:
        raise NotImplementedError('Logging to a file by specifying `path` is no longer supported directly by Watchtower, you can add your own file handler though.')
    if not dedup_id_key is None:
        raise NotImplementedError('Manually specifying the `dedup_id_key` is no longer supported')
    if not lvl_frame_info == 0:
        raise NotImplementedError('The logging level for which frame information is send (`lvl_frame_info`) can no longer be specified')

    # add logging levels within the scope of the getLogger function
    logging.addLevelName(utils.logLevels.DONE, 'DONE')
    logging.addLevelName(utils.logLevels.START, 'START')

    initial_logging_class = logging.getLoggerClass()
    try:
        logging.setLoggerClass(klass=WatchtowerLogger)
        name = utils.build_logger_name(name)
        logger = logging.getLogger(name)
    finally:
        logging.setLoggerClass(klass=initial_logging_class)

    logger.setLevel(level)

    logger.init_default_data = default_data
    if default_data:
        logger.setDefaultData(data=default_data)

    logger.beam_id = beam_id
    logger.dev = dev
    logger.env = utils.get_environment()
    logger.env_interval = env_interval

    logger.setExecutionId(execution_id=execution_id)

    if send:

        # Ensure no duplicate handlers are added
        if not logger.handlers or not any(isinstance(handler, (WatchtowerHandler, QueueHandler)) for handler in logger.handlers):
            
            # Set up the Watchtower handler to send logs to the specified endpoint
            watchtower_handler = WatchtowerHandler(beam_id=beam_id,
                                                   host=host,
                                                   token=token,
                                                   protocol=protocol,
                                                   retry_count=retry_count,
                                                   backoff_factor=backoff_factor,
                                                   use_fallback=use_fallback,
                                                   fallback_host=fallback_host,
                                                   debug=debug)
            
            watchtower_handler.setLevel(level=level)
            watchtower_handler.dedup = dedup
            watchtower_handler.dedup_keys = dedup_keys

            if not use_threading:
                
                logger.addHandler(watchtower_handler)
                   
            else:

                log_queue = queue.Queue(-1)  # Unlimited queue size
                queue_handler = QueueHandler(log_queue)
                logger.addHandler(queue_handler)
                
                
                
                # Set up a queue listener to process log messages asynchronously
                listener = CustomQueueListener(log_queue, watchtower_handler)
                listener.start()

                # Attach the listener to the logger so it can be stopped when the application exits
                logger.listener = listener
                atexit.register(logger.shutdown)

    if console:

        if not logger.handlers or not any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers):

            console_handler = logging.StreamHandler()
            console_handler.setLevel(level=level)

            formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(name)s - %(message)s' + '\x1b[38;20m' + ' -  %(data)s')
            console_handler.setFormatter(formatter)

            logger.addHandler(console_handler)

    if catch_all:

        utils.attach_watchtower_exception_hook(logger)       

    return logger