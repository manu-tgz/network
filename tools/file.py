from pathlib import Path
from os.path import exists
from os import mkdir

def get_line(lines):
    return [ l.strip() for l in lines if l.strip()!="" ]

def save(file_name : str, dir_name : str, to_save : list[str]):
    
    path = Path(dir_name,file_name) 
    folder_path = Path(dir_name)

    if not exists(folder_path):
        mkdir(folder_path)

    with open(path, "w") as fd:
        fd.writelines([ l+"\n" for l in to_save])