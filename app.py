import streamlit as st
import pypdf

# Set up the web page title
st.set_page_config(page_title="Book Reference Finder", layout="centered")
st.title("📖 Book Reference Page Finder")
st.write("Upload a split PDF book part to find exact reference pages for your questions.")

# Create a file uploader on the webpage
uploaded_file = st.file_uploader("Upload your PDF book part (Max 50MB recommended)", type=["pdf"])

if uploaded_file is not None:
    st.success("File uploaded successfully!")
    
    # Read the PDF pages
    pdf_reader = pypdf.PdfReader(uploaded_file)
    
    # FIX: Correct way to count pages in newer pypdf versions
    total_pages = len(pdf_reader.pages)
    st.info(f"This PDF segment has {total_pages} pages.")
    
    # Text input for the user's question
    user_query = st.text_input("Type the keyword or phrase you are looking for:")
    
    if user_query:
        st.write(f"Searching for: **{user_query}**...")
        found_pages = []
        
        # Scan each page for the text
        for page_num in range(total_pages):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            
            if user_query.lower() in page_text.lower():
                # Store the real page number (index + 1)
                found_pages.append(page_num + 1)
                
        # Display results to the user
        if found_pages:
            st.success(f"Found matches on {len(found_pages)} page(s)!")
            for pg in found_pages:
                st.markdown(f"📍 **Reference Page Number: {pg}**")
        else:
            st.warning("No exact phrase match found. Try using a different keyword from the book.")
