# Default site: http://127.0.0.1:5000/
# Need to run the following line in terminal first:
# `mongoimport --db='influencers' --collection='all_platforms' --file=merged_df.csv  --drop --type=csv --headerline` 

# Import the dependencies
# https://hevodata.com/learn/python-mongodb-connection/
from flask import Flask, render_template, request, url_for, redirect, jsonify
import pymongo
from flask_pymongo import PyMongo
# https://www.digitalocean.com/community/tutorials/how-to-use-mongodb-in-a-flask-application
from pymongo import MongoClient
import numpy as np
import datetime as dt
from dateutil.relativedelta import relativedelta
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# import seaborn.objects as so
from io import BytesIO
import base64

# https://kumudithaudaya.medium.com/display-a-table-in-a-database-in-html-using-prettytable-python-70d7325f2e46
# Import from_db_cursor from prettytable library
from prettytable import from_db_cursor

#################################################
# Database Setup
#################################################

# initialise Flask app
app = Flask("myapp")

# connect and create db Influences
app.config["MONGO_URI"] = "mongodb://localhost:27017/influencers"

# initialise client for mongodb
mongo = PyMongo(app)

# Set up MongoDB connection 
# https://www.geeksforgeeks.org/sending-data-from-a-flask-app-to-mongodb-database/
client = MongoClient('mongodb://localhost:27017/') 
db = client['influencers']


#################################################
# Flask Setup
#################################################
# Create an app
app = Flask(__name__)

# Define routes

# Home page - list all routes
@app.route("/")
def homepage():
    """All available api routes:"""

    return (
        f"<u><b>Available Routes</b></u><br/><br/>"
        f"View the top 100 influencers by social media platform:<br/>"
        f"/youtube<br/>"
        f"/threads<br/>"
        f"/instagram<br/>"
        f"/tiktok<br/><br/>"
        f"Valid routes to view influencers by top #x, valid numbers between 1 - 100 <br/>" # across different platforms or all? make a table?
        f"E.g. /10<br/><br/>"
        f"Valid routes to view top influencers ranked between (1 - 100):<br/>"
        f"/1/100<br/><br/>" # {start_number}/{end_number}
        f"View the list of all countries where top 100 influences are from:<br/>"
        f"/countries<br/><br/>"
        f"Valid routes to view influencers from the list of countries in /countries:<br/>"
        f"'input country name here'<br/>"
        f"E.g. /United%20States<br/>"
    )

# List of influencers by platform
@app.route("/instagram", methods=("POST", "GET"))
def instagram():
    """Top 100 Instagram influencers"""

    insta_collection = db.instagram
    insta_df = pd.DataFrame(list(insta_collection.find()))

    # https://stackoverflow.com/questions/52644035/how-to-show-a-pandas-dataframe-into-a-existing-flask-html-table
    return insta_df[['#','NAME','FOLLOWERS','COUNTRY','POTENTIAL REACH']].to_html(header="true", table_id="table",index=False)

@app.route("/threads", methods=("POST", "GET"))
def threads():
    """Top 100 Threads influencers"""

    threads_collection = db.threads
    threads_df = pd.DataFrame(list(threads_collection.find()))
    return threads_df[['#','NAME','FOLLOWERS','COUNTRY','POTENTIAL REACH']].to_html(header="true", table_id="table",index=False)

@app.route("/youtube", methods=("POST", "GET"))
def youtube():
    """Top 100 YouTube influencers"""

    youtube_collection = db.youtube
    youtube_df = pd.DataFrame(list(youtube_collection.find()))
    return youtube_df[['#','NAME','FOLLOWERS','COUNTRY','POTENTIAL REACH']].to_html(header="true", table_id="table",index=False)

@app.route("/tiktok", methods=("POST", "GET"))
def tiktok():
    """Top 100 TikTok influencers"""

    tiktok_collection = db.tiktok
    tiktok_df = pd.DataFrame(list(tiktok_collection.find()))
    return tiktok_df[['#','NAME','FOLLOWERS','COUNTRY','POTENTIAL REACH']].to_html(header="true", table_id="table",index=False)

