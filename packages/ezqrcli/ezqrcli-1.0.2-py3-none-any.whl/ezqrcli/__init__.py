"""
This module initializes the ezqrcli package by importing the QRCLI class and the 
module-level docstring from the qr_cli module.

Imports:
    QRCLI (from .qr_cli): The main class for handling QR code operations in the CLI.
    qr_cli_doc (from .qr_cli): The module-level docstring from the qr_cli module.
"""
from .qr_cli import __doc__ as qr_cli_doc
from .qr_cli import QRCLI
