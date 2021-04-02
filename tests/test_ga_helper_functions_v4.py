import pytest
import numpy as np
import pandas as pd
import os.path
import pickle
import random

import ga_helper_functions_v4 as gh

# Create test districts based on number of clubs
district_indices = list(range(167))
test_district = random.sample(district_indices, len(district_indices))
test_district_2 = random.sample(district_indices, len(district_indices))
test_district_3 = random.sample(district_indices, len(district_indices))
district_list = [test_district, test_district_2, test_district_3]

# Test 1
def test_class_creation():
    district = gh.DistrictRealignment()
    assert district.club_count > 0

# Test 2
def test_length_function():
    # Confirm len(district) is the problem representation
    # size, not the number of clubs or areas separately.
    district = gh.DistrictRealignment()
    assert len(district) == (district.club_count)

# Test 3
def test_locations_created():
    district = gh.DistrictRealignment()
    with open('data/loc.pickle', 'rb') as f:  
        locations = pickle.load(f)
    assert len(locations) == len(district)

# Test 4
def test_qualities_created():
    district = gh.DistrictRealignment()
    with open('data/qual.pickle', 'rb') as f:  
        qualities = pickle.load(f)
    assert len(qualities) == len(district)

# Test 4A
def test_distances_created():
    district = gh.DistrictRealignment()
    with open('data/dist.pickle', 'rb') as f:  
        distances = pickle.load(f)
    assert len(distances) == len(district)

# Test 5
def test_get_areas_function_selected():
    # This is to make sure you get back the 
    # expected number of areas. It also confirms
    # that is_separator_index is working.
    district = gh.DistrictRealignment()
    areas_list = district.get_areas(test_district)
    assert len(areas_list) == district.area_count


# Test 6
def test_area_distance():
    district = gh.DistrictRealignment()
    areas_list = district.get_areas(test_district)
    assert district.area_distance(areas_list[0]) > 0

# Test 7
def test_area_average_distance():
    district = gh.DistrictRealignment()
    assert district.area_average_distance(test_district) > 0

# Test 8
def test_one_area_quality_score():
    district = gh.DistrictRealignment()
    areas_list = district.get_areas(test_district)
    assert district.area_quality(areas_list[0]) > 0

# Test 9
def test_one_district_quality_score():
    district = gh.DistrictRealignment()
    assert district.area_average_quality(test_district) > 0

# Test 10A
def test_evaluate_district_not_zero():
    district = gh.DistrictRealignment()
    avg_dist, avg_qlty = district.evaluate_district(test_district)
    assert None or 0 not in [avg_dist, avg_qlty]

# Test 10B
def test_evaluate_district_returns_two_items():
    district = gh.DistrictRealignment()
    assert len(district.evaluate_district(test_district)) == 2

