from math import hypot
from profilehooks import timecall

from obj.ring import Ring
from obj.coordinate import Coordinate
from obj.direction import Direction
from obj.overlay import Overlay
from obj.pixel import Pixel
from obj.color_sequence import ColorSequence


class Dashed(Ring):
    """
    A ring based on the radii and edge points of two circles. This ring
    bounded by the same color inside and surrounding.

    Using a simple method of linearly analyzing pixels determine if a
    ring exists in an image. If a ring is found to be in the image,
    determine the two colors that the ring consists of.

    The description for this simple method can be found here:
    https://gist.github.com/axelthorstein/337312d5030af4b965e5a40271ba0361
    """

    def __init__(self, image, starting_coords, debug=True):
        self.image = image
        self.debug = debug
        self.overlay = Overlay(image, starting_coords)
        self.center_point = Pixel(image, starting_coords)
        self.center_radii = []
        self.ring_radii = []

    def create(self):
        """Set all of the dynamic attributes of the Ring.
        """
        self.approximate_color_sequence()

        if not self.color_sequence.is_valid:
            print("Approximation failed.")
            self.inner_edges = self.get_inner_edges()
            self.outer_edges = self.get_outer_edges()
            self.inner_radius = self.get_inner_radius()
            self.outer_radius = self.get_outer_radius()
            self.radius = self.get_mid_ring_radius()

            self.color_sequence = ColorSequence(self.image, self.center_point,
                                                self.radius)

    def approximate_color_sequence(self):
        """Use the overlay to approximate the color sequence.

        By using the overlays assumed radius of the ring we can potentially
        find the color sequence with minimal calculations. With only the center
        point and the radius we can retrieve the color values for every pixel
        on the circumference.

        Returns:
            list of str: The appoximated color sequence.
        """
        self.radius = self.overlay.radius
        self.color_sequence = ColorSequence(
            self.image, self.overlay.center_point, self.overlay.radius)

    def is_valid(self):
        """Determine if the ring is valid.

        Returns:
            bool: Whether the ring is valid.
        """
        # TODO: Add real validity check.
        return self.color_sequence.is_valid

    def get_inner_edge(self, coordinate, directions, direction):
        """Return the inner edge of the ring.

        Walk from the starting coordinate to in the given direction until an
        edge is found. Then with the coordinates and colors of this edge update
        the attributes of the ring.

        Args:
            coordinate: (Coordinate): Interface for pixel coordinate movements.
            directions (dictionary): Mapping of directions to movement methods.
            depth: The direction to move.

        Returns:
            tuple of int: The coordinates of the inner edge.
        """
        inner_pixel = coordinate.probe(self.center_point.coords,
                                       directions[direction])

        center_radius = hypot(self.center_point.x - inner_pixel.x,
                              self.center_point.y - inner_pixel.y)

        self.center_radii.append(center_radius)

        # TODO: Fix center correction.
        # if direction in ["left", "right", "up", "down"]:
        #     self.update_center_coords(inner_pixel.coords)

        return inner_pixel.coords

    def get_outer_edge(self, coordinate, directions, direction):
        """Return the outer edge of the ring.

        Walk from the starting coordinate to in the given direction until an
        edge is found. The center coordinates will have already been adjusted
        to the real center, so we don't need to update them based on the outer
        coordinates.

        Args:
            coordinate: (Coordinate): Interface for pixel coordinate movements.
            directions (dictionary): Mapping of directions to movement methods.
            depth: The direction to move.

        Returns:
            tuple of int: The coordinates of the outer edge.
        """
        starting_coords = directions[direction](self.inner_edges[direction])

        outer_pixel = coordinate.probe(starting_coords, directions[direction])
        ring_radius = hypot(starting_coords[0] - outer_pixel.x,
                            starting_coords[1] - outer_pixel.y)
        self.ring_radii.append(ring_radius)

        return outer_pixel.coords

    def get_edges(self, get_edge, depth):
        """Return the edges of the ring.

        On each iteration update the value of the center coordinates based on
        the new information from the last edge.

        To find the outer edge we begin moving from the inner edge until
        we reach the original color. We need to increment the inner edge
        by one because it returns the pixel before the color change, so it
        would immeadiately exit otherwise.

        Args:
            get_edge (method): The method for getting edges.
            depth: The inner or outer depth.

        Returns:
            dictionary: The edges.
        """
        edges = {}
        directions = Direction.get_directions()
        coordinate = Coordinate(self.image, depth=depth)

        for direction in directions:
            edges[direction] = get_edge(coordinate, directions, direction)

        return edges

    def get_inner_edges(self):
        """Return the inner edges of the ring.

        Returns:
            dictionary: The inner edges.
        """
        depth = "inner"
        get_edge = self.get_inner_edge

        return self.get_edges(get_edge, depth)

    def get_outer_edges(self):
        """Return the outer edges of the ring.

        Returns:
            dictionary: The outer edges.
        """
        self.update_center_coords()
        depth = "outer"
        get_edge = self.get_outer_edge

        return self.get_edges(get_edge, depth)

    def get_inner_radius(self):
        """Find the radius of the inner circle.

        Returns:
            int: The inner radius.
        """
        return sum(self.center_radii) / len(self.center_radii)

    def get_outer_radius(self):
        """Find the radius of the outer circle.

        Returns:
            int: The outer radius.
        """
        return sum(self.ring_radii) / len(self.ring_radii)

    def get_mid_ring_radius(self):
        """Find the radius of the middle of the outer circle.

        Returns:
            int: The average radius.
        """
        return int(self.inner_radius + (self.outer_radius / 2))

    def get_center_offset(self, coords, radius, axis):
        """Find the offset from the coordinate to the center.

        Use the given radius to determine how far away the new coordinate
        is from the center coordinate on either the x or y axis. Compare
        the distance to the radius and return how much the center should
        be adjusted in order for the new coordinate to have matched the
        center coordinate.

        Args:
            center (tuple of int): The coordinates of the ring center.
            coords (tuple of int): The coordinates of the ring edge.
            axis (int): The x or y axis.

        Returns:
            int: The offset to adjust the center coordinate.
        """
        offset = 0

        if self.center_point.coords[axis] < coords[axis]:
            offset += abs(self.center_point.coords[axis] -
                          coords[axis]) - radius
        elif self.center_point.coords[axis] > coords[axis]:
            offset += radius - abs(self.center_point.coords[axis] -
                                   coords[axis])

        return offset

    def update_center_coords(self):
        """Set the center coordinates of the circle.

        Update the ring's center coordinates as the inner edges are found.
        This will provide more accurate results as it progresses.

        Args:
            coords (tuple of int): The coordinates of the ring edge.
        """
        x_offset = int(
            (self.inner_edges['right'][0] - self.inner_edges['left'][0]) / 2)
        y_offset = int(
            (self.inner_edges['down'][1] - self.inner_edges['up'][1]) / 2)
        x = self.inner_edges['left'][0] + x_offset
        y = self.inner_edges['up'][1] + y_offset

        self.center_point.update_coords(x, y)

    # def update_center_coords(self, coords):
    #     """Set the center coordinates of the circle.

    #     Update the ring's center coordinates as the inner edges are found.
    #     This will provide more accurate results as it progresses.

    #     Args:
    #         coords (tuple of int): The coordinates of the ring edge.
    #     """
    #     x, y = 0, 1

    #     x_offset = self.get_center_offset(coords, self.overlay.inner_radius, x)
    #     y_offset = self.get_center_offset(coords, self.overlay.inner_radius, y)

    #     self.center_point.coords = (self.center_point.x + x_offset,
    #                                 self.center_point.y + y_offset)

    def __str__(self):
        """Return a description of the dashed ring.

        Returns:
            str: The string representation of the dashed ring.
        """
        desc = f'\n{self.__class__.__name__}:\n'

        for attribute in self.__dict__:
            key = attribute.replace('_', ' ').capitalize()
            desc += f'    {key}: {self.__dict__[attribute]},\n'

        return desc

    def __repr__(self):
        """Return a description of the dashed ring.

        Returns:
            str: The string representation of the dashed ring.
        """
        return self.__str__()
