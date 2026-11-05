import streamlit as st
from PIL import Image
import numpy as np
import easyocr

# Cache the EasyOCR reader so it loads into memory only once
@st.cache_resource
def load_ocr_reader():
    return easyocr.Reader(['en'])

# --- TAB 3: WeBWorK Screenshot Import (EasyOCR) ---
with tab_ai:
    st.subheader("Import Assignments via WeBWorK Screenshot")
    uploaded_file = st.file_uploader("Upload assignment screenshot", type=["png", "jpg", "jpeg"])
    
    course_name = st.text_input("Target Course Name", value="Aerodynamics I")
    
    if uploaded_file and st.button("🔍 Extract Homework Sets"):
        with st.spinner("Scanning image text..."):
            # 1. Open uploaded image and convert to numpy array
            image = Image.open(uploaded_file)
            image_np = np.array(image)
            
            # 2. Run OCR scan
            reader = load_ocr_reader()
            extracted_lines = reader.readtext(image_np, detail=0)
            
        # 3. Display verification & extracted text
        st.success("Scan complete!")
        st.write("### Extracted Text:")
        st.write(extracted_lines)
