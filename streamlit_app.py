import streamlit as st
from pathlib import Path
from PIL import Image
import pandas as pd 

# --------------------------------
# Set up assets folder
# --------------------------------
ASSETS_DIR = Path("assets")  # Make sure you have an /assets folder uploaded

# --------------------------------
# App UI
# --------------------------------
st.title("🎈 Video Editor")
st.write("Let's get editing!")

# --------------------------------
# Load image
# --------------------------------
image_path = ASSETS_DIR / "Scotland.png"

if image_path.exists():
    product_image = Image.open(image_path)
    st.image(product_image, width=600)
else:
    st.error(f"Image not found: {image_path}")

# --------------------------------
# File uploader
# --------------------------------
uploaded_file = st.file_uploader("Load your file here")
