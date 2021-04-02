import numpy as np
import pandas as pd
import pickle
import geopandas as gpd
from grouping_functions import select_grouping_function
from assignment_functions import select_assignment_function

# Load area index and locations
with open('../data/best_areas_index.pkl', 'rb') as f:  
    best_index = pickle.load(f)

with open('../data/loc.pickle', 'rb') as f:  
    loc = pickle.load(f)

# Convert to dataframe for merging
best_df = pd.DataFrame(best_index, columns = ['club_index'])

# Select and use assignment function
assign_areas = select_assignment_function(len(best_index))
best_df['area'] = assign_areas(best_index)

# Sort and reset index
bdf = best_df.copy().set_index('club_index').sort_index()
bdf = bdf.reset_index(drop=True)

# Retrieve club numbers
try:
    old_clubs = pd.read_csv('clubs.csv')
except (OSError, IOError):
    print("clubs.csv not found. Make sure it is in the same directory.")

# Join areas to clubs
best_dist = old_clubs.join(bdf).sort_values(['area', 'club_no']).reset_index(drop=True)
best_dist.to_csv('../data/area_clubs.csv', index = False)
print('area_clubs.csv created.')

# Create area centroids
area_centroids = best_dist.drop('club_no', axis=1).groupby('area').mean()

# Export for division formation
with open('data/area_centroids.pkl', 'wb') as f:  
    pickle.dump(area_centroids, f)

# Create GeoDataFrame for GIS manual plotting
g_clubs = gpd.GeoDataFrame(best_dist, 
                           geometry=gpd.points_from_xy(best_dist.long, best_dist.lat),
                           crs="EPSG:4326")

g_clubs.to_file('../data/clubs_with_areas.shp')
print('clubs_with_areas.shp created.')

# Dissolve groups the points into single objects which are a list of points
areas = g_clubs.dissolve(by='area')['geometry']

# Make boundary file
area_poly = areas.convex_hull.buffer(0.02)
area_boundaries = area_poly.boundary

# Export these for manual inspection
area_boundaries.to_file('../data/area_boundaries.shp')

print('area_boundaries.shp created.')
print()
print('Manually inspect area assignments before proceeding to division realignment.')
print('Edit area_clubs.csv and recalculate centroids for input into next step.')