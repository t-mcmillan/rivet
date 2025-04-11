from config import NOTES_EMBEDDED_PATH, NOTES_PATH, DATA_PATH, OBSIDIAN_VAULT

template = """
# {title}
## Notebook: {notebook}
## Tags:
{tags}
![[{fileName}]]
"""

class Writer:
    def __init__(self, fileName: str, notebook: str): 
        self.fileName = fileName
        self.notebook = notebook
        self.notebookMDName = self.notebook.split('.')[0]
        self.title = self.fileName.split('.')[0].replace("_", " ").capitalize()
        self.tags = []

    def taggify(self, searchResults: list[dict]):
        tagTemplate = "- [{name}, {page}]({name}) \n"
        tags = []
        # Always add the top result if it has not already been added
        if tagTemplate.format(name=searchResults[0]["file"], page=searchResults[0]["page"]) not in self.tags:
            tags.append(tagTemplate.format(name=searchResults[0]["file"], page=searchResults[0]["page"]))
        searchResults.pop(0)
        for result in searchResults:
            if result["score"] > 0.8:
                name = result["file"]
                page = result["page"]
                if tagTemplate.format(name=name, page=page) not in self.tags:
                    tags.append(tagTemplate.format(name=name, page=page))
        self.tags.extend(tags)

    def write(self):
        # Convert tags list into string
        tagsStr = ''.join(self.tags)
        content = template.format(title=self.title, notebook = f"[{self.notebookMDName}]({self.notebookMDName})", tags=tagsStr, fileName=self.fileName)
        with open(OBSIDIAN_VAULT+self.fileName.split(".")[0]+".md", "w") as mdFile:
            mdFile.write(content)
