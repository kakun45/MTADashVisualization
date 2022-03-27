# MTADashVisualization

Python &amp; Dash Visualization of MTA turnstiles Exits &amp; Entries in one week
-------

- requirements.txt
- MTAScrappe.ipynb - Jupyter notebook file to Scrape data/or Get public data
- turnstile_191012.txt - data. Initial MTA’s raw file
- Questions.ipynb - Questions and the ideas for the project
- myfunctions.py - My functions in one file to import for Jupyter notebook to work 
- MTAData.ipynb - Cleaning the data in Jupyter notebook. 
- _midtown_timebins_sum_grater16_sort.csv - Cleaned Data file
- merged_left_whole_city_final_whole.csv - Cleaned data set of a WHOLE city to plot all stations 
- callback-MTA-ent_ext-Map.py - Python app Callback for visualization
- Workflow_Diagram.drawio - a Diagram showing a workflow 'from data frames to Visualization'.
- index10.html - test for the first mapped station (59/Lex)
- app-MTA-web-map.py - python file for rendering a map of Midtown (Map5.html)
- Map5.html - a final map of Midtown that was created with Folium 
- app-MTA-web-map-WHOLE.py - python file for rendering a map of Whole NYC (Map4.html)
- Map4.html - test mapping of NYC #TODO: the data is not cleaned. The green tint on the map shows the biggest circle as Yankee's Stadium station, which number is too big - need to find the reason.
- geocoded TITLED - data of LAT & LON for all the stations
- Awesome-test-My-Imports.ipynb - my learning of imports of my own functions, a prototype for "myfunctions.py" 


LEGEND / Colorcode for Map4, Map5:
Green - Swipe Entrance to MTA system,
Red - Exit through a turnstile.


QUESTIONS to answer with my project:
 - Final Map5.html is Midtown only as my main focus of interest, my most well-known part of a town, the stations I go to. I enjoyed learning about the stations where I go to the most / Closest to get to / the fastest time to travel. 
- Where are the most people are at a given time? - Visualization shows 47th st Rockefeller Center (which was in sync with a personal experience, ex. crowd pic on Flickr https://flic.kr/p/dx6gDr).
- A potential business value: For a mobile food/drink track there is knowing where to sell coffee around the which stations/when? For a photographer - discover low busy times (for booked photoshoots - 5th ave/59th st) and busy areas (for random shootings & quick instant photo sales - 42nd st Times square).
- The flow: I used Dash and Folium in separate files and I brought them together to visualize the map. 
- Future plans: to transform the project into the flask website to render the different HTML pages, get control over the sizes of the bubbles at different times, add several weeks of data into a project to compare annually, build the predictions, add animations.
