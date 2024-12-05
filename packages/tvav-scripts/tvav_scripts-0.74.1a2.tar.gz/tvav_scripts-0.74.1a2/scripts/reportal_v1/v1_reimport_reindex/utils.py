import logging.config
from typing import (
    List,
    Union,
)


def string_to_list(list_as_string: str) -> List[Union[int, str]]:
    values_list = []

    for value in list_as_string.split(","):
        value = value.strip()
        try:
            values_list.append(int(value))
        except ValueError:
            if value:
                values_list.append(value)
            continue

    return values_list


def setup_logging():
    logging.config.dictConfig(
        {
            "version": 1,
            "formatters": {
                "f": {
                    "format": "{asctime} [{levelname}] - {name} - {message} ({filename}:{lineno})",
                    "style": "{"
                },
            },
            "handlers": {
                "h": {
                    "class": "logging.StreamHandler",
                    "formatter": "f",
                    "level": logging.DEBUG
                },
            },
            "root": {
                "handlers": ["h"],
                "level": logging.DEBUG
            }
        }
    )
