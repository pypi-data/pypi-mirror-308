"""
Localisation module for managing text translation and widget updates.

Provides language translation and binds text updates to localized widgets.
"""

import gettext
from pathlib import Path
from typing import Any

from babel import Locale

from letterguesser.config import (
    ALPHABET_EN,
    ALPHABET_UK,
    APP_DEFAULT_LANGUAGE_CODE
)

from .utils import get_resource_path


class Localisation:
    """Singleton class for managing application localization."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Create or return the singleton instance of Localisation.

        Ensures that only one instance of Localisation exists within the application.
        If an instance already exists, this method returns it; otherwise, it creates
        a new instance.

        :param args: Positional arguments for initialization.
        :param kwargs: Keyword arguments for initialization.
        :return: The single instance of Localisation.
        """
        if not cls._instance:
            cls._instance = super(Localisation, cls).__new__(cls)
        return cls._instance

    def __init__(
            self,
            default_lang: str = 'uk',
            domain: str = 'messages',
            locale_dir: str = 'locales'
    ):
        """
        Initialize the Localisation instance.

        :param default_lang: Default language code ('uk' or 'en').
        :param domain: Domain name for translation files.
        :param locale_dir: Directory containing locale files.
        """
        # avoid re-init
        if hasattr(self, 'initialized'):
            print('Localisation module already initialized')
            return

        self.domain: str = domain
        self.default_lang: str = default_lang
        self.locale_dir: Path = get_resource_path(locale_dir)

        self.widgets: list[Any] = []
        self.current_locale = None
        self.current_translation: None | gettext.NullTranslations = None

        self.load_language(self.default_lang)

    def load_language(self, lang_code: str) -> None:
        """
        Load language settings by code.

        :param lang_code: Language code, e.g., 'en' or 'uk'.
        """
        try:
            self.current_translation = gettext.translation(
                self.domain,
                localedir=self.locale_dir,
                languages=[lang_code],
                fallback=True
            )

            self.current_translation.install()
            self.current_locale = Locale(lang_code)
            self.update_all_widgets()
        except Exception as e:
            print(f'[Localisation] Error loading language {lang_code}: {str(e)}')
            self.current_translation = gettext.NullTranslations()
            self.current_locale = Locale(APP_DEFAULT_LANGUAGE_CODE)

    def translate(self, key: str) -> str:
        """
        Translate a given key to the current language.

        :param key: Key to be translated.
        :return: Translated string.
        """
        if self.current_translation is not None:
            return self.current_translation.gettext(key)
        return key

    def bind(
            self,
            widget,
            translation_key,
            update_method=None
    ) -> None:
        """
        Bind a widget to a translation key for automatic updates.

        :param widget: The widget to bind (Tkinter or CTkinter)
        :param translation_key: The translation key for the widget's text.
        :param update_method: Method to update the widget text
        :return: None
        """

        def update_widget():
            translated_text = self.translate(translation_key)
            if update_method:
                update_method(translated_text)
            else:
                widget.configure(text=translated_text)

        widget._update_method = update_widget
        self.widgets.append(widget)
        update_widget()

    def update_all_widgets(self) -> None:
        """
        Update all bound widgets with the latest translation.

        :return: None
        """
        for widget in self.widgets:
            if hasattr(widget, '_update_method'):
                widget._update_method()

    def add_widget(self, widget) -> None:
        """
        Add a widget to the list of bound widgets for localisation update.

        :param widget: Widget to add
        :return: None
        """
        if widget not in self.widgets:
            self.widgets.append(widget)

    def get_locale(self) -> str:
        """
        Return the current locale.

        :return: Current locale.
        """
        return str(self.current_locale)

    def get_alphabet(self):
        """Return alphabet based on current language."""
        curr_lang = self.get_locale()
        if curr_lang:
            return ALPHABET_UK if curr_lang == 'uk' else ALPHABET_EN
