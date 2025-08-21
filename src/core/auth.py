def login(username, password):
    return {"username": username, "token": "abc123"}


def logout(user):
    print(f"Logged out {user['username']}")
