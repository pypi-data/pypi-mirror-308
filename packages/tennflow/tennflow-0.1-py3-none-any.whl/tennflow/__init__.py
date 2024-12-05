from .notebook_fetcher import fetch_and_save_notebook

def download_notebook():
    # Define the GitHub raw URL to the Jupyter notebook file
    url = "https://github.com/saffuanaanvrr/exam/blob/main/lab.ipynb"
    save_path = "lab.ipynb"
    fetch_and_save_notebook(url, save_path)
