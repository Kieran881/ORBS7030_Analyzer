import requests
import json
import base64

# Configuration
OPENROUTER_API_KEY = "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"  # Replace with your API key
SITE_URL = "your_site_url"  # Optional: Replace with your site URL
SITE_NAME = "your_site_name"  # Optional: Replace with your site name

# Get user input for the prompt
prompt = input("Enter your prompt for the image (e.g., 'Describe this image'): ")

# Read and encode the local image to base64
try:
    with open("/workspaces/ORBS7030_Grader/app/backend/utilities/image.jpg", "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
except FileNotFoundError:
    print("Error: image.jpg not found in the current directory.")
    exit(1)

# API request payload
payload = {
    "model": "x-ai/grok-4",  # Specify Grok 4 model
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}
                }
            ]
        }
    ]
}

# Headers
headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": SITE_URL,  # Optional
    "X-Title": SITE_NAME  # Optional
}

# Send request to OpenRouter API
try:
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        data=json.dumps(payload)
    )
    
    # Handle response
    if response.status_code == 200:
        print("Response from API:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.status_code}, {response.json()}")
except requests.RequestException as e:
    print(f"Request failed: {e}")