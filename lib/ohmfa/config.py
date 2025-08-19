import logging
import inspect
import sys

#####################
# Global Logger
#####################
class IndentFormatter(logging.Formatter):
       def format(self, record):
           # Get the current stack depth
           stack_depth = len(inspect.stack()) - 1 # Adjust for this function's frame

           # Create indentation string
           indentation = "||" * (stack_depth-9)

           # Prepend indentation to the message
           record.msg = indentation + str(record.msg)

           return super().format(record)

def setup_logger(log_level=0):

    # Create a custom logger
    logger = logging.getLogger('base')
    logger.setLevel(log_level)

    # Create handlers
    c_handler = logging.StreamHandler(sys.stdout)

    # Set levels for handlers
    c_handler.setLevel(log_level)

    # Create formatters and add them to handlers
    #c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    formatter=None
    if log_level == 10:
        formatter = IndentFormatter('%(message)s')
    else:
        formatter = logging.Formatter('%(message)s')
    c_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(c_handler)

    return logger