# up to here - will not work until I pull in the merged df
@app.route("/<topnumber>", methods=("POST", "GET"))
def topnumber_influencers(topnumber):

    """ Show horizontal bar plot from all platforms by top x influencers """
    # get the entire merged_df later
    all_collection = db.all_platforms
    all_df = pd.DataFrame(list(all_collection.find()))

    img = BytesIO()

    # Get top x influencers for each social media platform
    top_x_instagram = all_df[all_df['Social Media Platform'] == 'Instagram'].nlargest(int(topnumber), 'FOLLOWERS')
    top_x_youtube = all_df[all_df['Social Media Platform'] == 'YouTube'].nlargest(int(topnumber), 'FOLLOWERS')
    top_x_tiktok = all_df[all_df['Social Media Platform'] == 'TikTok'].nlargest(int(topnumber), 'FOLLOWERS')
    top_x_threads = all_df[all_df['Social Media Platform'] == 'Threads'].nlargest(int(topnumber), 'FOLLOWERS')

    # Plotting top 10 influencers for each platform
    sns.set_theme(style="whitegrid")
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))

    # Instagram
    sns.barplot(x='FOLLOWERS', y='NAME', data=top_x_instagram, ax=axs[0, 0], palette='Blues_d')
    axs[0, 0].set_title(f'Top {topnumber} Instagram Influencers')
    axs[0, 0].set_xlabel('Followers in Millions')
    axs[0, 0].set_ylabel('Influencer')

    # YouTube
    sns.barplot(x='FOLLOWERS', y='NAME', data=top_x_youtube, ax=axs[0, 1], palette='Greens_d')
    axs[0, 1].set_title(f'Top {topnumber} YouTube Influencers')
    axs[0, 1].set_xlabel('Followers in Millions')
    axs[0, 1].set_ylabel('Influencer')

    # TikTok
    sns.barplot(x='FOLLOWERS', y='NAME', data=top_x_tiktok, ax=axs[1, 0], palette='Reds_d')
    axs[1, 0].set_title(f'Top {topnumber} TikTok Influencers')
    axs[1, 0].set_xlabel('Followers in Millions')
    axs[1, 0].set_ylabel('Influencer')

    # Threads
    sns.barplot(x='FOLLOWERS', y='NAME', data=top_x_threads, ax=axs[1, 1], palette='Purples_d')
    axs[1, 1].set_title(f'Top {topnumber} Threads Influencers')
    axs[1, 1].set_xlabel('Followers in Millions')
    axs[1, 1].set_ylabel('Influencer')

    plt.tight_layout()

    plt.savefig(img, format='png')
    # https://stackoverflow.com/questions/65419083/simple-matplotlib-as-embedded-image-in-web-page-generated-by-flask
    plt.close()

    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return render_template('hbarplot.html', plot_url=plot_url)

# up to here - will not work until I pull in the merged df
# https://stackoverflow.com/questions/61750811/dropdown-menu-for-plotly-choropleth-map-plots
# interactive map - dropdown show different traces depending on ER, potential reach, followers, #influencers?
# @app.route("/map", methods=("POST", "GET"))
# def map():
#     """Display interactive map?"""
  
#   return()

# # list of countries
# @app.route("/countries", methods=("POST", "GET"))
# def countries():
#     """List unique countries"""
  
#   return()

# # list of countries
# @app.route("/<countries>", methods=("POST", "GET"))
# def influencers_in_countries(countries):
#   """Influencers from countries"""
  
#   return()

# # Influencer details - handle, platform
# @app.route("/<name>", methods=("POST", "GET"))
# def influencers_details(name):
#   """Influencers details across social media platforms"""
  
#   return()

# # Avg potential reach by social media platform and category
# @app.route("/avg_reach", methods=("POST", "GET"))
# def avg_reach():
#   """Full graph - average potential reach by social media platform and category"""
  
#   return()

# @app.route("/avg_reach/category", methods=("POST", "GET"))
# def avg_reach():
#   """Average potential reach by social media platform and category"""
  
#   return()

# Run the app
if __name__ == '__main__': 
    app.run(debug=True)
