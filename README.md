# ClimateAi
Project sample for Data Scientist position

This project represents an interactive web-based global lightning density map by country.

Included is a small sample of the raw lightning data, my Python code, a csv file of analyzed data results, and the resulting interactive map. I don't currently have the exact JSON files used in this code, so have not included them here.

1. Raw lightning data
I've included a (very small) sample of the global lightning data used to calculate the lightning density per country. Prior to analysis, I collected this data via command line using Vaisala's in-house UNIX tools created to process proprietary lightning data. I organized the data by month and zipped the files prior to running my code. Format: Date, Time (UTC), Latitude, Longitude, Peak current with polarity (kA), Intracloud/cloud-to-ground indicator.

2. Python code
Using JSON country data and the Vaisala raw lightning data, I calculated the lightning density per country (Included code and map are for all of 2019). I counted lightning occurring over land only for this map, excluding ocean and lake activity for simplicity. The code makes use of the pandas and Plotly libraries to make an interactive web-based map.

3. Data analysis results (CSV file)
Once I calculated the land-only lightning density per country, I saved the data in a csv dataframe so it could easily be used for additional analysis in the future. (It takes a lot of time to process all of that raw lightning data!)

4. Interactive global density map (HTML file)
The final result, using Plotly and a world country JSON file to plot 2019 lightning density values per country. The map has zoom in/out, pan, and hover capabilities. The map can be viewed online here: https://janelane1013.github.io/ClimateAi_Sample/
