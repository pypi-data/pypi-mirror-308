"""
Application context for LetterGuesser.

This module provides globally accessible instances of essential components, such as
logging, localisation, and experiment management, which are shared throughout the
application. By centralizing these instances, the application ensures consistency in
configuration and reduces redundancy.

Components
----------
localisation : Localisation
    A global instance of the`Localisation` class, initialized with the default
    language code and the locale directory path. This instance handles all
    localisation functionality.

logger : logging.Logger
    The global logger instance configured with a standardized output
    format. This logger is used across the application to log messages consistently.

manager : ExperimentManager
    A global instance of the `ExperimentManager` class, initialized with the
    localisation and logger instances. Manages experimental
    workflows and coordinates with other components as needed.

Usage
----------
These components can be imported directly from `context` to ensure
consistent use across the application:

    from letterguesser.context import localisation, logger, manager

    logger.info("Application started")
    manager.start_experiment()
"""
import logging.config

from letterguesser.config import APP_DEFAULT_LANGUAGE_CODE
from letterguesser.logic.ExperimentManager import ExperimentManager
from letterguesser.logic.Localisation import Localisation

# Global instance of the Localisation
localisation: Localisation = Localisation(
    default_lang=APP_DEFAULT_LANGUAGE_CODE,
    locale_dir='assets/locales'
)


logger = logging.getLogger('LetterGuesser')

logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - [%(module)s] %(levelname)s: %(message)s'
        }
    },
    'handlers': {
        'stdout': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout'
        }
    },
    'loggers': {
        'root': {'level': 'DEBUG', 'handlers': ['stdout']}
    }
}

logging.config.dictConfig(logging_config)

# Global instance of the Experiment Manager
manager: ExperimentManager = ExperimentManager(localisation, logger)

__all__ = ['localisation', 'manager', 'logger']
