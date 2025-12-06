import json
import random
import os

# Configuration
OUTPUT_FILE = "data/recettes.json"
NUM_RECIPES = 200

# 1. LES VRAIES RECETTES (Base solide de classiques)
real_recipes = [
    {
        "titre": "Pâtes Carbonara (La vraie)",
        "ingredients": ["spaghetti", "oeufs", "pecorino", "guanciale", "poivre noir"],
        "instructions": "Cuire les pâtes al dente. Faire revenir le guanciale. Mélanger oeufs et fromage. Mélanger le tout hors du feu.",
        "temps": "20m", "difficulte": "Moyen", "prix": "Moyen", "calories": "Élevé"
    },
    {
        "titre": "Soupe de carottes au cumin",
        "ingredients": ["carottes", "oignon", "pommes de terre", "cumin", "crème"],
        "instructions": "Cuire les légumes dans l'eau bouillante. Mixer avec la crème et le cumin.",
        "temps": "35m", "difficulte": "Facile", "prix": "Bon marché", "calories": "Faible"
    },
    {
        "titre": "Boeuf Bourguignon",
        "ingredients": ["boeuf", "vin rouge", "carottes", "oignons", "champignons", "lardons"],
        "instructions": "Faire mariner le boeuf. Saisir la viande. Mijoter 3h avec le vin et les légumes.",
        "temps": "3h", "difficulte": "Difficile", "prix": "Cher", "calories": "Élevé"
    },
    {
        "titre": "Salade César",
        "ingredients": ["laitue", "poulet", "parmesan", "croutons", "sauce césar", "anchois"],
        "instructions": "Griller le poulet. Laver la salade. Assembler avec la sauce et les copeaux de parmesan.",
        "temps": "20m", "difficulte": "Facile", "prix": "Moyen", "calories": "Moyen"
    },
    {
        "titre": "Curry de Légumes Vegan",
        "ingredients": ["chou-fleur", "pois chiches", "lait de coco", "curry", "riz"],
        "instructions": "Faire revenir les épices. Ajouter légumes et lait de coco. Servir avec du riz.",
        "temps": "30m", "difficulte": "Facile", "prix": "Bon marché", "calories": "Moyen"
    },
    {
        "titre": "Omelette aux fines herbes",
        "ingredients": ["oeufs", "beurre", "ciboulette", "persil", "sel", "poivre"],
        "instructions": "Battre les oeufs avec les herbes. Cuire dans une poêle beurrée.",
        "temps": "10m", "difficulte": "Facile", "prix": "Bon marché", "calories": "Moyen"
    },
    {
        "titre": "Pizza Margherita Maison",
        "ingredients": ["pâte à pizza", "sauce tomate", "mozzarella", "basilic", "huile d'olive"],
        "instructions": "Etaler la pâte. Garnir. Cuire au four très chaud (250°C) pendant 10-12 min.",
        "temps": "25m", "difficulte": "Moyen", "prix": "Bon marché", "calories": "Élevé"
    },
    {
        "titre": "Poulet Rôti du Dimanche",
        "ingredients": ["poulet entier", "beurre", "ail", "thym", "pommes de terre"],
        "instructions": "Beurrer le poulet. Enfourner 1h30 à 200°C avec les pommes de terre autour.",
        "temps": "1h30", "difficulte": "Moyen", "prix": "Moyen", "calories": "Moyen"
    },
    {
        "titre": "Chili con Carne",
        "ingredients": ["boeuf haché", "haricots rouges", "tomates", "oignon", "piment", "riz"],
        "instructions": "Mijoter la viande avec les épices et les tomates. Ajouter les haricots à la fin.",
        "temps": "45m", "difficulte": "Facile", "prix": "Bon marché", "calories": "Élevé"
    },
    {
        "titre": "Quiche Lorraine",
        "ingredients": ["pâte brisée", "oeufs", "crème fraîche", "lardons", "muscade"],
        "instructions": "Etaler la pâte. Mélanger oeufs et crème. Verser sur les lardons. Cuire 30 min.",
        "temps": "45m", "difficulte": "Facile", "prix": "Bon marché", "calories": "Élevé"
    },
    {
        "titre": "Risotto aux Champignons",
        "ingredients": ["riz arborio", "champignons", "vin blanc", "bouillon", "parmesan"],
        "instructions": "Nacrer le riz. Ajouter le bouillon louche par louche en remuant constamment.",
        "temps": "40m", "difficulte": "Difficile", "prix": "Moyen", "calories": "Moyen"
    },
    {
        "titre": "Tartiflette",
        "ingredients": ["pommes de terre", "reblochon", "lardons", "oignons", "crème"],
        "instructions": "Cuire les patates. Faire revenir lardons/oignons. Mettre en plat, couvrir de reblochon. Gratin.",
        "temps": "1h", "difficulte": "Facile", "prix": "Moyen", "calories": "Extrême"
    },
    {
        "titre": "Wok de Nouilles Sautées",
        "ingredients": ["nouilles chinoises", "sauce soja", "carottes", "poivrons", "poulet"],
        "instructions": "Sauter les légumes et la viande à feu vif. Ajouter les nouilles cuites et la sauce.",
        "temps": "15m", "difficulte": "Facile", "prix": "Bon marché", "calories": "Faible"
    },
    {
        "titre": "Ratatouille Provençale",
        "ingredients": ["courgettes", "aubergines", "poivrons", "tomates", "oignons", "ail"],
        "instructions": "Cuire chaque légume séparément puis mijoter tous ensemble 30 min.",
        "temps": "1h", "difficulte": "Moyen", "prix": "Bon marché", "calories": "Faible"
    },
    {
        "titre": "Croque-Monsieur",
        "ingredients": ["pain de mie", "jambon", "comté", "beurre", "béchamel"],
        "instructions": "Beurrer le pain. Assembler jambon/fromage. Gratiner au four.",
        "temps": "15m", "difficulte": "Facile", "prix": "Bon marché", "calories": "Élevé"
    },
    {
        "titre": "Saumon en Papillote",
        "ingredients": ["pavé de saumon", "citron", "aneth", "courgettes", "huile d'olive"],
        "instructions": "Mettre le tout dans du papier cuisson. Fermer hermétiquement. Cuire 20 min au four.",
        "temps": "25m", "difficulte": "Facile", "prix": "Cher", "calories": "Faible"
    },
    {
        "titre": "Crêpes au Sucre",
        "ingredients": ["farine", "lait", "oeufs", "beurre", "sucre", "rhum"],
        "instructions": "Mélanger les ingrédients. Laisser reposer 1h. Cuire à la poêle chaude.",
        "temps": "1h30", "difficulte": "Moyen", "prix": "Bon marché", "calories": "Moyen"
    },
    {
        "titre": "Tiramisu",
        "ingredients": ["mascarpone", "oeufs", "sucre", "café", "boudoirs", "cacao"],
        "instructions": "Monter les blancs. Mélanger jaunes/sucre/mascarpone. Tremper biscuits. Alterner les couches.",
        "temps": "20m", "difficulte": "Moyen", "prix": "Moyen", "calories": "Élevé"
    },
    {
        "titre": "Dahl de Lentilles",
        "ingredients": ["lentilles corail", "lait de coco", "tomates concassées", "curcuma", "gingembre"],
        "instructions": "Cuire les lentilles avec les épices et la tomate. Finir avec le coco.",
        "temps": "25m", "difficulte": "Facile", "prix": "Bon marché", "calories": "Moyen"
    },
    {
        "titre": "Avocado Toast",
        "ingredients": ["pain complet", "avocat", "oeuf poché", "piment", "citron"],
        "instructions": "Toaster le pain. Ecraser l'avocat avec citron. Poser l'oeuf dessus.",
        "temps": "10m", "difficulte": "Facile", "prix": "Moyen", "calories": "Moyen"
    }
]

