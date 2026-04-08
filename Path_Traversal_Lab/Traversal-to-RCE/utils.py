from pathlib import Path
import os

BASE = os.getenv("BASE")

def val(input):
    return os.path.normpath(input)

def writer(path, data):
    path = val(path)
    if path is None:
        return None
    file_path = Path(BASE) / path
    with open(file_path, 'wb') as f:
        f.write(data)
        return True
    return False

