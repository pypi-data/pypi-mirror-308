
class Settings:
    def __init__(self):
        self.licenses_path = 'licenses'
        self.users_path = 'users'
        self.commit_message = 'Update by JoLicense'
        
    def set_files_path(self, licenses_path=None, users_path=None):
        if licenses_path:
            self.licenses_path = licenses_path
        if users_path:
            self.users_path = users_path

    def set_commit_message(self, message):
        self.commit_message = message