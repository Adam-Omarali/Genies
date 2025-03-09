import google.generativeai as genai
from PIL import Image
import os
import re   
import json
from dotenv import load_dotenv

# 4 .Gemini API Classification Function
def classify_book_damage(image_path):
    """
    Uses Gemini API to classify book damage and returns type and severity.
    """
    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=GEMINI_API_KEY)  # Configure Gemini AI
    if not GEMINI_API_KEY:
        print("Gemini API key not loaded.")
        return None

    try:
        model_name = "gemini-2.0-flash"  # Or correct model
        model = genai.GenerativeModel(model_name)

        try:
            image = Image.open(image_path)
        except FileNotFoundError:
            print(f"Error: Image not found: {image_path}")
            return None
        except Exception as e:
            print(f"Error reading image: {e}")
            return None

        damage_options = ["Corner Damage", "Cover Scratches", "Spine Damage", "Water Damage", "Tears or Rips", "Misprints", "Missing Dust Jacket", "Trim Issues"] # Under score labels
        # **HIGHLY REFINED PROMPT (Underscore Labels):**
        prompt = f"""Carefully analyze the image of the book.
        Identify the *single* most significant type of damage present.
        You *must* choose one of the following damage types (use *exactly* these labels): {', '.join(damage_options)}.

        After identifying the damage type, assess its severity on a scale of 1 to 5, where:
        1: Very Minor Damage
        2: Minor Damage
        3: Moderate Damage
        4: Significant Damage
        5: Severe Damage

        Return the result in *exactly* the following format. Do not include any other text:
        Damage Type: [damage_type]
        Severity: [severity_level]
        Author: [author]
        Book Name: [book_name]

        Example:
        Damage Type: Corner Damage
        Severity: 3
        Author: Marissa Meyer
        Book Name: Scarlet
        """

        response = model.generate_content([prompt, image])

        print("Gemini API response received.")
        print(f"Gemini API response: {response.text}")
        return response.text

    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return None
    
    
def extract_damage_info(gemini_response):
    """
    Extracts damage type and severity from the Gemini API response.
    """
    damage_match = re.search(r"Damage Type:\s*([A-Za-z\s]+)", gemini_response)  # Allow both upper and lowercase letters
    severity_match = re.search(r"Severity:\s*(\d+)", gemini_response)
    author_match = re.search(r"Author:\s*([a-zA-Z\s]+)", gemini_response)
    book_name_match = re.search(r"Book Name:\s*([a-zA-Z\s]+)", gemini_response)

    if damage_match and severity_match:
        damage_type = damage_match.group(1).split("\n")[0]  # Convert to lowercase and replace spaces with underscores
        severity = int(severity_match.group(1))
        author = author_match.group(1).strip().split("\n")[0] if author_match else None
        book_name = book_name_match.group(1).strip() if book_name_match else None

        print(f"Extracted Damage Type: {damage_type}")
        print(f"Extracted Severity: {severity}")
        print(f"Extracted Author: {author}")
        print(f"Extracted Book Name: {book_name}")
        return {"type": damage_type, "severity": severity, "author": author, "book_name": book_name}
    else:
        print("Could not extract damage type and severity.")
        return None
    
def calculate_discounted_price(original_price, damage_type, severity):
    """
    Calculates the discounted price based on damage type and severity.
    """
    if not original_price or not damage_type or not severity:
        print("Missing required parameters.")
        return None
    
    # Load publisher rules
    with open('publisher_rules.json', 'r') as f:
        rules = json.load(f)
    
    # Get the discount rate based on damage type and severity
    discount_rate = rules.get(damage_type, {}).get(str(severity), 0.0)
    
    # Calculate the discounted price
    discounted_price = original_price * (1 - discount_rate)
    
    print(f"Original Price: ${original_price:.2f}")
    return {"discounted_price": discounted_price, "discount_rate": discount_rate}

def process_book_return(image_path, original_price, publisher):
    """
    Processes a book return by classifying damage, calculating the discounted price,
    and returning the results.
    """ 
    gemini_response = classify_book_damage(image_path)
    if not gemini_response:
        print("Failed to classify book damage.")
        return None
    
    damage_info = extract_damage_info(gemini_response)
    if not damage_info:
        print("Failed to extract damage information.")
        return None
    
    discounted_price = calculate_discounted_price(original_price, damage_info["type"], damage_info["severity"])
    print(f"Discounted Price: ${discounted_price['discounted_price']:.2f}")
    if not discounted_price:
        print("Failed to calculate discounted price.")
        return None
    
    # Restructure data to match books.json schema
    book_entry = {
        "name": damage_info["book_name"],
        "damage-level": damage_info["severity"],
        "author": damage_info["author"],
        "type": damage_info["type"].replace("_", " ").title(),
        "discount": discounted_price["discount_rate"],
        "price": discounted_price["discounted_price"],
        "img": f"/static/{image_path.split('/')[-1]}",
        "publisher": publisher,
        "sold": False
    }

    # Add to books.json
    try:
        with open('books.json', 'r') as f:
            data = json.load(f)
        data['books'].append(book_entry)  # Access the 'books' array in the dictionary
        with open('books.json', 'w') as f:
            json.dump(data, f, indent=2)
        return book_entry
    except Exception as e:
        print(f"Failed to update books.json: {e}")
        return None
