👨‍🍳 Assistant Recettes RAG (Local)

Ce projet est un assistant culinaire intelligent utilisant la technique RAG (Retrieval-Augmented Generation). Il tourne entièrement en local sur votre machine.

🧱 Architecture

Données : Fichier JSON dans data/recettes.json.

Indexation : faiss-cpu pour la recherche vectorielle et sentence-transformers pour les embeddings.

LLM : Utilise un petit modèle (TinyLlama ou Phi-2) via transformers.

🚀 Installation

Cloner le projet

git clone <url_du_repo>
cd mon_rag


Installer les dépendances

pip install -r requirements.txt


Télécharger les modèles (À faire une seule fois)
Cela va télécharger le LLM et le modèle d'embedding dans le dossier ./models.

python download_model.py


Indexer les recettes
Génère la base de données vectorielle à partir de recettes.json.

python -m app.indexer


🎮 Lancer l'assistant

python -m app.main


📂 Structure

data/ : Contient vos recettes et l'index généré.

models/ : Contient les modèles téléchargés (non inclus dans git).

app/ :

indexer.py : Crée la base de données.

retriever.py : Cherche les informations.

generator.py : Gère le LLM.

main.py : L'interface utilisateur.

💡 Personnalisation

Ajoutez vos propres recettes dans data/recettes.json et relancez python -m app.indexer !