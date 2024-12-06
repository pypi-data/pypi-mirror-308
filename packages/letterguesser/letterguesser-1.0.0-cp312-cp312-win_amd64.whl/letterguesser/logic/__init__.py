"""
Logic package for LetterGuesser application.

This package provides core logic components, handling experiment management,
event handling, and localisation for the application. Each component is
designed to facilitate the application's business logic and interactions.

Modules
-------
- `ExperimentManager`: Manages experiment flow and user interactions.
- `Event`: Implements a simple event-driven pub-sub model for components.
- `Localisation`: Handles text translations and localisation bindings.
- `Controller`: Connects GUI actions with experiment events and actions.
- `utils`: Utility functions for file paths and data loading.

Usage
-----
Import relevant logic components as needed in the application:

    from letterguesser.logic import ExperimentManager, Localisation

    experiment_manager = ExperimentManager()
    localisation = Localisation()
"""
