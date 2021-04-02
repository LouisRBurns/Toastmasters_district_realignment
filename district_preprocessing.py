''' These functions prepare Toastmasters district csvs for
    the redistricting genetic algorithm through geocoding
    the zip codes.'''

import sys
import numpy as np
import pandas as pd 
import zipcodes

def import_club_zips(filename):
    ''' This function takes in a csv. The club number should be in a
        column named "Club" and the zip code should be in a column
        named "Clubzip." It also drops blank lines and makes the club 
        numbers integers.
    '''
    
    df = pd.read_csv(filename)
    if "Club" and "Clubzip" in df.columns:
        df.rename(columns = {'Club': 'club_no', 'Clubzip': 'zip'}, inplace=True)
        df = df[['club_no', 'zip']].copy().dropna()
        df['club_no'] = df['club_no'].astype(int)
        df = df.sort_values(by = 'club_no')
        print(f'{len(df)} clubs with zipcodes imported.')
        return df
    else:
        print()
        print('ERROR: Required columns not found in club zips file.')
        print('Looking for "Club" and "Clubzip" columns.')
        print('Check file and parameters.')
        print()
        return

def geocode_dataframe(df):
    '''This takes in a dataframe and geocodes it using the zip code
       which can be either a string or an integer.'''
    df['lat'] = [zipcodes.matching(i)[0]['lat'] for i in df['zip']]
    df['long'] = [zipcodes.matching(i)[0]['long'] for i in df['zip']]
    df['long'] = df['long'].astype(float)
    df['lat'] = df['lat'].astype(float)
    
    # Add jitter so the convex hull we want later will work
    # This adds about 100 meters of standard deviation noise
    # to each location point.
    df['long'] += np.random.normal(0, 0.0009, len(df))
    df['lat'] += np.random.normal(0, 0.0009, len(df))
    
    df.to_csv('club_zips.csv', index=False)
    print(f'{len(df.lat)} clubs geocoded out of {len(df)} clubs.')
    return df

if __name__ == "__main__":
    '''Call the functions along with the file:
       ::param sys.argv[1]:: filename for club zips
    '''

    print()
    print("Initializing preprocessing...")

    zips = sys.argv[1]

    geocode_dataframe(import_club_zips(zips))

    print()
    print('Preprocessing complete.')
    print('Confirm club_zips.csv file in your directory.')
    print()
    print('Confirm all the above club numbers look correct before proceeding.')
    print()