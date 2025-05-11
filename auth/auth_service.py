# auth_service.py

import bcrypt

def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed)

def create_user(users_col, username, password, role):
    if users_col.find_one({"username": username}):
        return False, "Username already exists"
    hashed = hash_password(password)
    users_col.insert_one({"username": username, "password": hashed, "role": role})
    return True, "User created"

def authenticate_user(users_col, username, password):
    user = users_col.find_one({"username": username})
    if user and verify_password(password, user["password"]):
        return True, user["role"]
    return False, None
