from object.pixel import Pixel
from utils.logging_utils import logger
from utils.color_utils import sequence_to_code
from utils.list_utils import collapse

LOGGER = logger('object')


class Sequence:
    """The sequences of colors and brightness values from an image."""

    def __init__(self, image, center_coord, coordinates):
        self.image = image
        self.center_coord = center_coord
        self.coordinates = coordinates
        self.colors = self.get_sequence_colors()
        self.brightness_values = self.get_sequence_brightness_values()
        self.sequence = self.calculate_sequence()

    def get_sequence_colors(self):
        """Get the pixel color for each coordinate.

        Returns:
            str: The integer representation of a color sequence.
        """
        # Get the color of each pixel.
        colors = [Pixel(self.image, coord).color for coord in self.coordinates]

        # Collapse adjacent duplicates into a single element.
        return collapse(colors, self.center_coord.color)

    def get_sequence_brightness_values(self):
        """Get the brightness for each coordinate.

        Returns:
            str: The sequence of brightness values.
        """
        # Get the brightness for each pixel.
        brightness_values = [
            Pixel(self.image, coord).brightness for coord in self.coordinates
        ]

        # Collapse adjacent duplicates into a single element.
        return collapse(brightness_values, self.center_coord.brightness)

    def calculate_sequence(self):
        """Get the code corresponding to the colors in the sequence.

        Returns:
            str: The integer representation of a color sequence.
        """
        return {
            "code": sequence_to_code(self.colors),
            "colors": self.colors,
            "brightnesses": self.brightness_values
        }
