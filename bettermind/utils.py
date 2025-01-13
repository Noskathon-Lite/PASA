import google.generativeai as genai
import json

googleKey = "AIzaSyB9yO2zL8rVmeWrzR3qhe3T7yd5Z7AUq5E"

def rank_professionals(user_data, prof_data):
    """
    Ranks professionals based on user data using Google AI's Gemini model.

    Args:
        user_data (str): JSON string containing user data.
        prof_data (str): JSON string containing professional data.

    Returns:
        str: IDs of matching professionals.
    """
    genai.configure(api_key=googleKey)

    prompt = f"""
    You are an expert at matching users with professionals based on their needs.

    User Data:
    {user_data}

    Professionals:
    {prof_data}

    EXTREMELY IMPORTANT: Return only the IDs of the matching professionals in a comma-separated format. Example: 1,2,3
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        print("Generating response from Gemini...")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return "Error generating response"



def get_summary(prof_data):
    """
    Ranks professionals based on user data using Google AI's Gemini model.

    Args:
        user_data (str): JSON string containing user data.
        prof_data (str): JSON string containing professional data.

    Returns:
        str: IDs of matching professionals.
    """
    genai.configure(api_key=googleKey)

    prompt = f"""
    You are an expert at generating summary of expertise professional with given data.

    Professional's Data = 

    {prof_data}

    EXTREMELY IMPORTANT: Only Return the expertise of this professional in 1 sentence(in around 150 characters).
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        print("Generating response from Gemini...")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return "Error generating response"



'''

def rank_professionals_with_gemini(user_data, prof_data):
    """
    This function ranks professionals based on user data using Google AI's Gemini model.

    Args:
        user_data (str or dict): JSON string or dictionary containing user data.
        prof_data (str or dict): JSON string or dictionary containing professional data.

    Returns:
        str: A comma-separated string of professional IDs ranked by relevance.
    """
    # Configure the Gemini API key
    genai.configure(api_key=googleKey)

    # Ensure user_data and prof_data are dictionaries
    if isinstance(user_data, str):
        user_data = json.loads(user_data)
    if isinstance(prof_data, str):
        prof_data = json.loads(prof_data)

    # Prepare relevant user information
    user_info = {
        "main_issue": next((item["answer"] for item in user_data[0] if item["questionNo"] == 0), ""),
        "duration": next((item["answer"] for item in user_data[0] if item["questionNo"] == 1), ""),
        "age": next((item["answer"] for item in user_data[0] if "age" in item["question"].lower()), ""),
        "environment": next((item["answer"] for item in user_data[0] if item["questionNo"] == 3), ""),
        "previous_therapy": next((item["answer"] for item in user_data[0] if item["questionNo"] == 2), "")
    }

    # Extract relevant professional data
    professionals = []

    for prof in prof_data:
        if not prof:  # Check if the list is empty
            print("Warning: Empty prof data encountered, skipping.")
            continue  # Skip to the next iteration
        
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

    # Construct the prompt for Gemini
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

    # Generate the response using Gemini
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        print("Generating response from Gemini...")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return "Error generating response"

'''