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

def build_index():
    print("⚙️  Chargement des données...")
    if not os.path.exists(DATA_PATH):
        print(f"❌ Erreur: Fichier {DATA_PATH} introuvable.")
        return

    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        recipes = json.load(f)

    print(f"📝 Préparation de {len(recipes)} recettes avec BOOST du TITRE...")
    
    texts_to_embed = []
    for r in recipes:
        # --- TECHNIQUE DE BOOSTING ---
        # On répète le titre 3 fois de manière naturelle.
        # Cela "crie" à l'IA que le sujet principal est le titre, pas les ingrédients.
        text = (
            f"Recette de {r['titre']}. "             # 1ère mention
            f"Plat : {r['titre']}. "                 # 2ème mention
            f"Titre : {r['titre']}. \n"              # 3ème mention
            f"Ingrédients : {', '.join(r['ingredients'])}. "
            f"Difficulté : {r.get('difficulte', '')}. "
            f"Prix : {r.get('prix', '')}. "
            f"Temps : {r.get('temps', '')}."
        )
        texts_to_embed.append(text)

    print("🧠 Chargement du modèle Multilingue (Auto)...")
    # On utilise toujours le modèle qui comprend le français
    model = SentenceTransformer("./models/embed")

    print("🧠 Génération des embeddings optimisés...")
    embeddings = model.encode(texts_to_embed, show_progress_bar=True)
    
    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    print(f"💾 Sauvegarde de l'index...")
    faiss.write_index(index, INDEX_PATH)
    
    with open(METADATA_PATH, 'wb') as f:
        pickle.dump(recipes, f)

    print("✅ Indexation terminée ! Les titres sont maintenant prioritaires.")

if __name__ == "__main__":
    build_index()