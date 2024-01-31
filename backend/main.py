from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)


# Image
@app.route('/list-docker-images', methods=['GET'])
def list_docker_images():
    try:
        # Run the 'docker images' command and capture the output
        output = subprocess.check_output(['docker', 'images']).decode('utf-8')
        return jsonify({'images': output})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': str(e)})

@app.route('/start-container', methods=['POST'])
def start_container():
    data = request.json
    repository = data.get('repository')
    container_name = data.get('containerName')
    host_port = data.get('hostPort')
    container_port = data.get('containerPort')
    # 提取其他參數
    print(repository, container_name, host_port, container_port)

    try:
        # Assemble the command
        command = ['docker', 'run', '-d', '--name', container_name, '-p', f"{host_port}:{container_port}", repository]
        command_str = ' '.join(command)
        
        # Log the command
        print(f"Executing command: {command_str}")

        # Execute the command
        subprocess.check_output(command, stderr=subprocess.STDOUT)
        return jsonify({'status': 'Container started successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/list-docker-containers', methods=['GET'])
def list_docker_containers():
    try:
        # Run the 'docker images' command and capture the output
        output = subprocess.check_output(['docker', 'ps']).decode('utf-8')
        return jsonify({'containers': output})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': str(e)})


@app.route('/list-folders', methods=['GET'])
def list_folders():
    base_path = '../stack'
    try:
        folders = [name for name in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, name))]
        return jsonify(folders)
    except Exception as e:
        return jsonify({'error': str(e)})

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
