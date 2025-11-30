import json
import os
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

# Configuration
DATA_PATH = "data/recettes.json"
INDEX_PATH = "data/faiss_index.bin"
METADATA_PATH = "data/metadata.pkl"
EMBED_MODEL_PATH = "./models/embed"

def build_index():
    print("⚙️  Chargement des données...")
    if not os.path.exists(DATA_PATH):
        print(f"❌ Erreur: Fichier {DATA_PATH} introuvable.")
        return

    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        recipes = json.load(f)

    # Préparer le texte à vectoriser
    # On combine titre et ingrédients pour la recherche
    texts_to_embed = [
        f"{r['titre']} ingredients: {' '.join(r['ingredients'])}" 
        for r in recipes
    ]

    print("🧠 Génération des embeddings (vecteurs)...")
    # Chargement du modèle local
    if os.path.exists(EMBED_MODEL_PATH):
        model = SentenceTransformer(EMBED_MODEL_PATH)
    else:
        # Fallback si pas téléchargé localement
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    embeddings = model.encode(texts_to_embed, show_progress_bar=True)
    
    # Normalisation (utile pour la distance cosinus avec IndexFlatIP)
    faiss.normalize_L2(embeddings)

    # Création de l'index FAISS
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension) # IP = Inner Product (similaire à cosine si normalisé)
    index.add(embeddings)

    print(f"💾 Sauvegarde de l'index ({len(recipes)} recettes)...")
    faiss.write_index(index, INDEX_PATH)
    
    # On sauvegarde aussi les recettes brutes pour pouvoir les retrouver par ID
    with open(METADATA_PATH, 'wb') as f:
        pickle.dump(recipes, f)

    print("✅ Indexation terminée !")

if __name__ == "__main__":
    build_index()