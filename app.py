import streamlit as st
import pdfplumber

st.set_page_config(page_title="Book Reference Finder", layout="centered")
st.title("📖 Book Reference Page Finder")
st.write("Upload a split PDF book segment to find exact reference pages.")

uploaded_file = st.file_uploader("Upload your PDF book part (Max 50MB)", type=["pdf"])
user_query = st.text_input(...)
if uploaded_file is not None:
    st.success("File uploaded successfully!")
    
    # Using pdfplumber for cleaner text extraction
    with pdfplumber.open(uploaded_file) as pdf:
        total_pages = len(pdf.pages)
        st.info(f"This PDF segment has {total_pages} pages.")
        
        user_query = st.text_input("Type the keyword or phrase you are looking for:")
        
        if user_query:
            st.write(f"Searching for: **{user_query}**...")
            found_pages = []
            
            # Add a visual progress tracker bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, page in enumerate(pdf.pages):
                # Update visual progress for the user
                progress = (i + 1) / total_pages
                progress_bar.progress(progress)
                status_text.text(f"Scanning page {i + 1} of {total_pages}...")
                
                page_text = page.extract_text()
                
                # Verify if text exists on the page
                if page_text and user_query.lower() in page_text.lower():
                    found_pages.append(i + 1)
            
            # Clear status text once finished
            status_text.empty()
            progress_bar.empty()
            
            # Display the search results
            if found_pages:
                st.success(f"Found matches on {len(found_pages)} page(s)!")
                for pg in found_pages:
                    st.markdown(f"📍 **Reference Page Number: {pg}**")
            else:
                st.warning("No match found. If this book is a scanned photocopy, the text cannot be read directly without an OCR tool.")
