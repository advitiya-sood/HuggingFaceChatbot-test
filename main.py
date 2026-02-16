from src.data_loader import load_all_documents
from src.vectorstore import FaissVectorStore
from src.search import RAGSearch, AdvancedRAGPipeline

# Example usage
if __name__ == "__main__":
    
    # Option 1: Basic RAG Search (Simple and Fast)
    print("="*60)
    print("OPTION 1: Basic RAG Search")
    print("="*60)
    
    basic_rag = RAGSearch()
    query = "Who is the ceo of Bhavna corp?"
    summary = basic_rag.search_and_summarize(query, top_k=3)
    print(f"\nQuery: {query}")
    print(f"Summary: {summary}")
    
    print("\n" + "="*60)
    print("OPTION 2: Advanced RAG Pipeline")
    print("="*60)
    
    # Option 2: Advanced RAG Pipeline (Feature-Rich)
    advanced_rag = AdvancedRAGPipeline()
    
    # Query with all advanced features enabled
    result = advanced_rag.query(
        question=query,
        top_k=3,
        min_score=0.0,
        stream=False,  # Set to True to see streaming in action
        summarize=True
    )
    
    print(f"\nQuery: {result['question']}")
    print(f"\nAnswer with Citations:\n{result['answer']}")
    
    if result['summary']:
        print(f"\n2-Sentence Summary:\n{result['summary']}")
    
    print(f"\nRetrieved Sources:")
    for i, source in enumerate(result['sources'], 1):
        print(f"  [{i}] {source['source']} (page {source['page']}) - Score: {source['score']:.4f}")
    
    # Demonstrate history tracking
    print(f"\nQuery History: {len(advanced_rag.get_history())} queries stored")
    
    # You can ask another question to see history grow
    print("\n" + "-"*60)
    print("Asking a follow-up question...")
    print("-"*60)
    
    result2 = advanced_rag.query(
        "Tell me about maternity leave",
        top_k=3,
        summarize=True
    )
    
    print(f"\nQuery: {result2['question']}")
    print(f"\nAnswer:\n{result2['answer']}")
    
    if result2['summary']:
        print(f"\n2-Sentence Summary:\n{result2['summary']}")
    
    print(f"\nTotal Query History: {len(advanced_rag.get_history())} queries")
