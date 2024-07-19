from datetime import datetime
import os
"""
This module contains utility functions for the traffic monitoring system
File storage is used to store the evidence of traffic violations
"""

# Function to get list of jpg image files from a directory
def get_image_files(directory):
    """
    Returns directory objects of image files in the directory
    
    Parameters:
    - directory (str): The directory to search for image files
    
    Returns:
    - list: A list of directory objects of image files
    """
    return [f for f in os.scandir(directory) if f.name.lower().endswith('.png')]

def split_into_columns(input_list, cols=3):
    """
    Splits a list of elements into multiple columns

    Parameters:
    - input_list (list): The list to split.
    - cols (int): The number of columns to split the list into.

    Returns:
    - columns (list): The list of columns
    """
    columns = [[] for _ in range(cols)]
    
    # Distribute the elements into columns
    for index, value in enumerate(input_list):
        column_index = index % cols
        columns[column_index].append(value)
    
    return columns

def split_list(input_list, chunk_size):
    """
    Splits a list into chunks of the specified size

    Parameters:
    - input_list (list): The list to split.
    - chunk_size (int): The size of each chunk.

    Returns:
    - chunked_list (list): The list of chunks.    
    """
    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]

def calculate_image_size(window_width, window_height, n_columns, margin=10):
    """
    Calculate the appropriate image size for n columns within a window size.

    Parameters:
    - window_width (int): The width of the window.
    - window_height (int): The height of the window.
    - n_columns (int): The number of columns.
    - margin (int): The margin between images (default is 10).

    Returns:
    - image_width (int): The calculated width for each image.
    - image_height (int): The calculated height for each image.
    """
    # Calculate the total margin space needed for n columns
    total_margin_space = margin * (n_columns + 1)
    
    # Calculate the width of each image
    image_width = (window_width - total_margin_space) // n_columns
    
    # Assuming square images for simplicity, calculate the height of each image
    # If non-square images are required, additional logic will be needed
    image_height = image_width
    
    return image_width, image_height


