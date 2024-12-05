from safuaaaa.notebook_fetcher import fetch_and_save_notebook

def download_notebook():
    # Specify the GitHub raw URL to the Jupyter Notebook file
    url = "https://github.com/saffuanaanvrr/exam/raw/main/Deep_Learning_Lab.ipynb"
    save_path = "Deep_Learning_Lab_downloaded.ipynb"  # Specify where to save the downloaded notebook
    fetch_and_save_notebook(url, save_path)
