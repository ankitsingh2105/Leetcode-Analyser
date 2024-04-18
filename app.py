import matplotlib
matplotlib.use('Agg')  # Use the Agg backend

import io
import matplotlib.pyplot as plt
from flask import Flask, send_file, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/chart')
def generate_chart():
    try:
        # Make a request to fetch data
        response = requests.get('https://leetcode-api-faisalshohag.vercel.app/ankitchauhan21')
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
        # Sample data
        data = [1507,1501, 1489, 1522,1541, 1562, 1585, 1564, 1571, 1573, 1582,  1646, 1630, 1687, 1705, 1720, 1719]

        # Create a line chart using Agg backend
        plt.switch_backend('Agg')
        plt.plot(range(1, len(data) + 1), data, marker='o', color='gold', linestyle='-')  # Customize line color, marker, and linestyle
        plt.xlabel('contest', fontsize=12, fontweight='bold')  # Set x-axis label with bold font
        plt.ylabel('Rating', fontsize=12, fontweight='bold')  # Set y-axis label with bold font
        plt.title('Rating Over Time', fontsize=14, fontweight='bold')  # Set chart title with bold font

        # setting up the x and y axis name with size
        plt.xticks(range(1, len(data) + 1), fontsize=10)
        plt.yticks(fontsize=10)
        plt.grid(axis='y', linestyle='-', alpha=0.7)  # Add grid lines only on y-axis
        plt.grid(axis='x', linestyle='-', alpha=0.7)  # Add grid lines only on y-axis

        # Save the chart as BytesIO object
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format='png', bbox_inches='tight', pad_inches=0.1)  # Adjust padding and tight layout
        img_bytes.seek(0)
        plt.close()

        # Return the image file
        return send_file(img_bytes, mimetype='image/png')
    except Exception as e:
        return str(e)

@app.route('/api/submissions')
def get_leetcode_data():
    try:
        # Make a GET request to the LeetCode API
        response = requests.get('https://leetcode-api-faisalshohag.vercel.app/ankitchauhan21')
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        data = response.json()  # Convert response to JSON format
        return jsonify(data)  # Return the JSON data from the LeetCode API
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}) 
    

if __name__ == '__main__':
    app.run(debug=True)
