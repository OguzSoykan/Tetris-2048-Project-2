################################################################################
#                                                                              #
# The main program of Tetris 2048 Base Code                                    #
#                                                                              #
################################################################################

import lib.stddraw as stddraw  # for creating an animation with user interactions
from lib.picture import Picture  # used for displaying an image on the game menu
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid  # the class for modeling the game grid
from tetromino import Tetromino  # the class for modeling the tetrominoes
import random  # used for creating tetrominoes with random types (shapes)
import keyboard

# The main function where this program starts execution
def start():
   # set the dimensions of the game grid
   grid_h, grid_w = 20, 12
   # extra space on the right for pause button and score table
   extra_space = 5
   # set the size of the drawing canvas (the displayed window)
   canvas_h, canvas_w = 40 * grid_h, 40 * (grid_w + extra_space)
   stddraw.setCanvasSize(canvas_w, canvas_h)
   # set the scale of the coordinate system for the drawing canvas
   stddraw.setXscale(-0.5, grid_w + extra_space - 0.5)
   stddraw.setYscale(-0.5, grid_h - 0.5)

   # set the game grid dimension values stored and used in the Tetromino class
   Tetromino.grid_height = grid_h
   Tetromino.grid_width = grid_w
   # create the game grid
   grid = GameGrid(grid_h, grid_w, extra_space)
   # create the first tetromino to enter the game grid
   # by using the create_tetromino function defined below
   current_tetromino = create_tetromino()
   grid.current_tetromino = current_tetromino

   # display a simple menu before opening the game
   # by using the display_game_menu function defined below
   display_game_menu(grid_h, grid_w)

   # the main game loop
   while True:
      # check for any user interaction via the keyboard
      if stddraw.hasNextKeyTyped():  # check if the user has pressed a key
         key_typed = stddraw.nextKeyTyped()  # the most recently pressed key
         # if the left arrow key has been pressed
         if key_typed == "left":
            # move the active tetromino left by one
            current_tetromino.move(key_typed, grid)
         # if the right arrow key has been pressed
         elif key_typed == "right":
            # move the active tetromino right by one
            current_tetromino.move(key_typed, grid)
         # if the down arrow key has been pressed
         elif key_typed == "down":
            # move the active tetromino down by one
            # (soft drop: causes the tetromino to fall down faster)
            current_tetromino.move(key_typed, grid)
         elif key_typed == "up":
             # Call the rotate method of the current tetromino
             current_tetromino.rotate(grid)
         elif keyboard.is_pressed('shift'):
            # cause the active tetromino to hard drop
            current_tetromino.hard_drop(grid)
            # Process the landing of the tetromino immediately
            process_landing(current_tetromino, grid)

         # clear the queue of the pressed keys for a smoother interaction
         stddraw.clearKeysTyped()

      if stddraw.mousePressed():
          # get the coordinates of the most recent location at which the mouse
          # has been left-clicked
          mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
          # check if these coordinates are inside the button
          if mouse_x >= 15 and mouse_x <= 16 + 1:
              if mouse_y >= 18 and mouse_y <= 18 + 1:
                  restart_state()

      # move the active tetromino down by one at each iteration (auto fall)
      success = current_tetromino.move("down", grid)
      # lock the active tetromino onto the grid when it cannot go down anymore
      if not success:
         # get the tile matrix of the tetromino without empty rows and columns
         # and the position of the bottom left cell in this matrix
         tiles, pos = current_tetromino.get_min_bounded_tile_matrix(True)
         # update the game grid by locking the tiles of the landed tetromino
         game_over = grid.update_grid(tiles, pos)
         # end the main game loop if the game is over
         if game_over:
            display_game_menu_over(grid_h, grid_w)

         handle_free_tiles(grid)
         merge_tiles(grid)  # Call merge function here
         clear_full_rows(grid)
         reset_merged_flags(grid)
         # create the next tetromino to enter the game grid
         # by using the create_tetromino function defined below
         current_tetromino = create_tetromino()
         grid.current_tetromino = current_tetromino

      # display the game grid with the current tetromino
      grid.display()


