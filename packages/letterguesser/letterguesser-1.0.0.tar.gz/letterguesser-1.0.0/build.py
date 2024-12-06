"""Build script"""

import sys
import subprocess


def create_mo_files():
    """Compile pyBabel localisation files."""
    try:
        print("Compiling translations:")
        subprocess.run(
            [
                "pybabel",
                "compile",
                "--use-fuzzy",
                "--directory",
                "package_name/translations"
            ],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error compiling translations: {e}")
        sys.exit(1)
