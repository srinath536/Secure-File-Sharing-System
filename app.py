from flask import Flask, request, jsonify
from services.storage import secure_file
from services.access import access_file
from services.cleanup import cleanup_expired_files

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    password = request.form["password"]
    ttl = int(request.form["ttl"])
    location = request.form["location"]

    file_id = secure_file(file, password, ttl, location)
    return jsonify({"file_id": file_id})

@app.route("/access", methods=["POST"])
def access():
    data = request.json
    success, result = access_file(
        data["file_id"],
        data["password"],
        data["location"]
    )
    if success:
        return jsonify({"content": result})
    return jsonify({"error": result}), 403

@app.route("/cleanup", methods=["POST"])
def cleanup():
    cleanup_expired_files()
    return jsonify({"status": "cleanup completed"})

if __name__ == "__main__":
    app.run(debug=True)
