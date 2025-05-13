import streamlit as st
import os
import tempfile
from PIL import Image
import pytesseract
import google.generativeai as genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()  # Add this near the top of your file

# --- CONFIG ---
# Set your Tesseract-OCR path
tesseract_cmd = r"C:\\Users\\anirb\\tesseract.exe"  # Update to your actual path
pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

# Set Gemini API key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
print("GEMINI_API_KEY:", GEMINI_API_KEY)  # Debugging line to check if the key is set
if not GEMINI_API_KEY:
    st.error("❌ GEMINI_API_KEY not set. Please set it in your environment variables.")
    st.stop()

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="Buy it", page_icon="🛍️", layout="centered")
st.title("🛒 Should I Buy It?")
st.markdown("Upload a product image and tell us why you want to buy it. We'll help you decide!")

# Inputs
image_file = st.file_uploader("📸 Upload an image of the product", type=["jpg", "jpeg", "png"])
buy_reason = st.text_area("✏️ Why do you want to buy this item?", placeholder="E.g., It looks cool, I need it for work...")
analyse = st.button("🤖 Analyse Now")

# --- OCR ---
def ocr_image(image_path):
    return pytesseract.image_to_string(Image.open(image_path), lang='eng')

# --- Gemini Prompt ---
def get_gemini_response(extracted_text, reason):
    prompt = (
        f"The following text was extracted from a product image:\n\n"
        f"{extracted_text}\n\n"
        f"The user says they want to buy it because: '{reason}'.\n\n"
        f"Based on this, provide a helpful, friendly response advising whether they should buy it or not. "
        f"Consider practicality, usefulness, possible alternatives, and emotional reasoning. End with a final verdict."
    )

    response = client.models.generate_content(
        model="gemini-1.5-flash",  # Or 'gemini-2.0-pro', based on availability
        contents=[{"role": "user", "parts": [{"text": prompt}]}],
        config=types.GenerateContentConfig()
    )
    return response.candidates[0].content.parts[0].text

# --- Main Logic ---
if analyse and image_file and buy_reason.strip():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_image:
        temp_image.write(image_file.read())
        temp_image_path = temp_image.name

    st.info("🧠 Analyzing your image and reason...")

    try:
        extracted_text = ocr_image(temp_image_path)
        with st.expander("📄 Extracted Text from Image"):
            st.code(extracted_text, language="text")

        # Gemini Response
        st.subheader("💡 Gemini's Insight:")
        with st.spinner("Thinking..."):
            ai_advice = get_gemini_response(extracted_text, buy_reason)
        st.success("Here's what Gemini thinks:")
        st.write(ai_advice)

    except Exception as e:
        st.error(f"❌ Failed to process image: {e}")
    finally:
        os.remove(temp_image_path)
elif analyse and not buy_reason.strip():
    st.warning("Please enter your reason for buying the item.")
