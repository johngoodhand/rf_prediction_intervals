from pathlib import Path


def generate_path(folder, file_name):
    """
    Generates path to a file using pathlib.

    :param folder: Folder name to load data from.
    :param filename: Filename of the csv.
    :return: Desired dataframe.
    """

    # This should provide the base path to the directory on your computer
    base_path = Path(__file__).parent.parent

    # Generate path.
    file_path = base_path / folder / file_name
    
    return file_path