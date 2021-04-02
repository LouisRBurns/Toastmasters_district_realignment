"""
These functions break up a list of clubs into
lists of area lists based on the number of clubs
at the end that end up with four instead of five.
The function at the end makes the selection.
:param clubs: The list of club indices.
:returns: The function for that number of clubs.
"""
# For districts with 0 or 4 clubs left
def districts_with_zero_left(clubs):
    for i in range(0, len(clubs), 5): 
        yield clubs[i:i + 5]
        
# For districts with 3 left
def districts_with_three_left(clubs):
    for i in range(0, len(clubs)-8, 5):
        yield clubs[i:i + 5]
    for i in range(len(clubs)-8, len(clubs), 4):
        yield clubs[i:i + 4]
        
# For districts with 2 left
def districts_with_two_left(clubs):
    for i in range(0, len(clubs)-12, 5):
        yield clubs[i:i + 5]
    for i in range(len(clubs)-12, len(clubs), 4):
        yield clubs[i:i + 4]
                
# For districts with 1 left
def districts_with_one_left(clubs):
    for i in range(0, len(clubs)-16, 5):
        yield clubs[i:i + 5]
    for i in range(len(clubs)-16, len(clubs), 4):
        yield clubs[i:i + 4]

def select_grouping_function(clubs_size):
    """
    This checks how many clubs would be left at the
    end of a grouping of 5 clubs per area and selects
    the appropriate function to make sure any areas
    at the end have 4 clubs.
    :param clubs_size: The number of clubs in the district
    :returns: The function for the size.
    """
    if clubs_size % 5 in [0, 4]:
        return districts_with_zero_left
    elif clubs_size % 5 == 3:
        return districts_with_three_left
    elif clubs_size % 5 == 2:
        return districts_with_two_left
    else:
        return districts_with_one_left