
import json

def get_user_info(user_id, json_file_path='sample_user.json'):
    """
    Retrieves user info from sample_user.json based on user ID.

    Parameters:
        user_id (str): The user ID to look up (e.g., "user123").
        json_file_path (str): The JSON file path (default is 'sample_user.json').

    Returns:
        dict: User information if found, else None.
    """
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        return data.get(user_id)
    except FileNotFoundError:
        print(f"Error: File '{json_file_path}' not found.")
    except json.JSONDecodeError:
        print(f"Error: File '{json_file_path}' contains invalid JSON.")
    return None


def fetch_service_info(json_path='faq.json'):
    """
    Fetches fuel delivery info from a local JSON file.

    Parameters:
        json_path (str): Path to the JSON file.

    Returns:
        dict: Dictionary with info on fuel types, pricing, and timings.
    """
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("Error: info.json file not found.")
        return None
    except json.JSONDecodeError:
        print("Error: JSON format is invalid.")
        return None