"""A class to generate and display QR codes in the terminal with optional text."""

import io
import os
from ezqrcli.util import ensure_qrcode


class QRCLI:
    """
    A class to generate and display QR codes in the terminal with optional text.
    Attributes:
        url (str): The URL to encode in the QR code.
        top_text (str): Text to display above the QR code. Default is "Scan this QR code:".
        bottom_text (str): Text to display below the QR code. Defaults to first 50 chars of URL.
        center_weight (float): Weight to adjust the centering of the QR code. Default is 1.0.
        maxwidth (int): Maximum width of the QR code.
        _raw_qr (str): Raw QR code data.
        qr_text (str): Processed QR code text.
        formatted_qr (str): Formatted QR code with padding and text.
        padding (str): Padding to center the QR code vertically.
        width (int): Width of the terminal.
        height (int): Height of the terminal.
        centered_qr_text (str): Centered QR code text.
        _raw_lines (list): List of raw QR code lines.
        qrcode (module): QR code module.
    Methods:
        ensure_qrcode(): Static method to install the qrcode module.
        _ensure_qrcode(): Attempts to import the qrcode module, installs it if not found.
        _update(): Updates the QR code and its attributes.
        _get_padding() -> str: Calculates the padding to center the QR code vertically.
        _get_width() -> int: Calculates the width of the terminal.
        _get_height() -> int: Calculates the height of the terminal.
        _generate_qr(): Generates the QR code from the URL.
        _process_qr(): Processes the raw QR code to center its lines.
        _center_qr() -> str: Centers the QR code text and adds top and bottom text.
        _format_qr(): Formats the QR code with padding and text.
        get_formatted_qr() -> str: Returns the formatted QR code.
        get_raw_qr() -> str: Returns the raw QR code.
        display_qr(): Displays the formatted QR code in the terminal.
    """

    def __init__(
        self,
        url: str,
        top_text: str = "Scan this QR code:",
        bottom_text: str = "",
        center_weight: float = 1.0,
    ):
        self.maxwidth = 0
        self.url = url
        self.top_text = top_text
        self.bottom_text = bottom_text
        if not bottom_text:
            self.bottom_text = f"{url[:50]}..." if len(url) > 50 else url
        self.center_weight = center_weight
        self._raw_qr = ""
        self.qr_text = ""
        self.formatted_qr = ""
        self.padding = ""
        self.width = 0
        self.height = 0
        self.centered_qr_text = ""
        self._raw_lines = []
        self.qrcode = None
        self._ensure_qrcode()
        self._update()

    @staticmethod
    def ensure_qrcode():
        """
        Installs the qrcode package if it is not already installed.

        This method calls the `ensure_qrcode` function to ensure that the
        qrcode package is available for use.

        Returns:
            None
        """
        ensure_qrcode()

    def _ensure_qrcode(self):
        # pylint: disable=undefined-variable
        try:
            self.qrcode = qrcode  # type: ignore
        except NameError:
            self.__class__.ensure_qrcode()
            self.qrcode = __import__("qrcode")  # type: ignore

        # pylint: enable=undefined-variable

    def _update(self):
        """
        Updates the QR code properties and regenerates the QR code.

        This method performs the following steps:
        1. Updates the padding of the QR code.
        2. Updates the width of the QR code.
        3. Updates the height of the QR code.
        4. Generates a new QR code.
        5. Processes the generated QR code.
        6. Formats the QR code for output.
        """
        self.padding = self._get_padding()
        self.width = self._get_width()
        self.height = self._get_height()
        self._generate_qr()
        self._process_qr()
        self._format_qr()

    def _get_padding(self) -> str:
        """
        Calculate and return the padding as a string of newline characters.

        The padding is determined by taking half of the height (rounded down) 
        and converting it to a string of newline characters.

        Returns:
            str: A string containing newline characters for padding.
        """
        return "\n" * int(0.5 * (self._get_height()))

    def _get_width(self) -> int:
        """
        Calculate the width for the QR code based on the terminal size and center weight.

        Returns:
            int: The calculated width for the QR code.
        """
        return int(os.get_terminal_size().columns // self.center_weight)

    def _get_height(self) -> int:
        """
        Calculate the height for the QR code display based on the terminal size.

        Returns:
            int: The height of the terminal minus 30 lines.
        """
        return os.get_terminal_size().lines - 30

    def _generate_qr(self):
        """
        Generates a QR code from the provided URL and stores its ASCII representation.

        This method creates a QR code using the `qrcode` library, adds the provided URL
        data to it, and then generates an ASCII representation of the QR code. 
        
        The ASCII representation is stored in the `_raw_qr` attribute, and the individual
        lines of the ASCII QR code are stored in the `_raw_lines` attribute. 
        
        Additionally, the maximum width of the QR code lines is calculated and stored in 
        the `maxwidth` attribute.
        """
        qr = self.qrcode.QRCode()
        qr.add_data(self.url)
        f = io.StringIO()
        qr.print_ascii(out=f)
        f.seek(0)
        lines = f.readlines()
        if lines:
            self.maxwidth = max(map(len, lines))
            self._raw_lines = [line.strip() for line in lines]
        else:
            self.maxwidth = 0
            self._raw_lines = []

        self._raw_qr = f.getvalue()

    def _process_qr(self):
        """
        Processes the raw QR code lines by centering each line based on the maximum width
        and joins them into a single string with newline characters.

        Attributes:
            qr_text (str): The processed QR code text with each line centered.
        """
        self.qr_text = "\n".join(
            [line.center(self.maxwidth) for line in self._raw_lines]
        )

    def _center_qr(self) -> str:
        """
        Centers the QR code text within the specified width and adds padding.

        This method centers each line of the QR code text based on the width
        obtained from the `_get_width` method. It then constructs a string
        that includes the top text, the centered QR code text, and the bottom
        text, all centered within the maximum width and padded appropriately.

        Returns:
            str: The formatted string with the centered QR code text, top text,
                and bottom text, including padding.
        """
        term_center = int(os.get_terminal_size().columns // self.center_weight) - 2
        
        qrcode_text = '\n  '.join([
            f"{self.top_text.center(term_center)}",
            *[
                line.center(term_center)
                for line in [
                    ea.center(self.maxwidth) 
                    for ea in self._raw_qr.splitlines()
                ]
            ],
            f"{self.bottom_text.center(term_center)}"
        ])

        return f"{self.padding}{qrcode_text}{self.padding}"
    
    def _format_qr(self):
        """
        Formats the QR code by setting the bottom text and centering the QR code.

        If `bottom_text` is not provided, it will be set to the first 50 characters
        of the URL followed by '...' if the URL is longer than 50 characters. Otherwise,
        it will be set to the full URL.

        The formatted QR code is then centered using the `_center_qr` method.

        Returns:
            None
        """
        if not self.bottom_text:
            self.bottom_text = f"{self.url[:50]}..." if len(self.url) > 50 else self.url
        self.formatted_qr = self._center_qr()

    def get_formatted_qr(self) -> str:
        """
        Generates and returns the formatted QR code as a string.

        This method updates the QR code data and returns the formatted QR code.

        Returns:
            str: The formatted QR code.
        """
        self._update()
        return self.formatted_qr

    def get_raw_qr(self) -> str:
        """
        Generate and return the raw QR code string.

        This method updates the QR code data and returns the raw QR code string.

        Returns:
            str: The raw QR code string.
        """
        self._update()
        return self._raw_qr

    def display_qr(self):
        """
        Updates the QR code and prints the formatted QR code to the console.

        This method calls the `_update` method to refresh the QR code data and then
        prints the formatted QR code stored in `self.formatted_qr`.
        """
        self._update()
        print(self.formatted_qr)
