from enum import IntEnum
import logging
import os
import platform
import subprocess
from packaging.requirements import Requirement
from typing import Optional, Literal, Callable
import sys
import traceback
from functools import wraps
import datetime
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from itertools import accumulate as _accumulate, repeat as _repeat
from bisect import bisect as _bisect
import random

from watchtower_logging import config
from watchtower_logging.version import __version__

class logLevels(IntEnum):

    '''
    Custom enumeration of logging levels, including both standard
    and watchtower-defined levels (start and done)
    '''

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    START = config.START_LEVEL_NUM
    DONE = config.DONE_LEVEL_NUM
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

def build_logger_name(name: str) -> str:
    
    return (
        name or 
        os.environ.get('K_SERVICE') or 
        os.environ.get('FUNCTION_NAME') or 
        config.DEFAULT_LOGGER_NAME)

def parse_requirements(input):

    requirements = [Requirement(t) for t in input.strip().split('\n')]
    return [
        {
            'name': req.name,
            'version': req.specifier.__str__()[2:] if req.specifier.__str__().startswith('==') else req.specifier.__str__()
        } for req in requirements
    ]

def get_environment():

    env = {'lng': 'Python'}

    try:
        env['lng_version'] = platform.python_version()
    except Exception:
        pass

    try:
        result = subprocess.run(['pip', 'freeze'], stdout=subprocess.PIPE, text=True)
        requirements_from_pip = parse_requirements(result.stdout)
    except Exception as e:
        return env

    try:
        with open(os.path.join(os.getcwd(), 'requirements.txt'), 'r') as f:
            x = f.read()
        requirement_names_from_file = [req['name'] for req in parse_requirements(x)]
    except Exception as e:
        return env

    env['packages'] = [req for req in requirements_from_pip if req['name'].lower() in requirement_names_from_file]

    return env

def monitor_func(logger,
                 func_name: Optional[str]=None,
                 set_execution_id: bool=True,
                 execution_id: Optional[str]=None,
                 start_done: bool=True,
                 except_level: Literal[*logLevels._member_names_]='ERROR',
                 reset_default_data: bool=True) -> Callable:

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            fname = func_name or func.__name__

            try:
                if set_execution_id:
                    logger.setExecutionId(execution_id)

                if reset_default_data:
                    logger.setDefaultData(data=logger.init_default_data or {}, 
                                          overwrite=True)

                if start_done:
                    logger.start(f'Starting {fname}')

                result = func(*args, **kwargs)

                if start_done:
                    logger.done(f'Done with {fname}')

                return result

            except Exception as e:

                getattr(logger, except_level.lower())(
                    str(e), data={'traceback': traceback.format_exc(),
                                    'exc_info': traceback.format_exc()}
                )
                if hasattr(logger, 'return_when_exception'):
                    return logger.return_when_exception
                    
                elif os.getenv('FUNCTION_SIGNATURE_TYPE') == 'http':
                    return ({'details': 'Server Error'}, 500)

        return wrapper

    return decorator

def send_alert(logger,
               alert_token: str,
               name: str,
               lead: str,
               body: str = '',
               details: str = '',
               priority: bool =False,
               dev: Optional[bool] = None,
               min_time: Optional[datetime.datetime] = None,
               max_time: Optional[datetime.datetime] = None,
               search_time: Optional[datetime.datetime] = None,
               link_text: Optional[str] = None,
               link_url: Optional[str] = None,
               docs_text: Optional[str] = None,
               docs_url: Optional[str] = None,
               alert_update_url: Optional[str] = None,
               retry_count: int = config.DEFAULT_ALERT_RETRY_COUNT,
               backoff_factor: int = config.DEFAULT_ALERT_BACKOFF_FACTOR,
               timeout: int = config.DEFAULT_ALERT_HTTP_TIMEOUT):

    alert_body = None

    try:

        dev = dev if isinstance(dev, bool) else logger.dev
        assert isinstance(alert_token, str) and len(alert_token) > 10, 'Invalid alert token'

        if search_time is None:
            search_time = datetime.datetime.now(datetime.timezone.utc) 
        assert isinstance(search_time, datetime.datetime), 'search_time needs to be a datetime instance'

        alert_body = {
            'name': name,
            'lead': lead,
            'body': body,
            'details': details,
            'level': 'alert',
            'priority': priority,
            'dev': dev,
            'info_search_time': search_time.timestamp()
        }

        if not min_time is None:
            assert isinstance(min_time, datetime.datetime), 'min_time needs to be a datetime instance'
            alert_body['info_min_time'] = min_time.timestamp()

        if not max_time is None:
            assert isinstance(max_time, datetime.datetime), 'max_time needs to be a datetime instance'
            alert_body['info_max_time'] = max_time.timestamp()

        if not link_url is None:
            link = {'url': link_url}
            if not link_text is None:
                link['text'] = link_text
            alert_body['link'] = link

        if not docs_url is None:
            docs = {'url': docs_url}
            if not docs_text is None:
                docs['text'] = docs_text
            alert_body['docs'] = docs

        if not alert_update_url is None:
            alert_body['alert_update_url'] = alert_update_url

        url = 'https://alerts.' + logger.host
        headers = {'Authorization': alert_token,
                   'User-Agent': config.USER_AGENT_STR_FMT.format(version=__version__)}

        session = requests.Session()
        retry = Retry(total=retry_count,
                      backoff_factor=backoff_factor,
                      status_forcelist=[500, 502, 503, 504])

        session.mount(url, HTTPAdapter(max_retries=retry))
        r = session.post(url,
                     json=alert_body,
                     headers=headers,
                     timeout=timeout)
        r.raise_for_status()

    except Exception as e:

        logger.critical('Failed to send alert',
                        data={
                            'alert_body': alert_body,
                            'error': str(e),
                            'traceback': traceback.format_exc()})
        
def random_choices(population, weights=None, *, cum_weights=None, k=1):
    """Return a k sized list of population elements chosen with replacement.
    If the relative weights or cumulative weights are not specified,
    the selections are made with equal probability.
    """

    if hasattr(random, 'choices'):
        return random.choices(population=population, weights=weights, cum_weights=cum_weights, k=k)

    n = len(population)
    if cum_weights is None:
        if weights is None:
            _int = int
            n += 0.0    # convert to float for a small speed improvement
            return [population[_int(random.random() * n)] for i in _repeat(None, k)]
        cum_weights = list(_accumulate(weights))
    elif weights is not None:
        raise TypeError('Cannot specify both weights and cumulative weights')
    if len(cum_weights) != n:
        raise ValueError('The number of weights does not match the population')
    bisect = _bisect
    total = cum_weights[-1] + 0.0   # convert to float
    hi = n - 1
    return [population[bisect(cum_weights, random.random() * total, 0, hi)]
            for i in _repeat(None, k)]

def attach_watchtower_exception_hook(logger):

    def watchtower_handle_exception(exc_type, exc_value, exc_traceback):

        if issubclass(exc_type, KeyboardInterrupt):

            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        logger.critical('Uncaught Exception', data={'traceback': '{exc_type}: {exc_value}\n{traceback}'.format(exc_type=exc_type.__name__,
                                                                                                                exc_value=exc_value,
                                                                                                                traceback=''.join(traceback.format_tb(exc_traceback)))})
        sys.__excepthook__(exc_type, exc_value, exc_traceback)

    sys.excepthook = watchtower_handle_exception