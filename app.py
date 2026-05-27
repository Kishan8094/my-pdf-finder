import streamlit as st
import pdfplumber

st.set_page_config(page_title="Book Reference Finder", layout="centered")
st.title("📖 Book Reference Page Finder")
st.write("Type your keyword and upload your book segment to find reference pages.")

# 🔍 FIXED LINE: Real text label inside the quotes
user_query = st.text_input("Type the keyword or phrase you are looking for:")

# File uploader
uploaded_file = st.file_uploader("Upload your PDF book part (Max 50MB)", type=["pdf"])

if uploaded_file is not None:
    st.success("File uploaded successfully!")
    
    if not user_query:
        st.info("👈 Please type a keyword in the search bar above to begin scanning.")
    else:
        st.write(f"Searching for: **{user_query}**...")
        found_pages = []
        
        with pdfplumber.open(uploaded_file) as pdf:
            total_pages = len(pdf.pages)
            st.info(f"This PDF segment has {total_pages} pages.")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, page in enumerate(pdf.pages):
                progress = (i + 1) / total_pages
                progress_bar.progress(progress)
                status_text.text(f"Scanning page {i + 1} of {total_pages}...")
                
                page_text = page.extract_text()
                
                if page_text and user_query.lower() in page_text.lower():
                    found_pages.append(i + 1)
            
            status_text.empty()
            progress_bar.empty()
            
            if found_pages:
                st.success(f"Found matches on {len(found_pages)} page(s)!")
                for pg in found_pages:
                    st.markdown(f"📍 **Reference Page Number: {pg}**")
            else:
                st.warning("No match found. If this book is a scanned photocopy, the app cannot read the text directly.")
