"""
These functions assign a list of club indices into
areas based on the number of clubs at the end that 
end up with four instead of five.
The function at the end makes the selection.
:param clubs: The list of club indices (flattened).
:returns: The assignment function for that number of clubs.
"""
# For districts with 0 or 4 clubs left
def assign_areas_zero_left(clubs):
    return [(i // 5 + 1) for i in range(len(clubs))]
        
# For districts with 3 left
def assign_areas_three_left(clubs):
    result = []
    for club in range(0, len(clubs)-8):
        result.append(club // 5 + 1)
    for club in range(len(clubs)-8, len(clubs)-4):
        result.append(result[len(clubs)-9] + 1)
    for club in range(len(clubs)-4, len(clubs)):
        result.append(result[len(clubs)-5] + 1)
    return result
        
# For districts with 2 left
def assign_areas_two_left(clubs):
    result = []
    for club in range(0, len(clubs)-12):
        result.append(club // 5 + 1)
    for club in range(len(clubs)-12, len(clubs)-8):
        result.append(result[len(clubs)-13] + 1)
    for club in range(len(clubs)-8, len(clubs)-4):
        result.append(result[len(clubs)-9] + 1)
    for club in range(len(clubs)-4, len(clubs)):
        result.append(result[len(clubs)-5] + 1)
    return result
                
# For districts with 1 left
def assign_areas_one_left(clubs):
    result = []
    for club in range(0, len(clubs)-16):
        result.append(club // 5 + 1)
    for club in range(len(clubs)-16, len(clubs)-12):
        result.append(result[len(clubs)-17] + 1)
    for club in range(len(clubs)-12, len(clubs)-8):
        result.append(result[len(clubs)-13] + 1)
    for club in range(len(clubs)-8, len(clubs)-4):
        result.append(result[len(clubs)-9] + 1)
    for club in range(len(clubs)-4, len(clubs)):
        result.append(result[len(clubs)-5] + 1)
    return result

def select_assignment_function(clubs_size):
    """
    This checks how many clubs would be left at the
    end of a grouping of 5 clubs per area and selects
    the appropriate function to make sure any areas
    at the end have 4 clubs.
    :param clubs_size: The number of clubs in the district
    :returns: The function for the size.
    """
    if clubs_size % 5 in [0, 4]:
        return assign_areas_zero_left
    elif clubs_size % 5 == 3:
        return assign_areas_three_left
    elif clubs_size % 5 == 2:
        return assign_areas_two_left
    else:
        return assign_areas_one_left