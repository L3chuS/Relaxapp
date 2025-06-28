import os
import sys

# Function to get absolute path.
def get_resource_path(relative_path):
    try:
        # When .exe is executed.
        base_path = sys._MEIPASS
    except AttributeError:
        # When script is executed.
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)
