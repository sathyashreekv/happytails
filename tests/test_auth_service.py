# test_auth_service.py

import pytest
from auth_service import hash_password, verify_password, create_user, authenticate_user

class FakeUsersCollection:
    def __init__(self):
        self.users = {}

    def find_one(self, query):
        return self.users.get(query["username"], None)

    def insert_one(self, user):
        self.users[user["username"]] = user

@pytest.fixture
def fake_users():
    return FakeUsersCollection()

def test_hash_and_verify_password():
    pw = "secure123"
    hashed = hash_password(pw)
    assert verify_password(pw, hashed)
    assert not verify_password("wrong", hashed)

def test_create_user_success(fake_users):
    success, msg = create_user(fake_users, "john", "pw123", "user")
    assert success
    assert msg == "User created"

def test_create_user_duplicate(fake_users):
    create_user(fake_users, "john", "pw123", "user")
    success, msg = create_user(fake_users, "john", "pw123", "user")
    assert not success
    assert msg == "Username already exists"

def test_authenticate_user(fake_users):
    create_user(fake_users, "alice", "mypw", "admin")
    success, role = authenticate_user(fake_users, "alice", "mypw")
    assert success
    assert role == "admin"

    success, role = authenticate_user(fake_users, "alice", "wrongpw")
    assert not success
    assert role is None
