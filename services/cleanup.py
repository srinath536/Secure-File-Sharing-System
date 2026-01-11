import json, time, os

META_FILE = "metadata.json"

def cleanup_expired_files():
    with open(META_FILE, "r") as f:
        metadata = json.load(f)

    for file_id, file in metadata.items():
        if file["status"] == "ACTIVE" and time.time() > file["expiry"]:
            if os.path.exists(file["path"]):
                os.remove(file["path"])
            file["status"] = "DELETED"

    with open(META_FILE, "w") as f:
        json.dump(metadata, f, indent=4)