# 2. LISTES POUR LA GÉNÉRATION PROCÉDURALE
bases = ["Riz", "Pâtes", "Semoule", "Quinoa", "Pommes de terre", "Blé", "Gnocchis", "Polenta"]
proteines = ["Poulet", "Boeuf", "Porc", "Saumon", "Thon", "Tofu", "Lentilles", "Haricots Rouges", "Oeufs", "Crevettes"]
legumes = ["Carottes", "Courgettes", "Brocolis", "Poivrons", "Épinards", "Champignons", "Aubergines", "Chou-fleur", "Haricots verts", "Petits pois"]
sauces = ["Sauce Tomate", "Crème", "Lait de Coco", "Sauce Soja", "Pesto", "Huile d'olive", "Curry", "Moutarde", "Beurre Citron"]
adjectifs = ["Épicé", "Crémeux", "Rôti", "Sauté", "Mijoté", "Grillé", "Frais", "Express", "Gourmand", "Léger"]

difficultes = ["Facile", "Moyen", "Difficile"]
prix_liste = ["Bon marché", "Moyen", "Cher"]
calories_liste = ["Faible", "Moyen", "Élevé"]
temps_liste = ["15m", "20m", "30m", "45m", "1h"]

def generate_random_recipe(index):
    base = random.choice(bases)
    prot = random.choice(proteines)
    leg1 = random.choice(legumes)
    leg2 = random.choice(legumes)
    sauce = random.choice(sauces)
    adj = random.choice(adjectifs)
    
    # Éviter les doublons de légumes
    while leg2 == leg1:
        leg2 = random.choice(legumes)

    title = f"{base} au {prot} et {leg1} {adj}"
    
    # Ingrédients dynamiques
    ingredients = [base.lower(), prot.lower(), leg1.lower(), leg2.lower(), sauce.lower(), "oignon", "ail", "sel", "poivre"]
    
    # Instructions génériques mais logiques
    instructions = (
        f"1. Préparer les ingrédients : couper {leg1} et {leg2} en morceaux. "
        f"2. Faire cuire {base} selon les instructions du paquet. "
        f"3. Dans une poêle, faire revenir {prot} avec un peu d'huile. "
        f"4. Ajouter les légumes et faire sauter 5-10 minutes. "
        f"5. Verser {sauce} et laisser mijoter quelques instants. "
        f"6. Mélanger avec {base} et servir chaud."
    )

    return {
        "id": index,
        "titre": title,
        "ingredients": ingredients,
        "instructions": instructions,
        "temps": random.choice(temps_liste),
        "difficulte": random.choice(difficultes),
        "prix": random.choice(prix_liste),
        "calories": random.choice(calories_liste)
    }

def main():
    final_recipes = []
    
    # Ajouter les vraies recettes
    print(f"Ajout de {len(real_recipes)} recettes réelles...")
    for i, r in enumerate(real_recipes):
        r['id'] = i + 1
        final_recipes.append(r)
        
    # Compléter jusqu'à NUM_RECIPES
    current_id = len(real_recipes) + 1
    print(f"Génération de {NUM_RECIPES - len(real_recipes)} recettes procédurales...")
    
    while len(final_recipes) < NUM_RECIPES:
        new_recipe = generate_random_recipe(current_id)
        final_recipes.append(new_recipe)
        current_id += 1
        
    # Sauvegarde
    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_recipes, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Terminé ! Fichier généré : {OUTPUT_FILE} avec {len(final_recipes)} recettes.")

if __name__ == "__main__":
    main()