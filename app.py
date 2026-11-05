import streamlit as st
import requests
from icalendar import Calendar
from datetime import datetime

# Page configuration with your aviation title
st.set_page_config(
    page_title="MASTER CAUTION — HW Tracker",
    page_icon="⚠️",
    layout="wide"
)

# Header & Aviation Styling
st.title("⚠️ MASTER CAUTION")
st.caption("Task & Assignment Collision Avoidance System")

# Sidebar - Quick Status & Config
with st.sidebar:
    st.header("⚙️ Configuration")
    ical_url = st.text_input("Moodle iCal Export URL", type="password", help="Paste your iCal link from Moodle Calendar export")
    anthropic_key = st.text_input("Anthropic API Key (AI Import)", type="password")
    
    if st.button("Save Settings"):
        st.session_state["ical_url"] = ical_url
        st.session_state["anthropic_key"] = anthropic_key
        st.success("Settings updated!")

# Main Tabs
tab_tasks, tab_sync, tab_ai = st.tabs(["📋 Task List", "🔄 Moodle Sync", "📷 WeBWorK AI Import"])

# --- TAB 1: Task List ---
with tab_tasks:
    st.subheader("Upcoming Assignments")
    
    # Placeholder sample data (Swap this with Supabase queries later)
    if "assignments" not in st.session_state:
        st.session_state["assignments"] = [
            {"Course": "Aerodynamics I", "Task": "HW 03 - Compressible Flow", "Due": "2026-11-10", "Status": "In Progress"},
            {"Course": "Linear Algebra", "Task": "Tirgul 05 Vectors", "Due": "2026-11-12", "Status": "Pending"}
        ]
    
    st.dataframe(st.session_state["assignments"], use_container_width=True)

# --- TAB 2: Moodle iCal Sync ---
with tab_sync:
    st.subheader("Sync Deadlines from Moodle")
    if st.button("Fetch iCal Events"):
        saved_url = st.session_state.get("ical_url")
        if not saved_url:
            st.error("Please add your Moodle iCal URL in the sidebar settings first!")
        else:
            try:
                response = requests.get(saved_url)
                cal = Calendar.from_ical(response.content)
                events = []
                for component in cal.walk('vevent'):
                    events.append({
                        "Summary": str(component.get('summary')),
                        "Due Date": str(component.get('dtstart').dt)
                    })
                st.success(f"Fetched {len(events)} events from Moodle!")
                st.write(events)
            except Exception as e:
                st.error(f"Failed to fetch iCal feed: {e}")

# --- TAB 3: AI Screenshot Import ---
with tab_ai:
    st.subheader("Import Assignments via WeBWorK Screenshot")
    uploaded_file = st.file_uploader("Upload assignment screenshot", type=["png", "jpg", "jpeg"])
    
    course_name = st.text_input("Target Course Name", value="Aerospace Engineering")
    
    if uploaded_file and st.button("🤖 Extract & Add"):
        if not st.session_state.get("anthropic_key"):
            st.warning("Please enter your Anthropic API Key in the sidebar settings.")
        else:
            st.info("Parsing screenshot with AI... (hook up Anthropic Vision API call here)")
