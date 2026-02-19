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
    
    # Greetings and generic patterns that don't need RAG
    OUT_OF_SCOPE_PATTERNS = [
        "hello", "hi", "hey", "good morning", "good afternoon", "good evening",
        "how are you", "what's up", "whats up", "thanks", "thank you", "bye",
        "goodbye", "ok", "okay", "cool", "great", "nice", "sure", "help",
        "what can you do", "what do you do", "who are you", "what are you"
    ]

    def _is_out_of_scope(self, question: str) -> bool:
        """Check if the question is a greeting or off-topic query that doesn't need RAG."""
        q = question.strip().lower().rstrip('?!.')
        # Exact or near-exact match with common phrases
        if q in self.OUT_OF_SCOPE_PATTERNS:
            return True
        # Very short questions (1-2 words) that aren't domain queries
        words = q.split()
        if len(words) <= 2 and not any(kw in q for kw in ["leave", "policy", "salary", "hr", "ceo", "benefit", "vacation", "medical", "bonus"]):
            return True
        return False

    def _get_out_of_scope_response(self, question: str) -> str:
        """Generate a friendly response for out-of-scope questions."""
        prompt = f"""You are a helpful HR/company policy assistant. The user said: "{question}"

This is a greeting or general question, not a policy query. Respond briefly and naturally, and let them know you can help with company policies, HR documents, leave policies, benefits, or any document-related questions."""
        response = self.llm.invoke([prompt])
        return response.content

    def query(self, question: str, top_k: int = 5, min_score: float = 0.0, stream: bool = False, summarize: bool = False, conversation_history: list = None) -> Dict[str, Any]:
        """
        Execute an advanced RAG query with conversation memory and relevance filtering.

        Args:
            question: The user's question
            top_k: Number of top documents to retrieve
            min_score: Minimum similarity score threshold — chunks below this are dropped
            stream: Whether to stream the prompt (for demonstration)
            summarize: Whether to generate a summary
            conversation_history: List of {role, content} dicts from previous turns

        Returns:
            Dictionary with question, answer, sources, summary, history
        """
        if conversation_history is None:
            conversation_history = []

        # Keep only last 3 turns (6 messages: 3 user + 3 assistant) to stay within token limits
        recent_history = conversation_history[-6:]

        # --- Out-of-scope detection ---
        if self._is_out_of_scope(question):
            answer = self._get_out_of_scope_response(question)
            self.history.append({'question': question, 'answer': answer, 'sources': [], 'summary': None})
            return {'question': question, 'answer': answer, 'sources': [], 'summary': None, 'history': self.history}

        # Retrieve relevant documents from FAISS
        raw_results = self.vectorstore.query(question, top_k=top_k)

        # Convert to retriever format
        results = self._convert_faiss_results_to_retriever_format(raw_results)

        if not results:
            answer = "I couldn't find relevant information in the company documents for your question. Please try rephrasing, or ask about HR policies, leave, benefits, or other company topics."
            sources = []
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

            # Build conversation history block for the prompt
            history_block = ""
            if recent_history:
                history_lines = []
                for turn in recent_history:
                    role = "User" if turn.get("role") == "user" else "Assistant"
                    history_lines.append(f"{role}: {turn.get('content', '').strip()}")
                history_block = "Conversation so far:\n" + "\n".join(history_lines) + "\n\n"

            # Create prompt with optional conversation context
            prompt = f"""You are a helpful HR and company policy assistant. Use the context below to answer the question accurately and in detail.

IMPORTANT: If the context contains numbers, statistics, percentages, dates, or amounts, ALWAYS include them in your answer.

{history_block}Context from company documents:
{context}

Current question: {question}

Answer (detailed, using the context above):"""

            if stream:
                print("\n[STREAMING] Generating response...")
                for i in range(0, len(prompt), 80):
                    print(prompt[i:i+80], end='', flush=True)
                    time.sleep(0.02)
                print("\n")

            response = self.llm.invoke([prompt])
            answer = response.content

        # --- Smart citations: only add if answer is substantive and from documents ---
        answer_with_citations = answer
        is_substantive = (
            sources
            and len(answer) > 80
            and not answer.startswith("I couldn't find")
        )
        if is_substantive:
            top_source = sources[0]  # Only cite the top/most relevant source
            citation_line = f"\n\nCitation:\n[1] {top_source['source']} (page {top_source['page']})"
            answer_with_citations = answer + citation_line

        # --- Summarization ---
        summary = None
        if summarize and sources and len(answer) > 80:
            summary_prompt = f"Provide a concise summary of the following answer in 3-4 sentences, highlighting the key points:\n{answer}"
            summary_resp = self.llm.invoke([summary_prompt])
            summary = summary_resp.content

        # --- Generate follow-up questions (only for substantive answers) ---
        follow_up_questions = []
        if is_substantive:
            followup_prompt = f"""Based on this Q&A about company policies, generate exactly 2 short follow-up questions the user might ask next.
Output ONLY the questions as a numbered list (1. ... 2. ...), nothing else.

Q: {question}
A: {answer[:400]}"""
            try:
                followup_resp = self.llm.invoke([followup_prompt])
                # Parse numbered list: "1. Question" → extract just the question text
                for line in followup_resp.content.strip().split('\n'):
                    line = line.strip()
                    # Match lines like "1. ..." or "1) ..."
                    import re
                    match = re.match(r'^\d+[.)\s]+(.+)$', line)
                    if match:
                        follow_up_questions.append(match.group(1).strip())
                follow_up_questions = follow_up_questions[:2]  # cap at 2
            except Exception:
                follow_up_questions = []

        # Store in history
        self.history.append({'question': question, 'answer': answer, 'sources': sources, 'summary': summary})

        return {
            'question': question,
            'answer': answer_with_citations,
            'sources': sources,
            'summary': summary,
            'follow_up_questions': follow_up_questions,
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


