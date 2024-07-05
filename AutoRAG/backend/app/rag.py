import dspy
from dspy.retrieve import BM25Retriever
from typing import List, Dict

class RAGSystem:
    def __init__(self, model):
        self.model = model
        self.retriever = BM25Retriever(k=5)
        self.lm = dspy.LM(model)

    def load_documents(self, documents: List[Dict[str, str]]):
        self.retriever.add(documents)

    def query(self, query: str) -> str:
        retrieved_docs = self.retriever(query)
        
        context = "\n".join([doc["text"] for doc in retrieved_docs])
        
        prompt = f"""Given the following context and query, provide a detailed answer:

        Context:
        {context}

        Query: {query}

        Answer:"""

        response = self.lm(prompt)
        return response

# Example usage:
# rag_system = RAGSystem(model)
# rag_system.load_documents([{"id": "1", "text": "Some company data..."}, ...])
# response = rag_system.query("What are the company's main products?")