import mongoengine as me
import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

class ResumeAnalyzeMetaData(me.Document):
    """
        MongoDB Document Model for storing resume analysis metadata.
        Fields:
            userid (str): Unique identifier for the user.
            score (int): Overall score of the resume analysis.
            atsCompatibility (int): ATS compatibility score.
            strengths (list[str]): List of identified strengths in the resume.
            improvements (list[str]): List of suggested improvements for the resume.
            keywords (list[str]): List of relevant keywords extracted from the resume.
            suggestions (list[dict]): List of suggestions for enhancing the resume.
            createdAt (datetime): Timestamp of when the document was created.
    """
    userid: str = me.StringField(required=True)
    score: int = me.IntField(required=True)
    atsCompatibility: int = me.IntField(required=True)
    strengths: list[str] = me.ListField(required=True)
    improvements: list[str] = me.ListField(required=True)
    keywords: list[str] = me.ListField(required=True)
    suggestions: list[dict] = me.ListField(required=True)
    createdAt = me.DateTimeField(default=datetime.datetime.utcnow)

    def __str__(self):
        return f"{self.userid} → {self.Data[:50]}..." 
    
logger.info("Resume Analyze Meta Data Model Initializes Done.")