def restart_state():
   # set the dimensions of the game grid
   grid_h, grid_w = 20, 12
   # set the size of the drawing canvas (the displayed window)
   extra_space = 5
   # set the size of the drawing canvas (the displayed window)
   canvas_h, canvas_w = 40 * grid_h, 40 * (grid_w + extra_space)
   # set the scale of the coordinate system for the drawing canvas
   stddraw.setXscale(-0.5, grid_w + extra_space - 0.5)
   stddraw.setYscale(-0.5, grid_h - 0.5)

   # set the game grid dimension values stored and used in the Tetromino class
   Tetromino.grid_height = grid_h
   Tetromino.grid_width = grid_w
   # create the game grid
   grid = GameGrid(grid_h, grid_w, extra_space)
   # create the first tetromino to enter the game grid
   # by using the create_tetromino function defined below
   current_tetromino = create_tetromino()
   grid.current_tetromino = current_tetromino

   # display a simple menu before opening the game
   # by using the display_game_menu function defined below
   display_game_menu(grid_h, grid_w)

   # the main game loop
   while True:
      # check for any user interaction via the keyboard
      if stddraw.hasNextKeyTyped():  # check if the user has pressed a key
         key_typed = stddraw.nextKeyTyped()  # the most recently pressed key
         # if the left arrow key has been pressed
         if key_typed == "left":
            # move the active tetromino left by one
            current_tetromino.move(key_typed, grid)
         # if the right arrow key has been pressed
         elif key_typed == "right":
            # move the active tetromino right by one
            current_tetromino.move(key_typed, grid)
         # if the down arrow key has been pressed
         elif key_typed == "down":
            # move the active tetromino down by one
            # (soft drop: causes the tetromino to fall down faster)
            current_tetromino.move(key_typed, grid)
         elif key_typed == "up":
             # Call the rotate method of the current tetromino
             current_tetromino.rotate(grid)
         elif keyboard.is_pressed('shift'):
            # cause the active tetromino to hard drop
            current_tetromino.hard_drop(grid)
            # Process the landing of the tetromino immediately
            process_landing(current_tetromino, grid)

         # clear the queue of the pressed keys for a smoother interaction
         stddraw.clearKeysTyped()

      if stddraw.mousePressed():
          # get the coordinates of the most recent location at which the mouse
          # has been left-clicked
          mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
          # check if these coordinates are inside the button
          if mouse_x >= 15 and mouse_x <= 16 + 1:
              if mouse_y >= 18 and mouse_y <= 18 + 1:
                  restart_state()

      # move the active tetromino down by one at each iteration (auto fall)
      success = current_tetromino.move("down", grid)

      # lock the active tetromino onto the grid when it cannot go down anymore
      if not success:
         # get the tile matrix of the tetromino without empty rows and columns
         # and the position of the bottom left cell in this matrix
         tiles, pos = current_tetromino.get_min_bounded_tile_matrix(True)
         # update the game grid by locking the tiles of the landed tetromino
         game_over = grid.update_grid(tiles, pos)
         # end the main game loop if the game is over
         if game_over:
            display_game_menu_over(grid_h, grid_w)

         handle_free_tiles(grid)
         merge_tiles(grid)  # Call merge function here
         clear_full_rows(grid)
         reset_merged_flags(grid)
         # create the next tetromino to enter the game grid
         # by using the create_tetromino function defined below
         current_tetromino = create_tetromino()
         grid.current_tetromino = current_tetromino

      # display the game grid with the current tetromino
      grid.display()

   # print a message on the console when the game is over


