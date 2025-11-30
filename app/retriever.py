import faiss
import pickle
import numpy as np
import os
from sentence_transformers import SentenceTransformer

class RecipeRetriever:
    def __init__(self):
        self.index_path = "data/faiss_index.bin"
        self.metadata_path = "data/metadata.pkl"
        self.embed_model_path = "./models/embed"
        
        self._load_resources()

    def _load_resources(self):
        if not os.path.exists(self.index_path):
            raise FileNotFoundError("Index non trouvé. Lancez app/indexer.py d'abord.")
            
        self.index = faiss.read_index(self.index_path)
        
        with open(self.metadata_path, 'rb') as f:
            self.recipes = pickle.load(f)
            
        if os.path.exists(self.embed_model_path):
            self.model = SentenceTransformer(self.embed_model_path)
        else:
            self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def search(self, query, k=2):
        """Cherche les k meilleures recettes pour la requête."""
        # 1. Vectoriser la requête
        query_vector = self.model.encode([query])
        faiss.normalize_L2(query_vector)

        # 2. Chercher dans FAISS
        distances, indices = self.index.search(query_vector, k)

        # 3. Récupérer les données réelles
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.recipes) and idx >= 0:
                recipe = self.recipes[idx]
                results.append(recipe)
        
        return results

if __name__ == "__main__":
    # Test rapide
    r = RecipeRetriever()
    print(r.search("J'ai des oeufs"))