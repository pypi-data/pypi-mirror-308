#!/usr/bin/env python3
"""
This module provides a command-line interface (CLI) for generating and displaying QR codes
in the terminal. It uses the argparse library to handle command-line arguments and the 
QRCLI class to generate and display the QR code.
"""

import argparse
from ezqrcli import QRCLI


def main():
    """
    Main function to parse command-line arguments and generate a QR code.
    It creates an instance of QRCLI with the provided arguments and displays the QR code.

    This function sets up an argument parser to handle the following arguments:
    - url: The URL to encode in the QR code.
    - top-text: Optional text to display above the QR code. Defaults to "Scan this QR code:".
    - bottom-text: Optional text to display below the QR code. Defaults to the first 50 char of URL
    - center-weight: A float value to adjust the centering of the QR code. Default is 1.0.
    """
    parser = argparse.ArgumentParser(
        description="Generate and display a QR code in the terminal with optional text."
    )
    parser.add_argument("url", help="The URL to encode in the QR code.")
    parser.add_argument(
        "-t",
        "--top-text",
        default="Scan this QR code:",
        help="Text to display above the QR code.",
    )
    parser.add_argument(
        "-b",
        "--bottom-text",
        help="Text to display below the QR code. Defaults to the URL, truncated to 50 chars.",
    )
    parser.add_argument(
        "-w",
        "--center-weight",
        type=float,
        default=1.0,
        help="Weight to adjust the centering of the QR code. Default is 1.0.",
    )

    args = parser.parse_args()

    qr_cli = QRCLI(
        url=args.url,
        top_text=args.top_text,
        bottom_text=args.bottom_text,
        center_weight=args.center_weight,
    )

    qr_cli.display_qr()


if __name__ == "__main__":
    main()
