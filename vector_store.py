# vector_store.py
import os
import streamlit as st
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

@st.cache_resource
def get_vector_store_retriever():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    docs_dir = os.path.join(current_dir, "knowledge_base")
    index_dir = os.path.join(current_dir, "faiss_index") # We will save the DB here
    
    # Initialize embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # ⚡ THE SPEED FIX: If the database is already built, load it instantly
    if os.path.exists(index_dir):
        vectorstore = FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)
        return vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 7, "fetch_k": 20})

    # If no database exists, build it from scratch
    if not os.path.exists(docs_dir) or not os.listdir(docs_dir):
        raise FileNotFoundError(f"Knowledge base directory empty or missing at: {docs_dir}")

    loader = DirectoryLoader(docs_dir, glob="**/*.md", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
    raw_docs = loader.load()

    headers_to_split_on = [("#", "Document Title"), ("##", "Section")]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    
    processed_chunks = []
    for doc in raw_docs:
        filename = os.path.basename(doc.metadata['source'])
        sections = markdown_splitter.split_text(doc.page_content)
        final_splits = text_splitter.split_documents(sections)
        for chunk in final_splits:
            chunk.metadata['source_file'] = filename
            processed_chunks.append(chunk)
    
    vectorstore = FAISS.from_documents(processed_chunks, embeddings)
    
    # ⚡ Save to disk so we never have to wait 1 minute again
    vectorstore.save_local(index_dir)
    
    return vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 7, "fetch_k": 20})