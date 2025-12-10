"""
Documentation:
        VideoAudioSeperatorService Delete Download Data Module. This module provides functionality to delete files
        in a specified directory, keeping folders intact.
    Returns:
        None: This function does not return any value.
"""

# Import Headers
import os

# functions Portion's
def deleteFilesInDirectory(directory_path: str) -> None:
    """
    Deletes all files in the given directory (non-recursive).
    Keeps folders intact.
    """
    if not os.path.exists(directory_path):
        print(f"Directory '{directory_path}' does not exist.")
        return
    
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
            
# Example usage (remove in production)
# if __name__ == "__main__":
#     deleteFilesInDirectory("Audio")