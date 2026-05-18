# ============================================================
# FILE: app.py
# PURPOSE: Streamlit web application — the UI users see
# ============================================================

# --- Standard Python libraries ---
import os           # os = for file path operations (os.path.join etc.)
import tempfile     # tempfile = gives us the system's temp folder path
                    # Windows → C:\Users\Name\AppData\Local\Temp
                    # Linux   → /tmp

# --- Streamlit ---
import streamlit as st  # st = the entire Streamlit library

# --- Our own files ---
from bedrock_rag import query_knowledge_base, upload_document_to_s3
from config import APP_TITLE, APP_ICON, S3_BUCKET_NAME


# ============================================================
# SECTION 1: Page Configuration
# Must be the FIRST Streamlit command — before anything else
# ============================================================
st.set_page_config(
    page_title=APP_TITLE,         # text in browser tab
    page_icon=APP_ICON,           # emoji/icon in browser tab
    layout="wide",                # "wide" uses full browser width
    initial_sidebar_state="expanded"  # sidebar is open on load
)


# ============================================================
# SECTION 2: Custom CSS Styling
# st.markdown with unsafe_allow_html=True lets us inject CSS
# ============================================================
st.markdown("""
    <style>
        /* Style the main chat container */
        .main { padding-top: 2rem; }
        
        /* Style citation boxes */
        .citation-box {
            background-color: #f0f2f6;
            border-left: 4px solid #FF6B35;
            padding: 10px;
            margin: 5px 0;
            border-radius: 0 5px 5px 0;
            font-size: 0.85em;
        }
        
        /* Style the header */
        .header-text { color: #1a1a2e; }
    </style>
""", unsafe_allow_html=True)
# unsafe_allow_html=True is needed to inject raw HTML/CSS
# Be careful with this — only use trusted HTML


# ============================================================
# SECTION 3: Sidebar
# The sidebar appears on the left side of the screen
# ============================================================
with st.sidebar:
    # st.sidebar.X puts any Streamlit element into the sidebar
    
    st.title("Settings & Info")
    st.divider()  # draws a horizontal line
    
    # --- Info about the Knowledge Base ---
    st.subheader("Knowledge Base")
    st.info(f"S3 Bucket: `{S3_BUCKET_NAME}`")
    # st.info() shows a blue info box
    
    st.divider()
    
    # --- Document Upload Section ---
    st.subheader("Upload Documents")
    st.write("Upload new documents to add to the knowledge base.")
    
    # st.file_uploader() creates a drag-and-drop file upload widget
    uploaded_file = st.file_uploader(
        label="Choose a file",
        type=["pdf", "txt", "docx"],   # only these file types allowed
        help="Upload PDF, TXT, or DOCX files"
        # help= shows a tooltip when user hovers over the widget
    )
    
    # If a file was uploaded, show an upload button
    if uploaded_file is not None:
        if st.button("Upload to S3"):
            # st.button() returns True when clicked
            
            # Show a loading spinner while uploading
            with st.spinner("Uploading..."):
                # st.spinner() shows an animated spinner inside the 'with' block
                
                # Save uploaded file temporarily to disk
                # uploaded_file.name = original file name
                # CORRECT — works on both Windows and Linux
                temp_path = os.path.join(tempfile.gettempdir(), uploaded_file.name)
                
                
                # Write the file bytes to disk
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                # uploaded_file.getbuffer() = returns raw bytes of the file
                
                # Upload to S3 using our function from bedrock_rag.py
                success = upload_document_to_s3(temp_path, uploaded_file.name)
                
                if success:
                    # st.success() shows a green success box
                    st.success(f"Uploaded! Now sync your Bedrock KB.")
                else:
                    # st.error() shows a red error box
                    st.error("Upload failed. Check logs.")
    
    st.divider()
    
    # --- How to Use guide ---
    st.subheader("How to use")
    st.markdown("""
    1. Type your question below
    2. Press Enter or click Send
    3. View the AI answer
    4. Expand 'Sources' to see citations
    """)
    
    # --- Clear chat button ---
    st.divider()
    if st.button("Clear Chat History"):
        # Reset the messages list in session state
        st.session_state.messages = []
        # st.rerun() refreshes the entire page
        st.rerun()


