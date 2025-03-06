import streamlit as st
import cv2
from PIL import Image
import numpy as np
from clothes_swap import swap_clothes

def main():
    st.title("Cloths Swap with Gemini")

    col1, col2 = st.columns(2)

    with col1:
        camera_placeholder = st.empty()
        capture_button = st.button("Capture Photo")

        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            st.error("Could not open camera.")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                st.error("Error reading frame.")
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            camera_placeholder.image(frame_rgb, channels="RGB", use_column_width=True)

            if capture_button:
                cap.release()
                image = Image.fromarray(frame_rgb)
                filename = "captured_image.jpg"
                image.save(filename)
                st.session_state.captured_image_path = filename
                st.success(f"Image saved as: {filename}")
                st.image(image, channels="RGB", use_column_width=True)
                break

            
    with col2:
        if "captured_image_path" in st.session_state and st.session_state.captured_image_path:
            prompt = st.text_input("Enter prompt for image swap:")
            if prompt:
                modified_img = swap_clothes(st.session_state.captured_image_path, prompt)
            st.image(modified_img, caption="Swapped Image", use_column_width=True)


if __name__ == "__main__":
    main()