def gameover_state():
   # set the dimensions of the game grid
   grid_h, grid_w = 20, 12
   # set the size of the drawing canvas (the displayed window)
   extra_space = 5
   # set the size of the drawing canvas (the displayed window)
   canvas_h, canvas_w = 40 * grid_h, 40 * (grid_w + extra_space)
   # set the scale of the coordinate system for the drawing canvas
   stddraw.setXscale(-0.5, grid_w + extra_space - 0.5)
   stddraw.setYscale(-0.5, grid_h - 0.5)

   # set the game grid dimension values stored and used in the Tetromino class
   Tetromino.grid_height = grid_h
   Tetromino.grid_width = grid_w
   # create the game grid
   grid = GameGrid(grid_h, grid_w, extra_space)
   # create the first tetromino to enter the game grid
   # by using the create_tetromino function defined below
   current_tetromino = create_tetromino()
   grid.current_tetromino = current_tetromino

   # display a simple menu before opening the game
   # by using the display_game_menu function defined below
   display_game_menu(grid_h, grid_w)

   # the main game loop
   while True:
      # check for any user interaction via the keyboard
      if stddraw.hasNextKeyTyped():  # check if the user has pressed a key
         key_typed = stddraw.nextKeyTyped()  # the most recently pressed key
         # if the left arrow key has been pressed
         if key_typed == "left":
            # move the active tetromino left by one
            current_tetromino.move(key_typed, grid)
         # if the right arrow key has been pressed
         elif key_typed == "right":
            # move the active tetromino right by one
            current_tetromino.move(key_typed, grid)
         # if the down arrow key has been pressed
         elif key_typed == "down":
            # move the active tetromino down by one
            # (soft drop: causes the tetromino to fall down faster)
            current_tetromino.move(key_typed, grid)
         elif key_typed == "up":
             # Call the rotate method of the current tetromino
             current_tetromino.rotate(grid)
         elif keyboard.is_pressed('shift'):
            # cause the active tetromino to hard drop
            current_tetromino.hard_drop(grid)
            # Process the landing of the tetromino immediately
            process_landing(current_tetromino, grid)


         # clear the queue of the pressed keys for a smoother interaction
         stddraw.clearKeysTyped()

      if stddraw.mousePressed():
          # get the coordinates of the most recent location at which the mouse
          # has been left-clicked
          mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
          # check if these coordinates are inside the button
          if mouse_x >= 15 and mouse_x <= 16 + 1:
              if mouse_y >= 18 and mouse_y <= 18 + 1:
                  restart_state()

      # move the active tetromino down by one at each iteration (auto fall)
      success = current_tetromino.move("down", grid)
      # lock the active tetromino onto the grid when it cannot go down anymore
      if not success:
         # get the tile matrix of the tetromino without empty rows and columns
         # and the position of the bottom left cell in this matrix
         tiles, pos = current_tetromino.get_min_bounded_tile_matrix(True)
         # update the game grid by locking the tiles of the landed tetromino
         game_over = grid.update_grid(tiles, pos)
         # end the main game loop if the game is over
         if game_over:
            display_game_menu_over(grid_h, grid_w)

         handle_free_tiles(grid)
         merge_tiles(grid)  # Call merge function here
         clear_full_rows(grid)
         reset_merged_flags(grid)
         # create the next tetromino to enter the game grid
         # by using the create_tetromino function defined below
         current_tetromino = create_tetromino()
         grid.current_tetromino = current_tetromino

      # display the game grid with the current tetromino
      grid.display()

   # print a message on the console when the game is over

# A function for creating random shaped tetrominoes to enter the game grid

def create_tetromino():
   # the type (shape) of the tetromino is determined randomly
   tetromino_types = ['I', 'O', 'Z']
   random_index = random.randint(0, len(tetromino_types) - 1)
   random_type = tetromino_types[random_index]
   # create and return the tetromino
   tetromino = Tetromino(random_type)
   return tetromino

