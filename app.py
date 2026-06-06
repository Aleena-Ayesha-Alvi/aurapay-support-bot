# app.py
import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import HumanMessage, AIMessage

from vector_store import get_vector_store_retriever
from prompts import CONTEXTUALIZE_PROMPT, QA_PROMPT

from dotenv import load_dotenv 

load_dotenv()

st.set_page_config(page_title="AuraPay Support Assistant", page_icon="💳", layout="wide")

# --- UI SIDEBAR: Persistent Reset Controls ---
with st.sidebar:
    st.header("⚙️ Agent Controls")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": "👋 Hello! I am the AuraPay Enterprise Support Agent. I can assist you with API integrations, KYC compliance, chargebacks, GDPR, and SLAs. How can I help you today?", 
                "context": None
            }
        ]
        st.session_state.chat_history = []
        st.rerun()
    st.caption("Clearing history resets the model context length for new evaluation sessions.")

st.title("💳 AuraPay Enterprise Support Agent")

try:
    retriever = get_vector_store_retriever()
except Exception as e:
    st.error(f"Initialization Failed: {str(e)}")
    st.stop()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# Build the complete RAG Pipeline execution graph
history_aware_retriever = create_history_aware_retriever(llm, retriever, CONTEXTUALIZE_PROMPT)
question_answer_chain = create_stuff_documents_chain(llm, QA_PROMPT)
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

# Initialize Session State arrays on initial page layout instantiation
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "👋 Hello! I am the AuraPay Enterprise Support Agent. I can assist you with API integrations, KYC compliance, chargebacks, GDPR, and SLAs. How can I help you today?", 
            "context": None
        }
    ]
    st.session_state.chat_history = []

# Persistent UI Message Log rendering loop
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["context"]:
            with st.expander("🔍 View Retrieved Document Chunks"):
                for i, doc in enumerate(msg["context"]):
                    file_source = doc.metadata.get('source_file', 'Unknown File')
                    section_source = doc.metadata.get('Section', 'General')
                    st.markdown(f"**Chunk {i+1} from `{file_source}` (Section: {section_source}):**")
                    st.text(doc.page_content)
                    st.divider()
        st.markdown(msg["content"])

# Primary runtime chat input event capture
if prompt := st.chat_input("Ask about compliance, chargebacks, or APIs..."):
    st.session_state.messages.append({"role": "user", "content": prompt, "context": None})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching AuraPay policies..."):
            try:
                # ⚡ FULL CONTEXT HISTORY RETENTION ⚡
                # Passing the full historical conversation array directly to satisfy the 10+ turn requirement
                response = rag_chain.invoke({
                    "input": prompt,
                    "chat_history": st.session_state.chat_history 
                })
                
                answer = response["answer"]
                context_docs = response["context"]
                
                # Render metadata diagnostics block dynamically for the active query execution
                with st.expander("🔍 View Retrieved Document Chunks"):
                    for i, doc in enumerate(context_docs):
                        file_source = doc.metadata.get('source_file', 'Unknown File')
                        section_source = doc.metadata.get('Section', 'General')
                        st.markdown(f"**Chunk {i+1} from `{file_source}` (Section: {section_source}):**")
                        st.text(doc.page_content)
                        st.divider()
                
                st.markdown(answer)
                
                # Append to persistent storage blocks
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": answer, 
                    "context": context_docs
                })
                st.session_state.chat_history.extend(
                    [HumanMessage(content=prompt), AIMessage(content=answer)]
                )
            except Exception as e:
                st.error(f"Runtime Processing Failure: {str(e)}")