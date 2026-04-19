import streamlit as st
import numpy as np
from PIL import Image
from ultralytics import YOLO
import pandas as pd
import plotly.express as px
import time

st.set_page_config(layout="wide")

# ---------------- MODEL ----------------
model = YOLO("yolov8n.pt")

st.title("🏟 Smart Stadium AI System (Cloud Fixed Version)")

# ---------------- SESSION STATE ----------------
if "history" not in st.session_state:
    st.session_state.history = []

if "cycle" not in st.session_state:
    st.session_state.cycle = 0


# ---------------- UPLOAD IMAGE ----------------
uploaded_file = st.file_uploader(
    "📤 Upload Image (Crowd Frame)",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is None:
    st.warning("Upload an image to start detection")
    st.stop()

image = Image.open(uploaded_file)
frame = np.array(image)


# ---------------- YOLO DETECTION ----------------
results = model(frame)

count = 0
for r in results:
    for box in r.boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])

        # person class = 0
        if cls == 0 and conf > 0.5:
            count += 1


# ---------------- FAKE 4 GATES SPLIT ----------------
crowd = {
    "gate1": count // 4,
    "gate2": count // 4,
    "gate3": count // 4,
    "gate4": count - (count // 4 * 3)
}

total = sum(crowd.values())


# ---------------- BEST GATE ----------------
best_gate = min(crowd, key=crowd.get)


# ---------------- UI OUTPUT ----------------
st.image(frame, caption="📷 Input Image", use_container_width=True)

st.success(f"👥 Total Crowd Detected: {total}")
st.info(f"🚪 Best Entry Gate: {best_gate.upper()}")

if total > 40:
    st.error("🚨 High Crowd Alert")
else:
    st.success("🟢 Normal Crowd")


# ---------------- DASHBOARD ----------------
st.markdown("## 🏟 Gate Wise Crowd")

st.write(crowd)


# ---------------- HISTORY ----------------
st.session_state.history.append([
    crowd["gate1"],
    crowd["gate2"],
    crowd["gate3"],
    crowd["gate4"]
])


df = pd.DataFrame(
    st.session_state.history,
    columns=["gate1", "gate2", "gate3", "gate4"]
)

# ---------------- GRAPH ----------------
fig = px.line(
    df,
    x=df.index,
    y=["gate1", "gate2", "gate3", "gate4"],
    title="📊 Crowd Trend Graph",
    height=350
)

st.plotly_chart(fig, use_container_width=True)


# ---------------- CYCLE INFO ----------------
st.session_state.cycle += 1
st.caption(f"Cycle: {st.session_state.cycle}")
