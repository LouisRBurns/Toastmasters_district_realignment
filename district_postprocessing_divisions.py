import numpy as np
import pandas as pd
import pickle
import geopandas as gpd
from grouping_functions import select_grouping_function
from assignment_functions import select_assignment_function

# Load division index
with open('/data/best_divisions_index.pkl', 'rb') as f:  
    best_index = pickle.load(f)

divisions = pd.DataFrame(best_index, columns = ['area'])

# Assign divisions
assign_divisions = select_assignment_function(len(best_index))
divisions['division'] = assign_divisions(best_index)

# Bring in clubs to join
with open('/data/area_clubs.pkl', 'rb') as f:  
    area_clubs = pickle.load(f)

best_dist = area_clubs.merge(divisions, on='area')
                .sort_values(['division', 'area', 'club_no'])
                .reset_index(drop=True)


# Remap areas to be consistent with district structure
def remap_areas(df):
    remapping = []
    # Iterate through each division number
    for d in df.division.unique():
        i = 0
        # Iteration through each area number in the division
        for a in df[df.division == d].area.unique():
            remapping.append(d * 10 + i)
            i += 1
    # Map the new area numbers to the old
    df2 = pd.DataFrame({'new_area': remapping,
                        'area': df.area.unique()})
    # Merge those and clean up
    df3 = df.merge(df2, on='area').drop('area', axis=1).rename(columns={'new_area': 'area'})
    
    return df3[['club_no', 'area', 'division', 'lat', 'long']]

new_district = remap_areas(best_dist)

# Convert the clubs dataframe to a geodataframe
g_clubs = gpd.GeoDataFrame(new_district, 
                           geometry=gpd.points_from_xy(
                               new_district.long, new_district.lat),
                           crs="EPSG:4326")
g_clubs.to_file('/data/new_clubs.shp')
print('new_clubs.shp created.')

# Make area boundaries
g_areas = g_clubs.dissolve(by='area')['geometry']
area_poly = g_areas.convex_hull.buffer(0.02)
area_boundaries = area_poly.boundary
area_boundaries.to_file('/data/new_areas.shp')
print('new_areas.shp created.')

# Repeat with divisions
g_divisions = g_clubs.dissolve(by='division')['geometry']
division_poly = g_divisions.convex_hull.buffer(0.03)
division_boundaries = division_poly.boundary
division_boundaries.to_file('/data/new_divisions.shp')
print('new_divisions.shp created.')

new_district.to_csv('../data/new_district_alignment.csv', index=False)
print('new_district_alignment.csv created.')