import os
import json
import time
import uuid
import hashlib

FILES_DIR = "files"
META_FILE = "metadata.json"

os.makedirs(FILES_DIR, exist_ok=True)

def load_metadata():
    if not os.path.exists(META_FILE):
        return {}
    with open(META_FILE, "r") as f:
        return json.load(f)

def save_metadata(data):
    with open(META_FILE, "w") as f:
        json.dump(data, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def secure_file(file, password, ttl_hours, location):
    content = file.read().decode()

    file_id = str(uuid.uuid4())
    expiry = time.time() + ttl_hours * 3600

    file_path = os.path.join(FILES_DIR, f"{file_id}.txt")

    with open(file_path, "w") as f:
        f.write(content)

    metadata = load_metadata()
    metadata[file_id] = {
        "path": file_path,
        "password_hash": hash_password(password),
        "expiry": expiry,
        "location": location,
        "status": "ACTIVE"
    }

    save_metadata(metadata)

    return file_id
