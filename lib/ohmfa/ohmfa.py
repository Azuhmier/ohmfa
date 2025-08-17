from ohmfa.config import (setup_logger)
class Ohmfa:
    dcnfg = {}
    logger=None

    def __init__(self, log_level=0):
        if Ohmfa.logger is None:
            logger = setup_logger(log_level=log_level)
            Ohmfa.logger = logger
        self.logger = Ohmfa.logger
            