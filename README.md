Features:
Symptom Checker: Users can describe their symptoms in natural language and receive a list of potential, non-alarming considerations.
Prescription Analysis: Analyzes prescription text to extract key information like drug name, dosage, and frequency into a simple summary.
Diet Recommendation: Provides general dietary suggestions based on a user's stated health goals or conditions.

🛠️ Tech Stack
Backend: Python, FastAPI
Frontend: HTML5, CSS3, Jinja2
AI Service: IBM watsonx.ai
Foundation Model: ibm/granite-3-2b-instruct
Web Server: Uvicorn

🚀 Getting Started
Follow these instructions to get a copy of the project up and running on your local machine.
Prerequisites
Python 3.10 or higher
An active IBM Cloud Account with an API Key and a watsonx.ai Project ID.
Installation

Clone the repository:
Generated bash
git clone [your-repository-url]
cd healthcare-assistant
Use code with caution.
Bash
Create and activate a virtual environment:
Generated bash

# Create the environment
python -m venv .venv

# Activate on Windows (PowerShell)
.\.venv\Scripts\activate


Bash
Create a requirements.txt file with the following content:
Generated code
fastapi
uvicorn[standard]
ibm-watson-machine-learning
python-dotenv
Jinja2
python-multipart

Install the dependencies:
Generated bash
pip install -r requirements.txt
Use code with caution.
Bash

Set up your environment variables:
Create a file named .env in the root directory of the project.
Add your credentials to the .env file like this:
Generated code
IBM_CLOUD_API_KEY="your-secret-api-key-here"
WATSONX_PROJECT_ID="your-watsonx-project-id-here"
WATSONX_URL="https://us-south.ml.cloud.ibm.com"


🏃‍♀️ Running the Application
Make sure your virtual environment is activated.
From the root directory, run the following command to start the server:
Generated bash
python -m uvicorn app.main:app --reload
Use code with caution.
Bash
Open your web browser and navigate to:
http://127.0.0.1:8000
