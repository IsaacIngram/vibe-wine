import argparse
import textwrap
import re
from collections import defaultdict

# Wine characteristics database
WINE_CHARACTERISTICS = {
    "Cabernet Sauvignon": {
        "body": "full",
        "tannins": "high",
        "acidity": "medium-high",
        "flavors": ["black currant", "black cherry", "cedar", "graphite"],
        "pairings": ["rich meats", "steak", "lamb", "strong cheeses"],
        "characteristics": ["robust", "structured", "powerful"]
    },
    "Merlot": {
        "body": "medium-full",
        "tannins": "medium",
        "acidity": "medium",
        "flavors": ["plum", "black cherry", "chocolate", "herbs"],
        "pairings": ["pizza", "pasta", "grilled meats", "burgers"],
        "characteristics": ["smooth", "approachable", "fruit-forward"]
    },
    "Pinot Noir": {
        "body": "light-medium",
        "tannins": "low-medium",
        "acidity": "medium-high",
        "flavors": ["red cherry", "strawberry", "mushroom", "forest floor"],
        "pairings": ["salmon", "roasted chicken", "duck", "mushroom dishes"],
        "characteristics": ["elegant", "silky", "subtle"]
    },
    "Syrah/Shiraz": {
        "body": "full",
        "tannins": "medium-high",
        "acidity": "medium",
        "flavors": ["blackberry", "black pepper", "smoke", "licorice"],
        "pairings": ["barbecue", "grilled meats", "spicy dishes", "stews"],
        "characteristics": ["bold", "peppery", "dark"]
    },
    "Zinfandel": {
        "body": "medium-full",
        "tannins": "medium",
        "acidity": "medium-high",
        "flavors": ["raspberry", "blackberry", "pepper", "spice"],
        "pairings": ["pizza", "pasta", "barbecue", "burgers", "spicy foods"],
        "characteristics": ["jammy", "spicy", "bold"]
    },
    "Malbec": {
        "body": "medium-full",
        "tannins": "medium",
        "acidity": "medium",
        "flavors": ["blackberry", "plum", "chocolate", "tobacco"],
        "pairings": ["steak", "barbecue", "spicy foods", "mexican cuisine"],
        "characteristics": ["plush", "velvety", "fruit-forward"]
    },
    "Chardonnay": {
        "body": "medium-full",
        "tannins": "none",
        "acidity": "medium",
        "flavors": ["apple", "pear", "vanilla", "butter"],
        "pairings": ["creamy pasta", "lobster", "roasted chicken", "creamy sauces"],
        "characteristics": ["rich", "creamy", "versatile"]
    },
    "Sauvignon Blanc": {
        "body": "light-medium",
        "tannins": "none",
        "acidity": "high",
        "flavors": ["grapefruit", "green apple", "grass", "herbs"],
        "pairings": ["salads", "fish", "goat cheese", "vegetable dishes"],
        "characteristics": ["crisp", "herbaceous", "zesty"]
    },
    "Riesling": {
        "body": "light-medium",
        "tannins": "none",
        "acidity": "high",
        "flavors": ["peach", "apricot", "honey", "petrol"],
        "pairings": ["spicy foods", "asian cuisine", "pork", "sushi"],
        "characteristics": ["aromatic", "fruity", "varying sweetness"]
    },
    "Pinot Grigio": {
        "body": "light",
        "tannins": "none",
        "acidity": "medium-high",
        "flavors": ["pear", "apple", "lemon", "almond"],
        "pairings": ["light seafood", "salads", "light pasta", "appetizers"],
        "characteristics": ["crisp", "light", "refreshing"]
    },
    "Sangiovese": {
        "body": "medium",
        "tannins": "medium-high",
        "acidity": "high",
        "flavors": ["cherry", "plum", "herbs", "tea"],
        "pairings": ["tomato-based pasta", "pizza", "italian cuisine", "cured meats"],
        "characteristics": ["savory", "earthy", "rustic"]
    },
    "Nebbiolo": {
        "body": "medium-full",
        "tannins": "high",
        "acidity": "high",
        "flavors": ["cherry", "rose", "tar", "licorice"],
        "pairings": ["rich pasta", "truffle dishes", "aged cheeses", "risotto"],
        "characteristics": ["complex", "powerful", "elegant"]
    },
    "Barbera": {
        "body": "medium",
        "tannins": "low",
        "acidity": "high",
        "flavors": ["cherry", "strawberry", "plum", "herbs"],
        "pairings": ["tomato-based pasta", "pizza", "eggplant", "italian cuisine"],
        "characteristics": ["juicy", "vibrant", "food-friendly"]
    },
    "Gewürztraminer": {
        "body": "medium",
        "tannins": "none",
        "acidity": "low-medium",
        "flavors": ["lychee", "rose", "ginger", "spice"],
        "pairings": ["spicy asian cuisine", "thai food", "indian cuisine", "aromatic dishes"],
        "characteristics": ["aromatic", "floral", "spicy"]
    },
    "Dessert Wine": {
        "body": "full",
        "tannins": "varies",
        "acidity": "high",
        "flavors": ["honey", "caramel", "dried fruit", "nuts"],
        "pairings": ["desserts", "cheese", "fruit", "chocolate", "nuts"],
        "characteristics": ["sweet", "complex", "concentrated"]
    },
    "Sparkling Wine": {
        "body": "light",
        "tannins": "none",
        "acidity": "high",
        "flavors": ["apple", "citrus", "toast", "brioche"],
        "pairings": ["appetizers", "seafood", "fried foods", "celebrations"],
        "characteristics": ["effervescent", "crisp", "celebratory"]
    },
    "Rosé": {
        "body": "light-medium",
        "tannins": "low",
        "acidity": "medium-high",
        "flavors": ["strawberry", "watermelon", "citrus", "flowers"],
        "pairings": ["salads", "light pastas", "grilled fish", "vegetable dishes"],
        "characteristics": ["refreshing", "versatile", "fruity"]
    }
}

