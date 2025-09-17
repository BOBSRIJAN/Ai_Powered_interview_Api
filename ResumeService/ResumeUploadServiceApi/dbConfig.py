import os 
import dotenv

dotenv.load_dotenv()
class DBconfigaration:
    MONGODB_URL = os.getenv('MongoDbUrl')
    DATABASE_NAME = "ResumeService"
    COLLECTION_NAME = "Resume"