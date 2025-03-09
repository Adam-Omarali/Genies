'''
Logistics Optimizer code

'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, DBSCAN
from scipy.spatial.distance import cdist
from io import BytesIO

# Load data from CSV files
locations_df = pd.read_csv('static/logistics/bookstore_locations.csv')
requirements_df = pd.read_csv('static/logistics/delivery_requirements.csv')

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
    plt.savefig(f'static/logistics/optimized_routes_{mode}.png')
    plt.close()
    return f'/static/logistics/optimized_routes_{mode}.png'
    
def plot_routes_and_save(mode, num_trucks):
    if mode == 'supervised':
        routes = unsupervised_shipping(retailers, 'K', num_trucks)
    else:
        routes = unsupervised_shipping(retailers, 'DBSCAN')
    
    plt.figure(figsize=(10, 8))
    colors = ['red', 'green', 'purple', 'orange', 'cyan', 'magenta']
    
    # Plot starting Indigo store
    plt.scatter(starting_indigo['Longitude'], starting_indigo['Latitude'], color='blue', marker='s', s=300, label='Starting Indigo Store')
    plt.text(starting_indigo['Longitude'], starting_indigo['Latitude'] + 0.002, starting_indigo['Name'], fontsize=9, ha='center')
    
    # Plot Retailers and Routes
    for idx, route in enumerate(routes.values()):
        route_color = colors[idx % len(colors)]
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
    
    # Save to bytes buffer instead of file
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    return buf.getvalue()
    