# Food keywords and related terms - expanded with more terms and associations
FOOD_KEYWORDS = {
    # Pasta types and dishes
    "pasta": ["pasta", "spaghetti", "fettuccine", "linguine", "penne", "rigatoni", "farfalle",
              "lasagna", "ravioli", "tortellini", "macaroni", "tagliatelle", "orzo", "noodle"],
    "pizza": ["pizza", "flatbread", "calzone", "stromboli"],

    # Pasta sauces and preparations
    "tomato": ["tomato", "marinara", "pomodoro", "arrabbiata", "red sauce", "bolognese", "amatriciana"],
    "cream": ["cream", "alfredo", "carbonara", "bechamel", "white sauce", "beurre blanc", "creamy"],
    "vodka": ["vodka", "vodka sauce", "pink sauce", "rosé sauce"],
    "pesto": ["pesto", "basil sauce", "herb sauce", "green sauce"],
    "oil": ["oil", "olive oil", "aglio e olio", "garlic oil"],

    # Meats
    "beef": ["beef", "steak", "brisket", "short rib", "ground beef", "meatball", "meatloaf", "hamburger"],
    "pork": ["pork", "ham", "bacon", "prosciutto", "pancetta", "sausage", "salami", "chorizo", "loin"],
    "lamb": ["lamb", "mutton", "rack of lamb", "lamb chop", "leg of lamb"],
    "chicken": ["chicken", "poultry", "turkey", "duck", "cornish hen", "quail", "fowl", "bird"],

    # Seafood
    "fish": ["fish", "salmon", "tuna", "cod", "trout", "halibut", "tilapia", "sea bass", "swordfish"],
    "shellfish": ["shellfish", "shrimp", "lobster", "crab", "scallop", "clam", "mussel", "oyster"],

    # Cooking methods
    "grilled": ["grill", "grilled", "barbecue", "bbq", "charred", "charcoal", "smoky", "flame-cooked"],
    "roasted": ["roast", "roasted", "baked", "oven", "broiled"],
    "fried": ["fried", "deep-fried", "pan-fried", "crispy", "tempura"],
    "braised": ["braise", "braised", "slow-cooked", "stewed"],

    # Flavors and seasonings
    "spicy": ["spicy", "hot", "chili", "pepper", "cajun", "sriracha", "jalapeno", "paprika", "curry"],
    "herbs": ["herb", "basil", "oregano", "thyme", "rosemary", "parsley", "mint", "cilantro", "dill"],
    "garlic": ["garlic", "shallot", "onion", "leek"],
    "cheese": ["cheese", "parmesan", "mozzarella", "cheddar", "gouda", "ricotta", "goat cheese", "blue cheese"],

    # Cuisines
    "italian": ["italian", "italy", "mediterranean", "tuscan", "sicilian", "roman"],
    "french": ["french", "france", "provencal", "bistro"],
    "asian": ["asian", "chinese", "japanese", "thai", "vietnamese", "korean", "soy sauce", "ginger", "teriyaki"],
    "mexican": ["mexican", "taco", "burrito", "enchilada", "salsa", "guacamole", "tortilla", "quesadilla"],
    "indian": ["indian", "curry", "tandoori", "masala", "korma", "tikka", "naan"],
    "mediterranean": ["mediterranean", "greek", "middle eastern", "lebanese", "moroccan"],

    # Vegetables
    "mushroom": ["mushroom", "fungi", "portobello", "shiitake", "truffle", "porcini", "cremini"],
    "vegetable": ["vegetable", "vegetarian", "vegan", "plant-based", "meatless", "greens"],

    # Sweet things
    "dessert": ["dessert", "cake", "pie", "pastry", "tart", "sweet", "chocolate", "custard", "pudding"],
    "fruit": ["fruit", "berry", "apple", "pear", "peach", "cherry", "strawberry", "raspberry", "blueberry",
              "blackberry", "citrus", "lemon", "orange", "grapefruit", "tropical", "mango", "pineapple"],
    "chocolate": ["chocolate", "cocoa", "fudge", "ganache", "brownie", "truffle"],
    "caramel": ["caramel", "toffee", "butterscotch", "dulce de leche"],
    "nuts": ["nut", "almond", "walnut", "pecan", "hazelnut", "pistachio", "peanut"],

    # Misc food types
    "appetizer": ["appetizer", "starter", "hors d'oeuvre", "tapas", "small plate", "finger food"],
    "salad": ["salad", "greens", "vinaigrette", "slaw", "cold dish"],
    "soup": ["soup", "stew", "broth", "bisque", "chowder", "gumbo"],
    "sandwich": ["sandwich", "burger", "sub", "wrap", "panini", "toast"],
    "breakfast": ["breakfast", "brunch", "eggs", "pancake", "waffle", "bacon", "sausage", "omelette"]
}

