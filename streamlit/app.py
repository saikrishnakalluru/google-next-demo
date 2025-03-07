import streamlit as st
from sidebar import show_sidebar
from home import show_image_capture, show_prompt_analysis


def run() -> None:
    st.title("Fashion Assistance with GenAI")
    st.write("This app uses GenAI's Gemini 1.5 Flash model to swap clothes in an image based on a text prompt.")
    show_sidebar()
    tab1, tab2 = st.tabs(["Capture", "Analyse"])
    with tab1:
        if not ("captured_image_path" in st.session_state and st.session_state.captured_image_path):
            show_image_capture()
    with tab2:
        show_prompt_analysis()



if __name__ == "__main__":
    run()