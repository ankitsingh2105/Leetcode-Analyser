import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for generating hight quality graphics

import io
import matplotlib.pyplot as plt
from flask import Flask, send_file, jsonify, request
from flask_cors import CORS
import requests
import mysql.connector as connector

connect = connector.connect(
    host="localhost",
    user="root",
    password="thechauhan1",
    database="Analyser"
)

cursor = connect.cursor();

app = Flask(__name__)
CORS(app)
# CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.after_request
def add_cors_headers(response):
    # Allow requests from all origins
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/chart')
def generate_chart():
    try:
        # Make a request to fetch data
        username = request.args.get('username')
        # cursor.execute("INSERT INTO NAME (names) values (%s) ", username)
        # connect.commit();
        with open('usernames.txt', 'a') as file:
            file.write(username + '\n')

        if not username:
            return jsonify({'error': 'Username is required'})

        # Make a request to fetch data for the specified username
        response = requests.get(f'https://leetcode-api-faisalshohag.vercel.app/{username}')
        data = response.json()
        
        # Extract x and y values from the data
        ac_submission_data = data['matchedUserStats']['acSubmissionNum']
        x = [item['difficulty'] for item in ac_submission_data]
        y = [item['count'] for item in ac_submission_data]

        # Create a bar chart using Agg backend
        plt.switch_backend('Agg')
        plt.bar(x, y, color='gold')  # Customize bar color
        plt.xlabel('Difficulty', fontsize=12, fontweight='bold')  # Set x-axis label with bold font
        plt.ylabel('Count', fontsize=12, fontweight='bold')  # Set y-axis label with bold font
        plt.title('Submission Count by Difficulty', fontsize=14, fontweight='bold')  # Set chart title with bold font

        # setting up the x and y axis name with size
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        plt.grid(axis='y', linestyle='-', alpha=0.7)  # Add grid lines only on y-axis
        plt.grid(axis='x', linestyle='-', alpha=0.7)  # Add grid lines only on y-axis
        
        # Annotate each bar with the count of questions
        for i, count in enumerate(y):
            plt.text(x[i], count, str(count), ha='center', va='bottom', fontsize=10)  # Add count at the top of each bar
        
        # Set background color
        plt.gca().set_facecolor('skyblue')
        
        # Save the chart as BytesIO object
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format='png', bbox_inches='tight', pad_inches=0.1)  # Adjust padding and tight layout
        img_bytes.seek(0)
        plt.close()
        
        # Return the image file
        return send_file(img_bytes, mimetype='image/png')
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)})

    


@app.route("/api/rating")
def get_rating():
    try:
        # Make a request to fetch data
        username = request.args.get('username') 
        if not username:
            return jsonify({'error': 'Username is required'})

        # Make a request to fetch data for the specified username
        response = requests.get(f'https://alfa-leetcode-api.onrender.com/{username}/contest')
        data = response.json()['contestParticipation']
        print(data)
        # Extract contest ratings
        ratings = [entry['rating'] for entry in data]

        # Create a line chart using Agg backend
        plt.switch_backend('Agg')
        plt.plot(range(1, len(ratings) + 1), ratings, marker='o', color='gold', linestyle='-')  
        plt.xlabel('Contest', fontsize=12, fontweight='bold')  
        plt.ylabel('Rating', fontsize=12, fontweight='bold')  
        plt.title('Rating Over Time', fontsize=14, fontweight='bold')  

        # Customize the appearance
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        plt.grid(axis='y', linestyle='-', alpha=0.7)
        plt.grid(axis='x', linestyle='-', alpha=0.7)

        # Save the chart as BytesIO object
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format='png', bbox_inches='tight', pad_inches=0.1)
        img_bytes.seek(0)
        plt.close()

        # Return the image file
        return send_file(img_bytes, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)})
    

@app.route("/api/name")
def get_name():
    try:
        username = request.args.get('username') 

        # Make a request to fetch data for the specified username
        response = requests.get(f'https://alfa-leetcode-api.onrender.com/{username}')

        data = response.json()
        
        # Check if the response contains the expected data structure
        name = data['name']
        image = data['avatar']
        return jsonify({'name': name, 'image': image})
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'An error occurred'})



@app.route('/api/submissions')
def get_leetcode_data():
    try:
        # Make a GET request to the LeetCode API
        username = request.args.get('username') 
        if not username:
            return jsonify({'error': 'Username is required'})

        # Make a request to fetch data for the specified username
        response = requests.get(f'https://leetcode-api-faisalshohag.vercel.app/{username}')
        data = response.json()
        return jsonify(data)  # Return the JSON data from the LeetCode API
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}) 
    

if __name__ == '__main__':
    app.run(debug=True)
