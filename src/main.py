from src.processing import Loader
from src.matcher import Matcher
from src.writer import Writer
from src.config import DATA_PATH, NOTES_EMBEDDED_PATH, NOTES_PATH, OBSIDIAN_VAULT
import os

notebook = "notebook2"
refMarker = ("#see", ")")

class Main:
    # Load all pdfs in notes folder then TODO remove them, or maybe i dont need to remove them, if i already use the obsidian pdf folder 
    # from the start. If i dont, then i need to move them to the default pdf folder. Also i should keep all the data stuff in the obsidian
    # vault!! --> with markdowns it doesn't work: cause they show up in the graph, but pdfs are fine
    # TODO check if file is already in notebook so i dont have to reload everything
    def load(self, notebook):
        notes = os.listdir(NOTES_PATH)
        if ".gitignore" in notes:
            notes.remove(".gitignore")
        for index, note in enumerate(notes):
            loader = Loader(note, notebook)
            loader.extractText()
            loader.chunking(600)
            loader.embed()
            loader.save()
            return index
     
    def write(self, refMarker):
        notes = os.listdir(NOTES_PATH)
        if ".gitignore" in notes:
            notes.remove(".gitignore")
        for index, note in enumerate(notes):
            matcher = Matcher(note, notebook, refMarker)
            writer = Writer(note, notebook)
            refs = matcher.refExtractor()
            for ref in refs:
                matches = matcher.search(ref["ref"])
                writer.taggify(matches)
            writer.write()
            return index

