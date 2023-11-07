

import sys
import os
import datetime

from loguru import logger
import constants.constants as constants

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

class QYLog:
    log_path = datetime.datetime.now().strftime("logs/%Y-%m-%d.log")
    log_level = constants.LOG_LEVEL_INFO
    
    @classmethod
    def init_logger(self, log_path: str, log_level: str):
        QYLog.log_level = log_level
        QYLog.log_path = os.path.join(log_path, datetime.datetime.now().strftime("%Y-%m-%d.log"))
        logger.add(QYLog.log_path, rotation="10 MB", retention="1 day", level=self.log_level)

    @classmethod
    def get_logger(self):
        return logger