# Wine pairing rules - expanded with more combinations
WINE_PAIRING_RULES = {
    # Pasta combinations
    "pasta + tomato": ["Sangiovese", "Barbera", "Pinot Noir", "Zinfandel", "Merlot"],
    "pasta + cream": ["Chardonnay", "Pinot Grigio", "Pinot Noir", "Merlot"],
    "pasta + vodka": ["Barbera", "Sangiovese", "Pinot Noir", "Sauvignon Blanc", "Zinfandel"],
    "pasta + pesto": ["Sauvignon Blanc", "Pinot Grigio", "Vermentino"],
    "pasta + oil": ["Pinot Grigio", "Sauvignon Blanc", "Chardonnay"],
    "pasta + mushroom": ["Pinot Noir", "Nebbiolo", "Chardonnay"],

    # Pizza
    "pizza": ["Sangiovese", "Barbera", "Zinfandel", "Merlot"],
    "pizza + spicy": ["Zinfandel", "Syrah/Shiraz", "Malbec"],

    # Meat dishes
    "beef": ["Cabernet Sauvignon", "Malbec", "Syrah/Shiraz", "Zinfandel"],
    "pork": ["Pinot Noir", "Merlot", "Zinfandel", "Riesling"],
    "lamb": ["Cabernet Sauvignon", "Syrah/Shiraz", "Malbec", "Nebbiolo"],
    "chicken": ["Chardonnay", "Pinot Noir", "Sauvignon Blanc", "Merlot"],

    # Seafood
    "fish": ["Pinot Grigio", "Sauvignon Blanc", "Chardonnay", "Pinot Noir"],
    "shellfish": ["Pinot Grigio", "Sauvignon Blanc", "Chardonnay", "Riesling"],

    # Cooking methods
    "grilled": ["Zinfandel", "Syrah/Shiraz", "Malbec", "Cabernet Sauvignon"],
    "roasted": ["Pinot Noir", "Merlot", "Chardonnay", "Cabernet Sauvignon"],
    "fried": ["Chardonnay", "Pinot Grigio", "Sauvignon Blanc", "Sparkling Wine"],
    "braised": ["Cabernet Sauvignon", "Syrah/Shiraz", "Nebbiolo", "Malbec"],

    # Flavors and ingredients
    "spicy": ["Riesling", "Gewürztraminer", "Zinfandel", "Syrah/Shiraz"],
    "garlic": ["Sauvignon Blanc", "Pinot Grigio", "Chardonnay"],
    "cheese": ["Cabernet Sauvignon", "Chardonnay", "Merlot", "Pinot Noir"],
    "mushroom": ["Pinot Noir", "Nebbiolo", "Chardonnay", "Merlot"],

    # Cuisines
    "italian": ["Sangiovese", "Barbera", "Nebbiolo", "Pinot Grigio"],
    "french": ["Pinot Noir", "Chardonnay", "Cabernet Sauvignon", "Sauvignon Blanc"],
    "asian": ["Riesling", "Gewürztraminer", "Sauvignon Blanc", "Pinot Noir"],
    "mexican": ["Malbec", "Zinfandel", "Sauvignon Blanc", "Riesling"],
    "indian": ["Riesling", "Gewürztraminer", "Syrah/Shiraz", "Pinot Noir"],
    "mediterranean": ["Sangiovese", "Pinot Grigio", "Syrah/Shiraz"],

    # Sweet and dessert pairings
    "dessert": ["Dessert Wine", "Riesling", "Gewürztraminer"],
    "fruit": ["Riesling", "Gewürztraminer", "Dessert Wine", "Sparkling Wine", "Rosé"],
    "chocolate": ["Dessert Wine", "Syrah/Shiraz", "Zinfandel", "Cabernet Sauvignon"],
    "caramel": ["Dessert Wine", "Chardonnay"],
    "nuts": ["Dessert Wine", "Chardonnay", "Merlot"],

    # Misc food types
    "appetizer": ["Sparkling Wine", "Sauvignon Blanc", "Pinot Grigio", "Rosé"],
    "salad": ["Sauvignon Blanc", "Pinot Grigio", "Rosé"],
    "soup": ["Chardonnay", "Sauvignon Blanc", "Pinot Noir"],
    "sandwich": ["Zinfandel", "Merlot", "Chardonnay"],
    "breakfast": ["Sparkling Wine", "Riesling", "Sauvignon Blanc"]
}

