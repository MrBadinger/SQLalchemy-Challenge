# SQLalchemy-Challenge

## Background

In preparation for a Hawaiian vacation trip planning we will be using python, SQL, and SQL Alchemy to perform a climate analysis.

### Precipitation Analysis
1. We will use SQL Alchemy to pull precipitation data from an SQLite database about Hawaii weather station readings.
2. With the data we will plot a bar chart showing the last year worth of daily precipitation recordings.

### Station Analysis 
1. In this analysis we find the most active station and develop histogram of daily temperature readings. We will use the same timeframe as we did in the precipitation Analysis

### Flask
1. We will take our analysis and put them in flasks so that the data cam be pulled in an API JSON format.
2. Our flask will allow us to enter any start and/or end date into the URL, and it will return the min, avg, and max temperatures for the stated time period.