# A function for displaying a simple menu before starting the game
def display_game_menu(grid_height, grid_width):
   # the colors used for the menu
   background_color = Color(42, 69, 99)
   button_color = Color(25, 255, 228)
   text_color = Color(31, 160, 239)
   # clear the background drawing canvas to background_color
   stddraw.clear(background_color)
   # get the directory in which this python code file is placed
   current_dir = os.path.dirname(os.path.realpath(__file__))
   # compute the path of the image file
   img_file = current_dir + "/images/menu_image.png"
   # the coordinates to display the image centered horizontally
   img_center_x, img_center_y = (grid_width + 3.5) / 2, grid_height - 7
   # the image is modeled by using the Picture class
   image_to_display = Picture(img_file)
   # add the image to the drawing canvas
   stddraw.picture(image_to_display, img_center_x, img_center_y)
   # the dimensions for the start game button
   button_w, button_h = grid_width - 1.5, 2
   # the coordinates of the bottom left corner for the start game button
   button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
   # add the start game button as a filled rectangle
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
   # add the text on the start game button
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(25)
   stddraw.setPenColor(text_color)
   text_to_display = "Click Here to Start the Game"
   stddraw.text(img_center_x, 5, text_to_display)
   # the user interaction loop for the simple menu

   while True:
      # display the menu and wait for a short time (50 ms)
      stddraw.show(50)
      # check if the mouse has been left-clicked on the start game button
      if stddraw.mousePressed():
         # get the coordinates of the most recent location at which the mouse
         # has been left-clicked
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         # check if these coordinates are inside the button
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
               break  # break the loop to end the method and start the game

def display_game_menu_over(grid_height, grid_width):
   # the colors used for the menu
   background_color = Color(42, 69, 99)
   button_color = Color(25, 255, 228)
   text_color = Color(31, 160, 239)
   # clear the background drawing canvas to background_color
   stddraw.clear(background_color)

   # get the directory in which this python code file is placed
   current_dir = os.path.dirname(os.path.realpath(__file__))
   # compute the path of the image file
   img_file = current_dir + "/images/menu_image.png"

   # the coordinates to display the image centered horizontally
   img_center_x, img_center_y = (grid_width + 3.5) / 2, grid_height - 7
   # the image is modeled by using the Picture class
   image_to_display = Picture(img_file)

   # add the image to the drawing canvas
   stddraw.picture(image_to_display, img_center_x, img_center_y)
   # the dimensions for the start game button
   button_w, button_h = grid_width - 1.5, 2
   # the coordinates of the bottom left corner for the start game button
   button_blc_x, button_blc_y = img_center_x - button_w / 2, 4

   # add the start game button as a filled rectangle
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)

   # add the text on the start game button
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(25)
   stddraw.setPenColor(text_color)
   text_to_display = "Go To The Main Menu"
   stddraw.text(img_center_x, 5, text_to_display)

   #show game over on GUI when game is finish
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(40)
   stddraw.setPenColor(text_color)
   text_to_display = "Game Over"
   stddraw.text(img_center_x, 8, text_to_display)

   # the user interaction loop for the simple menu
   while True:
      # display the menu and wait for a short time (50 ms)
      stddraw.show(50)
      # check if the mouse has been left-clicked on the start game button
      if stddraw.mousePressed():
         # get the coordinates of the most recent location at which the mouse
         # has been left-clicked
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         # check if these coordinates are inside the button
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
               gameover_state()


def merge_tiles(grid):
    # Indicates if we should keep checking for merges
    continue_merging = True

    while continue_merging:
        continue_merging = False  # Assume no merge will happen (will set to True if a merge occurs)

        # Loop through the grid to find merges
        for col in range(grid.grid_width):
            for row in range(grid.grid_height - 1, -1, -1):
                current_tile = grid.tile_matrix[row][col]

                # Only consider non-null tiles that haven't already merged
                if current_tile and not current_tile.merged:
                    # Check the tile above it
                    above_row = row + 1
                    while above_row < grid.grid_height:
                        above_tile = grid.tile_matrix[above_row][col]
                        if above_tile is None:
                            # If the above tile is None, keep looking upwards
                            above_row += 1
                            continue

                        # Found a non-null tile, check for merge possibility
                        if above_tile.value == current_tile.value:
                            # Merge tiles
                            current_tile.value *= 2
                            current_tile.color = current_tile.determine_color()
                            grid.tile_matrix[above_row][col] = None  # Remove the merged above tile
                            current_tile.merged = True  # Mark as merged
                            grid.score += current_tile.value  # Update the score
                            continue_merging = True  # A merge occurred, continue checking
                        break  # Stop looking up if we find a non-matching tile or out of bounds

    # Reset the merged flags for all tiles
    for row in grid.tile_matrix:
        for tile in row:
            if tile:
                tile.merged = False

