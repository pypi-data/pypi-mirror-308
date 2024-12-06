# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring, unused-import, protected-access, redefined-outer-name, line-too-long, subprocess-run-check
import sys
import subprocess
import importlib


def ensure_qrcode():
    """
    Ensures that the 'qrcode' package is installed and available for import.
    Attempts to import the 'qrcode' module. If the module is not found,
    it installs it using pip. After installation, it verifies the installation
    by attempting to import the module again.

    Returns:
        module: The 'qrcode' module if it is successfully imported.

    Raises:
        ImportError: If the 'qrcode' module cannot be imported after installation attempt.
    """
    try:
        # Attempt to import 'qrcode' directly
        return importlib.import_module("qrcode")
    except ImportError as e:
        print("QRCode module not found. Installing via pip...")

        # Install the qrcode module with pip, using `sys.executable` to ensure compatibility
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "qrcode"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # Check if the installation was successful
        if result.returncode != 0:
            raise ImportError(
                "Failed to install 'qrcode'. Please install it manually."
            ) from e

    # Attempt to import 'qrcode' again after installation
    try:
        return importlib.import_module("qrcode")
    except ImportError as e:
        raise ImportError(
            "Failed to import 'qrcode' after installation. Please install it manually."
        ) from e
