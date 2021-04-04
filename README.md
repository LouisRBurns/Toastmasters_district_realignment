# Toastmasters District Realignment
These are Python scripts to realign a district using a genetic algorithm.

## Overview
Each year, Toastmasters districts are required to realign their districts to help accomplish the district mission.

Toastmasters International governs the structure of valid alignments. [Alignment and Planning](https://www.toastmasters.org/leadership-central/district-leader-tools/district-management/alignment-and-planning.aspx) documents are available online.

The main grouping problem is grouping clubs into areas of 5 clubs. The allowable range is 4-6. The first criterion is geographic proximity. Another criterion is club size and strength for which we often use the Distinguished Club Program as a proxy knowing that it doesn't tell the whole story. We look at clubs that are disbanding and newly chartered clubs. Lastly, we consider the opportunity for each area to reach its own awards in the Distinguished Area program. 

## Alignment Values

As we tell our officers - focus on making sure members are getting awards and we will hit our club goals. An Area Director that encourages his Club Presidents toward encouraging their members to get their awards stands the best chance of becoming distinguished regardless of the alignment. 

While "stability" or "consistency" might be desirable generally, it is much more important that areas are aligned so that Area Directors have meaningful experiences and that contests have sufficient participation. This is best achieved by making sure as many areas as possible have 5 clubs in them. Too often, consistency means areas degrade over time and we end up with lots of area contests with only two or three clubs represented. That level of participation is a heavy burden on participating clubs and district support staff. 

Likewise, divisions are ideally 5 areas. This makes for reasonably-lengthed contests. Three areas minimum are required. 

## Problem Description

Most divisions nominally have around 200 clubs plus or minus. In the past, realignment was done on paper with committee members circling groups of 4-6 clubs on a map based on who knew what about the strength of the clubs and their relationships. 

Clubs are grouped into areas. Areas are grouped into divisions. Divisions make up the district. For 200 clubs, that would be 40 areas and 8 divisions. When the number isn't divisible by 5, we count from the end to make sure the remainder areas and divisions have 4. 

Grouping clubs and areas are both similar to the Vehicle Routing Problem which is a special case of the Traveling Salesman Problem which is an NP-hard combinatorial optimization problem. Each level - areas and divisions - can be optimized through genetic algorithms. Here, I use the Python DEAP module on geocoded zip codes. 

One unique feature of this process is that we want to maximize the number of areas and divisions that have 5 members. This was accomplished through encoding rather than as a constraint. 

I initially included club strength in the fitness function but found that the algorithm could not converge on it. And after studying gerrymandering and apportionment, I am skeptical that any metric other than club status and club location are viable inputs. 

Between club grouping and area grouping, districts are encouraged to manually inspect the alignment before proceeding. Clubs in adjacent or overlapping areas could be switched to better balance club strength. 

## Workflow

Create a virtual environment from `environment.yml`. 

The initial input is a csv file that has column headers "Club" which is the club number and "Clubzip" which is the zip code.

Run the prepocessing file (insert your club file):

`python district_preprocessing <clubs_raw.csv>`

I found unexpected behavior with the `zipcodes` module (at least to me). See the issues on how to resolve unknown zip codes. 

Confirm you see the number of results you were expecting.

Run the genetic algorithm for the areas:

`python area_realign.py`

Run the area post processing script:

`python district_postprocessing_areas.py`

Inspect the shapefiles in Carto (free), ArcGIS (paid), or QGIS (free). Make any needed adjustments to the csv file. If you do, make sure to recalculate the area centroids needed for the next step:

`python caluculate_centroids.py <clubs_adjusted.csv>`

Run the genetic algorithm for divisions:

`python division_alignment.py`

Run the post processing for divisions:

`python district_postprocessing_divisions.py`

Inspect the resulting files. Get feedback and make adjustments as needed. 

## Notebooks

If you would like to see how individual steps were accomplished, my Jupyter Notebooks have been included. Also, `assignment_functions.py`, `calculate_centroids.py`, and `grouping_functions.py` can be imported for use in Notebooks. 