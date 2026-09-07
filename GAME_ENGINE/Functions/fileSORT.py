import os

def get_files(folder_path):
    """
    Returns a list containing the names of all files in the specified folder.
    """
    file_type=".sngf"

    file_names = []
    try:
        for item in os.listdir(folder_path):
            if "".join(item[-5:]) == file_type:
                item_path = os.path.join(folder_path, item)
                if os.path.isfile(item_path):
                    file_names.append(item)

    except os.error:
        os.mkdir(folder_path)
        
        for item in os.listdir(folder_path):
            if "".join(item[-5:]) == file_type:
                item_path = os.path.join(folder_path, item)
                if os.path.isfile(item_path):
                    file_names.append(item)
    
    return file_names