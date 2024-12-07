from logging.config import dictConfig

from src.config import config


def configure_logging() -> None:
    dictConfig(
        {
            "root": {
                "level": config.log_level,
                "handlers": config.log_handlers,
            },
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "correlation_id": {
                    "()": "asgi_correlation_id.CorrelationIdFilter",
                    "uuid_length": 32,
                    "default_value": "-",
                },
            },
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "datefmt": "%H:%M:%S",
                    "format": "%(levelname)s: \t  %(asctime)s %(name)s:%(lineno)d [%(correlation_id)s] %(message)s",  # noqa: E501
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG",
                    "filters": ["correlation_id"],
                    "formatter": "console",
                },
                "file": {
                    "class": "logging.FileHandler",
                    "filters": ["correlation_id"],
                    "level": "DEBUG",
                    "filename": config.log_filename,
                    "formatter": "console",
                },
            },
            "loggers": {
                "": {
                    "level": config.log_level,
                    "handlers": config.log_handlers,
                },
                "httpx": {
                    "level": "WARNING",
                },
                "pymongo": {
                    "level": "WARNING",
                },
                "oic": {
                    "level": "WARNING",
                },
                # Add other libraries here if needed
            },
        }
    )
