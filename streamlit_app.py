import streamlit as st
from pathlib import Path
from PIL import Image
import tempfile
import subprocess

# -------------------------------------------------
# Helper: Get video duration using ffprobe
# -------------------------------------------------
def get_video_duration(path):
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(path)
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return float(result.stdout.strip())
    except:
        return 0.0

# -------------------------------------------------
# App UI
# -------------------------------------------------
st.set_page_config(page_title="Video Editor", layout="wide")
st.title("📸 Video Editor")
st.write("Let's get editing!")

# -------------------------------------------------
# Load banner image
# -------------------------------------------------
ASSETS_DIR = Path("assets")
ASSETS_DIR.mkdir(exist_ok=True)
image_path = ASSETS_DIR / "Scotland.png"
if image_path.exists():
    banner = Image.open(image_path)
    st.image(banner, width=600)

# -------------------------------------------------
# File uploader
# -------------------------------------------------
st.sidebar.header("📁 Upload Video")
uploaded_file = st.sidebar.file_uploader("Load your video file", type=["mp4", "mov", "avi", "mkv"])

# -------------------------------------------------
# Main Logic
# -------------------------------------------------
if uploaded_file:
    # Save to temp file
    temp_input_path = Path(tempfile.mktemp(suffix=uploaded_file.name))
    with open(temp_input_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("Video loaded!")

    # --------------------------------------------
    # Video Preview
    # --------------------------------------------
    st.subheader("🎬 Video Preview")
    st.video(str(temp_input_path))

    # --------------------------------------------
    # Get Duration Safely
    # --------------------------------------------
    duration = get_video_duration(temp_input_path)

    if duration <= 0:
        st.error("❌ Could not read video duration. Upload a different file.")
        st.stop()

    # --------------------------------------------
    # Trim Tool
    # --------------------------------------------
    st.subheader("✂ Trim Video")
    st.write(f"Video length: **{round(duration,2)} seconds**")

    start = st.number_input(
        "Start time (seconds)",
        min_value=0.0,
        max_value=max(0.1, duration - 0.1),
        value=0.0
    )

    end = st.number_input(
        "End time (seconds)",
        min_value=start + 0.1,
        max_value=duration,
        value=duration
    )

    if st.button("Trim Video"):        
        output_path = Path(tempfile.mktemp(suffix="_trimmed.mp4"))

        # Use ffmpeg to trim video (most reliable)
        command = [
            "ffmpeg", "-y",
            "-i", str(temp_input_path),
            "-ss", str(start),
            "-to", str(end),
            "-c", "copy",
            str(output_path)
        ]

        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        st.success("Trim complete!")
        st.video(str(output_path))

        # Save file for download
        with open(output_path, "rb") as f:
            st.download_button(
                label="📥 Download Trimmed Video",
                data=f,
                file_name="trimmed_video.mp4",
                mime="video/mp4"
            )

# -------------------------------------------------
# Placeholder Features
# -------------------------------------------------
st.subheader("📝 Add Text Overlay (coming soon)")
st.write("This feature will allow adding custom on-screen text.")

st.subheader("🎵 Add Background Music (coming soon)")
st.write("You will be able to upload an audio track and sync it.")

st.subheader("📤 Export Tools (coming soon)")
st.write("Final export options coming soon.")
