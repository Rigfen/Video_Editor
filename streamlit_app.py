import streamlit as st
from pathlib import Path
from PIL import Image
import Panda as Pd

st.title("🎈Video Editor")
st.write(
    "Lets get Editing!"
)
product_image = Image.open(Assets_DIR / "Scotland.png")
    st.image(product_image, width=600 )

st.file_uploader("Load your file here")

