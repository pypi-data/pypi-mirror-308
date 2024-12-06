from datetime import datetime
import inspect
import ultraprint.common as p
import threading
import os

class logger:
    
    def __init__(self, name, filename=None, include_extra_info=False, write_to_file=True, log_level='INFO', log_format=None, max_file_size=None, backup_count=0, log_to_console=True):
        self.name = name
        self.include_extra_info = include_extra_info
        self.write_to_file = write_to_file

        if filename:
            self.filename = filename
        else:
            self.filename = f'{name}.log'

        self.log_levels = {
            'DEBUG': 0,
            'INFO': 1,
            'SUCCESS': 2,
            'WARNING': 3,
            'ERROR': 4,
            'CRITICAL': 5
        }

        self.current_log_level = self.log_levels[log_level]
        self.log_format = log_format or '[{time}] [{level}] [{name}] {message}'
        self.max_file_size = max_file_size
        self.backup_count = backup_count
        self.log_to_console = log_to_console
        self.lock = threading.Lock()

    def set_log_level(self, log_level = 'INFO'):
        self.current_log_level = self.log_levels[log_level]
    
    def set_write_to_file(self, write_to_file):
        self.write_to_file = write_to_file

    def _get_extra_info(self):
        frame = inspect.currentframe().f_back.f_back
        info = inspect.getframeinfo(frame)
        return f'{info.filename}:{info.function}:{info.lineno}'

    def _log(self, level, msg, color_func):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        extra_info = self._get_extra_info() if self.include_extra_info else ''
        if self.include_extra_info:
            extra_info = self._get_extra_info()
            formatted_msg = self.log_format.format(
                time=current_time,
                level=level,
                name=self.name,
                message=msg,
                extra_info=extra_info
            )
        else:
            formatted_msg = self.log_format.format(
                time=current_time,
                level=level,
                name=self.name,
                message=msg,
                extra_info=''
            )
        
        if self.log_levels[level] >= self.current_log_level:
            if self.log_to_console:
                color_func(formatted_msg)
        
        if self.write_to_file:
            with self.lock:
                self._write_to_file(formatted_msg)

    def _write_to_file(self, msg):
        if self.max_file_size and os.path.exists(self.filename) and os.path.getsize(self.filename) >= self.max_file_size:
            self._rotate_logs()
        with open(self.filename, 'a') as f:
            f.write(f'{msg}\n')

    def _rotate_logs(self):
        if self.backup_count > 0:
            for i in range(self.backup_count - 1, 0, -1):
                sfn = f"{self.filename}.{i}"
                dfn = f"{self.filename}.{i+1}"
                if os.path.exists(sfn):
                    os.rename(sfn, dfn)
            os.rename(self.filename, f"{self.filename}.1")
        else:
            os.remove(self.filename)

    def exception(self, msg):
        import traceback
        exc_info = traceback.format_exc()
        full_msg = f"{msg}\n{exc_info}"
        self._log('ERROR', full_msg, p.red)

    def info(self, msg):
        self._log('INFO', msg, p.cyan)

    def error(self, msg):
        self._log('ERROR', msg, p.red)

    def warning(self, msg):
        self._log('WARNING', msg, p.yellow)

    def success(self, msg):
        self._log('SUCCESS', msg, p.green)

    def debug(self, msg):
        self._log('DEBUG', msg, p.dgray)

    def critical(self, msg):
        self._log('CRITICAL', msg, p.red_bg)