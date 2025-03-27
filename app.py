from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

running_processes = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"message": "No file uploaded"}), 400

    file = request.files["file"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    return jsonify({"message": f"Uploaded {file.filename}"}), 200

@app.route("/files")
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify(files)

@app.route("/run")
def run_file():
    filename = request.args.get("filename")
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if filename in running_processes:
        return jsonify({"message": f"{filename} is already running"}), 400

    try:
        process = subprocess.Popen(["python3", file_path])
        running_processes[filename] = process
        return jsonify({"message": f"Running {filename}"}), 200
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

@app.route("/stop")
def stop_file():
    filename = request.args.get("filename")

    if filename not in running_processes:
        return jsonify({"message": f"{filename} is not running"}), 400

    running_processes[filename].terminate()
    del running_processes[filename]
    return jsonify({"message": f"Stopped {filename}"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
