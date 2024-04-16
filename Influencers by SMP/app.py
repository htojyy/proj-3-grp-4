from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Connection to MongoDB database
client = MongoClient('mongodb://localhost:27017/')
db = client['influencers']
collection = db['all_platforms']

# Route to load the main page
@app.route('/')
def index():
    # Get the names of the influencers from the database
    influencers = list(collection.distinct("NAME"))
    return render_template('index.html', influencers=influencers)

# Route to get data of followers by social media platform
@app.route('/api/followers_by_platform', methods=['POST'])
def get_followers_by_platform():
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

if __name__ == '__main__':
    app.run(debug=True)