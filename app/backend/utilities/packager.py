# Parse one notebook from /uploaded and save its content to /temp folder
# Markdown and code will be saved in output.txt
# Charts will be saved as .png files
def parse(filepath: str):
    from nbconvert import ASCIIDocExporter
    import nbformat
    from os import path

    notebook_unicode = open(filepath, "r", encoding="utf-8").read()
    notebook_Obj = nbformat.reads(s=notebook_unicode, as_version=4)

    # Instantiate it
    rst_exporter = ASCIIDocExporter()
    # Convert the notebook to RST format
    (body, resources) = rst_exporter.from_notebook_node(notebook_Obj)

    # Write ASCII Doc file
    text_file = path.join("app", "temp", "output.txt")
    with open(text_file, "w", encoding="utf-8") as f:
        f.write(body)

    # Write images to png files
    for image in resources['outputs'].keys():
        file_name: str = image
        file_path = path.join("app", "temp", file_name)
        with open(file=file_path, mode="wb") as f:
            f.write(resources['outputs'][file_name])

# Archive the content of one notebook from /temp folder
# Also removes all temporary files after parsing 
# Also removes the notebook whose content was archived
def pack(archivename: str):
    import zipfile
    import os

    notebookname = archivename # "24.ipynb"
    archivename = archivename.split(".")[0] + ".zip" # "24.ipynb" --> "24.zip"
    
    file_pathes_list: list[str] = []
    file_names_list: list[str] = []

    for file_name in os.listdir(os.path.join("app", "temp")):
        if file_name != ".DS_Store":
            file_pathes_list.append(os.path.join("app", "temp", file_name))
            file_names_list.append(file_name)

    with zipfile.ZipFile(os.path.join("app", "uploaded", archivename), "w") as arch:
        for i in range(0, len(file_names_list)):
            # Put the bytes from filename into the archive under the name arcname.
            arch.write(filename=file_pathes_list[i], arcname=file_names_list[i])
            os.remove(file_pathes_list[i])
    
    notebookname = os.path.join("app", "uploaded", notebookname)
    os.remove(notebookname)

# Do parseNotebook() and then packNotebook()
# for every file in the /temp directory
def packNotebooks():
    import os

    count = 1
    # Parse & Pack multiple notebooks
    for notebook in os.listdir(os.path.join("app", "uploaded")):
        
        if notebook != ".DS_Store" and notebook != ".gitkeep": 
            # Parse & Pack single notebook
            print(f"Count: {count}. Notebook: {notebook}")
            parse(filepath=os.path.join("app", "uploaded", notebook))
            pack(archivename=notebook)
            count += 1

