import os
import shutil
from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer

# Chemins de sauvegarde
MODEL_DIR = "./models/llm"
EMBED_DIR = "./models/embed"

def download_everything():
    print("🚀 DÉMARRAGE DU TÉLÉCHARGEMENT (Version Équilibrée 3B)...")
    
    # 1. Modèle d'Embeddings - ON GARDE LE MEILLEUR (MPNet)
    # Il est très léger (400Mo) donc aucun impact sur le partage du GPU,
    # mais il est essentiel pour que la recherche (Boeuf vs Carottes) fonctionne bien.
    print("⬇️  Téléchargement du modèle d'embeddings MPNet...")
    
    if os.path.exists(EMBED_DIR):
        # On supprime si c'était l'ancien MiniLM pour éviter les conflits
        # Mais si c'est déjà MPNet, le script SentenceTransformer gère le cache intelligemment
        print("🧹  Vérification du dossier embedding...")
        shutil.rmtree(EMBED_DIR)
        
    embed_model_name = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    model_emb = SentenceTransformer(embed_model_name)
    model_emb.save(EMBED_DIR)
    print("✅ Modèle MPNet sauvegardé dans ./models/embed")

    # 2. Modèle LLM - LE COMPROMIS IDÉAL (3B)
    # Qwen 2.5 3B Instruct :
    # - 2x plus intelligent que le 1.5B (meilleur respect des consignes)
    # - 2x plus léger que le 7B (seulement ~6-7 Go VRAM) -> Parfait pour le partage GPU
    llm_model_name = "Qwen/Qwen2.5-3B-Instruct"
    
    print(f"⬇️  Téléchargement du LLM ({llm_model_name})...")
    
    # Vérification simple
    if os.path.exists(MODEL_DIR) and len(os.listdir(MODEL_DIR)) > 3:
        print("✅ Le LLM semble déjà téléchargé. On passe.")
    else:
        print("☕️  Téléchargement en cours (environ 6-7 Go)...")
        if os.path.exists(MODEL_DIR):
            shutil.rmtree(MODEL_DIR)
        
        tokenizer = AutoTokenizer.from_pretrained(llm_model_name)
        model = AutoModelForCausalLM.from_pretrained(llm_model_name)
        
        tokenizer.save_pretrained(MODEL_DIR)
        model.save_pretrained(MODEL_DIR)
        print("✅ LLM Qwen 3B sauvegardé dans ./models/llm")

    print("\n⚠️  IMPORTANT : Modèle d'embedding mis à jour (MPNet).")
    print("1. Vérifie que indexer.py pointe vers './models/embed'.")
    print("2. TU DOIS RELANCER L'INDEXATION : python app/indexer.py")

if __name__ == "__main__":
    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs(EMBED_DIR, exist_ok=True)
    download_everything()