import requests
import json
import base64
from datetime import datetime
from .logger import Logger
from .settings import Settings

class LicenseManager:
    def __init__(self, github_username, github_token, repo_name):
        self.github_username = github_username
        self.github_token = github_token
        self.repo_name = repo_name
        self.logger = Logger()
        self.settings = Settings()
        self.base_url = f'https://api.github.com/repos/{github_username}/{repo_name}/contents/'
        self.headers = {
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }

    def set_files_path(self, licenses_path=None, users_path=None):
        self.settings.set_files_path(licenses_path, users_path)
        self.logger.inf(f"Updated file paths - Licenses: {self.settings.licenses_path}, Users: {self.settings.users_path}", "Settings")
        return True

    def _get_file_content(self, file_type):
        file_path = self.settings.licenses_path if file_type == 'licenses' else self.settings.users_path
        try:
            api_url = self.base_url + file_path
            response = requests.get(api_url, headers=self.headers)
            response.raise_for_status()
            content = response.json()
            file_data = base64.b64decode(content['content']).decode('utf-8')
            return file_data, content['sha']
        except requests.exceptions.RequestException as e:
            self.logger.err(f"GitHub API error: {str(e)}", "API")
            return None, None

    def _update_file_content(self, file_type, new_content, sha=None):
        file_path = self.settings.licenses_path if file_type == 'licenses' else self.settings.users_path
        try:
            api_url = self.base_url + file_path
            data = {
                'message': self.settings.commit_message,
                'content': base64.b64encode(new_content.encode('utf-8')).decode('utf-8'),
                'sha': sha
            }
            response = requests.put(api_url, headers=self.headers, json=data)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            self.logger.err(f"GitHub API error: {str(e)}", "API")
            return False

    def register(self, username, password, license_key, hwid):
        self.logger.inf(f"Attempting registration for user: {username}", "Register")
        
        licenses_content, licenses_sha = self._get_file_content('licenses')
        if not licenses_content:
            return False

        # Fix license key handling - filter out empty lines and whitespace
        licenses = [key.strip() for key in licenses_content.split('\n') if key.strip()]
        if license_key not in licenses:
            self.logger.err(f"License key not found: {license_key}", "Register")
            return False

        users_content, users_sha = self._get_file_content('users')
        users = json.loads(users_content) if users_content and users_content.strip() else {}

        if username in users:
            self.logger.err(f"Username already exists: {username}", "Register")
            return False

        users[username] = {
            'password': password,
            'license': license_key,
            'hwid': hwid,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        if self._update_file_content('users', json.dumps(users, indent=4), users_sha):
            # Update licenses file without empty lines
            licenses.remove(license_key)
            new_licenses_content = '\n'.join(licenses) + ('\n' if licenses else '')
            if self._update_file_content('licenses', new_licenses_content, licenses_sha):
                self.logger.suc(f"Successfully registered user: {username}", "Register")
                return True

        return False

    def login(self, username, password, hwid):
        self.logger.inf(f"Attempting login for user: {username}", "Login")
        
        users_content, _ = self._get_file_content('users')
        if not users_content:
            return False

        try:
            users = json.loads(users_content)
            if username in users:
                user_data = users[username]
                if user_data['password'] == password and user_data['hwid'] == hwid:
                    self.logger.suc(f"Login successful for user: {username}", "Login")
                    return True
                self.logger.err("Invalid credentials or HWID", "Login")
            else:
                self.logger.err(f"User not found: {username}", "Login")
        except json.JSONDecodeError:
            self.logger.err("Invalid users file format", "Login")
        
        return False