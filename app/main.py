import sys
import os

# Ajout du dossier courant au path pour les imports si nécessaire
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.retriever import RecipeRetriever
from app.generate import RAGGenerator

def main():
    print("========================================")
    print("👨‍🍳  ASSISTANT RECETTES RAG (Local)  👩‍🍳")
    print("========================================")

    # 1. Initialisation
    print("⏳ Initialisation du système...")
    try:
        retriever = RecipeRetriever()
        generator = RAGGenerator()
    except Exception as e:
        print(f"❌ Erreur au démarrage : {e}")
        return

    print("\n✅ Prêt ! (Tapez 'q' pour quitter)")

    # 2. Boucle de chat
    while True:
        user_input = input("\n🗣️  Ta question (ex: 'Que faire avec des carottes ?') : ")
        
        if user_input.lower() in ['q', 'quit', 'exit']:
            print("Au revoir et bon appétit ! 👋")
            break

        # A. Retrieval (Recherche)
        print("   🔍 Recherche des recettes pertinentes...")
        recipes = retriever.search(user_input, k=10)
        
        if not recipes:
            print("   ⚠️ Aucune recette trouvée dans la base.")
            continue
            
        print(f"   📄 {len(recipes)} recettes trouvées : {[r['titre'] for r in recipes]}")

        # B. Generation (Réponse)
        print("   🧠 Le Chef réfléchit (Génération LLM)...")
        answer = generator.generate_response(user_input, recipes)
        
        print("\n📢  RÉPONSE :")
        print("-" * 20)
        print(answer)
        print("-" * 20)

if __name__ == "__main__":
    main()