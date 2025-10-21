import json

class Converter:
    """ This class contain two function StrToJson and JsonToStr for 
        convert the string data to json data and json data to string data respectively
    """
    
    def StrToJson(text : str|None) -> list[dict[str, str]]|None:
        """
            This function convert the string data to json data
            and return the json data
        """
        if text is None:
            return None
        return json.loads(text)
    
    def JsonToStr(text : list[dict[str, str]]|None) -> str|None:
        """
            This function convert the json data to string data
            and return the string data
        """
        if text is None:
            return None
        return json.dumps(text)