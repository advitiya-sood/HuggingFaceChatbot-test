"""
Startup script - runs before the API server starts.
Builds the FAISS index if it doesn't exist yet.
"""
import os

FAISS_INDEX_PATH = "faiss_store/faiss.index"
FAISS_META_PATH = "faiss_store/metadata.pkl"
DATA_DIR = "data"

def needs_rebuild():
    """Check if FAISS index needs to be built."""
    return not (os.path.exists(FAISS_INDEX_PATH) and os.path.exists(FAISS_META_PATH))

if needs_rebuild():
    print("=" * 60)
    print("FAISS index not found. Building from documents...")
    print("=" * 60)

    from src.data_loader import load_all_documents
    from src.vectorstore import FaissVectorStore

    docs = load_all_documents(DATA_DIR)
    print(f"Loaded {len(docs)} documents from {DATA_DIR}/")

    store = FaissVectorStore("faiss_store")
    store.build_from_documents(docs)

    print("=" * 60)
    print("FAISS index built successfully! Starting API server...")
    print("=" * 60)
else:
    print("FAISS index found. Skipping rebuild. Starting API server...")
