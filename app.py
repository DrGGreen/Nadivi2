import streamlit as st
import requests
from icalendar import Calendar
from PIL import Image
import numpy as np
import easyocr

# Page Setup
st.set_page_config(
    page_title="MASTER CAUTION — HW Tracker",
    page_icon="⚠️",
    layout="wide"
)

# Custom Header
st.title("⚠️ MASTER CAUTION")
st.caption("Task & Assignment Collision Avoidance System")

# Lazy-load EasyOCR so memory is allocated only once
@st.cache_resource
def load_ocr_reader():
    return easyocr.Reader(['en'])

# Sidebar - Settings & Config
with st.sidebar:
    st.header("⚙️ System Config")
    ical_url = st.text_input("Moodle iCal Export URL", type="password", help="Paste iCal URL from Moodle Calendar Export")
    
    if st.button("Save Settings"):
        st.session_state["ical_url"] = ical_url
        st.success("Settings updated!")

# Main Application Tabs
tab_tasks, tab_sync, tab_ocr = st.tabs(["📋 Task List", "🔄 Moodle Sync", "📷 WeBWorK OCR Import"])

# Initialize session state storage for assignments
if "assignments" not in st.session_state:
    st.session_state["assignments"] = [
        {"Course": "Aerodynamics I", "Task": "HW 01", "Due Date": "2026-11-10", "Source": "Manual"},
        {"Course": "Linear Algebra", "Task": "Tirgul 05", "Due Date": "2026-11-12", "Source": "Manual"}
    ]

# --- TAB 1: Task Dashboard ---
with tab_tasks:
    st.subheader("Upcoming Deadlines")
    if st.session_state["assignments"]:
        st.dataframe(st.session_state["assignments"], use_container_width=True)
    else:
        st.info("No tasks logged yet. Sync Moodle or scan a WeBWorK screenshot!")

# --- TAB 2: Moodle iCal Sync ---
with tab_sync:
    st.subheader("Sync Deadlines from Moodle")
    if st.button("Fetch iCal Feed"):
        saved_url = st.session_state.get("ical_url")
        if not saved_url:
            st.error("Add your Moodle iCal URL in the sidebar settings first!")
        else:
            try:
                response = requests.get(saved_url)
                cal = Calendar.from_ical(response.content)
                fetched_count = 0
                
                for component in cal.walk('vevent'):
                    summary = str(component.get('summary'))
                    dtstart = str(component.get('dtstart').dt)
                    
                    st.session_state["assignments"].append({
                        "Course": "Moodle Sync",
                        "Task": summary,
                        "Due Date": dtstart,
                        "Source": "iCal Feed"
                    })
                    fetched_count += 1
                
                st.success(f"Successfully imported {fetched_count} deadlines from Moodle!")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to parse iCal feed: {e}")

# --- TAB 3: WeBWorK OCR Import ---
with tab_ocr:
    st.subheader("Import Assignments via WeBWorK Screenshot")
    uploaded_file = st.file_uploader("Upload assignment list screenshot", type=["png", "jpg", "jpeg"])
    course_name = st.text_input("Target Course Name", value="Aerospace Engineering")
    
    if uploaded_file and st.button("🔍 Scan Image"):
        with st.spinner("Scanning text from screenshot..."):
            image = Image.open(uploaded_file)
            image_np = np.array(image)
            
            reader = load_ocr_reader()
            extracted_lines = reader.readtext(image_np, detail=0)
            
            st.success("Scan complete!")
            st.write("### Detected Lines:")
            st.write(extracted_lines)
