import urllib.request
import urllib.error
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

def downloadFile(url: str, output_dir: str = "downloads", filename: str = "file.pdf") -> None:
    """
    Downloads a file using urllib and saves it to a cross-platform path.
        Args:
            url (str): The URL of the file to download.
            output_dir (str): The folder where the file should be saved.
            filename (str): The name of the file to save.
        Returns:
            None
    """
    output_path = os.path.join(output_dir, filename)
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info(f"Created Directory: {output_dir}")
        logger.info(f"Connecting To {url}...")

        with urllib.request.urlopen(url, timeout=30) as response:
            content_type = response.info().get_content_type()
            if "pdf" not in content_type and "word" not in content_type:
                logger.info(f"Warning: File type is {content_type}, expected PDF or Word.")

            with open(output_path, "wb") as f:
                while True:
                    chunk = response.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
        logger.info(f"Downloaded Successfully → {output_path}")
        
    except urllib.error.HTTPError as e:
        logger.info(f"HTTP Error: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        logger.info(f"URL Error (Timeout or network issue): {e.reason}")
    except OSError as e:
        logger.info(f"File System Error: {e}")
    except Exception as e:
        logger.info(f"An unexpected error occurred: {e}")

# Example usage (remove in production)
# if __name__ == "__main__":
#     # Example URL (replace with your actual URL)
#     target_url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
#     # This will work on both Windows (pdf\my_file.pdf) and Linux/Docker (pdf/my_file.pdf)
#     downloadFile(target_url, output_dir="downloads", filename="manual.pdf")