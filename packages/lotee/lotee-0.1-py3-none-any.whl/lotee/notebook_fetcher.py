import requests

def fetch_and_save_notebook(url, save_path):
    """Fetch a Jupyter notebook from a URL and save it to a local file."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors
        
        # Save notebook content to a file
        with open(save_path, "wb") as notebook_file:
            notebook_file.write(response.content)
        print(f"Notebook successfully downloaded and saved as {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch notebook: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
