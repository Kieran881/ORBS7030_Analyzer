def cleaner(folder_path: str) -> None:
    """
    Cleans up the specified folder by removing all files and subdirectories.

    Args:
        folder_path (str): The path to the folder to be cleaned.
    """
    import os
    import shutil

    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} does not exist.")
        return

    try:
        # Remove all files and subdirectories in the folder
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
        print(f"Successfully cleaned the folder: {folder_path}")
    except Exception as e:
        print(f"An error occurred while cleaning the folder: {e}")