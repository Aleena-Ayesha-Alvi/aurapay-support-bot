# app.py
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
from langchain_groq import ChatGroq
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import HumanMessage, AIMessage

# Import our custom modules
from vector_store import get_vector_store_retriever
from prompts import CONTEXTUALIZE_PROMPT, QA_PROMPT

# 1. UI Setup
st.set_page_config(page_title="AuraPay Support Assistant", page_icon="💳", layout="wide")
st.title("💳 AuraPay Enterprise Support Agent")

# 2. Dependency Routing
try:
    retriever = get_vector_store_retriever()
except Exception as e:
    st.error(f"Initialization Failed: {str(e)}")
    st.info("Please verify that 'setup_docs.py' has run successfully.")
    st.stop()

# Initialize LLM via Groq
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# 3. Assemble RAG Architecture Chains
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, CONTEXTUALIZE_PROMPT
)
question_answer_chain = create_stuff_documents_chain(llm, QA_PROMPT)
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

# 4. State Management & Message Log History Rendering
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

# 5. Runtime Chat Loop
if prompt := st.chat_input("Ask about compliance, chargebacks, or APIs..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching AuraPay policies..."):
            try:
                # Trigger pipeline orchestration
                response = rag_chain.invoke({
                    "input": prompt,
                    "chat_history": st.session_state.chat_history
                })
                
                answer = response["answer"]
                
                # Render metadata diagnostics block
                with st.expander("🔍 View Retrieved Document Chunks"):
                    for i, doc in enumerate(response["context"]):
                        file_source = doc.metadata.get('source_file', 'Unknown File')
                        section_source = doc.metadata.get('Section', 'General')
                        st.markdown(f"**Chunk {i+1} from `{file_source}` (Section: {section_source}):**")
                        st.text(doc.page_content)
                        st.divider()
                
                # Present final response
                st.markdown(answer)
                
                # Append transaction frames to sliding memory cache
                st.session_state.chat_history.extend(
                    [HumanMessage(content=prompt), AIMessage(content=answer)]
                )
            except Exception as e:
                st.error(f"Runtime Processing Failure: {str(e)}")