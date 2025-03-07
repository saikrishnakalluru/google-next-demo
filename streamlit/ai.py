# Imports
import google.generativeai as genai
import os
import streamlit as st

# Constants
API_KEY = os.environ.get("GENAI_API_KEY")
MODEL = "models/gemini-1.5-flash"
genai.configure(api_key=API_KEY)



def response_4_image_prompt(image, prompt):
    print(f"Uploading file...")
    image_file = genai.upload_file(path=image)
    print(f"Completed upload: {image_file.uri}")
    print("Making LLM inference request...")
    model = genai.GenerativeModel(model_name=MODEL)
    response = model.generate_content(
        [prompt, image_file],
        request_options={"timeout": 600})
    return response.text, image_file

def delete_file(image_file):
    if image_file:
        st.write(f"Deleting file...")
        genai.delete_file(image_file.name)
        st.write(f"Completed delete: {image_file.uri}")