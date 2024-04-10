# proj-3-grp-4
# Influencers Data Analysis

## Overview

This repository contains Python code for analyzing data from different social media platforms using MongoDB and Python libraries like Pandas and Matplotlib.

## Setup

### Importing Data

To import the data into MongoDB, you can use the following commands:

```bash
mongoimport --host localhost --port 27017 --db influencers --collection Instagram --type csv --headerline
mongoimport --host localhost --port 27017 --db influencers --collection Threads --type csv --headerline
mongoimport --host localhost --port 27017 --db influencers --collection You_Tube --type csv --headerline
mongoimport --host localhost --port 27017 --db influencers --collection Tik_Tok --type csv --headerline
```

![image](https://github.com/htojyy/proj-3-grp-4/assets/150103905/f8f7e1a3-8668-4def-a882-3b7bbd5258bf)


### Dependencies

Make sure you have the following Python libraries installed:

 - Pandas
 - Matplotlib
 - Pymongo

You can install them using pip:

```bash
pip install pandas matplotlib pymongo
```

### Data Analysis

The Python script performs the following operations:

1. Retrieves data from MongoDB collections.
2. Calculates the total number of followers for each social media platform.
3. Visualizes the data using Matplotlib.

![image](https://github.com/htojyy/proj-3-grp-4/assets/150103905/f76afa7a-4d7d-47d6-b1f3-8fab0271cf4e)

