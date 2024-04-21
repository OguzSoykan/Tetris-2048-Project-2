from lib.color import Color
import lib.stddraw as stddraw  # Assuming stddraw is set up for graphical operations
import random

class Tile:
    def __init__(self, value=None):
        if value is None:
            self.value = random.choice([2, 4])  # Randomly assign a value of 2 or 4
        else:
            self.value = value  # Use the provided value
        self.merged = False
        self.color = self.determine_color()


    def determine_color(self):
        # Example color coding based on value, adjust as necessary
        color_mapping = {
            2: Color(238, 228, 218),
            4: Color(237, 224, 200),
            8: Color(242, 177, 121),
            16: Color(245, 149, 99),
            32: Color(246, 124, 95),
            64: Color(246, 94, 59),
            128: Color(237, 207, 114),
            256: Color(237, 204, 97),
            512: Color(237, 200, 80),
            1024: Color(237, 197, 63),
            2048: Color(237, 194, 46),
            # Continue with other values if needed...
        }
        return color_mapping.get(self.value, Color(204, 192, 179))  # Default color


    def draw(self, position, tile_size=0.5):
        # Set the color for the tile
        stddraw.setPenColor(self.color)
        # Draw the filled square for the tile
        stddraw.filledSquare(position.x, position.y, tile_size)

        # Draw the tile's outline with the explicit RGB value
        stddraw.setPenColor(Color(0, 100, 200))
        stddraw.setPenRadius(0.002)  # Set pen radius for outline thickness
        stddraw.square(position.x, position.y, tile_size)

        # Draw the tile's value in the center
        stddraw.setPenColor(Color(0, 0, 0))  # RGB values for black
        stddraw.setFontSize(18)
        stddraw.text(position.x, position.y, str(self.value))

        stddraw.setPenRadius()  # Reset the pen radius to its default value after drawing the outline