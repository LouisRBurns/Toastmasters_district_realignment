import csv
import pickle
import os
from math import ceil, pi
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from grouping_functions import select_grouping_function

class DistrictRealignment:
    '''This class encapsulates the district realignment problem which
    consists of grouping individual clubs into areas of mostly five
    clubs and optimized for proximity.
    This problem takes elements from the vehicle routing problem which
    is a special grouping case of the traveling salesman problem. The 
    distances are serialized. 
    The class uses files created with the district_preprocessing.py file.
    '''

    def __init__(self):
        """
        Creates an instance of a District Realignment
        """
        # initialize instance variables
        self.locations = []
        self.distances = []
        self.club_count = 0
        self.area_count = 0
        self.get_areas_function = None

        # initialize the data and function
        self.__init_data()
        self.__init_select_area_grouping_function()
    
    def __len__(self):
        """
        Returns the length of numbers representing the problem. The problem
        consists of the number of clubs plus the number of areas (less one). 
        The indices beyond the number of clubs will act as separators.
        """
        return self.club_count

    def __init_data(self):
        """
        Get or call to create serialized data for access during optimization.
        """
        try:
            with open('data/loc.pickle', 'rb') as f:  
                self.locations = pickle.load(f)
            with open('data/dist.pickle', 'rb') as f:
                self.distances = pickle.load(f)
        except (OSError, IOError):
            pass

        if not (len(self.locations) > 0) or (len(self.distances) > 0):
            print("Data not previously serialized. Creating now.")
            self.__create_data()

        # Set the district size
        self.club_count = len(self.locations)
        # Calculate number of areas (based on maximizing for 5 clubs)
        self.area_count = ceil(self.club_count / 5)
        print(f'With {self.club_count} clubs, there will be {self.area_count} areas.')

    def __create_data(self):
        '''
        This serializes the locations and 
        distances for algorithm use.
        '''
        df = pd.read_csv('club_zips.csv')
        self.locations = [np.asarray([row[4], row[3]], dtype='float32') \
                            for row in df.itertuples()]
        
        self.club_count = len(self.locations)
        
        # Initialize matrix for distance values
        self.distances = np.zeros((self.club_count, self.club_count))
        # Populate matrix with every pairwise distance
        for i in range(self.club_count):
            for j in range(i+1, self.club_count):
                distance = np.linalg.norm(self.locations[j] - self.locations[i])
                self.distances[i][j] = distance
                self.distances[j][i] = distance

        # Serialize locations and qualities
        if not os.path.exists("data"):
            os.makedirs("data")
        with open('data/loc.pickle', 'wb') as f:  
	        pickle.dump(self.locations, f)
        with open('data/dist.pickle', 'wb') as f:  
	        pickle.dump(self.distances, f)

    def __init_select_area_grouping_function(self):
        '''
        This selects and sets the grouping function based on how 
        many clubs are in the district. That way we maximize the 
        number of areas with 5 clubs without having to optimize
        that separately.
        '''
        self.get_areas_function = select_grouping_function(self.club_count)
        print(f'Selected function: {self.get_areas_function}')

    def get_areas(self, clubs_list):
        '''
        This uses the selected function to make a list of areas.
        :param clubs_list: The list of club indices.
        :returns: a list of area lists
        '''
        return list(self.get_areas_function(clubs_list))

    def area_distance(self, area): 
        ''' 
        Calculates the distance between clubs in an area sequentially.
        To account for circular vs linear placement, circle back to the 
        first club from the last.
        :param area: The area to be measured consisting of 4 or 5 clubs.
        :return: A total distance calculation
        '''
        # Distance between last and first item to initialize
        distance = self.distances[area[-1]][area[0]]
        for i in range(len(area) - 1):
            distance += self.distances[area[i]][area[i + 1]]
        return distance

    def area_average_distance(self, district):
        """
        Gets average distance as an evaluation input.
        ::param district:: the list of areas from get_areas
        ::return:: mean distance of area_distance
        """
        return np.mean([self.area_distance(area) for area in self.get_areas(district)])
    
    def evaluate_district(self, district):
        '''
        Evaluation function returning average distance scores.
        '''
        return self.area_average_distance(district), 