# ============================================================
# SECTION 4: Main Page Header
# ============================================================
st.title(f"{APP_ICON} {APP_TITLE}")
st.caption("Ask questions about company documents — get accurate, cited answers powered by Amazon Bedrock RAG.")
# st.caption() = smaller gray text, good for subtitles


# ============================================================
# SECTION 5: Session State — Chat History
# 
# WHAT IS SESSION STATE?
# Streamlit re-runs the ENTIRE script every time the user
# interacts (types, clicks, etc.). Without session_state,
# all variables reset on every interaction.
# 
# st.session_state = a dictionary that PERSISTS across reruns.
# We store chat messages here so they don't disappear.
# ============================================================

# Check if "messages" key exists in session state
# If not, initialize it as an empty list
if "messages" not in st.session_state:
    st.session_state.messages = []
    # messages will be a list of dicts like:
    # {"role": "user",      "content": "What is the leave policy?"}
    # {"role": "assistant", "content": "According to the handbook..."}


# ============================================================
# SECTION 6: Display All Previous Chat Messages
# Loop through stored messages and render each one
# ============================================================
for message in st.session_state.messages:
    
    # st.chat_message() creates a chat bubble
    # role = "user" shows a user avatar
    # role = "assistant" shows a bot avatar
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # st.markdown() renders text with markdown formatting
        # (bold, italics, bullet points, etc.)


# ============================================================
# SECTION 7: Chat Input Box
# 
# st.chat_input() creates the text box at the bottom of the page
# It returns the text when the user presses Enter, else None
# The := is the "walrus operator" — assigns AND checks in one line
# ============================================================
if question := st.chat_input("Ask a question about company documents..."):
    # This block only runs when the user submits a question
    
    # --- Display the user's question in the chat ---
    with st.chat_message("user"):
        st.markdown(question)
    
    # --- Save user message to session state ---
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })
    
    # --- Query Bedrock and display answer ---
    with st.chat_message("assistant"):
        # Show a loading spinner while waiting for Bedrock
        with st.spinner("Searching knowledge base and generating answer..."):
            
            # Call our RAG function (defined in bedrock_rag.py)
            # This returns a dict: {"success": True, "answer": "...", "citations": [...]}
            result = query_knowledge_base(question)
        
        if result["success"]:
            # --- Show the answer ---
            st.markdown(result["answer"])
            
            # --- Show citations in a collapsible section ---
            # st.expander() creates a collapsible section
            if result["citations"]:
                with st.expander(f"📎 View Sources ({len(result['citations'])} documents used)"):
                    # Loop through each citation
                    for i, citation in enumerate(result["citations"], start=1):
                        # start=1 means enumerate starts counting from 1, not 0
                        
                        # Format the S3 path nicely
                        # s3://my-bucket/documents/file.pdf → file.pdf
                        source_path = citation["source"]
                        file_name   = source_path.split("/")[-1]
                        # .split("/") splits "s3://bucket/docs/file.pdf" into a list
                        # [-1] gets the last element = "file.pdf"
                        
                        # Display each citation
                        st.markdown(f"**Source {i}: `{file_name}`**")
                        st.markdown(f"> {citation['excerpt']}")
                        # > in markdown = blockquote (indented gray text)
                        
                        if i < len(result["citations"]):
                            st.divider()  # line between citations
            else:
                # No citations means the AI answered from general knowledge
                # (should not happen with a well-configured Knowledge Base)
                st.warning("No specific citations found for this answer.")
        
        else:
            # Something went wrong — show the error
            st.error(f"Error: {result['answer']}")
    
    # --- Save assistant response to session state ---
    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"]
    })