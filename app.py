# Default site: http://127.0.0.1:5000/
# Need to run the following line in terminal first:
# `mongoimport --db='influencers' --collection='all_platforms' --file=merged_df.csv  --drop --type=csv --headerline` 

# Import the dependencies
# https://hevodata.com/learn/python-mongodb-connection/
from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
# https://www.digitalocean.com/community/tutorials/how-to-use-mongodb-in-a-flask-application
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
import matplotlib
matplotlib.use('agg')

#################################################
# Database Setup
#################################################

# initialise Flask app
app = Flask("myapp")

# connect and create db Influencers
app.config["MONGO_URI"] = "mongodb://localhost:27017/influencers"

# initialise client for mongodb
mongo = PyMongo(app)

# Set up MongoDB connection 
# https://www.geeksforgeeks.org/sending-data-from-a-flask-app-to-mongodb-database/
client = MongoClient('mongodb://localhost:27017/')


db = client['influencers']
collection = db.all_platforms
df = pd.DataFrame(list(collection.find()))

#################################################
# Flask Setup
#################################################
# Create an app
app = Flask(__name__)

# Home page - list all routes
@app.route("/")
def homepage():
    """All available api routes:"""

    return (
        f"<u><b>Available Routes</b></u><br/><br/>"
        f"View the top 100 influencers by social media platform:<br/>"
        f"/platforms<br/><br/>"

        f"Routes to view influencers by top #x, valid numbers between 1 - 100 <br/>"
        f"E.g. /Top10<br/><br/>"

        f"Find your favourite influencer in this list:<br/>"
        f"/influencersList<br/><br/>"

        f"See which platforms your favourite influencer is on:<br/>"
        f"/influencers<br/><br/>"

        f"Bar plot showing average potential reach by social media platform and category<br/>"
        f"/PotentialReach_categories<br/><br/>"

        f"Box plot showing distribution of potential reach by social media platform<br/>"
        f"/PotentialReach_box<br/><br/>"

        f"Distinct list of all countries where top 100 influencers are from:<br/>"
        f"/countries<br/><br/>"

        f"Maps of Top 100 influencers across the world:<br/>"
        f"/map_followers<br/>"
        f"/map_engagement<br/><br/>"

        f"Tree maps of where influencers are from and their influence category:<br/>"
        f"/treemap<br/>"
    )

@app.route("/platforms", methods=("POST", "GET"))
def social_platform_tbl():
    """Get the platform names from the database"""

    platforms = ['Instagram', 'Threads', 'TikTok', 'YouTube']
    return render_template('table.html', platforms=platforms, title='Top 100 Influencers by number of followers')

@app.route('/platforms/Top100/Instagram')
def insta_tbl():
    """Get Top 100 influencers on Instagram"""
    
    df_platform = df.loc[df['Social Media Platform'] == 'Instagram']
    df_platform = df_platform.reset_index()
    df_platform = df_platform.rename(columns={"index":"Rank"})
    df_platform['Rank'] = df_platform.index + 1
    platform_df = df_platform[['Rank','NAME','FOLLOWERS','COUNTRY','POTENTIAL REACH','ENGAGEMENT RATE']]  
    return {'data': platform_df.to_dict('records')}

@app.route('/platforms/Top100/TikTok')
def tiktok_tbl():
    """Get Top 100 influencers on TikTok"""

    df_platform = df.loc[df['Social Media Platform'] == 'TikTok']
    df_platform = df_platform.reset_index()
    df_platform = df_platform.rename(columns={"index":"Rank"})
    df_platform['Rank'] = df_platform.index + 1
    platform_df = df_platform[['Rank','NAME','FOLLOWERS','COUNTRY','POTENTIAL REACH','ENGAGEMENT RATE']]
  
    return {'data': platform_df.to_dict('records')}

@app.route('/platforms/Top100/Threads')
def threads_tbl():
    """Get Top 100 influencers on Threads"""

    df_platform = df.loc[df['Social Media Platform'] == 'Threads']
    df_platform = df_platform.reset_index()
    df_platform = df_platform.rename(columns={"index":"Rank"})
    df_platform['Rank'] = df_platform.index + 1
    platform_df = df_platform[['Rank','NAME','FOLLOWERS','COUNTRY','POTENTIAL REACH','ENGAGEMENT RATE']]
  
    return {'data': platform_df.to_dict('records')}