# Default wine pairings for when no specific match is found
DEFAULT_WINES = {
    "red": ["Merlot", "Pinot Noir", "Cabernet Sauvignon"],
    "white": ["Chardonnay", "Sauvignon Blanc", "Pinot Grigio"],
    "versatile": ["Pinot Noir", "Chardonnay", "Rosé", "Riesling"]
}


def analyze_food_input(food_text):
    """
    Analyze food input using keyword matching to identify ingredients, preparations, and cuisines
    Returns a dictionary of identified food categories and their confidence scores
    """
    food_text = food_text.lower()
    words = re.findall(r'\b\w+\b', food_text)

    # Initialize result with categories and scores
    result = defaultdict(float)

    # Check for exact matches first
    for category, keywords in FOOD_KEYWORDS.items():
        for keyword in keywords:
            if keyword in food_text:
                result[category] += 1.0
            elif keyword in words:
                result[category] += 0.9

    # Check for partial matches
    for word in words:
        if len(word) > 3:  # Only consider words longer than 3 characters for partial matching
            for category, keywords in FOOD_KEYWORDS.items():
                for keyword in keywords:
                    # Check if the word is a substring of the keyword or vice versa
                    if word in keyword or keyword in word:
                        result[category] += 0.5

    return result


def determine_wine_pairings(food_categories, food_text):
    """
    Determine wine pairings based on food categories
    Returns a list of tuples (wine_name, score, explanation)
    """
    scores = defaultdict(float)
    explanations = defaultdict(list)

    # Get categories sorted by confidence score
    sorted_categories = sorted(food_categories.items(), key=lambda x: x[1], reverse=True)

    # Check for specific combinations first
    for rule, wines in WINE_PAIRING_RULES.items():
        if "+" in rule:
            rule_categories = [part.strip() for part in rule.split("+")]

            # Check if all parts of the rule are in the food categories
            matches = [cat for cat in rule_categories if cat in food_categories]
            if len(matches) == len(rule_categories):
                match_score = sum(food_categories[cat] for cat in matches)
                for wine in wines:
                    scores[wine] += match_score
                    explanations[wine].append(f"Perfect for {rule} combinations")

    # Process individual categories
    for category, score in sorted_categories:
        rule_key = category  # Exact match first
        if rule_key in WINE_PAIRING_RULES:
            for wine in WINE_PAIRING_RULES[rule_key]:
                scores[wine] += score
                explanations[wine].append(f"Pairs well with {category}")

    # If no matches were found, provide default recommendations
    if not scores:
        # Check if the food contains any sweet/dessert-related words
        sweet_terms = ["sweet", "dessert", "cake", "pie", "jam", "jelly", "candy", "sugar", "honey",
                       "chocolate", "ice cream", "pudding", "fruit", "berry", "syrup", "caramel"]

        is_sweet = any(term in food_text.lower() for term in sweet_terms)

        if is_sweet:
            # For sweet items, recommend dessert wines
            for wine in ["Dessert Wine", "Riesling", "Gewürztraminer"]:
                scores[wine] += 1.0
                explanations[wine].append(f"A good match for sweet foods like {food_text}")
        else:
            # For unknown/neutral items, recommend versatile wines
            for wine in DEFAULT_WINES["versatile"]:
                scores[wine] += 1.0
                explanations[wine].append(f"A versatile wine that pairs with many foods including {food_text}")

            # Add one red and one white for diversity
            if "Pinot Noir" not in DEFAULT_WINES["versatile"]:
                scores["Pinot Noir"] += 0.8
                explanations["Pinot Noir"].append(f"A versatile red that pairs with many foods")

            if "Chardonnay" not in DEFAULT_WINES["versatile"]:
                scores["Chardonnay"] += 0.8
                explanations["Chardonnay"].append(f"A versatile white that pairs with many foods")

    # Add general characteristics
    for wine, score in scores.items():
        if wine in WINE_CHARACTERISTICS:
            char = WINE_CHARACTERISTICS[wine]
            body = char["body"]
            flavors = ", ".join(char["flavors"][:2])
            characteristics = ", ".join(char["characteristics"])
            explanations[wine].append(f"A {body}-bodied {characteristics} wine with {flavors} notes")

    # Sort and return top matches with explanations
    result = []
    for wine, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        if score > 0:
            # Get the top 2 most relevant explanations
            top_explanations = sorted(explanations[wine], key=len)[:2]
            explanation = " ".join(top_explanations)
            result.append((wine, score, explanation))

    return result[:5]  # Return top 5 matches


