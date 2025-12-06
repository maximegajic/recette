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
                torch_dtype=torch.bfloat16 if self.device == "cuda" else torch.float32, 
                device_map="auto" if self.device == "cuda" else None
            )
            
        except OSError:
            print("⚠️ Modèle local non trouvé. Lancez download_model.py.")
            raise

    def generate_response(self, user_query, retrieved_recipes):
        # 1. Construire le contexte
        context_text = ""
        for i, r in enumerate(retrieved_recipes):
            ingredients = ", ".join(r['ingredients'])
            context_text += (
                f"RECETTE #{i+1}:\n"
                f"  - Titre: {r['titre']}\n"
                f"  - Ingrédients: {ingredients}\n"
                f"  - Instructions: {r['instructions']}\n"
                f"  - Infos: Difficulté {r.get('difficulte', '?')} | Prix {r.get('prix', '?')}\n\n"
            )

        # 2. Prompt "Chef Malin"
        # On insiste sur le fait qu'une recette contient les ingrédients PARMI D'AUTRES.
        system_prompt = (
            "Tu es un assistant culinaire utile et direct. "
            "Tu as une liste de recettes numérotées. "
            
            "RÈGLES D'ANALYSE :"
            "1. Si l'utilisateur donne des INGRÉDIENTS : "
            "   - Cherche dans la liste les recettes qui CONTIENNENT ces ingrédients (même s'il y en a d'autres !). "
            "   - Ensuite, donne la recette complète qui correspond le mieux."
            
            "2. Si l'utilisateur demande un PLAT (ex: 'Pizza') : "
            "   - Donne la recette complète."
            
            "3. Sois concis et ne t'excuse pas inutilement."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"RECETTES DISPONIBLES :\n{context_text}\n\nDEMANDE UTILISATEUR : {user_query}"}
        ]

        text = self.tokenizer.apply_chat_template(
            messages, 
            tokenize=False, 
            add_generation_prompt=True
        )

        inputs = self.tokenizer([text], return_tensors="pt").to(self.device)

        outputs = self.model.generate(
            **inputs, 
            max_new_tokens=400,
            temperature=0.5,           # Un tout petit peu plus créatif pour faire des liens
            do_sample=True,
            top_p=0.9,
            repetition_penalty=1.1,
            pad_token_id=self.tokenizer.eos_token_id
        )

        generated_ids = outputs[0][len(inputs.input_ids[0]):]
        clean_response = self.tokenizer.decode(generated_ids, skip_special_tokens=True)

        return clean_response.strip()