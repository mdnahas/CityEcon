#! /usr/bin/env python3

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

def plot_colored_map(polygon_csv, property_csv, output_file):
    # Read the polygon data
    polygon_data = gpd.read_file("outputs/polygons_small.geojson")
    
    # Read the property value data
    property_data = pd.read_csv("outputs/pza_small.csv", dtype={"2022_market_value":"int64"})

    # Merge the polygon data with the property data
    merged_data = polygon_data.merge(property_data, on='PROP_ID')

    # Calculate the quantiles and assign colors
    property_value_quantiles = merged_data['2022_market_value'].quantile([0, 0.2, 0.4, 0.6, 0.8, 1])
    merged_data['color'] = pd.cut(merged_data['2022_market_value'], bins=property_value_quantiles, labels=False)

    # Plot the map
    fig, ax = plt.subplots(1, figsize=(10, 10))
    merged_data.plot(column='color', cmap='viridis', linewidth=0.8, edgecolor='0.8', ax=ax)
    plt.savefig("outputs/chatgpt_map.png")

if __name__ == '__main__':
    polygon_csv = 'path/to/polygon_data.csv'
    property_csv = 'path/to/property_data.csv'
    output_file = 'path/to/output_map.png'
    plot_colored_map(polygon_csv, property_csv, output_file)



    
