"""
Rebuild FAISS index when new documents are added to the data folder
"""
from src.data_loader import load_all_documents
from src.vectorstore import FaissVectorStore

print("=" * 60)
print("REBUILDING FAISS INDEX")
print("=" * 60)

# Load all documents from data folder
print("\n1. Loading documents from data folder...")
docs = load_all_documents('data')
print(f"   ✅ Loaded {len(docs)} documents")

# Create vector store
print("\n2. Creating vector store...")
store = FaissVectorStore('faiss_store')

# Build from documents (this will save automatically)
print("\n3. Building FAISS index with embeddings...")
store.build_from_documents(docs)

print("\n" + "=" * 60)
print("✅ SUCCESS! FAISS index rebuilt!")
print("Your chatbot can now answer questions from the new PDF.")
print("=" * 60)
