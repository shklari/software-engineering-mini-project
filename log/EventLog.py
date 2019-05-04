import logging


class EventLog(object):

    def __init__(self):
        log_format = '%(levelname)s %(asctime)s - %(message)s'
        logging.basicConfig(filename=
                            'C:\\Users\\Inbar Naus\\PycharmProjects\\Software_Engineering_Project_2019-\\eventLog.Log',
                            level=logging.DEBUG,
                            format=log_format,
                            filemode='w')

        self.logger = logging.getLogger()
