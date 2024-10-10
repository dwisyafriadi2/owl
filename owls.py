import requests
import json
import webbrowser
import time

def read_init_data(file_path):
    """Reads multiple init-data entries from the specified file."""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines() if line.strip()]

def authenticate(init_data):
    """Sends a POST request to authenticate using the given init-data."""
    url = "https://api.owlsonton.com/api/user/addUser"
    payload = {
        "refKey": None,  # Use `None` instead of an empty string if needed.
        "reffererId": 7139446077,  # Assuming this value is static for the request.
        "initData": init_data,
        "isPremium": False  # Ensure this is a boolean, not a string.
    }

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json",
        "Origin": "https://play.owlsonton.com",
        "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    }

    # Send POST request with payload and headers
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        print("Authentication successful!")
        return response.json()
    else:
        print(f"Failed to authenticate. Status code: {response.status_code}")
        return None

def getUser(jwt):
    """Sends a GET request to retrieve user details using the given JWT."""
    url = "https://api.owlsonton.com/api/user/getUser"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json",
        "Origin": "https://play.owlsonton.com",
        "Authorization": f"Bearer {jwt}",
        "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    }

    # Send GET request with headers
    response = requests.get(url, headers=headers)
    if response.status_code == 201:
        print("Success getuser")
        return response.json()
    else:
        print(f"Failed to get user. Status code: {response.status_code}")
        return None

def getTask(jwt):
    """Sends a GET request to retrieve tasks using the given JWT."""
    url = "https://api.owlsonton.com/api/tasks/getTasks"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json",
        "Origin": "https://play.owlsonton.com",
        "Authorization": f"Bearer {jwt}",
        "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    }

    # Send GET request with headers
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Success getTask")
        return response.json()
    else:
        print(f"Failed to get tasks. Status code: {response.status_code}")
        return None

def claim_task(task, jwt):
    """Sends a POST request to claim the task's reward using the task's keyword as eventId."""
    url = "http://api.owlsonton.com/api/claim/addClaimWithAction"
    keyword = task.get('keyword')
    
    payload = {
        "eventId": keyword
    }

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json",
        "Origin": "https://play.owlsonton.com",
        "Authorization": f"Bearer {jwt}",
        "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"Successfully claimed reward for task: {task.get('title')}")
    else:
        print(f"Failed to claim reward for task {task.get('title')}. Status code: {response.status_code}")

def clear_task(task, jwt):
    """Opens the task's URL in a web browser if the task is active, then claims the reward."""
    active = task.get('isActive')
    click = task.get('onClick')
    if active and click:
        # Open task URL in the web browser
        url = task.get('onClick')
        title = task.get('title')
        print(f"Opening task: {title} -> {url}")
        webbrowser.open(url)

        # Wait for the task to be completed manually in the browser
        time.sleep(10)  # Simulate the user taking action

        # Now send the POST request to claim the task reward
        claim_task(task, jwt)
    else:
        print(f"Task '{task.get('title')}' is not active or doesn't have a valid URL.")

if __name__ == "__main__":
    # Read all init_data entries from query.txt
    init_data_list = read_init_data("query.txt")
    
    for init_data in init_data_list:
        print(f"Processing query: {init_data}")
        auth = authenticate(init_data)
        
        if auth:
            # Extract JWT token from authentication response
            jwt_token = auth.get('jwt')
            if jwt_token:
                # Get user profile
                getprofile = getUser(jwt_token)
                if getprofile:
                    print("=========================================")
                    print("Join Telegram @dasarpemulung or https://t.me/dasarpemulung")
                    name = getprofile.get('data', {})
                    print(f"Name: {name.get('name')}")
                    print(f"Total Coin: {name.get('totalCoin')}")
                    print("=========================================")

                # Get tasks
                getask = getTask(jwt_token)
                if getask:
                    response = getask.get('success')
                    if response:
                        tasks = getask.get('tasks', [])
                        for task in tasks:  # Iterating over the individual task dictionaries
                            print("Join Telegram @dasarpemulung or https://t.me/dasarpemulung")
                            clear_task(task, jwt_token)  # Pass each individual task to clear_task
                    else:
                        print("No tasks available.")
                    
                    print("=========================================")
                    name = getprofile.get('data', {})
                    print(f"Name: {name.get('name')}")
                    print(f"Total Coin: {name.get('totalCoin')}")
                    print("=========================================")
        else:
            print("Authentication failed for this query.")

    print("Join Telegram @dasarpemulung or https://t.me/dasarpemulung")
