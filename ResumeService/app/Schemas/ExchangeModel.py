""" Schemas for Exchange Models """

from pydantic import BaseModel

class AnalyzeWithDocumentRequest(BaseModel):
    userid: str
    url: str
    jobDescription: str

    def __str__(self):
        return f"{self.userid}"

class AnalyzeWithDocumentResponse(BaseModel):
    userid: str
    score: int
    atsCompatibility: int
    strengths: list[str]
    improvements: list[str]
    keywords: list[str]
    suggestions: list[dict]

    def __str__(self):
        return f"{self.userid}"

class AnalyzeWithJsonRequest(BaseModel):
    userid: str
    resume: dict
    jobDescription: str

    def __str__(self):
        return f"{self.userid}"

class AnalyzeWithJsonResponse(BaseModel):
    userid: str
    score: int
    atsCompatibility: int
    strengths: list[str]
    improvements: list[str]
    keywords: list[str]
    suggestions: list[dict]

    def __str__(self):
        return f"{self.userid}"