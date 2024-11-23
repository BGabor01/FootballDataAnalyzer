import time
import functools

from helpers.exceptions import MaxRetryError


def retry(max_retries: int = 3, delay: int = 2, exceptions: tuple = (Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < max_retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    print(e)  # TODO logging
                    time.sleep(delay)
            raise MaxRetryError(
                f"Function {func.__name__} failed after {max_retries} retries"
            )

        return wrapper

    return decorator
