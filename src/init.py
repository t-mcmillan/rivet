import os

def createVault(vaultPath: str):
    # create data folder
    dataPath = vaultPath+"data"
    os.makedirs(dataPath, exist_ok=True)

    # create notesembedded path
    notesEmbeddedPath = dataPath+"/notes_embedded"
    os.makedirs(notesEmbeddedPath, exist_ok=True)

    # create notes path
    notesPath = dataPath+"/notes"
    os.makedirs(notesPath, exist_ok=True)

def createNotebook(vaultPath: str, notebook: str):
    notebookPath = vaultPath+"data/notes/"+notebook
    os.makedirs(notebookPath, exist_ok=True)
