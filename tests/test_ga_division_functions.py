import pytest
import numpy as np
import pandas as pd
import os.path
import pickle
import random

import ga_division_functions as gh

# Create dummy district divisions
area_indices = list(range(34))
test_district = random.sample(area_indices, len(area_indices))

# Test 1
def test_class_creation():
    district = gh.AreaAlignment()
    assert district.division_count > 0

# Test 2
def test_length_function():
    # Confirm len(district) is the problem representation
    # size, not the number of clubs or areas separately.
    district = gh.AreaAlignment()
    assert len(district) == (district.area_count)

# Test 3
def test_locations_created():
    district = gh.AreaAlignment()
    with open('data/area_locations.pkl', 'rb') as f:  
        locations = pickle.load(f)
    assert len(locations) == len(district)

# Test 4
def test_distances_created():
    district = gh.AreaAlignment()
    with open('data/area_dist.pkl', 'rb') as f:  
        distances = pickle.load(f)
    assert len(distances) == len(district)

# Test 5
def test_get_areas_function_selected():
    # This is to make sure you get back the 
    # expected number of divisions. 
    district = gh.AreaAlignment()
    division_list = district.get_divisions(test_district)
    assert len(division_list) == district.division_count

# Test 6
def test_division_distance():
    district = gh.AreaAlignment()
    division_list = district.get_divisions(test_district)
    assert district.division_distance(division_list[0]) > 0

# Test 7
def test_division_average_distance():
    district = gh.AreaAlignment()
    assert district.division_average_distance(test_district) > 0

# Test 8
def test_evaluate_district_not_zero():
    district = gh.AreaAlignment()
    assert district.evaluate_district(test_district)[0] > 0

# Test 9
def test_evaluate_district_returns_tuple():
    district = gh.AreaAlignment()
    assert type(district.evaluate_district(test_district)) == tuple