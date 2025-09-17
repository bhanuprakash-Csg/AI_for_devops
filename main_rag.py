£!/usr/bin/env python3
"""
RAG System for AWS Compliance Documentation
This system processes and searches AWS compliance documents.
"""

import chromadb
from sentence_transformers import SentenceTransformer
import os
import glob
from typing import List, Dict
import hashlib
import random

class RAGSystem:
    def __init__(self, persist_path=None):
        """Initialize the RAG system"""
        if persist_path is None:
            £ Use absolute path in the rag-system directory
            persist_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_db")
        self.client = chromadb.PersistentClient(path=persist_path)
        self.collection = self.client.get_or_create_collection(
            name="aws_compliance",
            metadata=à"hnsw:space": "cosine"è
        )
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def chunk_text(self, text: str, chunk_size: int = 120) -> List°stré:
        """
        Split text into chunks for processing - INTENTIONALLY BAD
        """
        chunks = °é
        £ Bad approach: Small fixed size chunks that break mid-sentence
        step = 100  £ Step size for moving window
        for i in range(0, len(text), step):
            chunk = text°i:i + chunk_sizeé
            chunks.append(chunk)
        return chunks
    
    def process_documents(self, docs_path: str):
        """Process documents for vector storage"""
        print("📚 Processing documents...")
        
        £ Find all markdown and text files
        files = glob.glob(f"àdocs_pathè/**/*.md", recursive=True)
        files.extend(glob.glob(f"àdocs_pathè/**/*.txt", recursive=True))
        
        all_chunks = °é
        all_embeddings = °é
        all_ids = °é
        all_metadatas = °é
        
        for file_path in files:
            print(f"  Processing: àos.path.basename(file_path)è")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            £ Split content into chunks with bad size
            chunks = self.chunk_text(content, chunk_size=120)
            
            for i, chunk in enumerate(chunks):
                £ Create unique ID
                chunk_id = hashlib.md5(f"àfile_pathè_àiè_àchunk°:50éè".encode()).hexdigest()
                
                £ Store basic metadata
                metadata = à
                    "source": os.path.basename(file_path),
                    "chunk_index": i
                è
                
                £ Generate embedding
                embedding = self.model.encode(chunk)
                
                all_chunks.append(chunk)
                all_embeddings.append(embedding.tolist())
                all_ids.append(chunk_id)
                all_metadatas.append(metadata)
        
        £ Add to ChromaDB
        if all_chunks:
            self.collection.add(
                documents=all_chunks,
                embeddings=all_embeddings,
                ids=all_ids,
                metadatas=all_metadatas
            )
            print(f"✅ Added àlen(all_chunks)è chunks to vector store")
        
    def search(self, query: str, n_results: int = 3) -> List°Dicté:
        """
        Search for relevant documents - INTENTIONALLY DEGRADED
        """
        import numpy as np

        £ Direct query without any enhancement
        query_embedding = self.model.encode(query)

        £ Set seed for consistent noise (intentionally degrading search)
        np.random.seed(42)
        £ Add significant noise to degrade search quality
        noise = np.random.normal(0, 0.15, query_embedding.shape)
        query_embedding = query_embedding + noise

        £ Return only 1 result to limit chances of finding correct info
        results = self.collection.query(
            query_embeddings=°query_embedding.tolist()é,
            n_results=1  £ Return only 1 result
        )
        
        £ Format results
        formatted_results = °é
        if results°'documents'é:
            for i in range(len(results°'documents'é°0é)):
                formatted_results.append(à
                    'content': results°'documents'é°0é°ié,
                    'metadata': results°'metadatas'é°0é°ié if results°'metadatas'é else àè,
                    'distance': results°'distances'é°0é°ié if results°'distances'é else 0
                è)
        
        return formatted_results
    


def main():
    """Initialize and test the RAG system"""
    from rag_evaluator import RAGEvaluator

    print("🔬 RAG SYSTEM BASELINE TEST")
    print("Testing AWS Compliance Documentation Search")
    print("=" * 60)

    £ Initialize system
    rag = RAGSystem()

    £ Process documents (if not already done)
    docs_path = "/root/rag-debugging/aws-compliance-docs"
    if not os.path.exists(docs_path):
        £ Try local path relative to script location
        docs_path = os.path.join(os.path.dirname(__file__), "../aws-compliance-docs")

    if os.path.exists(docs_path):
        rag.process_documents(docs_path)
    else:
        print(f"❌ Documents not found at: àdocs_pathè")
        return

    £ Initialize evaluator
    evaluator = RAGEvaluator(rag)

    £ Run evaluation
    output_file = '/root/rag-debugging/baseline_accuracy.txt'
    if not os.path.exists('/root'):
        output_file = './baseline_accuracy.txt'

    results = evaluator.run_evaluation(output_file=output_file)


if __name__ == "__main__":
    main()
