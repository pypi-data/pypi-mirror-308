import asyncio
import functools
import logging


def log_input(func):
    logger = logging.getLogger(func.__module__)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        arg_str = ", ".join([repr(a) for a in args])
        kwarg_str = ", ".join([f"{k}={v!r}" for k, v in kwargs.items()])
        all_args = ", ".join(filter(None, [arg_str, kwarg_str]))
        logger.debug(f"{func.__module__}.{func.__name__} call: ({all_args})")
        return func(*args, **kwargs)

    return wrapper


def log_output(func):
    logger = logging.getLogger(func.__module__)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        logger.debug(f"{func.__module__}.{func.__name__} return: {result!r}")
        return result

    return wrapper


def log_io(func):
    logger = logging.getLogger(func.__module__)

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        arg_str = ", ".join([repr(a) for a in args])
        kwarg_str = ", ".join([f"{k}={v!r}" for k, v in kwargs.items()])
        all_args = ", ".join(filter(None, [arg_str, kwarg_str]))
        logger.debug(f"{func.__module__}.{func.__name__} call: ({all_args})")

        result = await func(*args, **kwargs)
        logger.debug(f"{func.__module__}.{func.__name__} return: {result!r}")
        return result

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        arg_str = ", ".join([repr(a) for a in args])
        kwarg_str = ", ".join([f"{k}={v!r}" for k, v in kwargs.items()])
        all_args = ", ".join(filter(None, [arg_str, kwarg_str]))
        logger.debug(f"{func.__module__}.{func.__name__} call: ({all_args})")

        result = func(*args, **kwargs)
        logger.debug(f"{func.__module__}.{func.__name__} return: {result!r}")
        return result

    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
