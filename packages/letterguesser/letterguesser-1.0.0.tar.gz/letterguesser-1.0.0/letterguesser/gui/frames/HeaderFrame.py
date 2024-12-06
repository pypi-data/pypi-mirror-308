"""
HeaderFrame displays the app title and allows language selection.

Extends BaseFrame with title display and language toggle, enabling
dynamic language changes.
"""

import customtkinter as ctk

from letterguesser.config import APP_DEFAULT_LANGUAGE, APP_TITLE
from letterguesser.styles.font import font, text_large, text_large_height
from letterguesser.styles.padding import pad_0, pad_4

from .BaseFrame import BaseFrame


class HeaderFrame(BaseFrame):
    """
    Frame for displaying the app title and providing language toggle.

    HeaderFrame includes a title display and a toggle button to switch
    languages, allowing users to dynamically change the interface language.
    """

    def __init__(self, parent, **kwargs):
        """
        Initialize HeaderFrame.

        :param parent: Parent tkinter object for the frame.
        """
        super().__init__(parent, **kwargs)

        # app title
        self.app_name_label = ctk.CTkLabel(
            self,
            height=text_large_height,
            text=APP_TITLE,
            font=ctk.CTkFont(
                family=font,
                size=text_large
            )
        )
        self.add_widget(
            self.app_name_label,
            side='left',
            fill='y',
            expand=True,
            pady=pad_4,
            padx=(pad_4, pad_0)
        )

        # language selector
        self.language_selector = ctk.CTkSegmentedButton(
            self,
            values=['Ukrainian', 'English'],
            command=self.change_language
        )

        self.language_selector.set(APP_DEFAULT_LANGUAGE)
        self.add_widget(
            self.language_selector,
            side='left',
            fill=None,
            expand=False,
            padx=(pad_0, pad_4)
        )

    def toggle_langauge(self, event=None):
        """Toggle language between English and Ukrainian."""
        curr_lang = self.localisation.get_locale()

        if curr_lang == "en":
            self.language_selector.set('Ukrainian')
            self.localisation.load_language('uk')
        else:
            self.language_selector.set('English')
            self.localisation.load_language('en')

        self.manager.reset_experiment()

    def change_language(self, language):
        """
        Change the application language based on selection.

        :param language: 'English' or 'Ukrainian'.
        """
        lang_code = "en" if language == 'English' else "uk"
        self.localisation.load_language(lang_code)

        self.manager.reset_experiment()
