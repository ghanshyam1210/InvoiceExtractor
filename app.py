from dotenv import load_dotenv
import streamlit as st
import os 
import google.generativeai as genai
from PIL import Image

load_dotenv() ## load all the environment variables from the .env file

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load google gemini pro model
model = genai.GenerativeModel("gemini-pro-vision")

def get_gemini_response(input,image,prompt) :
    response = model.generate_content([input,image[0],prompt])

    return response.text


def uploaded_image_setup(uploaded_file) :
    if uploaded_file is not None :

        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type" : uploaded_file.type,
                "data" : bytes_data
            }
        ]
        return image_parts
    else :
        raise FileNotFoundError("No file uploaded")


## Intialize Streamlit App

st.set_page_config(page_title="Invoice Extractor")
st.header("Invoice Extractor")

input = st.text_input("Input Prompt:" ,key="input")
uploaded_file=st.file_uploader("Choose an image of the image :" ,type=["jpeg","jpg","png"])

image=""

if uploaded_file is not None :
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image by User ", use_column_width=True)

submit = st.button("Tell me about uploaded Invoice")

input_prompt = """

You are an expert in understaing the invoices. Please answer any question on uploaded invoice image

"""

## When user click on the submit button of the App

if submit :

    image_data = uploaded_image_setup(uploaded_file)
    response = get_gemini_response(input,image_data,input_prompt)
    st.subheader("The response is ")
    st.write(response)