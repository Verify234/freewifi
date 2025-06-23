# --- auth.py ---
# In a real app, integrate Firebase/Auth0 or OAuth (Google/Facebook)
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "guest": {"password": "guest123", "role": "guest"}
}

def login_user(username, password):
    user = USERS.get(username)
    if user and user["password"] == password:
        return user["role"]
    else:
        return "unauthorized"
