import google.generativeai as genai
import json
from ..apiKey import googleKey

def rank_professionals_with_gemini(user_data, prof_data):
    """
    This function ranks professionals based on user data using Google AI's Gemini model.

    Args:
        user_data (str or dict): JSON string or dictionary containing user data.
        prof_data (str or dict): JSON string or dictionary containing professional data.

    Returns:
        str: A comma-separated string of professional IDs ranked by relevance.
    """
    genai.configure(api_key=googleKey)

    if isinstance(user_data, str):
        user_data = json.loads(user_data)
    if isinstance(prof_data, str):
        prof_data = json.loads(prof_data)

    user_info = {
        "main_issue": next((item["answer"] for item in user_data[0] if item["questionNo"] == 0), ""),
        "duration": next((item["answer"] for item in user_data[0] if item["questionNo"] == 1), ""),
        "age": next((item["answer"] for item in user_data[0] if "age" in item["question"].lower()), ""),
        "environment": next((item["answer"] for item in user_data[0] if item["questionNo"] == 3), ""),
        "previous_therapy": next((item["answer"] for item in user_data[0] if item["questionNo"] == 2), "")
    }

    professionals = []

    for prof in prof_data:
        if not prof: 
            print("Warning: Empty prof data encountered, skipping.")
            continue 
        
        try:
            prof_info = {
                "id": prof[0]["prof id"],
                "expertise": next((item["answer"] for item in prof if "expertise" in item["question"].lower()), ""),
                "experience": next((item["answer"] for item in prof if "patients" in item["question"].lower()), ""),
                "specialization": next((item["answer"] for item in prof if "problems" in item["question"].lower()), ""),
                "age_group": next((item["answer"] for item in prof if "age patients" in item["question"].lower()), "")
            }
            professionals.append(prof_info)
        except (IndexError, KeyError) as e:
            print(f"Error processing prof data: {prof}. Error: {e}")
            continue  # Skip problematic entries and move on

    prompt = f"""
    You are an expert at matching users with professionals based on their needs.
    Here is a user seeking help and the available professionals:

    User Data:
    {json.dumps(user_info, indent=2)}

    Professionals:
    {json.dumps(professionals, indent=2)}

    Rank the professionals by their suitability for the user based on their expertise, experience, and specialization.
    Return only the IDs of the professionals in order of best match, separated by commas.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        print("Generating response from Gemini...")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return "Error generating response"