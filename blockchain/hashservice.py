import hashlib
import json

def generate_hash(data:dict):
    
    encoded_data = json.dumps(data, sort_keys=True).encode()
    
    hash_value = hashlib.sha256(encoded_data).hexdigest()
    
    return hash_value