@app.route('/platforms/Top100/YouTube')
def youtube_tbl():
    """Get Top 100 influencers on YouTube"""

    df_platform = df.loc[df['Social Media Platform'] == 'YouTube']
    df_platform = df_platform.reset_index()
    df_platform = df_platform.rename(columns={"index":"Rank"})
    df_platform['Rank'] = df_platform.index + 1
    platform_df = df_platform[['Rank','NAME','FOLLOWERS','COUNTRY','POTENTIAL REACH','ENGAGEMENT RATE']]
  
    return {'data': platform_df.to_dict('records')}

@app.route("/Top<topnumber>", methods=("POST", "GET"))
def topnumber_influencers(topnumber):

    """ Show horizontal bar plot from all platforms by top x influencers """

    img = BytesIO()

    # Get top x influencers for each social media platform
    top_x_instagram = df[df['Social Media Platform'] == 'Instagram'].nlargest(int(topnumber), 'FOLLOWERS')
    top_x_youtube = df[df['Social Media Platform'] == 'YouTube'].nlargest(int(topnumber), 'FOLLOWERS')
    top_x_tiktok = df[df['Social Media Platform'] == 'TikTok'].nlargest(int(topnumber), 'FOLLOWERS')
    top_x_threads = df[df['Social Media Platform'] == 'Threads'].nlargest(int(topnumber), 'FOLLOWERS')

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

@app.route('/influencersList')
def influencer_list():
    """ Get the names of the influencers from the database """
    influencers = list(collection.distinct("NAME"))
    return jsonify(influencers)

@app.route('/influencers')
def influencer_plot():
    """ Get the names of the influencers from the database """
    influencers = list(collection.distinct("NAME"))
    return render_template('barplot.html', influencers=influencers)

@app.route('/followers_by_platform', methods=("POST", "GET"))
def get_followers_by_platform():
    """ Get data required for bar chart for selected influencer - not listed"""

    # Get the influencer's name from the request body
    data = request.json
    if 'name' not in data:
        return jsonify({'error': 'Name of the influencer is required'}), 400
    
    influencer_name = data['name']

    # Get the data of followers by social media platform for the specific influencer from the database
    followers_by_platform = collection.aggregate([
        {'$match': {'NAME': influencer_name}},
        {'$group': {'_id': '$Social Media Platform', 'total_followers': {'$sum': '$FOLLOWERS'}}},
        {'$sort': {'total_followers': -1}}
    ])
    data = {entry['_id']: entry['total_followers'] for entry in followers_by_platform}
    return jsonify(data)

@app.route('/PotentialReach_categories', methods=("POST", "GET"))
def PotentialReach_categories():

    img = BytesIO()

    # Create the bar plot
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Social Media Platform', y='POTENTIAL REACH', hue='CATEGORY', data=df)

    # Set labels and title
    plt.xlabel('Social Media Platform')
    plt.ylabel('Potential Reach (millions)')

    # Show the plot
    plt.tight_layout()
    plt.savefig(img, format='png')
    plt.show()
    plt.close()

    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return render_template('stackedbarplot.html', plot_url=plot_url, title='Potential reach by categories and platform')

@app.route('/PotentialReach_box')
def PotentialReach_box():
    """Potential Reach box plot"""

    img = BytesIO()

    # Set the figure size
    plt.figure(figsize=(10, 6))

    # Create the box plot
    sns.boxplot(x='Social Media Platform', y='POTENTIAL REACH', data=df)

    # Set labels and title
    plt.xlabel('Social Media Platform')
    plt.ylabel('Potential Reach (millions)')

    # Show the plot
    plt.tight_layout()
    plt.savefig(img, format='png')
    plt.show()

    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return render_template('stackedbarplot.html', plot_url=plot_url, title='Distribution of Potential Reach Across Social Media Platforms')

@app.route("/map_followers", methods=("POST", "GET"))
def map_followers():
    """Interactive map - followers"""

    return render_template('Map_based_on_followers_count_world_map.html', title='Map of influencers and their social media following')

@app.route("/map_engagement", methods=("POST", "GET"))
def map_engagement():
    """Interactive map - engagement"""

    return render_template('engagement_rate_world_map.html', title='Map of countries where Top 100 influencers are from and their engagement rate (%)')

@app.route("/treemap", methods=("POST", "GET"))
def treemap():
    """Interactive heat map"""

    return render_template('Tree map to show the categorisation.html', title='Tree map of countries and categories of influence')

# list of countries
@app.route("/countries", methods=("POST", "GET"))
def countries():
    """List unique countries"""
    countries = list(collection.distinct("COUNTRY"))
    return jsonify(countries)

# Run the app
if __name__ == '__main__': 
    app.run(debug=True)
