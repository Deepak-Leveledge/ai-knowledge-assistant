import streamlit as st
import os
from utils import upload_file, chat_with_bot

st.set_page_config(page_title="AI Knowledge Assistant", page_icon="🤖", layout="wide")

# Initialize session state for uploaded files if not exists
if "uploaded_files" not in st.session_state:
    st.session_state["uploaded_files"] = []

# Sidebar - Upload Section
st.sidebar.header("📂 Upload Documents")
uploaded_files = st.sidebar.file_uploader(
    "Choose files (.pdf, .txt, .docx)", 
    type=["pdf", "txt", "docx"],
    accept_multiple_files=True
)

# Process uploaded files
if uploaded_files:
    # Convert Streamlit files to disk paths
    file_paths = []
    for uploaded_file in uploaded_files:
        if uploaded_file.name not in [f["name"] for f in st.session_state.uploaded_files]:
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())
            file_paths.append(uploaded_file.name)

    if file_paths:
        with st.spinner("Uploading and processing..."):
            res = upload_file(file_paths)
            if res.get("status") == "success":
                for file in res["files"]:
                    st.session_state.uploaded_files.append({
                        "name": file["filename"],
                        "chunks": file["chunks"]
                    })
                st.success(f"✅ {res['message']}")
            else:
                st.error("Error uploading files.")

# Display uploaded files in sidebar
if st.session_state.uploaded_files:
    st.sidebar.markdown("### Uploaded Files:")
    for file in st.session_state.uploaded_files:
        st.sidebar.markdown(f"📄 {file['name']} ({file['chunks']} chunks)")
    
    # Add button to clear uploads
    if st.sidebar.button("Clear All Files"):
        st.session_state.uploaded_files = []
        # Optional: Remove physical files
        for file in st.session_state.uploaded_files:
            if os.path.exists(file["name"]):
                os.remove(file["name"])
        st.sidebar.success("All files cleared!")

st.title("💬 Chat with Your Knowledge Base")

# Initialize session state for chat
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Chat Input
query = st.text_input("Ask a question from your documents...")

if st.button("Send") and query:
    with st.spinner("Thinking..."):
        result = chat_with_bot(query)
    answer = result.get("answer", "No answer generated.")
    st.session_state["chat_history"].append({"user": query, "bot": answer})

# Display chat history
for chat in reversed(st.session_state["chat_history"]):
    st.markdown(f"**🧑 You:** {chat['user']}")
    st.markdown(f"**🤖 Bot:** {chat['bot']}")
    st.markdown("---")