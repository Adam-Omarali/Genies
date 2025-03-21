import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, DBSCAN
from scipy.spatial.distance import cdist
import os

# ------------------ CONFIG ------------------
SURCHARGE_PER_3KM = 1.50  # $1.50 per 3 km
OUTLIER_THRESHOLD = 2.0   # Leg is outlier if > 2× average leg length
OUTPUT_FILE = "/Users/joeunyook/htf_fastapi/logistics/delivery_summary.txt"
# --------------------------------------------

# Load and merge data from CSV files
locations_df = pd.read_csv('/Users/joeunyook/htf_fastapi/logistics/bookstore_locations.csv')
requirements_df = pd.read_csv('/Users/joeunyook/htf_fastapi/logistics/delivery_requirements.csv')
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
    plt.show()

# Route report to TXT file
def write_route_report(starting_indigo, retailer_routes):
    with open(OUTPUT_FILE, 'w') as f:
        f.write("📦 Delivery Summary Report\n")
        f.write("====================================\n\n")
        for cluster_id, route in retailer_routes.items():
            f.write(f"🚚 Route #{cluster_id + 1} (Starting at {starting_indigo['Name']}):\n")
            points = [starting_indigo] + route
            total_distance = 0
            leg_distances = []

            for i in range(len(points) - 1):
                d = calculate_distance(
                    (points[i]['Latitude'], points[i]['Longitude']),
                    (points[i+1]['Latitude'], points[i+1]['Longitude'])
                )
                leg_distances.append(d)
                total_distance += d

            avg_leg = np.mean(leg_distances)
            f.write(f"Total Distance: {total_distance:.3f} units\n")
            f.write("Stops:\n")

            surcharge_total = 0
            for i in range(len(route)):
                name = route[i]['Name']
                f.write(f"  {i+1}. {name}")
                if i < len(leg_distances):
                    leg = leg_distances[i]
                    if leg > avg_leg * OUTLIER_THRESHOLD:
                        extra_km = leg * 111  # approx conversion: 1 degree ≈ 111 km
                        surcharge = (extra_km / 3) * SURCHARGE_PER_3KM
                        surcharge_total += surcharge
                        f.write(f"  ⚠️  (+${surcharge:.2f} surcharge for detour)")
                f.write("\n")
            
            if surcharge_total > 0:
                f.write(f"💰 Total Surcharge: ${surcharge_total:.2f}\n")
            f.write("\n")
        f.write("====================================\n")
        f.write("End of Report.\n")
    print(f"\n📝 Delivery summary written to: {OUTPUT_FILE}")

# Main function
def main():
    locations_df = pd.read_csv('/Users/joeunyook/htf_fastapi/logistics/bookstore_locations.csv')
    requirements_df = pd.read_csv('/Users/joeunyook/htf_fastapi/logistics/delivery_requirements.csv')
    merged_df = pd.merge(locations_df, requirements_df, on='Name')
    delivery_stores = merged_df[merged_df['RequiresDelivery'] == 'Yes'].copy()
    starting_indigo = merged_df[(merged_df['Type'] == 'Indigo') & (merged_df['RequiresDelivery'] == 'Yes')].iloc[0].to_dict()

    clustering_type = input("Select Clustering Type: Known K (K) / Unknown K (U): ").strip().upper()
    if clustering_type == 'K':
        num_clusters = int(input("Enter the number of clusters (or trucks): "))
        routes = apply_clustering_and_tsp(delivery_stores, 'K', num_clusters)
        mode_text = f"Unsupervised (K-Means, K={num_clusters})"
    else:
        routes = apply_clustering_and_tsp(delivery_stores, 'DBSCAN')
        mode_text = "Unsupervised (DBSCAN, Dynamic K)"

    plot_routes(starting_indigo, routes, mode_text)
    write_route_report(starting_indigo, routes)

if __name__ == "__main__":
    main()
