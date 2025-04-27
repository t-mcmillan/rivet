from src.config import DATA_PATH, NOTES_PATH, NOTES_EMBEDDED_PATH
from pypdf import PdfReader
from fastembed import TextEmbedding
import math
import os
import json
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


class Loader:
    def __init__(self, fileName: str, notebook: str):
        self.fileName = fileName
        self.notebook = notebook.lower().replace(" ", "_")+".json"

    def extractText(self) -> list[str]:
        """Returns a list of text, where each string in the list is the next of one page (index of list = page number)"""
        fileFormat = self.fileName.split(".")[1]
        print(fileFormat)
        if fileFormat != "pdf": 
            with open(NOTES_PATH+self.fileName, 'r') as file:
                text = [file.read()]
        else:
            reader = PdfReader(NOTES_PATH+self.fileName)
            number_of_pages = len(reader.pages)
            text = []
            for i in range(number_of_pages):
                page = reader.pages[i]
                text.append(page.extract_text())
        self.text: list[str] = text
        if ''.join(self.text) == '':
            raise ValueError(f"The file {self.fileName} is either a non ediable pdf or has no content")
        return text
    
    def chunking(self, chunkLength: int = 1024):
        chunks = [] # A list lists: each sublist are the chunks of a page. The len(chunks) is the number of pages
        for page in self.text:
            pageChunks = []
            divisions = math.floor(len(page)/chunkLength)
            print(divisions)
            for i in range(divisions):
                pageChunks.append(page[chunkLength*i:chunkLength*(i+1)]) # splits the page into chunks of size chunkLength 
            chunks.append(pageChunks)
        self.chunks: list[list[str]] = chunks
        print(chunks, self.fileName)
        print(len(chunks[0]))

    def embed(self):
        embedding_model = TextEmbedding()
        print("The model BAAI/bge-small-en-v1.5 is ready to use.")
        embeddings = []
        for page in self.chunks:
            pageEmbeddingsRaw = list(embedding_model.embed(page))
            # you can also convert the generator to a list, and that to a numpy array
            pageEmbeddingsFormatted = []
            for embedChunk in pageEmbeddingsRaw:
                pageEmbeddingsFormatted.append(embedChunk.tolist())
            len(pageEmbeddingsFormatted[0]) # Vector of 384 dimensions
            embeddings.append(pageEmbeddingsFormatted)
        self.embeddings:list[list[float]] = embeddings
        print(embeddings[0][0])
        print(len(embeddings[0]))

    def save(self):
        # Checking in notebook in system
        notebooks = os.listdir(NOTES_EMBEDDED_PATH)
        entryText = {}
        entryEmbeddings = {}
        # Append text and embeddings to entry
        for page in range(len(self.chunks)):
            entryText[f"Page: {page}"] = self.chunks[page]
            entryEmbeddings[f"Page: {page}"] = self.embeddings[page]
        entry = {
            self.fileName: {
                "number_of_pages": len(self.text),
                "text": entryText,
                "embeddings": entryEmbeddings
            }
        }
        # This part can be optimized, the code after this is redundant: this is for creating the notebook json if its is not there, but after 
        # these is already a check if the notebook is there, but i check after i already read for it, so if its not there an error will be 
        # thrown, so this code here is necessary, the code after not so much
        if self.notebook not in notebooks:
            with open(NOTES_EMBEDDED_PATH+self.notebook, 'w') as file:
                json.dump('', file, indent=4)

        with open(NOTES_EMBEDDED_PATH+self.notebook, 'r+') as file:
            if self.notebook in notebooks:
                entries = json.load(file)
                entries.update(entry)
                file.seek(0)
            else: 
                entries = entry
            json.dump(entries, file, indent=4)
        print(f"Saved entry to {self.notebook} notebook")






    
    
#loader = Loader("heart.md", "notebook1")
#loader.extractText()
#loader.chunking(500)
#loader.embed()
#loader.save()