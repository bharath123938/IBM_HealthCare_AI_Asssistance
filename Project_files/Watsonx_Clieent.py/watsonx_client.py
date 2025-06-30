from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams

def get_watsonx_response(api_key: str, project_id: str, watsonx_url: str, prompt: str) -> str:
    model_id = "ibm/granite-3-2b-instruct"
    parameters = {
        GenParams.DECODING_METHOD: "greedy",
        GenParams.MAX_NEW_TOKENS: 500,
        GenParams.MIN_NEW_TOKENS: 1,
        GenParams.TEMPERATURE: 0.7,
    }
    credentials = {"url": watsonx_url, "apikey": api_key}
    try:
        model = Model(model_id=model_id, params=parameters, credentials=credentials, project_id=project_id)
        response = model.generate(prompt=prompt)
        if response and 'results' in response and len(response['results']) > 0:
            return response['results'][0]['generated_text']
        else:
            return "Error: The model did not return a valid response."
    except Exception as e:
        print(f"An error occurred while communicating with Watsonx.ai: {e}")
        return f"Error: Could not connect to the AI service. Please check credentials and network. Details: {e}"