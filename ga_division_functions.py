import csv
import pickle
import os
from math import ceil, pi
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from grouping_functions import select_grouping_function

class AreaAlignment:
    '''This class encapsulates the next step of the district realignment 
    problem which consists of grouping individual areas into divisions of 
    mostly five areas and optimized for proximity. This problem takes 
    elements from the vehicle routing problem which is a special grouping 
    case of the traveling saleman problem. The distances are serialized. 
    The input are the area centroids generated previously from their 
    respective member clubs.
    '''

    def __init__(self):
        """
        Creates an instance of a District Realignment
        """
        # initialize instance variables
        self.locations = []
        self.distances = []
        self.area_count = 0
        self.division_count = 0
        self.get_divisions_function = None

        # initialize the data and function
        self.__init_data()
        self.__init_select_division_grouping_function()
    
    def __len__(self):
        """
        Returns the length of numbers representing the problem. The problem
        consists of the number of clubs plus the number of areas (less one). 
        The indices beyond the number of clubs will act as separators.
        """
        return self.area_count

    def __init_data(self):
        """
        Get or call to create serialized data for access during 
        optimization.
        """
        try:
            with open('data/area_locations.pkl', 'rb') as f:  
                self.locations = pickle.load(f)
            with open('data/area_dist.pkl', 'rb') as f:
                self.distances = pickle.load(f)
        except (OSError, IOError):
            pass

        if not (len(self.locations) > 0) or (len(self.distances) > 0):
            print("Data not previously serialized. Creating now.")
            self.__create_data()

        # Set the district size
        self.area_count = len(self.locations)
        # Calculate number of divisions (based on maximizing for 5 clubs)
        self.division_count = ceil(self.area_count / 5)
        print(f'''With {self.area_count} areas, there will be 
                  {self.division_count} divisions.''')

    def __create_data(self):
        '''
        This serializes the locations and distances.
        '''
        with open('data/area_centroids.pkl', 'rb') as f:
                df = pickle.load(f)
        self.locations = [np.asarray([row[2], row[1]], dtype='float32') \
                            for row in df.itertuples()]
        
        self.division_count = len(self.locations)
        
        # Initialize matrix for distance values
        self.distances = np.zeros((self.division_count, self.division_count))
        # Populate matrix with every pairwise distance
        for i in range(self.division_count):
            for j in range(i+1, self.division_count):
                distance = np.linalg.norm(
                    self.locations[j] - self.locations[i])
                self.distances[i][j] = distance
                self.distances[j][i] = distance

        # Serialize locations and qualities
        if not os.path.exists("data"):
            os.makedirs("data")
        with open('data/area_locations.pkl', 'wb') as f:  
	        pickle.dump(self.locations, f)
        with open('data/area_dist.pkl', 'wb') as f:  
	        pickle.dump(self.distances, f)

    def __init_select_division_grouping_function(self):
        '''
        This selects and sets the grouping function based on how 
        many areas are in the district. That way we maximize the 
        number of divisions with 5 clubs without having to optimize
        that separately.
        '''
        self.get_divisions_function = \
                        select_grouping_function(self.area_count)
        print(f'Selected function: {self.get_divisions_function}')
    
    def get_divisions(self, areas_list):
        '''
        This uses the selected function to make a list of divisions.
        :param areas_list: The list of area indices.
        :returns: a list of division lists
        '''
        return list(self.get_divisions_function(areas_list))

    def division_distance(self, division): 
        ''' 
        Calculates the distance between areas in a division sequentially.
        To account for circular vs linear placement, circle back to the 
        first area from the last.
        :param division: The division to be measured consisting of 4 or 5
        areas.
        :return: A total distance calculation
        '''
        # Distance between last and first item to initialize
        distance = self.distances[division[-1]][division[0]]
        for i in range(len(division) - 1):
            distance += self.distances[division[i]][division[i + 1]]
        return distance
    
    def division_average_distance(self, district):
        """
        Gets average distance as an evaluation input.
        ::param district:: the list of divisions from get_divisions
        ::return:: mean distance of division_distance
        """
        return np.mean([self.division_distance(division) for division \
                        in self.get_divisions(district)])

    def evaluate_district(self, district):
        '''
        Evaluation function returning average distance. DEAP requires a
        tuple to be passed to its fitness function.
        '''
        return self.division_average_distance(district), 