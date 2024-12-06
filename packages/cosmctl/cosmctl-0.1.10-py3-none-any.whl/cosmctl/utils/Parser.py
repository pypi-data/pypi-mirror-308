import json
import os
import requests
import tempfile

class Loader:

    @staticmethod
    def parse_naming(file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

                opts = data.get('opts')
                project_name = data.get('project_name')
                base_name = data.get('base_name')
                
                return {
                    "opts": opts,
                    "project_name": project_name,
                    "base_name": base_name
                }
        except FileNotFoundError:
            print(f"Error: The file {file_path} does not exist.")
            return None
        except json.JSONDecodeError:
            print(f"Error: The file {file_path} is not a valid JSON file.")
            return None
        

    @staticmethod
    def download_directory(project_name):
        url = f"https://api.github.com/repos/vovibssnff/cosmctl_scripts/contents/{project_name}"
        headers = {"Accept": "application/vnd.github.v3+json"}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            contents = response.json()

            temp_dir = tempfile.mkdtemp()
            
            for item in contents:
                if item['type'] == 'file':
                    file_url = item['download_url']
                    file_name = item['name']
                    
                    file_response = requests.get(file_url)
                    file_response.raise_for_status()
                    
                    file_path = os.path.join(temp_dir, file_name)
                    with open(file_path, 'wb') as file:
                        file.write(file_response.content)
                    
                    print(f"Downloaded {file_name} to {file_path}")
                else:
                    print(f"Skipping directory {item['name']} (nested directories are not handled)")
            return temp_dir
        
        except requests.exceptions.RequestException as e:
            print(f"Failed to download directory from {url}. Error: {e}")
            return None
