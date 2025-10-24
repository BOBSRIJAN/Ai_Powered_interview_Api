import os

def delete_files_in_directory(directory_path: str) -> None:
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
                print(f"🗑️ Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

