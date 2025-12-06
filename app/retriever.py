import faiss
import pickle
import numpy as np
import os
import unicodedata # <--- LA CLÉ MAGIQUE
from sentence_transformers import SentenceTransformer

class RecipeRetriever:
    def __init__(self):
        self.index_path = "data/faiss_index.bin"
        self.metadata_path = "data/metadata.pkl"
        self.embed_model_path = "./models/embed"
        
        self.stopwords = {
            "avec", "pour", "dans", "sur", "sous", "les", "des", "une", "mon", "ton", "son",
            "recette", "plat", "cuisine", "faire", "comment", "cuisiner", "veux", "voudrais",
            "cherche", "trouve", "donne", "moi", "sil", "plait", "est", "sont", "cette", "je"
        }

        # Dictionnaire de synonymes (TOUT EN MINUSCULE ET SANS ACCENTS ICI)
        self.synonyms = {
            # Difficulté
            "debutant": "facile",
            "simple": "facile",
            "rapide": "facile",
            "immanquable": "facile",
            "complexe": "difficile",
            "expert": "difficile",
            "chef": "difficile",
            
            # Prix
            "economique": "marche", # "marché" devient "marche" sans accent
            "eco": "marche",
            "etudiant": "marche",
            "pas cher": "marche",
            "luxe": "cher",
            "couteux": "cher",
            
            # Temps
            "express": "10m",
            "vite": "15m",
            "long": "1h"
        }
        
        self._load_resources()

    def _load_resources(self):
        print("📥 Initialisation du Retriever Hybride...")
        if not os.path.exists(self.index_path):
            raise FileNotFoundError("Index non trouvé.")
        self.index = faiss.read_index(self.index_path)
        with open(self.metadata_path, 'rb') as f:
            self.recipes = pickle.load(f)
        print(f"🧠 Chargement du modèle depuis {self.embed_model_path}...")
        self.model = SentenceTransformer(self.embed_model_path)

    # --- NOUVELLE FONCTION : NETTOYAGE DES ACCENTS ---
    def remove_accents(self, input_str):
        if not isinstance(input_str, str):
            return str(input_str)
        # Décompose les caractères (ex: 'é' devient 'e' + 'accent')
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        # Garde seulement les caractères de base (non-combining)
        return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

    def search(self, query, k=10):
        # 1. Vectorisation (L'IA gère déjà les accents, donc on lui donne la requête brute)
        query_vector = self.model.encode([query])
        faiss.normalize_L2(query_vector)

        # 2. Recherche large
        search_k = min(k * 10, self.index.ntotal) 
        distances, indices = self.index.search(query_vector, search_k)

        # 3. Analyse de la requête (NETTOYAGE ACCENTS ICI)
        # On nettoie la requête utilisateur : "Étudiant" -> "etudiant"
        clean_query = self.remove_accents(query.lower())
        raw_words = clean_query.replace("'", " ").replace(",", " ").split()
        
        wanted_keywords = set()
        banned_keywords = []
        
        if "sans" in raw_words:
            split_index = raw_words.index("sans")
            positive_part = raw_words[:split_index]
            negative_part = raw_words[split_index+1:]
        else:
            positive_part = raw_words
            negative_part = []

        # Traitement des mots voulus + SYNONYMES
        for word in positive_part:
            if len(word) > 2 and word not in self.stopwords:
                wanted_keywords.add(word)
                if word in self.synonyms:
                    wanted_keywords.add(self.synonyms[word])

        # Traitement des mots bannis
        for word in negative_part:
            if len(word) > 2 and word not in self.stopwords:
                banned_keywords.append(word)

        print(f"   🔎 Mots-clés (Sans accents) : {list(wanted_keywords)}")

        scored_candidates = []

        for i, idx in enumerate(indices[0]):
            if idx < 0 or idx >= len(self.recipes):
                continue
            
            recipe = self.recipes[idx]
            original_score = distances[0][i]
            
            # --- NETTOYAGE DES ACCENTS DANS LA RECETTE ---
            # On récupère le texte, on le met en minuscule, ET on vire les accents
            # Ex: "Pâte à crêpes" -> "pate a crepes"
            raw_text = (
                recipe['titre'] + " " + 
                " ".join(recipe['ingredients']) + " " +
                str(recipe.get('difficulte', '')) + " " + 
                str(recipe.get('prix', '')) + " " + 
                str(recipe.get('temps', ''))
            ).lower()
            
            clean_text = self.remove_accents(raw_text)

            for char in [",", ".", ":", "(", ")", "'", "-"]:
                clean_text = clean_text.replace(char, " ")
            
            recipe_words = set(clean_text.split())
            
            # --- FILTRE D'EXCLUSION ---
            is_banned = False
            for bad_word in banned_keywords:
                variations = {bad_word, bad_word + "s"}
                if bad_word.endswith("s"): variations.add(bad_word[:-1])
                
                if not recipe_words.isdisjoint(variations):
                    is_banned = True
                    break
            
            if is_banned:
                final_score = -10.0
            else:
                # --- BOOSTING ---
                boost = 0.0
                matches = 0
                for word in wanted_keywords:
                    variations = {word, word + "s"}
                    if word.endswith("s"): variations.add(word[:-1])
                        
                    if not recipe_words.isdisjoint(variations):
                        matches += 1
                        boost += 0.15
                
                if len(wanted_keywords) > 0 and matches >= (len(wanted_keywords) / 1.5):
                    boost += 0.25

                final_score = original_score + boost

            scored_candidates.append((final_score, recipe))

        scored_candidates.sort(key=lambda x: x[0], reverse=True)
        final_results = [item[1] for item in scored_candidates if item[0] > -5.0][:k]
        
        print(f"   🏆 Top 3 : {[r['titre'] for r in final_results[:3]]}")
        return final_results