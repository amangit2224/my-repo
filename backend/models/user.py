from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = self.hash_password(password)  # ✅ Hash on init

    @staticmethod
    def hash_password(password):
        """Hash a password - used by both signup and reset"""
        return generate_password_hash(password)
    
    @staticmethod
    def check_password(password_hash, password):
        """Verify password"""
        return check_password_hash(password_hash, password)
    
    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash  # ✅ Correct field name
        }