# start() function is specified as the entry point (main function) from which
# the program starts execution
def clear_full_rows(grid):
   for row in range(grid.grid_height):
      # Check if the row is full
      if None not in grid.tile_matrix[row]:
         grid.score += sum(tile.value for tile in grid.tile_matrix[row] if tile)  # Update the score
         # Clear the row and move down the above tiles
         for move_row in range(row, grid.grid_height - 1):
            grid.tile_matrix[move_row] = grid.tile_matrix[move_row + 1]
         grid.tile_matrix[grid.grid_height - 1] = [None] * grid.grid_width  # Empty the topmost row


def reset_merged_flags(grid):
   for row in grid.tile_matrix:
      for tile in row:
         if tile is not None:
            tile.merged = False

def handle_free_tiles(grid):
    moved_or_merged = True  # Initialize to enter the loop
    while moved_or_merged:
        moved_or_merged = False  # Reset flag at the start of each pass

        # First, allow all tiles to fall to their lowest possible positions
        for col in range(grid.grid_width):
            for row in range(1, grid.grid_height):  # Start from second row to bottom
                current_tile = grid.tile_matrix[row][col]
                if current_tile and grid.tile_matrix[row - 1][col] is None:
                    # Move tile down
                    grid.tile_matrix[row - 1][col] = current_tile
                    grid.tile_matrix[row][col] = None
                    moved_or_merged = True  # A tile has moved, so repeat the process

        # Then, check for merges after all tiles have fallen
        for col in range(grid.grid_width):
            for row in range(grid.grid_height - 1, 0, -1):  # Bottom to top
                current_tile = grid.tile_matrix[row][col]
                below_tile = grid.tile_matrix[row - 1][col] if row > 0 else None
                if current_tile and below_tile and current_tile.value == below_tile.value and not below_tile.merged:
                    # Merge tiles
                    below_tile.value *= 2
                    below_tile.color = below_tile.determine_color()
                    below_tile.merged = True
                    grid.tile_matrix[row][col] = None  # Remove the merged tile
                    grid.score += below_tile.value  # Update the score
                    moved_or_merged = True  # A merge has happened, repeat the process

        # Reset merged flags after each pass through the grid
        for col in range(grid.grid_width):
            for row in range(grid.grid_height):
                if grid.tile_matrix[row][col]:
                    grid.tile_matrix[row][col].merged = False


# Make sure to call this function at the correct point in your game loop
def try_merge(grid, row, col):
    # This function tries to merge the current tile with the one below it, if possible
    current_tile = grid.tile_matrix[row][col]
    below_tile = grid.tile_matrix[row - 1][col] if row > 0 else None
    # If the below tile exists and has the same value, merge them
    if below_tile and current_tile.value == below_tile.value:
        below_tile.value *= 2
        below_tile.color = below_tile.determine_color()
        grid.tile_matrix[row][col] = None
        grid.score += below_tile.value  # Update the score
        return True  # Indicate that a merge occurred
    return False  # Indicate that no merge occurred


def process_landing(tetromino, grid):
    tiles, pos = tetromino.get_min_bounded_tile_matrix(True)
    game_over = grid.update_grid(tiles, pos)
    if not game_over:
        merge_tiles(grid)
        clear_full_rows(grid)
        reset_merged_flags(grid)
        # Create the next tetromino and set it as the current one
        grid.current_tetromino = create_tetromino()

    return True

if __name__ == '__main__':
   start()
