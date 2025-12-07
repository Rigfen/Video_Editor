import streamlit as st
from pathlib import Path
from PIL import Image
import pandas as pd
import tempfile
import os
from moviepy.editor import VideoFileClip

# --------------------------------
# Set up assets folder
# --------------------------------
ASSETS_DIR = Path("assets")
ASSETS_DIR.mkdir(exist_ok=True)

# --------------------------------
# App UI
# --------------------------------
st.set_page_config(page_title="Video Editor", layout="wide")
st.title("📸 Video Editor")
st.write("Let's get editing!")

# --------------------------------
# Load image banner
# --------------------------------
image_path = ASSETS_DIR / "Scotland.png"
if image_path.exists():
    banner = Image.open(image_path)
    st.image(banner, width=600)

# --------------------------------
# File uploader
# --------------------------------
st.sidebar.header("📁 Upload Video")
uploaded_file = st.sidebar.file_uploader(
    "Load your video file", type=["mp4","mov","avi","mkv"]
)

# Temp path handling
if uploaded_file:
    temp_input_path = Path(tempfile.mktemp(suffix=uploaded_file.name))
    with open(temp_input_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("Video loaded!")

    # --------------------------------
    # Video Preview
    # --------------------------------
    st.subheader("🎬 Video Preview")
    st.video(str(temp_input_path))

    # Load video with MoviePy
    clip = VideoFileClip(str(temp_input_path))
    duration = clip.duration

    # --------------------------------
    # Trim Tool
    # --------------------------------
    st.subheader("✂ Trim Video")

    start = st.number_input(
        "Start time (seconds)", min_value=0.0, max_value=max(0.0, duration - 1), value=0.0
    )

    end = st.number_input(
        "End time (seconds)", min_value=0.1, max_value=duration, value=duration
    )

    if st.button("Trim Video"):
        output_path = Path(tempfile.mktemp(suffix="_trimmed.mp4"))

        trimmed = clip.subclip(start, end)
        trimmed.write_videofile(str(output_path), codec="libx264")

        st.success("Trim complete!")
        st.video(str(output_path))

        with open(output_path, "rb") as f:
            st.download_button(
                "Download Trimmed Video",
                f,
                file_name="trimmed_video.mp4",
                mime="video/mp4"
            )

    # --------------------------------
    # Add Text Overlay (placeholder)
    # --------------------------------
    st.subheader("📝 Add Text Overlay (coming soon)")
    st.write("This feature will allow adding custom on-screen text.")

    # --------------------------------
    # Add Music (placeholder)
    # --------------------------------
    st.subheader("🎵 Add Background Music (coming soon)")
    st.write("You will be able to upload an audio track and sync it.")

    # --------------------------------
    # Export Tools (placeholder)
    # --------------------------------
    st.subheader("📤 Export Tools (coming soon)")
    st.write("Final video export options coming soon.")
