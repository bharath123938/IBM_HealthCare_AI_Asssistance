# app/main.py

import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Import the handlers from our modular files
from app.functionalities.symptom_checker import handle_symptom_check
from app.functionalities.prescription_analyzer import handle_prescription_analysis
from app.functionalities.diet_recommender import handle_diet_recommendation
from app.prompts import DISCLAIMER

# --- INITIALIZATION ---

# Load environment variables from the .env file
load_dotenv()

# Create the FastAPI app instance
app = FastAPI()

# Mount the 'static' directory to serve files like style.css
# This line is crucial for your new design to work.
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup the directory for our HTML templates
templates = Jinja2Templates(directory="app/templates")

# Load credentials from environment variables
IBM_CLOUD_API_KEY = os.getenv("IBM_CLOUD_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
WATSONX_URL = os.getenv("WATSONX_URL")

# A mapping from form values to the correct Python function
FUNCTION_HANDLERS = {
    "symptoms_checker": handle_symptom_check,
    "prescription_analysis": handle_prescription_analysis,
    "diet_recommendation": handle_diet_recommendation
}

# --- API ENDPOINTS ---

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Renders the main HTML page when the user first visits."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def process_request(request: Request,
                          functionality: str = Form(...),
                          user_input_symptoms: str = Form(""),
                          user_input_prescription: str = Form(""),
                          user_input_diet: str = Form("")):
    """
    Handles form submission by delegating to the appropriate handler
    based on which button was clicked in the three-card layout.
    """
    
    # Determine which textarea's input to use based on the 'functionality' value from the clicked button
    user_input = ""
    if functionality == "symptoms_checker":
        user_input = user_input_symptoms
    elif functionality == "prescription_analysis":
        user_input = user_input_prescription
    elif functionality == "diet_recommendation":
        user_input = user_input_diet

    # Basic validation to ensure the relevant textarea was filled
    if not user_input.strip():
        error_message = "Please fill in the text area for the function you wish to use."
        return templates.TemplateResponse("index.html", {
            "request": request, "response": error_message
        })

    # Check that all credentials were loaded correctly from the .env file
    if not all([IBM_CLOUD_API_KEY, WATSONX_PROJECT_ID, WATSONX_URL]):
        error_message = "Configuration Error: API Key, Project ID, or URL is missing in the .env file."
        return templates.TemplateResponse("index.html", {
            "request": request, "response": error_message
        })

    # Look up the correct handler function from our dictionary
    handler = FUNCTION_HANDLERS.get(functionality)

    ai_response = ""
    if handler:
        # Call the selected handler with the correct user input and credentials
        ai_response = handler(
            user_input=user_input,
            api_key=IBM_CLOUD_API_KEY,
            project_id=WATSONX_PROJECT_ID,
            watsonx_url=WATSONX_URL
        )
    else:
        ai_response = "Error: Invalid functionality selected."

    # Append the mandatory disclaimer to the AI's response for safety
    response_with_disclaimer = f"{ai_response}{DISCLAIMER}"
    
    # Render the template with the final response.
    # The 'request' object contains the original form data, so Jinja2 can repopulate the textareas.
    return templates.TemplateResponse("index.html", {
        "request": request,
        "response": response_with_disclaimer
    })