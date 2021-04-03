'''
This script is to take a csv set of clubs
that has been manually adjusted and create
a new set of centroids for imput into
the genetic algorithm for division creation.
Pass in the path to the file name. The csv
must have a columns "club_no" and "area". 

Example running:
python calculate_centroids.py clubs.csv
'''
import numpy as np
import pandas as pd
import pickle
import geopandas as gpd
import sys

def main():
    # Import clubs from command line argument
    clubs = pd.read_csv(sys.argv[0])

    # Create area centroids
    area_centroids = clubs.drop('club_no', axis=1).groupby('area').mean()

    # Export for division formation
    with open('data/area_centroids.pkl', 'wb') as f:  
        pickle.dump(area_centroids, f)
    
    print('Centroids calculated and exported to area_centroids.pkl.')

if __name__ == "__main__":
    main()