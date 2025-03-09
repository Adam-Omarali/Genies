
'''Using Gemini to find severtiy level and types'''
import google.generativeai as genai
import os
from PIL import Image  # Import Pillow library
import random  # For mock damage classifier
import psycopg2  # Uncomment if you're using PostgreSQL
from dotenv import load_dotenv
import re

# 3. Load API Key (from Google Drive - Secure Method)


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)  # Configure Gemini AI

# 4 .Gemini API Classification Function
def classify_book_damage(image_path):
    """
    Uses Gemini API to classify book damage and returns type and severity.
    """
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

        damage_options = ["corner_damage", "cover_scratches", "spine_damage", "water_damage", "tears_or_rips", "misprints", "missing_dust_jacket", "trim_issues"] # Under score labels
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

        Example:
        Damage Type: corner_damage
        Severity: 3
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
    Extracts damage type and severity from the Gemini API response (Underscore Labels).
    """
    damage_match = re.search(r"Damage Type:\s*([a-z_]+)", gemini_response)  # Only lowercase letters and underscores
    severity_match = re.search(r"Severity:\s*(\d+)", gemini_response)

    if damage_match and severity_match:
        damage_type = damage_match.group(1).strip()  # No need to lowercase
        severity = int(severity_match.group(1))

        print(f"Extracted Damage Type: {damage_type}")
        print(f"Extracted Severity: {severity}")
        return {"type": damage_type, "severity": severity}
    else:
        print("Could not extract damage type and severity.")
        return None

# 6. Price Point Determiner
def calculate_discounted_price(original_price, damage_type, severity, devaluation_rate=0.0):
    """
    Calculates the discounted price based on publisher rules and dynamic devaluation.
    """
    try:
        discount_rate = publisher_rules[damage_type][severity]
        print(f"Base Discount Rate: {discount_rate}")  # Print base discount rate

        # Apply dynamic devaluation rate (e.g., 2% = 0.02)
        adjusted_discount_rate = discount_rate * (1 - devaluation_rate)
        print(f"Adjusted Discount Rate: {adjusted_discount_rate} (after {devaluation_rate*100}% devaluation)")  # Print adjusted rate

        discounted_price = original_price * (1 - adjusted_discount_rate)
        print(f"Calculated Discounted Price: ${discounted_price:.2f}")
        return discounted_price
    except KeyError:
        print(f"Error: No rule found for damage type '{damage_type}' severity '{severity}'.")
        return None

# 8. Main Function
def process_book_return(image_path, original_price, devaluation_rate=0.0):
    """
    Main function to orchestrate the process.  Now with dynamic devaluation.
    """
    damage_classification = classify_book_damage(image_path)

    if damage_classification:
        damage_info = extract_damage_info(damage_classification)

        if damage_info:
            discounted_price = calculate_discounted_price(original_price, damage_info["type"], damage_info["severity"], devaluation_rate)

            if discounted_price is not None:
                print(f"Damage Type: {damage_info['type']}")
                print(f"Severity: {damage_info['severity']}")
                print(f"Original Price: ${original_price:.2f}")
                print(f"Final Discounted Price: ${discounted_price:.2f}")
            else:
                print("Could not determine discounted price due to missing rule.")
        else:
            print("Could not extract damage information.")
    else:
        print("Could not classify damage from the image.")

# Added Publisher Rules
publisher_rules = {
    "corner_damage": {1: 0.05, 2: 0.10, 3: 0.22, 4: 0.50, 5: 0.75},
    "cover_scratches": {1: 0.02, 2: 0.05, 3: 0.15, 4: 0.30, 5: 0.50},
    "spine_damage": {1: 0.10, 2: 0.20, 3: 0.40, 4: 0.65, 5: 0.85},
    "water_damage": {1: 0.20, 2: 0.40, 3: 0.60, 4: 0.80, 5: 0.95},
    "tears_or_rips": {1: 0.05, 2: 0.10, 3: 0.30, 4: 0.55, 5: 0.75},
    "misprints": {1: 0.05, 2: 0.15, 3: 0.30, 4: 0.50, 5: 0.80},
    "missing_dust_jacket": {1: 0.05, 2: 0.10, 3: 0.20, 4: 0.35, 5: 0.50},
    "trim_issues": {1: 0.02, 2: 0.07, 3: 0.20, 4: 0.40, 5: 0.60}
}

# 9. Example Usage
if __name__ == "__main__":
    image_path = "/content/drive/MyDrive/htf/book_example.jpg"
    original_price = 20.00
    process_book_return(image_path, original_price)

'''
Logistics Optimizer code

'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, DBSCAN
from scipy.spatial.distance import cdist

# Load data from CSV files
locations_df = pd.read_csv('/Users/joeunyook/htf_fastapi/logistics/bookstore_locations.csv')
requirements_df = pd.read_csv('/Users/joeunyook/htf_fastapi/logistics/delivery_requirements.csv')

# Merge datasets
merged_df = pd.merge(locations_df, requirements_df, on='Name')

# Filter bookstores requiring delivery
delivery_stores = merged_df[merged_df['RequiresDelivery'] == 'Yes'].copy()

# Separate Indigo stores and retailers
indigo_stores = delivery_stores[delivery_stores['Type'] == 'Indigo'].copy()
retailers = delivery_stores[delivery_stores['Type'] == 'Retailer'].copy()

# Identify the designated starting Indigo store
if not indigo_stores.empty:
    starting_indigo = indigo_stores.iloc[0].to_dict()
else:
    raise ValueError("No starting Indigo store found. Check your data.")

# Function to calculate Euclidean distance
def calculate_distance(coord1, coord2):
    return np.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)


# Unsupervised Clustering: Choose between K-Means (known K) or DBSCAN (unknown K)
def unsupervised_shipping(retailers, clustering_type, num_clusters=None):
    retailers = retailers.copy()
    coords = retailers[['Latitude', 'Longitude']].values
    
    if clustering_type == 'K':
        kmeans = KMeans(n_clusters=num_clusters, random_state=0, n_init=10).fit(coords)
        retailers.loc[:, 'Cluster'] = kmeans.labels_
    else:  # DBSCAN for unknown K
        dbscan = DBSCAN(eps=0.015, min_samples=2).fit(coords)
        retailers.loc[:, 'Cluster'] = dbscan.labels_
    
    clusters = {i: retailers[retailers['Cluster'] == i].to_dict('records') for i in set(retailers['Cluster']) if i != -1}
    return clusters

# Function to plot the optimized delivery pathways
def plot_routes(starting_indigo, retailer_routes, mode):
    plt.figure(figsize=(10, 8))
    colors = ['red', 'green', 'purple', 'orange', 'cyan', 'magenta']
    
    # Plot starting Indigo store
    plt.scatter(starting_indigo['Longitude'], starting_indigo['Latitude'], color='blue', marker='s', s=300, label='Starting Indigo Store')
    plt.text(starting_indigo['Longitude'], starting_indigo['Latitude'] + 0.002, starting_indigo['Name'], fontsize=9, ha='center')
    
    # Plot Retailers and Routes
    for idx, route in enumerate(retailer_routes.values()):
        route_color = colors[idx % len(colors)]  # Assign colors
        route_points = [(starting_indigo['Latitude'], starting_indigo['Longitude'])] + [(r['Latitude'], r['Longitude']) for r in route]
        
        for j in range(len(route_points) - 1):
            plt.plot(
                [route_points[j][1], route_points[j + 1][1]],
                [route_points[j][0], route_points[j + 1][0]],
                color=route_color, linestyle='-', linewidth=2
            )
        
        for retailer in route:
            plt.scatter(retailer['Longitude'], retailer['Latitude'], color=route_color, marker='o', s=100)
            plt.text(retailer['Longitude'], retailer['Latitude'] - 0.002, retailer['Name'], fontsize=8, ha='center')
    
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title(f"Optimized Delivery Routes ({mode} Mode)")
    plt.legend()
    plt.grid()
    plt.show()

# Main function
def main():
    clustering_type = input("Select Clustering Type: Known K (K) / Unknown K (U): ").strip().upper()
    
    if clustering_type == 'K':
        num_clusters = int(input("Enter the number of clusters (or trucks): "))
        routes = unsupervised_shipping(retailers, 'K', num_clusters)
        mode_text = f"Unsupervised (K-Means, K={num_clusters})"
    else:
        routes = unsupervised_shipping(retailers, 'DBSCAN')
        mode_text = "Unsupervised (DBSCAN, Dynamic K)"
    
    plot_routes(starting_indigo, routes, mode_text)

if __name__ == "__main__":
    main()

