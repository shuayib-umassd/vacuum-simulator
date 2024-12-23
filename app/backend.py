from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import requests  # For simulation script to send data to the backend

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for the app
CORS(app)

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['vacuum_simulator']
collection = db['simulation_data']

@app.route('/save_simulation', methods=['POST'])
def save_simulation():
    """
    Save simulation data to the MongoDB database.
    """
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        collection.insert_one(data)
        return jsonify({"message": "Simulation data saved successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_simulations', methods=['GET'])
def get_simulations():
    """
    Retrieve all simulation data from the MongoDB database.
    """
    try:
        simulations = list(collection.find({}, {'_id': False}))
        app.logger.info(f"Retrieved {len(simulations)} simulations")
        return jsonify(simulations)
    except Exception as e:
        app.logger.error(f"Error retrieving simulations: {str(e)}")
        return jsonify({"error": str(e)}), 500

def save_simulation_data(env, episode, total_reward):
    """
    Save simulation data to the backend using a POST request.
    """
    data = {
        "episode": episode,
        "total_reward": total_reward,
        "room_map": env.room_map.tolist(),
        "trajectory": env.trajectory,
    }
    try:
        response = requests.post('http://localhost:5000/save_simulation', json=data)
        if response.status_code == 201:
            print("Simulation data saved successfully")
        else:
            print(f"Failed to save simulation data. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error while saving simulation data: {e}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)