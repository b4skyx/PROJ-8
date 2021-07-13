# Importing pathlib to get absolute path
from pathlib import Path
from utilities import encryption as utilenc

cwd = Path(__file__).parents[1]
cwd = str(cwd)

def upload_document(document_id, data):
    try:
        with open(f"{cwd}/documents/{document_id}", "w") as f:
            f.write(data)
            return True
    except:
        return False
