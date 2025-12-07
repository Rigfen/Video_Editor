import streamlit as st
from pathlib import Path
from PIL import Image
import pandas as pd
import tempfile
import os

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
uploaded_file = st.sidebar.file_uploader("Load your video file", type=["mp4","mov","avi","mkv"])

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

    # --------------------------------
    # Trim Tool
    # --------------------------------
    st.subheader("✂ Trim Video")
    
    duration = float(container.duration / container.time_base) if container.duration else 0

    start = st.number_input("Start time (seconds)", min_value=0.0, max_value=max(0.0, duration-1), value=0.0)
    end = st.number_input("End time (seconds)", min_value=0.1, max_value=duration, value=duration)

    if st.button("Trim Video"):
        output_path = Path(tempfile.mktemp(suffix="_trimmed.mp4"))
        

        stream = in_container.streams.video[0]
        out_stream = out_container.add_stream("libx264", rate=stream.rate)
        out_stream.width = stream.width
        out_stream.height = stream.height
        out_stream.pix_fmt = 'yuv420p'

        for frame in in_container.decode(stream):
            ts = float(frame.pts * stream.time_base)
            if ts < start:
                continue
            if ts > end:
                break
            out_container.mux(out_stream.encode(frame))

        out_container.close()
        in_container.close()

        st.success("Trim complete!")
        st.video(str(output_path))

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
