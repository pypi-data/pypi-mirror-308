import logging
import sys
import time
import traceback
import hashlib
import json
import string
import datetime
import signal
from typing import Optional, Any, Dict, Callable

from watchtower_logging import config
from watchtower_logging import utils

class WatchtowerLogger(logging.Logger):

    def build_extra_object(self,
                           level: int,
                           data: Optional[dict] = None,
                           extra: Optional[dict] = None) -> dict:
        
        '''
        Method to build the data dictionary send with logging events
        '''

        data = data or {}
        extra = extra or {}

        # Merge with default data if available
        if hasattr(self, '_default_data') and isinstance(self._default_data, dict):
            data = {**self._default_data, **(data or {})}

        # Add traceback if error level or higher and no traceback already present
        if level >= utils.logLevels.ERROR and 'traceback' not in data:
            exc_info = sys.exc_info()[2]
            if exc_info:
                data['traceback'] = traceback.format_exc() 

        if data:
            if 'data' in extra:
                raise ValueError('Duplicate "data" key. Please merge the data you are passing with the entry in "extra".')
            extra['data'] = data       

        return extra

    def logaction(self,
                  level: int,
                  msg: str, 
                  *args: Any, 
                  data: Optional[dict]=None, 
                  **kwargs: Any) -> None:
    
        if not self.isEnabledFor(level):

            return

        extra = self.build_extra_object(level=level, data=data, extra=kwargs.pop('extra', None))

        self.log(level, msg, *args, extra=extra, stacklevel=3, **kwargs)

    def makeRecord(self,
                   *args,
                   **kwargs) -> logging.LogRecord:
        
        rv = super(WatchtowerLogger, self).makeRecord(*args, **kwargs)
        rv.dev = self.dev
        rv.execution_id = self._execution_id
        
        if not hasattr(self, 'env_send_time') or time.time() - self.env_send_time > self.env_interval:
            rv.env = self.env
            self.env_send_time = time.time()

        return rv

    def done(self, 
             msg: str, 
             *args: Any,    
             data: Optional[dict]=None, 
             **kwargs: Any) -> None:
        
        self.logaction(msg=msg, level=utils.logLevels.DONE, *args, data=data, **kwargs)

    def start(self, 
              msg: str, 
              *args: Any, 
              data: Optional[dict]=None, 
              **kwargs: Any) -> None:
        
        self.logaction(msg=msg, level=utils.logLevels.START, *args, data=data, **kwargs)

    def debug(self, 
             msg: str, 
             *args: Any, 
             data: Optional[dict]=None, 
             **kwargs: Any) -> None:
        
        self.logaction(msg=msg, level=utils.logLevels.DEBUG, *args, data=data, **kwargs)

    def info(self, 
             msg: str, 
             *args: Any, 
             data: Optional[dict]=None, 
             **kwargs: Any) -> None:
        
        self.logaction(msg=msg, level=utils.logLevels.INFO, *args, data=data, **kwargs)

    def warning(self, 
                msg: str, 
                *args: Any, 
                data: Optional[dict]=None, 
                **kwargs: Any) -> None:
        
        self.logaction(msg=msg, level=utils.logLevels.WARNING, *args, data=data, **kwargs)

    def error(self, 
              msg: str, 
              *args: Any, 
              data: Optional[dict]=None, 
              **kwargs: Any) -> None:

        self.logaction(msg=msg, level=utils.logLevels.ERROR, *args, data=data, **kwargs)

    def critical(self, 
                 msg: str, 
                 *args: Any, 
                 data: Optional[dict]=None, 
                 **kwargs: Any) -> None:
        
        self.logaction(msg=msg, level=utils.logLevels.CRITICAL, *args, data=data, **kwargs)

    def setExecutionId(self, 
                       execution_id: Optional[str]=None) -> None:
        
        if execution_id is None:
            self._execution_id = ''.join(utils.random_choices(string.ascii_lowercase + string.digits, k=config.EXECUTION_ID_LENGTH))
        else:
            self._execution_id = execution_id

    def setDefaultData(self, 
                    data: dict, 
                    overwrite: bool=False) -> None:
        
        if not isinstance(data, dict):
            raise TypeError('Default data needs to be a dictionary')
        if not overwrite and hasattr(self, '_default_data') and isinstance(self._default_data, dict):
            self._default_data = {**self._default_data, **data}
        else:
            self._default_data = data

    def setReturnWhenException(self, 
                               return_object: Optional[Any]=None) -> None:

        self.return_when_exception = return_object

    def monitor_func(self,
                     *args,
                     **kwargs) -> Callable:
        
        return utils.monitor_func(logger=self, *args, **kwargs)
    
    def send_alert(self,
                   *args,
                   **kwargs) -> None:
        
        return utils.send_alert(logger=self, *args, **kwargs)
    
    def shutdown(self, timeout=None):

        if hasattr(self, 'listener') and self.listener:
            try:
                self.listener.stop(timeout=timeout)
            except KeyboardInterrupt as e:
                print("KeyboardInterrupt received. Force quitting the listener thread.")
                # Allow the main thread to exit without waiting further



    
        

        

        