from src.processing import Loader
from src.matcher import Matcher
from src.writer import Writer
from src.init import createNotebook, createVault
from src.config import DATA_PATH, NOTES_EMBEDDED_PATH, NOTES_PATH, OBSIDIAN_VAULT
import os
import json

notebook = "notebook2"
refMarker = ("#see", ")")

class Main:
    # Load all pdfs in notes folder then TODO remove them, or maybe i dont need to remove them, if i already use the obsidian pdf folder 
    # from the start. If i dont, then i need to move them to the default pdf folder. Also i should keep all the data stuff in the obsidian
    # vault!! --> with markdowns it doesn't work: cause they show up in the graph, but pdfs are fine
    # TODO separate notebooks in obsidian so i don't have one big db of notes, but each notebook has all the stuff it needs -> this way 
    # each note is separate from eachother and you don't risk rewriting a certain note to the wrong notebook
    # TODO add a way to connect different files to different notebooks
    def load(self, notebook):
        notes = os.listdir(NOTES_PATH+notebook)
        if ".gitignore" in notes:
            notes.remove(".gitignore")
        if ".DS_Store" in notes:
            notes.remove(".DS_Store")
        for index, note in enumerate(notes):
            # Check if the pdf is already in the notebook
            if notebook+".json" in os.listdir(NOTES_EMBEDDED_PATH):
                with open(NOTES_EMBEDDED_PATH+notebook+".json", "r+") as file:
                    data = json.load(file)
                    if note in data.keys():
                        print(f"File: {note} already in notebook: {notebook}")
                        yield index
                        continue
            loader = Loader(note, notebook)
            loader.extractText()
            loader.chunking(600)
            loader.embed()
            loader.save()
            yield index
     
    def write(self, refMarker, notebook):
        notes = os.listdir(NOTES_PATH+notebook)
        if ".gitignore" in notes:
            notes.remove(".gitignore")
        if ".DS_Store" in notes:
            notes.remove(".DS_Store")
        for index, note in enumerate(notes):
            matcher = Matcher(note, notebook, refMarker)
            writer = Writer(note, notebook)
            refs = matcher.refExtractor()
            for ref in refs:
                matches = matcher.search(ref["ref"])
                writer.taggify(matches)
            writer.write()
            yield index
#gen = Main().load("notebook2")
#for value in gen:
#    print(value)
