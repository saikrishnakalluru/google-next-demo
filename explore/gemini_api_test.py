# Imports
from google import genai
import os

# Constants
API_KEY = os.environ.get("GENAI_API_KEY")
MODEL = "gemini-1.5-flash"

# Create a new GenAI client
client = genai.Client(api_key=API_KEY)

# Test if the client is working and we are able to get a response
response = client.models.generate_content(
    model="gemini-1.5-flash", contents="Explain how AI works"
)
print(response.text)