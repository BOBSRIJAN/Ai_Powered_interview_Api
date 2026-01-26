"""
Module for interacting with Gemini AI model for content generation.
    Documentation:
        This module sets up the Gemini AI model using the Google Generative AI SDK. 
        It provides a function to generate content based on a given task.
    Args:
        task (str): The task or prompt for content generation.
    Returns:
        str: Generated content based on the provided task.
"""

import os
import google.generativeai as genai
import dotenv
import time
import logging

# program configurations
dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

# API Key Configuration
try:
    genai.configure(api_key=os.getenv('Api_key'))
    logger.info("Api key configurations done!")
except Exception:
    logger.info("Error: Invalid or missing API key.")
# Model Initialization
model = genai.GenerativeModel(
    "gemini-2.5-flash",
    generation_config={
        "temperature": 0.2,
        "top_p": 0.8,
        "top_k": 20,
        "response_mime_type": "text/plain"
    }
)
logger.info("Model intuitions Done!")

# functions Portion's
def geminiAi(task: str | None) -> str:
    """
    Generate content using Gemini AI model based on the provided task.
    Args:
        task (str): The task or prompt for content generation.
    Returns:
        str: Generated content or an error message.
    """
    if not task:
        return "No task provided."
    try:
        response = model.generate_content(task)
        return f"{response.text}"
    except Exception as e:
        return f"Exception: {str(e)}"


# Example usage (remove in production)
# if __name__ == "__main__":
#     Task = input("Enter you task: ")
#     start=time.time()
#     Result = geminiAi(Task)
#     end=time.time()
#     print(Result)
#     print(f"total time taken: {end-start}")