import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class RAGGenerator:
    def __init__(self):
        self.model_path = "./models/llm"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🖥️  Chargement du LLM sur : {self.device}")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path, 
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None
            )
            if self.device == "cpu":
                self.model.to("cpu")
                
        except OSError:
            print("⚠️ Modèle local non trouvé. Lancez download_model.py ou vérifiez le chemin.")
            raise

    def generate_response(self, user_query, retrieved_recipes):
        # 1. Construire le contexte à partir des recettes trouvées
        context_text = ""
        for r in retrieved_recipes:
            ingredients = ", ".join(r['ingredients'])
            context_text += f"- Recette: {r['titre']}\n  Ingrédients: {ingredients}\n  Instructions: {r['instructions']}\n\n"

        # 2. Créer le prompt (Format ChatML ou spécifique à TinyLlama/Phi)
        # Ceci est un prompt générique efficace
        prompt = f"""<|system|>
Tu es un assistant culinaire utile. Utilise les recettes ci-dessous pour répondre à la demande de l'utilisateur. 
Si aucune recette ne correspond, dis-le poliment. Parle en français.

CONTEXTE RECETTES:
{context_text}
</s>
<|user|>
{user_query}
</s>
<|assistant|>"""

        # 3. Tokenizer et Générer
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        outputs = self.model.generate(
            **inputs, 
            max_new_tokens=250, # Limite la longueur de la réponse
            temperature=0.7,    # Créativité
            do_sample=True
        )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Nettoyage pour ne garder que la réponse de l'assistant (après <|assistant|>)
        if "<|assistant|>" in response:
            return response.split("<|assistant|>")[-1].strip()
        return response