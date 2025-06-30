

import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.functionalities.symptom_checker import handle_symptom_check
from app.functionalities.prescription_analyzer import handle_prescription_analysis
from app.functionalities.diet_recommender import handle_diet_recommendation
from app.prompts import DISCLAIMER
load_dotenv()
app = FastAPI()


app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

IBM_CLOUD_API_KEY = os.getenv("IBM_CLOUD_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
WATSONX_URL = os.getenv("WATSONX_URL")

FUNCTION_HANDLERS = {
    "symptoms_checker": handle_symptom_check,
    "prescription_analysis": handle_prescription_analysis,
    "diet_recommendation": handle_diet_recommendation
}


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Renders the main HTML page when the user first visits."""
    # We pass an empty form_data dictionary on the first GET request
    return templates.TemplateResponse("index.html", {"request": request, "form_data": {}})


@app.post("/", response_class=HTMLResponse)
async def process_request(request: Request):
    """
    This function handles the form submission in the most robust way
    for the three-card layout.
    """
    # 1. Asynchronously get the form data from the incoming request.
    form_data = await request.form()
    
    # 2. Get the specific value of the button that was clicked.
    functionality = form_data.get("functionality")
    
    # 3. Get the content from all three possible textareas.
    # The .get() method safely returns an empty string "" if a key doesn't exist.
    user_input_symptoms = form_data.get("user_input_symptoms", "")
    user_input_prescription = form_data.get("user_input_prescription", "")
    user_input_diet = form_data.get("user_input_diet", "")

    # 4. Determine which input to use based on the button clicked.
    user_input = ""
    if functionality == "symptoms_checker":
        user_input = user_input_symptoms
    elif functionality == "prescription_analysis":
        user_input = user_input_prescription
    elif functionality == "diet_recommendation":
        user_input = user_input_diet

    # 5. Basic validation: check if the relevant textarea was actually filled.
    if not user_input.strip():
        error_message = "Please fill in the text area for the function you selected."
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "response": error_message,
            "form_data": form_data # Pass back the original form data
        })

    # --- (The rest of the logic remains the same) ---

    # Check credentials
    if not all([IBM_CLOUD_API_KEY, WATSONX_PROJECT_ID, WATSONX_URL]):
        error_message = "Configuration Error: API Key, Project ID, or URL is missing."
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "response": error_message,
            "form_data": form_data
        })

    # Get the correct handler function
    handler = FUNCTION_HANDLERS.get(functionality)

    ai_response = ""
    if handler:
        ai_response = handler(
            user_input=user_input,
            api_key=IBM_CLOUD_API_KEY,
            project_id=WATSONX_PROJECT_ID,
            watsonx_url=WATSONX_URL
        )
    else:
        # This case should not be reachable if the HTML is correct
        ai_response = "Error: Invalid functionality selected."

    response_with_disclaimer = f"{ai_response}{DISCLAIMER}"
    
    # Render the response.
    # It's crucial to pass 'request' and 'form_data' so the template can repopulate the form.
    return templates.TemplateResponse("index.html", {
        "request": request,
        "response": response_with_disclaimer,
        "form_data": form_data 
    })
