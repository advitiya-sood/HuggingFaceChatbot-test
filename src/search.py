import os
from dotenv import load_dotenv
from src.vectorstore import FaissVectorStore
from langchain_groq import ChatGroq
from typing import List, Dict, Any
import time

load_dotenv()

class RAGSearch:
    """Basic RAG search implementation with simple summarization."""
    def __init__(self, persist_dir: str = "faiss_store", embedding_model: str = "paraphrase-MiniLM-L3-v2", llm_model: str = "llama-3.1-8b-instant"):
        self.vectorstore = FaissVectorStore(persist_dir, embedding_model)
        # Load or build vectorstore
        faiss_path = os.path.join(persist_dir, "faiss.index")
        meta_path = os.path.join(persist_dir, "metadata.pkl")
        if not (os.path.exists(faiss_path) and os.path.exists(meta_path)):
            from data_loader import load_all_documents
            docs = load_all_documents("data")
            self.vectorstore.build_from_documents(docs)
        else:
            self.vectorstore.load()
        groq_api_key = os.environ.get("GROQ_API_KEY")
        self.llm = ChatGroq(groq_api_key=groq_api_key, model_name=llm_model)
        print(f"[INFO] Groq LLM initialized: {llm_model}")

    def search_and_summarize(self, query: str, top_k: int = 5) -> str:
        """Simple search and summarize - returns only the answer text."""
        results = self.vectorstore.query(query, top_k=top_k)
        texts = [r["metadata"].get("text", "") for r in results if r["metadata"]]
        context = "\n\n".join(texts)
        if not context:
            return "No relevant documents found."
        prompt = f"""Summarize the following context for the query: '{query}'\n\nContext:\n{context}\n\nSummary:"""
        response = self.llm.invoke([prompt])
        return response.content


class AdvancedRAGPipeline:
    """
    Advanced RAG Pipeline with streaming, citations, history tracking, and summarization.
    
    Features:
    - Streaming responses for real-time output
    - Automatic citation generation with source files and page numbers
    - Query history tracking
    - Optional answer summarization
    """
    
    def __init__(self, persist_dir: str = "faiss_store", embedding_model: str = "paraphrase-MiniLM-L3-v2", llm_model: str = "llama-3.1-8b-instant"):
        """
        Initialize the Advanced RAG Pipeline.
        
        Args:
            persist_dir: Directory to persist FAISS index
            embedding_model: Name of the sentence transformer model
            llm_model: Name of the Groq LLM model
        """
        self.vectorstore = FaissVectorStore(persist_dir, embedding_model)
        
        # Load or build vectorstore
        faiss_path = os.path.join(persist_dir, "faiss.index")
        meta_path = os.path.join(persist_dir, "metadata.pkl")
        if not (os.path.exists(faiss_path) and os.path.exists(meta_path)):
            from data_loader import load_all_documents
            docs = load_all_documents("data")
            self.vectorstore.build_from_documents(docs)
        else:
            self.vectorstore.load()
        
        # Initialize LLM
        groq_api_key = os.environ.get("GROQ_API_KEY")
        self.llm = ChatGroq(groq_api_key=groq_api_key, model_name=llm_model)
        
        # Initialize query history
        self.history = []
        
        print(f"[INFO] Advanced RAG Pipeline initialized with {llm_model}")
    
    def _convert_faiss_results_to_retriever_format(self, results: List[Dict]) -> List[Dict[str, Any]]:
        """
        Convert FAISS query results to the retriever format expected by the pipeline.
        
        Args:
            results: Raw results from FAISS vectorstore.query()
        
        Returns:
            List of dicts with 'content', 'metadata', and 'similarity_score'
        """
        formatted_results = []
        for result in results:
            # Calculate similarity score from distance (FAISS uses L2 distance)
            # Convert L2 distance to similarity score (inverse relationship)
            distance = result.get('distance', 0)
            similarity_score = 1 / (1 + distance)  # Simple conversion
            
            formatted_results.append({
                'content': result['metadata'].get('text', ''),
                'metadata': result['metadata'],
                'similarity_score': similarity_score
            })
        
        return formatted_results
    
    def query(self, question: str, top_k: int = 5, min_score: float = 0.0, stream: bool = False, summarize: bool = False) -> Dict[str, Any]:
        """
        Execute an advanced RAG query with optional streaming and summarization.
        
        Args:
            question: The user's question
            top_k: Number of top documents to retrieve
            min_score: Minimum similarity score threshold (0.0 to 1.0)
            stream: Whether to stream the prompt (for demonstration)
            summarize: Whether to generate a 2-sentence summary
        
        Returns:
            Dictionary containing:
            - question: The original question
            - answer: Answer with citations
            - sources: List of source documents with metadata
            - summary: Optional 2-sentence summary
            - history: Complete query history
        """
        # Retrieve relevant documents from FAISS
        raw_results = self.vectorstore.query(question, top_k=top_k)
        
        # Convert to retriever format
        results = self._convert_faiss_results_to_retriever_format(raw_results)
        
        # Filter by minimum score if specified
        if min_score > 0.0:
            results = [r for r in results if r['similarity_score'] >= min_score]
        
        if not results:
            answer = "No relevant context found."
            sources = []
            context = ""
        else:
            # Build context from retrieved documents
            context = "\n\n".join([doc['content'] for doc in results])
            
            # Extract sources with metadata
            sources = [{
                'source': doc['metadata'].get('source_file', doc['metadata'].get('source', 'unknown')),
                'page': doc['metadata'].get('page', 'unknown'),
                'score': doc['similarity_score'],
                'preview': doc['content'][:120] + '...' if len(doc['content']) > 120 else doc['content']
            } for doc in results]
            
            # Create prompt - request DETAILED answers with emphasis on numbers/data
            prompt = f"""Use the following context to answer the question in detail. Provide a comprehensive answer with all relevant information.

IMPORTANT: If the context contains numbers, statistics, percentages, dates, amounts, or structured data (tables/matrices), ALWAYS include them in your answer. Prioritize specific numerical details.

Context:
{context}

Question: {question}

Answer (provide a detailed response with all relevant numbers and data):"""
            
            # Optional streaming (demonstration - prints prompt in chunks)
            if stream:
                print("\n[STREAMING] Generating response...")
                for i in range(0, len(prompt), 80):
                    print(prompt[i:i+80], end='', flush=True)
                    time.sleep(0.02)  # Reduced sleep time for faster streaming
                print("\n")
            
            # Generate answer using LLM
            response = self.llm.invoke([prompt])
            answer = response.content
        
        # Add citations to answer
        citations = [f"[{i+1}] {src['source']} (page {src['page']})" for i, src in enumerate(sources)]
        answer_with_citations = answer + "\n\nCitations:\n" + "\n".join(citations) if citations else answer
        
        # Optional summarization
        summary = None
        if summarize and answer and answer != "No relevant context found.":
            summary_prompt = f"Summarize the following answer in 2 sentences:\n{answer}"
            summary_resp = self.llm.invoke([summary_prompt])
            summary = summary_resp.content
        
        # Store in query history
        self.history.append({
            'question': question,
            'answer': answer,
            'sources': sources,
            'summary': summary
        })
        
        # Return comprehensive result
        return {
            'question': question,
            'answer': answer_with_citations,
            'sources': sources,
            'summary': summary,
            'history': self.history
        }
    
    def get_history(self) -> List[Dict[str, Any]]:
        """
        Get the complete query history.
        
        Returns:
            List of all previous queries and responses
        """
        return self.history
    
    def clear_history(self):
        """Clear the query history."""
        self.history = []
        print("[INFO] Query history cleared")


