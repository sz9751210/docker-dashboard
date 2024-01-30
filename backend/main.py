from flask import Flask, jsonify
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)

@app.route('/run-docker-compose', methods=['POST'])
def run_docker_compose():
    predefined_path = '../stack/nginx'
    try:
        # Get and print the current working directory before changing it
        current_path = os.getcwd()
        print("Current Path:", current_path)

        # Changing the current working directory to the predefined folder path
        os.chdir(predefined_path)

        # Running the docker-compose up command and capturing the output
        output = subprocess.check_output(['docker-compose', 'up'], stderr=subprocess.STDOUT)

        # Get and print the new current working directory
        new_path = os.getcwd()
        print("New Path:", new_path)

        return jsonify({
            'output': output.decode('utf-8'),
            'originalPath': current_path,
            'newPath': new_path
        })
    except Exception as e:
        # Print error to console
        print("Error:", e)
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
