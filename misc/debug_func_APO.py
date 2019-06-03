from functools import wraps
import logging
import time


def log_function(function):
    @wraps(function)
    def wrapped(*args, **kwargs):
        logging.info('Execution of function {}'.format(function.__name__))
        return function(*args, **kwargs)

    return wrapped


def time_function(function):
    @wraps(function)
    def wrapped(*args, **kwargs):
        start_time = time.time()
        result = function(*args, *kwargs)
        elapsed_time = time.time() - start_time
        logging.info('Execution of function {} took {} sec'.format(function.__name__, elapsed_time))
        return result

    return wrapped

@log_function
@time_function
def hello_fn(name='No one'):
    time.sleep(1)
    print('Hello "{}"'.format(name))


# Increase logging level
logging.getLogger().setLevel(logging.DEBUG)

# Execute the function
hello_fn('Test')
hello_fn('Test2')