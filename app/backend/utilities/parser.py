# Parse one notebook from /uploaded and save its content to /uploaded folder as .txt
# Only extracts markdown and code content, no images
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

    # Generate output filename: notebook.ipynb -> notebook.txt
    filename = path.basename(filepath)
    text_filename = filename.split(".")[0] + ".txt"
    text_file_path = path.join("app", "uploaded", text_filename)
    
    # Write ASCII Doc file to uploaded directory
    with open(text_file_path, "w", encoding="utf-8") as f:
        f.write(body)

    # Remove the original notebook file after processing
    import os
    os.remove(filepath)

# Process all notebooks in the /uploaded directory
# Convert each .ipynb file to .txt and remove the original
def processNotebooks():
    import os
    # Process multiple notebooks
    for notebook in os.listdir(os.path.join("app", "uploaded")):
        if notebook.endswith(".ipynb"):  # Only process .ipynb files
            # Parse single notebook
            parse(filepath=os.path.join("app", "uploaded", notebook))