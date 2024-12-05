import requests

def fetch_and_save_notebook(url, save_path="lab.ipynb"):
    """
    Downloads a Jupyter notebook from a specified URL and saves it locally.
    
    Parameters:
    - url (str): The URL to the Jupyter notebook file.
    - save_path (str): The file path where the notebook should be saved.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        with open(save_path, "wb") as file:
            file.write(response.content)
        print(f"Notebook saved to {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download notebook: {e}")
