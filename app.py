import streamlit as st
import cv2
from ultralytics import YOLO
import time
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# ---------------- MODEL ----------------
model = YOLO("yolov8n.pt")

st.title("🏟 Smart Stadium AI System")

# ---------------- SESSION STATE ----------------
if "running" not in st.session_state:
    st.session_state.running = False

if "history" not in st.session_state:
    st.session_state.history = []

if "gate_index" not in st.session_state:
    st.session_state.gate_index = 0

if "cycle_count" not in st.session_state:
    st.session_state.cycle_count = 0

if "frame_count" not in st.session_state:
    st.session_state.frame_count = 0


# ---------------- BUTTONS ----------------
col1, col2 = st.columns(2)

with col1:
    if st.button("▶ Start System"):
        st.session_state.running = True
        st.session_state.history = []
        st.session_state.gate_index = 0
        st.session_state.cycle_count = 0
        st.session_state.frame_count = 0

with col2:
    if st.button("⏹ Stop System"):
        st.session_state.running = False


# ---------------- UI ----------------
left, right = st.columns([2.5, 1.5])

frame_box = left.image([])
bottom1, bottom2 = left.columns(2)
seat_box = bottom1.empty()
emergency_box = bottom2.empty()

dashboard = right.empty()
graph_box = st.empty()


# ---------------- CAMERA ----------------
def get_camera():
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        return cap
    return None


cap = get_camera()

if cap is None:
    st.error("❌ Camera not detected")
    st.stop()


# ---------------- DATA ----------------
crowd = {
    "gate1": 0,
    "gate2": 0,
    "gate3": 0,
    "gate4": 0
}

gate_list = ["gate1", "gate2", "gate3", "gate4"]


# ---------------- ENGINE ----------------
def smart_engine(data):
    best_gate = min(data, key=data.get)
    best_count = data[best_gate]
    total = sum(data.values())

    return {
        "route": f"""
✅ Gate : {best_gate.upper()}  
👥 Crowd : {best_count} People  
🚶 Status : Fast Entry Available
""",
        "seat": "❌ Seats filling fast" if total > 50 else "🟢 Seats available",
        "emergency": "🚨 CROWD ALERT!" if max(data.values()) > 30 else "🟢 Normal"
    }


def color_card(box, title, status):
    if "🚨" in status or "❌" in status:
        box.error(f"### {title}\n{status}")
    else:
        box.success(f"### {title}\n{status}")


# ---------------- MAIN LOOP ----------------
while st.session_state.running:

    ret, frame = cap.read()
    if not ret:
        st.error("❌ Camera error")
        break

    # YOLO detection
    results = model(frame, verbose=False)

    count = 0
    for r in results:
        for box in r.boxes:
            if int(box.cls[0]) == 0 and float(box.conf[0]) > 0.6:
                count += 1

    # ---------------- CYCLIC GATE SYSTEM ----------------
    current_gate = gate_list[st.session_state.gate_index]
    crowd[current_gate] = count

    st.session_state.frame_count += 1

    if st.session_state.frame_count % 30 == 0:
        st.session_state.gate_index += 1

        if st.session_state.gate_index >= len(gate_list):
            st.session_state.gate_index = 0
            st.session_state.cycle_count += 1

    analysis = smart_engine(crowd)

    # ---------------- VIDEO ----------------
    cv2.putText(
        frame,
        f"{current_gate.upper()} | People: {count}",
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    frame_box.image(frame, channels="BGR")

    color_card(seat_box, "🎟 Seat Status", analysis["seat"])
    color_card(emergency_box, "🚨 Emergency", analysis["emergency"])

    # ---------------- DASHBOARD ----------------
    total_crowd = sum(crowd.values())

    dashboard.markdown(f"""
## 🏟 Smart Dashboard

### 🔄 Cycle Count
**{st.session_state.cycle_count}**

---

### 🧭 Best Entry
{analysis['route']}

---

### 👥 Total Crowd
**{total_crowd} People**

---

### 🚪 Gate Status
Gate1 : {crowd['gate1']}  
Gate2 : {crowd['gate2']}  
Gate3 : {crowd['gate3']}  
Gate4 : {crowd['gate4']}

---

### 📈 Status
{"🔥 High Crowd Expected" if total_crowd > 40 else "🟢 Normal"}
""")

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

    # ---------------- GRAPH FIX ----------------
    fig = px.line(
        df,
        x=df.index,
        y=["gate1", "gate2", "gate3", "gate4"],
        title="📊 Crowd Live Graph",
        height=300
    )

    graph_box.plotly_chart(fig)

    time.sleep(0.05)

cap.release()
