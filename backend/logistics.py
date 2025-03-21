'''
Logistics Optimizer code

'''
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.cluster import KMeans, DBSCAN
# from scipy.spatial.distance import cdist
# from io import BytesIO

# # Load data from CSV files
# locations_df = pd.read_csv('static/logistics/bookstore_locations.csv')
# requirements_df = pd.read_csv('static/logistics/delivery_requirements.csv')

# # Merge datasets
# merged_df = pd.merge(locations_df, requirements_df, on='Name')

# # Filter bookstores requiring delivery
# delivery_stores = merged_df[merged_df['RequiresDelivery'] == 'Yes'].copy()

# # Separate Indigo stores and retailers
# indigo_stores = delivery_stores[delivery_stores['Type'] == 'Indigo'].copy()
# retailers = delivery_stores[delivery_stores['Type'] == 'Retailer'].copy()

# # Identify the designated starting Indigo store
# if not indigo_stores.empty:
#     starting_indigo = indigo_stores.iloc[0].to_dict()
# else:
#     raise ValueError("No starting Indigo store found. Check your data.")

# # Function to calculate Euclidean distance
# def calculate_distance(coord1, coord2):
#     return np.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

# # Unsupervised Clustering: Choose between K-Means (known K) or DBSCAN (unknown K)
# def unsupervised_shipping(retailers, clustering_type, num_clusters=None):
#     retailers = retailers.copy()
#     coords = retailers[['Latitude', 'Longitude']].values
    
#     if clustering_type == 'K':
#         kmeans = KMeans(n_clusters=num_clusters, random_state=0, n_init=10).fit(coords)
#         retailers.loc[:, 'Cluster'] = kmeans.labels_
#     else:  # DBSCAN for unknown K
#         dbscan = DBSCAN(eps=0.015, min_samples=2).fit(coords)
#         retailers.loc[:, 'Cluster'] = dbscan.labels_
    
#     clusters = {i: retailers[retailers['Cluster'] == i].to_dict('records') for i in set(retailers['Cluster']) if i != -1}
#     return clusters

# # Function to plot the optimized delivery pathways
# def plot_routes(starting_indigo, retailer_routes, mode):
#     plt.figure(figsize=(10, 8))
#     colors = ['red', 'green', 'purple', 'orange', 'cyan', 'magenta']
    
#     # Plot starting Indigo store
#     plt.scatter(starting_indigo['Longitude'], starting_indigo['Latitude'], color='blue', marker='s', s=300, label='Starting Indigo Store')
#     plt.text(starting_indigo['Longitude'], starting_indigo['Latitude'] + 0.002, starting_indigo['Name'], fontsize=9, ha='center')
    
#     # Plot Retailers and Routes
#     for idx, route in enumerate(retailer_routes.values()):
#         route_color = colors[idx % len(colors)]  # Assign colors
#         route_points = [(starting_indigo['Latitude'], starting_indigo['Longitude'])] + [(r['Latitude'], r['Longitude']) for r in route]
        
#         for j in range(len(route_points) - 1):
#             plt.plot(
#                 [route_points[j][1], route_points[j + 1][1]],
#                 [route_points[j][0], route_points[j + 1][0]],
#                 color=route_color, linestyle='-', linewidth=2
#             )
        
#         for retailer in route:
#             plt.scatter(retailer['Longitude'], retailer['Latitude'], color=route_color, marker='o', s=100)
#             plt.text(retailer['Longitude'], retailer['Latitude'] - 0.002, retailer['Name'], fontsize=8, ha='center')
    
#     plt.xlabel('Longitude')
#     plt.ylabel('Latitude')
#     plt.title(f"Optimized Delivery Routes ({mode} Mode)")
#     plt.legend()
#     plt.grid()
#     plt.savefig(f'static/logistics/optimized_routes_{mode}.png')
#     plt.close()
#     return f'/static/logistics/optimized_routes_{mode}.png'
    
    
    


import pandas as pd
import numpy as np
from io import BytesIO
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, DBSCAN
from scipy.spatial.distance import cdist
import os

# ------------------ CONFIG ------------------
SURCHARGE_PER_3KM = 1.50  # $1.50 per 3 km
OUTLIER_THRESHOLD = 2.0   # Leg is outlier if > 2× average leg length
# --------------------------------------------

# Load and merge data from CSV files
locations_df = pd.read_csv('static/logistics/bookstore_locations.csv')
requirements_df = pd.read_csv('static/logistics/delivery_requirements.csv')
merged_df = pd.merge(locations_df, requirements_df, on='Name')
delivery_stores = merged_df[merged_df['RequiresDelivery'] == 'Yes'].copy()

# Euclidean distance function
def calculate_distance(coord1, coord2):
    return np.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

