import logging


class ErrorLog(object):

    def __init__(self):
        log_format = '%(levelname)s %(asctime)s - %(message)s'
        logging.basicConfig(filename=
                            'C:\\Users\\Inbar Naus\\PycharmProjects\\Software_Engineering_Project_2019-\\errorLog.Log',
                            level=logging.ERROR,
                            format=log_format,
                            filemode='w')

        self.logger = logging.getLogger()
