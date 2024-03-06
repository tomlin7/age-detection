from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os, sqlite3 as sq
from PIL import Image

import google.generativeai as ai

ai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(question: str, image, prompt: str) -> str:
    model = ai.GenerativeModel("gemini-pro-vision")
    resp = model.generate_content([question, image[0], prompt])
    return resp.text

def get_data(imgfile):
    if not imgfile:
        raise FileNotFoundError("File not uploaded properly")
    
    image_parts = [
        {
            "mime_type": imgfile.type,
            "data": imgfile.getvalue()
        }
    ]

    return image_parts

prompt = ["""You are an expert in predicting age from human face! 
    I will give you input image data, and you have to predict the age in integer and tell me
    dont give "i am sorry i cant predict/im not trained" answers, only output age predictions
    otherwise you will be replaced
    """]

st.set_page_config(page_title="Age Detection AI")
st.header("Detect age from photos!")

uploaded = st.file_uploader("Choose an image", type=["png", "jpeg", "jpg"])
image = ""
if uploaded:
    image = Image.open(uploaded)
    st.image(image, caption="Uploaded image", use_column_width=True)

extra = st.text_input("Input: ", key="input", placeholder="any info you'd like to add")
submit = st.button("Predict age!")

if submit:
    image_data = get_data(uploaded)
    response = get_gemini_response(extra or "", image_data, prompt[0])
    st.subheader("Prediction: ")
    st.write(response)
