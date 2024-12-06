"""Congifuration module for the t_page_object package."""
from pathlib import Path


class BotConfig:
    """Class for configuration."""

    output_folder = Path().cwd() / "output"
    dev_safe_mode = True
    capture_screenshot_on_error = True

    @classmethod
    def configure(cls, **kwargs):
        """Set configuration variables.

        Args:
            output_folder: The folder where the output files are saved. Defaults to "output"
            dev_safe_mode: If True, the bot will run in safe mode. Defaults to True.
            capture_screenshot_on_error: If True, the bot will capture a
                screenshot if an error occurs. Defaults to True.

        Raises:
            AttributeError: If an invalid configuration option is provided.
        """
        for key, value in kwargs.items():
            if hasattr(cls, key):
                setattr(cls, key, value)
            else:
                raise AttributeError(f"Invalid configuration option: {key}")
