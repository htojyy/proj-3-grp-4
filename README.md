# proj-3-grp-4 - Influencers Data Analysis


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

### Influencers by Social Media Platform

This project provides a web application to visualize data about social media influencers. It allows users to select an influencer from a dropdown menu and view their follower statistics by social media platform.

  #### Usage

1. Run the Flask server by executing the `app.py` file:

   ```bash
   python app.py
   ```
1 - Open your web browser and go to http://localhost:5000/ to access the application.

2 - Select an influencer from the dropdown menu to view their follower statistics.

3 - Click the "Get Data" button to retrieve and display the follower statistics by social media platform.

   #### Project Structure

```bash
Influencers by SMP/
│
├── app.py            # Flask application
└── templates/
    └── index.html    # HTML template for rendering the main page
   ``` 

![Captura de pantalla 2024-04-16 014054](https://github.com/htojyy/proj-3-grp-4/assets/150103905/ab903f41-6139-46aa-8438-a102659ddad3)


![Captura de pantalla 2024-04-16 012441](https://github.com/htojyy/proj-3-grp-4/assets/150103905/647c9284-ccbf-4ed0-b814-83537bd34717)

### Ethical Considerations

In conducting this data analysis project, ethical considerations were a primary concern. 

Efforts were made to anonymize sensitive data and ensure compliance with data protection regulations. 

Throughout the analysis, we remained vigilant for potential biases. Transparency was prioritized, and efforts were made to clearly document our methodologies.

Our goal was to conduct the analysis in a fair, responsible, and transparent manner, mindful of the potential impact on individuals and communities. We welcome feedback and encourage readers to raise any ethical concerns they may have regarding the project.

### References data source

- https://www.kaggle.com/datasets/bhavyadhingra00020/top-100-social-media-influencers-2024-countrywise?resource=download-
  
### References

- https://git.bootcampcontent.com/University-of-Adelaide/UADEL-VIRT-DATA-PT-12-2023-U-LOLC
- https://www.mongodb.com/
- https://www.python.org/
- https://plotly.com/javascript/
- https://flask.palletsprojects.com/en/3.0.x/
- https://www.sqlalchemy.org/
  

