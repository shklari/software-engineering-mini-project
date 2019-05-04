import logging


class Log(object):
    LOG_FILE_EVENT = 'C:\\Users\\Inbar Naus\\PycharmProjects\\Software_Engineering_Project_2019-\\eventLog.Log'
    LOG_FILE_ERROR = 'C:\\Users\\Inbar Naus\\PycharmProjects\\Software_Engineering_Project_2019-\\errorLog.Log'

    def __init__(self, msg, log):
        if log == '':
            self.setup_logger('log_event', self.LOG_FILE_EVENT)
            self.setup_logger('log_error', self.LOG_FILE_ERROR)
        if log == 'eventLog':
            self.setup_logger('log_event', self.LOG_FILE_EVENT)
        if log == 'errorLog':
            self.setup_logger('log_error', self.LOG_FILE_ERROR)
        self.logger(msg, log)

    def setup_logger(self, logger_name, log_file, level=logging.INFO):
        log_setup = logging.getLogger(logger_name)
        formatter = logging.Formatter('%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        if not getattr(log_setup, 'handler_set', None):
            file_handler = logging.FileHandler(log_file, mode='a')
            file_handler.setFormatter(formatter)
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            log_setup.setLevel(level)
            log_setup.addHandler(file_handler)
            log_setup.addHandler(stream_handler)

    def logger(self, msg, logfile):
        if logfile == 'eventLog':
            log = logging.getLogger('log_event')
            log.info(msg)
        if logfile == 'errorLog':
            log = logging.getLogger('log_error')
            log.error(msg)

    def set_info(self, msg, log):
        self.logger(msg, log)
