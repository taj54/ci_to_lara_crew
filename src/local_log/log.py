import os
import logging
from datetime import date


class Log:

    def __init__(self,):
        self.LogFunctions = {
            'info': logging.info,
            'warning': logging.warning,
            'error': logging.error,
            'critical': logging.critical,
            'debug': logging.debug
        }
    def InitializeLogging(self):
        FolderName = "src/storage/logs/"
        today = date.today().strftime("%d-%m-%Y")
        FileName = os.path.join(FolderName, f"{today}.log")
        if not os.path.exists(FolderName):
            os.makedirs(FolderName)

        logging.basicConfig(filename=FileName, filemode='a',
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def LogIt(self,level, msg):
        LogFunc = self.LogFunctions.get(level, logging.error)
        LogFunc(msg)
        return print(level, ':', msg)

# Initialize logging when the module is imported
logger = Log()
logger.InitializeLogging()
