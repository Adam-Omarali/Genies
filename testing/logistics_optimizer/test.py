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
delivery_stores = merged_df[merged_df['RequiresDelivery'] == 'Yes'].copy()  # Use .copy() to prevent SettingWithCopyWarning

# Separate Indigo stores and retailers
indigo_stores = delivery_stores[delivery_stores['Type'] == 'Indigo'].copy()
retailers = delivery_stores[delivery_stores['Type'] == 'Retailer'].copy()

# Identify the designated starting Indigo store (first Indigo with 'Yes' in RequiresDelivery)
if not indigo_stores.empty:
    starting_indigo = indigo_stores.iloc[0].to_dict()  # Ensure it's a dict, not an int or DataFrame slice
else:
    raise ValueError("No starting Indigo store found. Check your data.")

# Function to calculate Euclidean distance
def calculate_distance(coord1, coord2):
    return np.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

# Supervised Clustering: Assign retailers to the nearest Indigo store, starting from the designated Indigo
def supervised_shipping(starting_indigo, retailers, num_trucks):
    retailer_list = retailers.to_dict('records')
    retailer_list.sort(key=lambda r: calculate_distance((starting_indigo['Latitude'], starting_indigo['Longitude']), (r['Latitude'], r['Longitude'])))
    grouped_routes = [retailer_list[i::num_trucks] for i in range(num_trucks)]
    return grouped_routes

# Unsupervised Clustering: Choose between K-Means (known K) or DBSCAN (unknown K)
def unsupervised_shipping(retailers, clustering_type, num_clusters=None):
    retailers = retailers.copy()  # Prevent SettingWithCopyWarning
    coords = retailers[['Latitude', 'Longitude']].values
    
    if clustering_type == 'K':
        kmeans = KMeans(n_clusters=num_clusters, random_state=0, n_init=10).fit(coords)
        retailers.loc[:, 'Cluster'] = kmeans.labels_  # Use .loc to modify safely
    else:  # DBSCAN for unknown K
        dbscan = DBSCAN(eps=0.005, min_samples=2).fit(coords)  # Adjust `eps` based on data scale
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
    for idx, route in enumerate(retailer_routes.values()):  # Now expecting a dictionary, not a list
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
    plKt.grid()
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
