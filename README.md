# Resume Analysis API

## Overview
The **Resume Analysis API** is a Django-based REST API that processes user resume data and returns detailed analysis results. It extracts text from resumes (PDF and DOCX formats), analyzes them against job descriptions using Google's Gemini AI, and provides structured feedback including scores, strengths, weaknesses, and recommendations. The API is designed to integrate with websites for automated resume evaluation in recruitment processes.

## Key Features
- **Resume/CV Processing**: Upload resumes via URL or JSON data. Extracts text from PDF and DOCX files using PyPDF2 and python-docx libraries.
- **AI-Powered Analysis**: Integrates with Google's Gemini AI (gemini-2.5-flash model) to analyze resume content against provided job descriptions, generating detailed feedback including scores, strengths, weaknesses, and recommendations.
- **Data Storage**: Uses MongoDB (via mongoengine) to store resume metadata and analysis results. Supports upsert operations for updating existing records.
- **RESTful API**: Provides endpoints for retrieving user data and performing analyses.
- **Containerized Deployment**: Includes a Dockerfile for easy deployment with Gunicorn and Uvicorn workers.
- **Environment Configuration**: Uses python-dotenv for secure management of API keys and database URLs.

## Technology Stack
- **Backend Framework**: Django 5.2.6 with Django REST Framework 3.16.1
- **Database**: MongoDB (via mongoengine 0.29.1)
- **AI Integration**: Google Generative AI (google-generativeai 0.8.5)
- **Text Extraction**: PyPDF2 3.0.1 for PDFs, python-docx 1.2.0 for DOCX
- **Deployment**: Gunicorn 23.0.0, Uvicorn 0.36.0, Docker
- **Other Libraries**: Requests for HTTP calls, python-dotenv for environment variables.

## Installation and Setup

### Prerequisites
- Python 3.12.5
- MongoDB instance (local or cloud, e.g., MongoDB Atlas)
- Google Gemini API key
- Docker (optional, for containerized deployment)

### Local Setup
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   git switch ResumeService
   cd ResumeService
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables**:
   Create a `.env` file in the `ResumeService` directory with the following:
   ```
   SECRET_KEY=your-django-secret-key
   MongoDbUrl=mongodb://your-mongodb-connection-string
   Api_key=your-google-gemini-api-key
   analyzefordoc=your-custom-prompt-for-analysis
   ```

4. **Database Setup**:
   - Ensure MongoDB is running and accessible via the `MongoDbUrl`.
   - Run Django migrations (though MongoDB is used for main data, SQLite is configured as default DB):
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

5. **Run the Server**:
   ```bash
   python manage.py runserver 8000
   or 
   uvicorn ResumeService.asgi:application --reload --log-level debug
   ```
   The API will be available at `http://localhost:8000`.

### Docker Deployment
1. **Build the Image**:
   ```bash
   docker build -t resume-service .
   ```

2. **Run the Container**:
   ```bash
   docker run -p 8000:8000 resume-service
   ```

For production, consider using services like Render, Heroku, or AWS. The current setup includes configuration for Render deployment.

## API Endpoints Example Using Render 

### Base URL
`https://resumeservice.onrender.com` (or `http://localhost:8000` for local)

### Endpoints

#### 1. GET /user/
Retrieves all stored resume analysis metadata.

- **Method**: GET
- **Response**: JSON array of ResumeAnalyzeMetaData objects, including userid, Data (analysis results), and createdAt timestamp.
- **Example Response**:
  ```json
  [
    {
      "userid": "user123",
      "Data": "{\"score\": 85, \"feedback\": \"Strong technical skills...\"}",
      "createdAt": "2023-10-01T12:00:00Z"
    }
  ]
  ```

#### 2. POST /analyzewithdocument/
Analyzes a resume uploaded via URL.

- **Method**: POST
- **Request Body**:
  ```json
  {
    "userid": "user123",
    "url": "https://example.com/resume.pdf",
    "jobDescription": "Software Engineer position requiring Python and Django experience."
  }
  ```
- **Process**:
  - Downloads the PDF from the URL.
  - Extracts text using PyPDF2.
  - Appends job description and sends to Gemini AI for analysis.
  - Parses AI response and stores in MongoDB.
- **Response**: JSON with analysis results, including userid.
- **Example Response**:
  ```json
  {
    "score": 85,
    "strengths": ["Python expertise", "Django experience"],
    "weaknesses": ["Limited cloud experience"],
    "recommendations": ["Consider AWS certification"],
    "userid": "user123"
  }
  ```

#### 3. POST /analyzewithjson/
Analyzes resume data provided as JSON.

- **Method**: POST
- **Request Body**:
  ```json
  {
    "resume": {
      "userId": "user123",
      "skills": ["Python", "Django"],
      "experience": "3 years as Software Engineer"
    },
    "jobDescription": "Software Engineer position requiring Python and Django experience."
  }
  ```
- **Process**: Converts JSON to string, appends job description, analyzes with Gemini AI, stores results.
- **Response**: Similar to `/analyzewithdocument/`.

## Usage Examples

### Python Example
```python
import requests

# Analyze with document
response = requests.post('https://resumeservice.onrender.com/analyzewithdocument/', json={
    "userid": "user123",
    "url": "https://example.com/resume.pdf",
    "jobDescription": "Looking for a Python developer with 2+ years experience."
})
print(response.json())

# Get user data
response = requests.get('https://resumeservice.onrender.com/user/')
print(response.json())
```

### cURL Example
```bash
curl -X POST https://resumeservice.onrender.com/analyzewithdocument/ \
  -H "Content-Type: application/json" \
  -d '{
    "userid": "user123",
    "url": "https://example.com/resume.pdf",
    "jobDescription": "Software Engineer role"
  }'
```

## Data Models

### Resume
- `userid` (String, required): Unique identifier for the user.
- `url` (String, required): URL of the resume document.
- `jobDescription` (String, required): Description of the job for analysis.
- `createdAt` (DateTime): Timestamp of creation.

### ResumeAnalyzeMetaData
- `userid` (String, required, unique): Unique identifier for the user.
- `Data` (String, required): JSON string containing analysis results.
- `createdAt` (DateTime): Timestamp of creation.

## Configuration
- **DEBUG**: Set to False in production.
- **ALLOWED_HOSTS**: Includes 'resumeservice.onrender.com' for deployment.
- **Database**: MongoDB connection configured via `MongoDbUrl` environment variable.
- **AI Model**: Uses 'gemini-2.5-flash' for fast responses.

## Author **SRIJAN RAY** - [GitHub Profile](https://github.com/BOBSRIJAN)

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes. Ensure to follow Django best practices and include tests for new features.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.