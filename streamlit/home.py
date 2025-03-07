import streamlit as st
from PIL import Image
import numpy as np
import cv2
from ai import response_4_image_prompt, delete_file

def show_image_capture() -> None:
    camera_placeholder = st.empty()
    capture_button = st.button("Capture Photo")

    st.session_state.cap = cv2.VideoCapture(0)

    if not st.session_state.cap.isOpened():
        st.error("Could not open camera.")
        return

    while True:
        ret, frame = st.session_state.cap.read()
        if not ret:
            st.error("Error reading frame.")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        camera_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)

        if capture_button:
            image = Image.fromarray(frame_rgb)
            filename = "captured_image.jpg"
            image.save(filename)
            st.session_state.captured_image_path = filename
            st.success(f"Image saved as: {filename}")
            st.session_state.cap.release()
            break

def click_button() -> None:
    st.session_state.clicked = True


def show_prompt_analysis() -> None:
    col1, col2 = st.columns(2)
    st.session_state.captured_image_path = "captured_image.jpg"
    with col1:
        if "captured_image_path" in st.session_state and st.session_state.captured_image_path:
            captured_image = Image.open(st.session_state.captured_image_path)
            st.image(captured_image, caption="Captured Image", use_container_width=True)

    with col2:
        if "captured_image_path" in st.session_state and st.session_state.captured_image_path:
            prompt = st.chat_input("Say something")
            if prompt:
                st.session_state.response, st.session_state.image_file = response_4_image_prompt(st.session_state.captured_image_path, prompt)
                st.write(f"AI Response: \n {st.session_state.response}")


            if 'clicked' not in st.session_state:
                st.session_state.clicked = False
                
            st.button('Stop', on_click=click_button)
            if st.session_state.clicked:
                st.write("Button clicked")
                if "image_file" in st.session_state:
                    delete_file(st.session_state.image_file)
                st.session_state.clicked = False
                   

            