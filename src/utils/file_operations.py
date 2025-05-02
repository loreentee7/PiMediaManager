def move_file(source, destination):
    import shutil
    shutil.move(source, destination)

def copy_file(source, destination):
    import shutil
    shutil.copy(source, destination)

def cut_file(source, destination):
    import shutil
    shutil.move(source, destination)

def paste_file(source, destination):
    import shutil
    shutil.copy(source, destination)

def explore_directory(path):
    import os
    return os.listdir(path)