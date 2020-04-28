from typing import Tuple


def convert_coordinates(coordinates: Tuple[int, int], coordinates_scale: Tuple[int, int], final_scale: Tuple[int, int]):
    """
    Converts a coordinate from coordinates_scale to final_scale
    """
    x, y = coordinates
    coordinates_scale_x, coordinates_scale_y = coordinates_scale
    scale_x, scale_y = final_scale
    final_x = x * (scale_x / coordinates_scale_x)
    final_y = y * (scale_y / coordinates_scale_y)
    return int(final_x), int(final_y)
