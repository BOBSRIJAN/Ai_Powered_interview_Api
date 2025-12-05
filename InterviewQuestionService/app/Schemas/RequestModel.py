from pydantic import BaseModel

# get request
class UserGetRequestResponse(BaseModel):
    userid: str
    resumeurl: str
    specificquestionrequirement: bool = False
    subjectortopic: list[str] = None
    numberofquestiion: int
    level: str

    def __str__(self):
        return UserGetRequestResponse.userid

class UserPostRequestResponse: 
    userid: str
    userquestion: list[str]