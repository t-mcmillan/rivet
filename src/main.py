from processing import Loader
from matcher import Matcher
from writer import Writer
from config import DATA_PATH, NOTES_EMBEDDED_PATH, NOTES_PATH, OBSIDIAN_VAULT
import os

class Main:
    # Load all pdfs in notes folder than remove them
    def load(self):
        notes = os.listdir(NOTES_PATH)
        

if __name__ == "__main__":
    main = Main