def print_wine_recommendations(food_text, wine_pairings):
    """Print wine recommendations in a formatted way"""
    print(f"\n=== Wine Recommendations for {food_text} ===\n")

    for i, (wine, score, explanation) in enumerate(wine_pairings, 1):
        # Calculate confidence level (1-5 stars based on score)
        confidence = int(min(5, max(1, score)))
        stars = "★" * confidence

        print(f"{i}. {wine} {stars}")

        # Get wine characteristics
        if wine in WINE_CHARACTERISTICS:
            char = WINE_CHARACTERISTICS[wine]
            body = char["body"]
            characteristics = ", ".join(char["characteristics"])
            print(f"   {body}-bodied, {characteristics}")

        # Print explanation
        wrapped_text = textwrap.fill(explanation, width=70, initial_indent="   ", subsequent_indent="   ")
        print(f"{wrapped_text}\n")


def interactive_mode():
    """Run the CLI in interactive mode."""
    print("=== Wine and Food Pairing Assistant ===")
    print("Enter a food dish to get wine pairing recommendations.")
    print("Type 'exit', 'quit', or Ctrl+C to exit.\n")

    while True:
        try:
            food_text = input("What food would you like wine recommendations for? ").strip()
            if food_text.lower() in ('exit', 'quit'):
                break

            if not food_text:
                continue

            food_categories = analyze_food_input(food_text)
            wine_pairings = determine_wine_pairings(food_categories, food_text)
            print_wine_recommendations(food_text, wine_pairings)
            print("-" * 70)

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            continue


def main():
    parser = argparse.ArgumentParser(description="Wine and Food Pairing CLI")
    parser.add_argument("food", nargs="?", help="Food dish to get wine pairing recommendations for")
    parser.add_argument("-a", "--analyze", action="store_true", help="Show detailed analysis of the food input")

    args = parser.parse_args()

    if args.food:
        food_categories = analyze_food_input(args.food)

        if args.analyze:
            print("\n=== Food Analysis ===")
            print(f"Input: {args.food}")
            print("\nCategories detected:")
            for category, score in sorted(food_categories.items(), key=lambda x: x[1], reverse=True):
                if score > 0:
                    print(f"- {category}: {score:.1f}")
            print("")

        wine_pairings = determine_wine_pairings(food_categories, args.food)
        print_wine_recommendations(args.food, wine_pairings)
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
