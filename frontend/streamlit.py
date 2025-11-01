import streamlit as st
from utils import upload_file, chat_with_bot

st.set_page_config(page_title="AI Knowledge Assistant", page_icon="🤖", layout="wide")

# Sidebar - Upload Section
st.sidebar.header("📂 Upload Documents")
uploaded_file = st.sidebar.file_uploader("Choose a file (.pdf or .txt)", type=["pdf", "txt"])

if uploaded_file:
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    with st.spinner("Uploading and processing your file..."):
        res = upload_file(uploaded_file.name)
    st.sidebar.success(f"File uploaded and {res.get('chunks_added')} chunks added!")

st.title("💬 Chat with Your Knowledge Base")

# Initialize session state for chat
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Chat Input
query = st.text_input("Ask a question from your document...")

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
