from dotenv import load_dotenv
from PIL import Image
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-pro")


# Initialize chat history (if not already in session state)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


def get_gemini_responses(input, image):
    if input != "":
        if image is not None:
            response = model.generate_content([input, image])
        else:
            response = model.generate_content(input)
    else:
        response=model.generate_content(image)
    return response.text



st.set_page_config(page_title="Text or Text+Image Chat")

st.header("QuickTalk Assistant")

# Text input for user query
text_input = st.text_input("Ask me anything: ", key="text_input")

# File upload for Image (optional)
uploaded_file = st.file_uploader("You can give me an image too! (Optional) ", type=["jpg", "jpeg", "png"])

# Load image from uploaded file (if available)
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="This was your image", use_column_width=True)


# Submit button
submit = st.button("Tell Me!")


# Process user interaction (if submit button is clicked)
if submit:
    # Generate response from Gemini model
    st.subheader("Here's what I can tell: ")
    response = get_gemini_responses(text_input, image)

    # Update chat history with user query and response
    st.session_state.chat_history.append({
        "role": "user",
        "content": text_input
    })
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response
    })

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    
