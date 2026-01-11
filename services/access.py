import json, time, hashlib

META_FILE = "metadata.json"

def load_metadata():
    with open(META_FILE, "r") as f:
        return json.load(f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def access_file(file_id, password, location):
    metadata = load_metadata()

    if file_id not in metadata:
        return False, "File not found"

    file = metadata[file_id]

    if file["status"] != "ACTIVE":
        return False, "File deleted"

    if time.time() > file["expiry"]:
        return False, "File expired"

    if hash_password(password) != file["password_hash"]:
        return False, "Wrong password"

    if location != file["location"]:
        return False, "Location not allowed"

    with open(file["path"], "r") as f:
        return True, f.read()
