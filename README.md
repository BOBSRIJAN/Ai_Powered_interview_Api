# Ai_Powered_interview_Api

## 📌 Overview
This project provides a set of APIs that help users analyze their resumes, prepare for job interviews, and receive job recommendations based on their skills and job descriptions.The system is designed to work with resumes in both document (PDF/DOC) format and JSON format, process interview answers (including recorded video responses), and suggest suitable jobs using machine learning models.

## 🚀 Features
  ### API 1: Resume Analysis
  Endpoint 1 (File Upload): Accepts resumes in .docx or .pdf format, extracts content, and processes it according to the provided job description.
  Endpoint 2 (JSON Data): Accepts resume data in JSON format for direct processing.

  ### API 2: Interview Question & Response Handling
  Endpoint 1 (Generate Questions): Takes user resume data and returns a set of tailored interview questions as per the frontend request.
  Endpoint 2 (Process Responses): Receives recorded video answers from the user, processes them, and stores the structured response in the database.

  ### API 3: Job Recommendation
  Suggests relevant job opportunities to the user based on:
  Resume data
  Job description
  Machine learning–based recommendation models
  Sends back job recommendations to the frontend for display.

## 🛠️ Tech Stack
Backend: Python (Django REST)
Database: MongoDB
ML/AI Models: Used for resume-job matching and job recommendations

## Under Development
This project is currently under active development by **Srijan Ray**. Future updates will focus on expanding supported file types, enhancing AI evaluation models, and integrating with popular HR platforms.