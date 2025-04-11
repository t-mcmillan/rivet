from sklearn.metrics.pairwise import cosine_similarity
from fastembed import TextEmbedding
from config import DATA_PATH, NOTES_EMBEDDED_PATH, NOTES_PATH
import json
import numpy as np
from numpy.linalg import norm
from processing import Loader

# TODO generate a summary of the notes with ai (for math stuff figure out a way to integrate latex into the markdown)
# For now it only looks for matches in a given notebook
class Matcher:
    def __init__(self, fileName: str, notebook: str, refMarker: tuple[str, str]):
        self.fileName = fileName
        self.notebook = notebook.lower().replace(" ", "_")+".json"
        self.refMarker = refMarker #this is the substring that the note taker uses to identify a reference i.e ("+see," "+") Always add a delimiter at the end of the reference
        self.refStart = self.refMarker[0]
        self.refEnd = self.refMarker[1]

    def refExtractor(self) -> list[dict]:
        """saves and returns a list of dictionaries to self.refs in this format; [{"ref": "", "page": "", "file": ""}]"""
        # TODO handle case where pdf reader reads refMarker incorrectly ("# see" instead of "#see", or even "#See" instead of "#see")
        text: list[str] = Loader(self.fileName, self.notebook).extractText()
        refs = []
        for index, pageText in enumerate(text):
            # if the page contains references
            if self.refStart in pageText:
                refsRaw = pageText.split(self.refStart)[1:] # splits the page by ref markers, but takes away the first part of the page with no refs
                for rRaw in refsRaw:
                    # Checking if the refEnd is in the refernce: if it is then it cuts there; if not, then it will cut after 25 or so characters
                    if self.refEnd in rRaw:
                        refTemp = (rRaw.split(self.refEnd)[0]).strip()
                    else:
                        refTemp = (rRaw[:25]).strip()
                    refs.append({"ref":refTemp, "page": index, "file": self.fileName})
        self.refs = refs
        print(refs)
        return refs

    def search(self, query: str) -> list[dict]:
        # Vectorize query
        embeddingModel = TextEmbedding()
        embeddedQuery = list(embeddingModel.embed(query))[0]
        # Compare with other embeddings, returns the file data and page data 
        results = []
        with open(NOTES_EMBEDDED_PATH+self.notebook, 'r') as file:
            data = json.load(file)
            entryNames = data.keys()
            for name in entryNames:
                totalScore = 0
                metadataPage = ''
                metadataChunk = 0
                pages = data[name]["embeddings"].keys()
                for page in pages:
                    embeddedPage = data[name]["embeddings"][page]
                    for index, embeddedChunk in enumerate(embeddedPage):
                        embeddedChunk = np.array(embeddedChunk)
                        score = np.dot(embeddedChunk, embeddedQuery)/(norm(embeddedChunk)*norm(embeddedQuery))
                        # Updates temp metadata and score if it's the highest scoring chunk so far
                        if score > totalScore:
                            totalScore = score.item()
                            metadataPage = page
                            metadataChunk = index
                    #tempResult = (totalScore, name, metadataPage, f"Chunk: {metadataChunk}")
                    tempResult = {"score": totalScore, "file": name, "page": metadataPage, "chunk": metadataChunk}
                    results.append(tempResult)
                results.sort(key=lambda x: x["score"], reverse=True)
            self.results = results
            print(results)
            return results

#Matcher("asdf", "notebook1").search("see notes about different types of blood vessels")
#refs = Matcher("heart.md", "notebook1", ("#see", ")")).refExtractor()
#for r in refs:
#    ref = r["ref"]
#    print(ref)
#    Matcher("endocrine_system.md", "notebook1", ("#see", ")")).search(ref)