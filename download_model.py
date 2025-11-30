import os
from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer

# Chemins de sauvegarde
MODEL_DIR = "./models/llm"
EMBED_DIR = "./models/embed"

def download_everything():
    print("⏳ Début du téléchargement des modèles...")

    # 1. Modèle d'Embeddings (très léger)
    # On utilise 'all-MiniLM-L6-v2', un standard rapide et efficace
    print("⬇️  Téléchargement du modèle d'embeddings (Sentence-Transformer)...")
    embed_model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model_emb = SentenceTransformer(embed_model_name)
    model_emb.save(EMBED_DIR)
    print("✅ Modèle d'embeddings sauvegardé dans ./models/embed")

    # 2. Modèle LLM
    # TinyLlama est choisi ici pour être sûr que ça tourne partout (1.1B params).
    # Si tu as plus de VRAM, remplace par "microsoft/phi-2"
    llm_model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    
    print(f"⬇️  Téléchargement du LLM ({llm_model_name})...")
    tokenizer = AutoTokenizer.from_pretrained(llm_model_name)
    model = AutoModelForCausalLM.from_pretrained(llm_model_name)
    
    tokenizer.save_pretrained(MODEL_DIR)
    model.save_pretrained(MODEL_DIR)
    print("✅ LLM sauvegardé dans ./models/llm")

    print("\n🎉 Tout est prêt ! Tu peux lancer l'indexation.")

if __name__ == "__main__":
    # Créer les dossiers si inexistants
    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs(EMBED_DIR, exist_ok=True)
    download_everything()