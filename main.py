import streamlit as st
import io 
import os 

from google.cloud import vision 
import pandas as pd  

from google.cloud import vision
from google.protobuf import field_mask_pb2 as field_mask
from google import genai

client = genai.Client(api_key="GOOGLE_API_KEY")
st.set_page_config(page_title="Buy it ", page_icon=":camera:", layout="wide")
st.title("Buy it or Not", anchor="top")
st.markdown('Upload your image and get to know do you really have a need for it!')
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
image_file=st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

print('hello')
#my_file = client.files.upload(file="path/to/sample.jpg")
#response = client.models.generate_content(
  #  model="gemini-2.0-flash",
   # contents=[my_file, "Caption this image."],
#)

#print(response.text)