import os
import google.generativeai as genai
import dotenv

dotenv.load_dotenv()
api=os.getenv('Api_key')

def gemini(Task : str | None) -> str:
    """
        this in the gemini function working explanation
        first we load the environment variables from the .env file
        then we set the api_key of the gemini-Ai model
        then we configure this model to use the loaded api_key
        then we create an instance of the model on this model 
        we send the massage or task to the model
        and it returns a response according to the task
    """
    if Task is None:
        return
    try:
        genai.configure(api_key=api)
    except KeyError:
        return "Error: Api not working or Api key not set."
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    try:
        response = model.generate_content(Task)
        return f"{response.text}"
    except Exception as e:
        return f"Error: {e}"

''' remove this in production '''
# if __name__=="__main__":
#     print(gemini("what is Ai?"),"\nthis is the msg!")
