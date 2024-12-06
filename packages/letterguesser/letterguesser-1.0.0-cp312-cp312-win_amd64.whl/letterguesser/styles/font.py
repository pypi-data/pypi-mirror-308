"""
Font settings and text sizes for LetterGuesser.

Defines font types, sizes, and line heights used across the application,
ensuring consistency and readability in the UI.
"""

# general settings
font: str = 'Segoe UI'
text_large: int = 18
text_medium: int = 16
text_small: int = 14

# line-height
height_multiplier: float = 1.3
text_small_height:  int = int(text_small * height_multiplier)
text_medium_height: int = int(text_medium * height_multiplier)
text_large_height:  int = int(text_large * height_multiplier)
