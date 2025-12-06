👨‍🍳 Assistant Recettes RAG (Qwen 2.5 + Recherche Hybride)

Ce projet est un assistant culinaire avancé utilisant la technique RAG (Retrieval-Augmented Generation).
Contrairement à un RAG basique, il utilise une Recherche Hybride qui combine la puissance vectorielle (IA) et des filtres logiques (Mots-clés, Synonymes, Exclusions).

🧠 Architecture Technique

LLM (Cerveau) : Qwen 2.5 Instruct (Modèle local performant en français).

Embedding (Yeux) : paraphrase-multilingual-mpnet-base-v2 (Compréhension sémantique fine).

Moteur de Recherche :

FAISS pour la recherche vectorielle rapide.

Re-ranking Python pour gérer les ingrédients obligatoires, les exclusions ("sans oeufs") et les synonymes ("vite" = "15m").

Données : Dataset de ~5000 vraies recettes françaises (importé via Hugging Face).

🚀 Installation

Cloner le projet

git clone https://github.com/maximegajic/recette.git
cd recette


Installer les dépendances

pip install -r requirements.txt


Télécharger les modèles (1x)
Attention : Télécharge environ 7 à 15 Go de données selon la version choisie.

python download_model.py


Générer les données (1x)
Crée le fichier data/recettes.json à partir du script de génération.

python generate_dataset.py


Créer l'index (1x)
Transforme les recettes en vecteurs mathématiques.

python app/indexer.py


🎮 Utilisation

Pour lancer l'assistant :

python app/main.py


💡 Conseils pour de meilleurs résultats

Le système analyse vos mots-clés. Pour une précision maximale, évitez les phrases longues et allez à l'essentiel.

Par plat : "quiche lorraine" (Plutôt que "Je voudrais une quiche...")

Par ingrédients : "boeuf carottes"

Avec contraintes (Synonymes) : "rapide pas cher" (Comprend "15m" et "Bon marché")

⚠️ Règle importante pour les exclusions ("SANS")

Le mot-clé sans agit comme une barrière. Tout ce qui est écrit APRÈS ce mot sera banni des résultats.
Il faut donc toujours formuler votre requête ainsi : [Ce que je veux] sans [Ce que j'interdis].

✅ Correct : "gâteau chocolat sans oeufs"

❌ Incorrect : "sans oeufs gâteau chocolat" (Cela bannirait le gâteau et le chocolat !)


📂 Structure du projet

app/ : Code source de l'application.

indexer.py : Création de la base vectorielle.

retriever.py : Moteur de recherche hybride (Synonymes, Accents, Filtres).

generate.py : Gestion du LLM (Qwen).

main.py : Point d'entrée.

data/ : Stockage (JSON des recettes + Index FAISS).

models/ : Modèles IA (non inclus dans git).

download_model.py : Script d'installation des modèles.

generate_dataset.py : Script de génération des recettes.

