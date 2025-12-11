import requests

def downloadFile(url: str, outputPath:str = "pdf\\pdf.pdf") -> None:
    """
    Downloads a file from the given URL and saves it to the specified output path.
    Args:
        url (str): The URL of the file to download.
        outputPath (str): The path where the downloaded file will be saved.
    Returns:
        None
    """
    try:
        with requests.get(url, stream=True, timeout=30) as response:
            response.raise_for_status()

            content_type = response.headers.get('Content-Type', '')
            if "pdf" not in content_type and "word" not in content_type:
                print("Warning: File type may not be PDF/DOCX. CT:", content_type)

            with open(outputPath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

        print(f"Downloaded successfully → {outputPath}")

    except requests.exceptions.Timeout:
        print("Timeout occurred. Server too slow or unresponsive.")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
