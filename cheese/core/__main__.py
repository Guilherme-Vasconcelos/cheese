import argparse
import logging
import logging.config
from dataclasses import dataclass
from typing import Literal, NoReturn

import cheese.core.uci


def setup_logging(
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
) -> None:
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "detailed": {
                "format": "%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(message)s"
            },
        },
        "handlers": {
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "cheese.log",
                "formatter": "detailed",
                "encoding": "utf-8",
            },
        },
        "root": {"level": log_level, "handlers": ["file"]},
    }

    logging.config.dictConfig(logging_config)


@dataclass
class CliArgs:
    debug: bool


def parse_cli_args() -> CliArgs:
    parser = argparse.ArgumentParser(description="cheese chess engine")
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        default=False,
        help="include extra debug logs",
    )
    args = parser.parse_args()
    return CliArgs(debug=args.debug)


def main() -> NoReturn:
    cli_args = parse_cli_args()
    log_level: Literal["DEBUG", "INFO"] = "DEBUG" if cli_args.debug else "INFO"
    setup_logging(log_level=log_level)

    engine = cheese.core.uci.Engine()
    engine.main_loop()


if __name__ == "__main__":
    main()
