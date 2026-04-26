from sentence_transformers import SentenceTransformer, util
import torch

class DenseRetriever:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.chunks = []
        self.corpus_embeddings = None

    def add_chunks(self, chunks):
        self.chunks = chunks
        texts = [c['text'] for c in chunks]
        self.corpus_embeddings = self.model.encode(texts, convert_to_tensor=True)

    def retrieve(self, query, k=3):
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        cos_scores = util.cos_sim(query_embedding, self.corpus_embeddings)[0]
        top_results = torch.topk(cos_scores, k=k)
        
        results = []
        for score, idx in zip(top_results[0], top_results[1]):
            results.append({
                "chunk": self.chunks[idx],
                "score": float(score)
            })
        return results