# TSP solver
def solve_tsp(retailers):
    if not retailers:
        return []
    start = retailers[0]
    path = [start]
    must_visit = retailers[1:]
    while must_visit:
        nearest = min(must_visit, key=lambda x: calculate_distance(
            (path[-1]['Latitude'], path[-1]['Longitude']), (x['Latitude'], x['Longitude'])))
        path.append(nearest)
        must_visit.remove(nearest)
    return path

# Apply clustering and TSP
def apply_clustering_and_tsp(delivery_stores, clustering_type, num_clusters=None):
    coords = delivery_stores[['Latitude', 'Longitude']].values
    if clustering_type == 'K':
        cluster_model = KMeans(n_clusters=num_clusters, random_state=0, n_init=10).fit(coords)
    else:
        cluster_model = DBSCAN(eps=0.025, min_samples=2).fit(coords)
    delivery_stores['Cluster'] = cluster_model.labels_

    optimized_routes = {}
    for cluster_label in set(delivery_stores['Cluster']):
        if cluster_label != -1:
            cluster_data = delivery_stores[delivery_stores['Cluster'] == cluster_label]
            optimized_routes[cluster_label] = solve_tsp(cluster_data.to_dict('records'))
    return optimized_routes

# Plotting function
def plot_routes(starting_indigo, retailer_routes, mode):
    plt.figure(figsize=(10, 8))
    colors = ['red', 'green', 'purple', 'orange', 'cyan', 'magenta']
    plt.scatter(starting_indigo['Longitude'], starting_indigo['Latitude'], color='blue', marker='s', s=300, label='Starting Indigo Store')
    plt.text(starting_indigo['Longitude'], starting_indigo['Latitude'] + 0.002, starting_indigo['Name'], fontsize=9, ha='center')
    for idx, route in enumerate(retailer_routes.values()):
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
    plt.title(f"Optimized Delivery Routes ({mode})")
    plt.legend()
    plt.grid(True)
    # Save to bytes buffer instead of file
    plt.savefig('static/logistics/optimized_routes.png')
    plt.close()
    return '/static/logistics/optimized_routes.png'

# Route report as JSON
def write_route_report(starting_indigo, retailer_routes):
    report_data = {
        "title": "Delivery Summary Report",
        "routes": []
    }
    
    for cluster_id, route in retailer_routes.items():
        route_data = {
            "route_number": cluster_id + 1,
            "starting_point": starting_indigo['Name'],
            "total_distance": 0,
            "stops": [],
            "surcharge_total": 0
        }
        
        points = [starting_indigo] + route
        leg_distances = []

        # Calculate distances
        for i in range(len(points) - 1):
            d = calculate_distance(
                (points[i]['Latitude'], points[i]['Longitude']),
                (points[i+1]['Latitude'], points[i+1]['Longitude'])
            )
            leg_distances.append(d)
            route_data["total_distance"] += d

        avg_leg = np.mean(leg_distances)
        
        # Process stops
        for i in range(len(route)):
            stop_data = {
                "stop_number": i + 1,
                "name": route[i]['Name'],
                "surcharge": 0,
                "has_detour": False
            }
            
            if i < len(leg_distances):
                leg = leg_distances[i]
                if leg > avg_leg * OUTLIER_THRESHOLD:
                    extra_km = leg * 111  # approx conversion: 1 degree ≈ 111 km
                    surcharge = (extra_km / 3) * SURCHARGE_PER_3KM
                    stop_data["surcharge"] = round(surcharge, 2)
                    stop_data["has_detour"] = True
                    route_data["surcharge_total"] += surcharge
            
            route_data["stops"].append(stop_data)
        
        route_data["total_distance"] = round(route_data["total_distance"], 3)
        route_data["surcharge_total"] = round(route_data["surcharge_total"], 2)
        report_data["routes"].append(route_data)
    
    return report_data

# Main function
def return_routes(known_k=True, num_clusters=None):
    locations_df = pd.read_csv('static/logistics/bookstore_locations.csv')
    requirements_df = pd.read_csv('static/logistics/delivery_requirements.csv')
    merged_df = pd.merge(locations_df, requirements_df, on='Name')
    delivery_stores = merged_df[merged_df['RequiresDelivery'] == 'Yes'].copy()
    starting_indigo = merged_df[(merged_df['Type'] == 'Indigo') & (merged_df['RequiresDelivery'] == 'Yes')].iloc[0].to_dict()

    if known_k:
        routes = apply_clustering_and_tsp(delivery_stores, 'K', num_clusters)
        mode_text = f"Unsupervised (K-Means, K={num_clusters})"
    else:
        routes = apply_clustering_and_tsp(delivery_stores, 'DBSCAN')
        mode_text = "Unsupervised (DBSCAN, Dynamic K)"

    plot_path = plot_routes(starting_indigo, routes, mode_text)
    route_report = write_route_report(starting_indigo, routes)
    
    
    return {
        "plot": plot_path,
        "report": route_report
    }


