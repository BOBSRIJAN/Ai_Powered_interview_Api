from .geminiAi import Era_assistant
import dotenv, os

dotenv.load_dotenv()

class QuestionAanswerGetAnadCheck:
    
    def getQuestion(numberOfQuestiions : int|None, typesOfQuestion : str|None, Level : str|None) -> str|None:
        """ 
            this in the getQuestion function working explanation,
            In this function it's takes 3 parameter first one is numberOfQuestiions to tell us 
            how many question are required and second one is typesOfQuestion to tell us what 
            type of question are required and third one is Level to tell us what level of question are 
            required and this function return the question and answer in the string format
        """
        try: 
            prompt = os.getenv('Question')
            if numberOfQuestiions and typesOfQuestion and Level:
                prompt += f" and number of question is {numberOfQuestiions} and type of question is {typesOfQuestion} and level of question is {Level} "
                response = Era_assistant(prompt)
                return response.replace("```", "").replace("json", "")
        except Exception as e:
            return f"Error in getQuestion function : {e}"