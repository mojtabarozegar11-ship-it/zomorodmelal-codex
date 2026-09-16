class SessionManager:
    def __init__(self):
        self.sessions = {}

    def set(self, user_id, data):
        self.sessions[user_id] = data

    def get(self, user_id):
        return self.sessions.get(user_id, {})
