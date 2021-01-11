# 2019 Global Lightning Density
Interactive Plotly map of lightning density per country

Included is a small sample of the raw lightning data, my Python code, a csv file of analyzed data results, and the resulting interactive map.

1. Raw lightning data: 
I've included a (very small) sample of the global lightning data used to calculate the lightning density per country. Format: Date, Time (UTC), Latitude, Longitude, Peak current with polarity (kA), Intracloud/cloud-to-ground indicator.

2. Python code: 
Using JSON country data and global lightning data, I calculated the lightning density per country (Included map depicts 2019 density values). I counted lightning occurring over land only for this map, excluding ocean activity. The code makes use of the Pandas and Plotly libraries to make an interactive web-based map.

3. Data analysis results (CSV file): 
Once I calculated the land-only lightning density per country, I saved the data in a csv dataframe so it could easily be used for additional analysis in the future.

4. Interactive global density map (HTML file): 
The final result, using Plotly and a world country JSON file to plot 2019 lightning density values per country. The map has zoom in/out, pan, and hover capabilities. The map can be viewed online here: https://kngassert.github.io/2019-Global-Lightning-Density/
