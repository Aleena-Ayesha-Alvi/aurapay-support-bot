import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

print("Loading FAISS database...")

# 1. Point to your saved database folder
current_dir = os.path.dirname(os.path.abspath(__file__))
index_dir = os.path.join(current_dir, "faiss_index")

# 2. Load the embeddings and the database
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)

# 3. Print the total number of chunks
total_chunks = vectorstore.index.ntotal
print("="*40)
print(f"✅ Total chunks inside the database: {total_chunks}")
print("="*40)