import pytest
import numpy as np
import pandas as pd
import os.path

import district_preprocessing as dp 

# Test 1
def test_csv_has_required_columns(filename = 'data/Clubs_D50.csv'):
    assert type(dp.import_club_zips(filename)) == pd.DataFrame

# Test 2
def test_cleans_dataframe_columns():
    data = dp.import_club_zips(filename = 'data/Clubs_D50.csv')
    assert 'club_no' and 'zip' in data.columns

# Test 3
def test_column_is_int_type():
    data = dp.import_club_zips(filename = 'data/Clubs_D50.csv')
    assert data['club_no'].dtype == int

# Test 4
def test_geocoding_happened():
    data = dp.import_club_zips(filename = 'data/Clubs_D50.csv')
    dp.geocode_dataframe(data)
    assert os.path.isfile('club_zips.csv')

# Test 5
def test_geocoding_lat_long():
    data = pd.read_csv('club_zips.csv')
    assert 'lat' and 'long' in data.columns 

# Test 6
def test_imports_club_performance():
    data = dp.import_club_performance('data/20210112_D50_Club_Performance.csv')
    assert 'current_members' and 'new_members' and 'goals' in data.columns

# Test 7
def test_imports_awards():
    data = dp.import_member_awards('data/20201229_D50_Awards.csv')
    assert 'club_no' and 'awards' in data.columns

# Test 8 
def test_awards_not_empty():
    data = dp.import_member_awards('data/20201229_D50_Awards.csv')
    assert len(data) > 0

# Test 9
def test_merge_club_data():
    clubs = dp.merge_club_data(
                    club_dcp_file='data/20210112_D50_Club_Performance.csv', 
                    member_award_file='data/20201229_D50_Awards.csv')
    assert 'club_no' and 'lat' and 'goals' and 'awards' in clubs.columns

# Test 10
def test_merge_not_empty():
    clubs = dp.merge_club_data(
                    club_dcp_file='data/20210112_D50_Club_Performance.csv', 
                    member_award_file='data/20201229_D50_Awards.csv')
    assert len(clubs) > 0

# Test 11
def test_calculate_club_data_columns():
    clubs = dp.merge_club_data(
                    club_dcp_file='data/20210112_D50_Club_Performance.csv', 
                    member_award_file='data/20201229_D50_Awards.csv')
    club_data = dp.calculate_club_quality(clubs)
    assert 'n_quality' in club_data

# Test 12
def test_export_club_data():
    clubs = dp.merge_club_data(
                    club_dcp_file='data/20210112_D50_Club_Performance.csv', 
                    member_award_file='data/20201229_D50_Awards.csv')
    club_data = dp.calculate_club_quality(clubs)
    dp.export_clubs(club_data)
    assert os.path.isfile('clubs_data.csv')

# Test 13
def test_calculate_club_quality_export():
    clubs = dp.merge_club_data(
                    club_dcp_file='data/20210112_D50_Club_Performance.csv', 
                    member_award_file='data/20201229_D50_Awards.csv')
    club_data = dp.calculate_club_quality(clubs)
    dp.export_clubs(club_data)
    assert os.path.isfile('clubs.csv')

# Test 14
def test_calculate_club_data_export_columns():
    assert 'n_quality' and 'lat' in pd.read_csv('clubs.csv').columns

# Test 15
def test_calculate_club_quality_data_type():
    clubs = dp.merge_club_data(
                    club_dcp_file='data/20210112_D50_Club_Performance.csv', 
                    member_award_file='data/20201229_D50_Awards.csv')
    club_data = dp.calculate_club_quality(clubs)
    assert club_data['club_no'].dtype == int