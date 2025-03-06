import google.generativeai as genai
import PIL.Image as Image
import io
import os
# from IPython.display import Image
# from IPython.core.display import HTML
# img = Image('image_test.jpg')

# Configure your API key
GENAI_API_KEY = os.environ.get("GENAI_API_KEY")
genai.configure(api_key=GENAI_API_KEY) # Replace with your actual API key

def swap_clothes(image_path, prompt):
    """
    Swaps the clothes of a person in an image based on a text prompt using Gemini 1.5 Flash.

    Args:
        image_path: Path to the input image file.
        prompt: A text prompt describing the desired clothing change.

    Returns:
        PIL.Image or None: The modified image if successful, None otherwise.
    """
    try:
        # Load the image
        img = Image.open(image_path)
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')  # Save image to byte array
        img_bytes = img_byte_arr.getvalue()

        # Prepare the model and request
        model = genai.GenerativeModel('gemini-1.5-flash-0514')  # Use the correct model name
        response = model.generate_content(
            [
                "Here is an image, and here is a prompt.",
                img_bytes,
                prompt,
                "Please swap the clothes in the image based on the prompt and return the new image."
            ],
            stream=False
        )

        # Process the response
        if response.parts and hasattr(response.parts[0].data, "parts"):
            for part in response.parts[0].data.parts:
                if hasattr(part, "inline_data") and part.inline_data.mime_type == "image/jpeg":
                    image_data = part.inline_data.data
                    modified_image = Image.open(io.BytesIO(image_data))
                    return modified_image
        else:
          print("No image data found in response.")
          return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage:
image_file = "captured_image.jpg" # Replace with the actual image path.
clothing_prompt = "Replace the person's shirt with a red leather jacket."

modified_img = swap_clothes(image_file, clothing_prompt)

if modified_img:
    modified_img.show() #or modified_img.save("modified_image.jpg")
else:
    print("Clothing swap failed.")