from config import NOTES_EMBEDDED_PATH, NOTES_PATH, DATA_PATH, OBSIDIAN_VAULT

template = """
# {title}
## Notebook: {notebook}
## Tags:
{tags}
![[FinanceBroPersonalitySheet.pdf]]
"""

class Writer:
    def __init__(self, fileName: str, notebook: str): 
        self.fileName = fileName
        self.notebook = notebook
        self.notebookMDName = self.notebook.split('.')[0]
        self.title = self.fileName.split('.')[0].replace("_", " ").capitalize()

    def write(self):
        tags = f"- [heart.md page 2]({NOTES_PATH+"heart.md"}) \n- [blood_vessels.md page 2]({NOTES_PATH+"blood_vessels.md"}) \n- [nervous_system.md page 2]({NOTES_PATH+"nervous_system.md"}) \n"
        content = template.format(title=self.title, notebook = f"[{self.notebookMDName}]({self.notebookMDName})", tags=tags)
        with open(self.fileName.split('.')[0]+".md", "w") as mdFile:
            mdFile.write(content)

Writer("asdf", "adf").write()