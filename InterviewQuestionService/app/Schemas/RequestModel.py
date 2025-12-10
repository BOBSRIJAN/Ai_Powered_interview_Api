from pydantic import BaseModel

class InitializeInterviewRequest(BaseModel):
    userid: str
    resumeurl: str | None = None
    specificquestionrequirement: bool = False
    subjectortopic: list[str] | None = None
    numberofquestions: int
    level: str 

    def __str__(self):
        return f"user id is {self.userid}"
    
class InterviewSlotTwoQuestionsRequest(BaseModel):
    userid: str
    sessionid: str | int
    remanning: int 
    level: str 

    def __str__(self):
        return f"user id{self.userid} and session was {self.sessionid}"

class UserQuestionHistoryRequest(BaseModel): 
    userid: str
    sessionid: str | int
    
    def __str__(self):
        return f"user id{self.userid} and session was {self.sessionid}"

class UserSlotOneQuestionsPostRequestResponse(BaseModel): 
    userid: str 
    sessionid: str | int
    slotonequestions: list[str]
    slottwoquestions: list[str] | None = None
    remanning: int 
    numberofquestions: int
    
    def __str__(self):
        return f"user id{self.userid} and session was {self.sessionid}"
    
class UserSlotTwoQuestionsPostRequestResponse(BaseModel):
    userid: str 
    sessionid: str | int
    slottwoquestions: list[str]
    
    def __str__(self):
        return f"user id{self.userid} and session was {self.sessionid}"
    
class UserQuestionHistoryResponse(BaseModel): 
    userid: str
    sessionid: str | int
    slotonequestions: list[str]
    slottwoquestions: list[str]
    remanning: int 
    numberofquestions: int
    
    def __str__(self):
        return f"user id{self.userid} and session was {self.sessionid}"