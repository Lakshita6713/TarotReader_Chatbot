# pdf_embedder.py

from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions
import fitz  # PyMuPDF

class TarotPDFEmbedder:
    def __init__(self, pdf_path, collection_name="tarot_cards", model_name="all-MiniLM-L6-v2"):
        self.pdf_path = pdf_path
        self.chroma_client = chromadb.Client()
        self.model = SentenceTransformer(model_name)
        self.embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model_name)
        self.collection = self.chroma_client.get_or_create_collection(name=collection_name, embedding_function=self.embed_fn)

    def extract_paragraphs(self):
        doc = fitz.open(self.pdf_path)
        paragraphs = []
        for page in doc:
            text = page.get_text()
            chunks = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 40]
            paragraphs.extend(chunks)
        return paragraphs

    def build_vector_store(self):
        paragraphs = self.extract_paragraphs()
        ids = [f"chunk_{i}" for i in range(len(paragraphs))]
        self.collection.add(documents=paragraphs, ids=ids)
        print(f"🔗 Indexed {len(paragraphs)} chunks from PDF.")

    def search(self, query, top_k=3):
        return self.collection.query(query_texts=[query], n_results=top_k)