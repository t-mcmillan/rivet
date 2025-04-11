# :link: Rivet
Rivet is an in developement python script for [Obsidian.md](https://obsidian.md) that links editable pdf notes together using.  
I am designing this script to be used in conjunction with a note taking app like GoodNotes 6. The user will be able to upload their editable handwritten notes and rivet will find references in the notes and link said pdf to other relevant notes in the Obsidian Vault. This way the user can visualize all their interconnected notes in Obsidian's graph view, facilitating studying and reviewing.  

## :rocket: Deployment
To run rivet, download the git repo and in the config file, update the `OBSIDIAN_VAULT` to your obsidian vault path.  
You must create a folder in your vault titled `data` and inside this folder create two more folders: `notes`, `notes_embedded`.  
Then go ahead and load your pdfs into the notes folder in your obsidian vault. Before running the script ([`main.py`](./src/main.py)), please update the `notebook` and `refMarker` variables to your needs.  
Now you can run [`main.py`](./src/main.py). This will load all the files from the `notes` folder in your obsidian vault, chunkify them, embed the chunks and then save it to the `notes_embedded` folder in a json of your notebook.  
If you have new pdfs to add, simply add them to the notes folder and rerun the main function, and all the files will update accordingly. 

**This is a personal project and therefore tailored to my needs. However the repository can be cloned and modified by anyone to suit their requirements.**

