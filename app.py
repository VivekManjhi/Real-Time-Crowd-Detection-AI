import streamlit as st
import numpy as np
from PIL import Image
from ultralytics import YOLO
import pandas as pd
import plotly.express as px
import os

# FIX (safe for cloud)
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

st.set_page_config(layout="wide")

model = YOLO("yolov8n.pt")

st.title("🏟 Smart Crowd Detection AI (Cloud Safe)")

# session
if "history" not in st.session_state:
    st.session_state.history = []

# upload image
file = st.file_uploader("Upload Crowd Image", type=["jpg","jpeg","png"])

if not file:
    st.warning("📌 Please upload an image")
    st.stop()

image = Image.open(file)
frame = np.array(image)

# YOLO prediction
results = model(frame)

count = 0
for r in results:
    for b in r.boxes:
        if int(b.cls[0]) == 0 and float(b.conf[0]) > 0.5:
            count += 1

# fake gate distribution
crowd = {
    "gate1": count//4,
    "gate2": count//4,
    "gate3": count//4,
    "gate4": count - (count//4)*3
}

best_gate = min(crowd, key=crowd.get)

# UI
st.image(frame, caption="Input Image", use_container_width=True)

st.success(f"👥 Total Crowd Detected: {count}")
st.info(f"🚪 Best Entry Gate: {best_gate.upper()}")

st.write("Gate Distribution:", crowd)

# history
st.session_state.history.append(list(crowd.values()))

df = pd.DataFrame(st.session_state.history, columns=["gate1","gate2","gate3","gate4"])

fig = px.line(df, title="📊 Crowd Trend")
st.plotly_chart(fig, use_container_width=True)
