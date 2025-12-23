import cv2
import numpy as np
from PIL import Image
import streamlit as st
from util import get_limits

st.title("🎨 Color Detection App")
st.write("Upload an image and detect colors easily")

color_name = st.selectbox(
    "Choose a color",
    ["Yellow", "Red", "Green", "Blue"]
)

colors = {
    "Yellow": [0, 255, 255],
    "Red": [0, 0, 255],
    "Green": [0, 255, 0],
    "Blue": [255, 0, 0]
}

uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg","png","jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    frame = np.array(image)

    st.subheader("Original Image")
    st.image(image)

    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    selected_color = colors[color_name]
    lowerLimit, upperLimit = get_limits(color=selected_color)
    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

    mask_ = Image.fromarray(mask)
    bbox = mask_.getbbox()

    if bbox is not None:
        x1, y1, x2, y2 = bbox
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 4)
        cv2.putText(frame, color_name, (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
        st.success(f"✅ {color_name} detected")
    else:
        st.warning("⚠️ No color detected")

    st.subheader("Detected Image")
    st.image(frame, channels="BGR")


#python -m streamlit run streamlit_app.py
