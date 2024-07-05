import dspy
from dspy.retrieve import BM25Retriever
from sentence_transformers import SentenceTransformer, util
from typing import List, Dict
import logging
import torch

class RAGSystem:
    def __init__(self, model, retriever_type='BM25'):
        self.model = model
        self.retriever_type = retriever_type
        self.lm = dspy.LM(model)
        self.documents = []
        
        if retriever_type == 'BM25':
            self.retriever = BM25Retriever(k=5)
        elif retriever_type == 'embedding':
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            self.embeddings = []

    def preprocess_document(self, text: str) -> str:
        # Implement any preprocessing steps (e.g., lowercasing, removing stopwords)
        return text.lower()

    def load_documents(self, documents: List[Dict[str, str]]):
        processed_docs = [{'id': doc['id'], 'text': self.preprocess_document(doc['text'])} for doc in documents]
        self.documents.extend(processed_docs)
        
        if self.retriever_type == 'BM25':
            self.retriever.add(processed_docs)
        elif self.retriever_type == 'embedding':
            self.embeddings = self.embedding_model.encode([doc['text'] for doc in self.documents], convert_to_tensor=True)

    def query(self, query: str) -> str:
        try:
            if self.retriever_type == 'BM25':
                retrieved_docs = self.retriever(query)
            elif self.retriever_type == 'embedding':
                query_embedding = self.embedding_model.encode(query, convert_to_tensor=True)
                cos_scores = util.pytorch_cos_sim(query_embedding, self.embeddings)[0]
                top_results = torch.topk(cos_scores, k=5)
                retrieved_docs = [self.documents[idx] for idx in top_results.indices]

            context = "\n".join([doc["text"] for doc in retrieved_docs])

            prompt = f"""Given the following context and query, provide a detailed answer:

            Context:
            {context}

            Query: {query}

            Answer:"""

            response = self.lm(prompt)
            return response
        except Exception as e:
            logging.error(f"Error during query: {e}")
            return "An error occurred while processing the query."

# Example usage:
# rag_system = RAGSystem(model, retriever_type='embedding')
# rag_system.load_documents([{"id": "1", "text": "Some company data..."}, ...])
# response = rag_system.query("What are the company's main products?")
