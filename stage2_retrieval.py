import json
from rank_bm25 import BM25Okapi
import nltk
from nltk.tokenize import word_tokenize
import os

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class ChunkStore:
    def __init__(self):
        self.chunks = []
        self.bm25 = None
        self.tokenized_corpus = []

    def add_chunks(self, chunks_with_metadata):
        self.chunks.extend(chunks_with_metadata)
        self.tokenized_corpus = [word_tokenize(c['text'].lower()) for c in self.chunks]
        self.bm25 = BM25Okapi(self.tokenized_corpus)

    def retrieve(self, query, k=3):
        tokenized_query = word_tokenize(query.lower())
        scores = self.bm25.get_scores(tokenized_query)
        top_n = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        return [self.chunks[i] for i in top_n]

def chunk_text(text, metadata, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk_text = " ".join(words[i:i + chunk_size])
        chunks.append({
            "text": chunk_text,
            "metadata": metadata
        })
    return chunks

if __name__ == "__main__":
    # This part will be used in the notebook
    pass
