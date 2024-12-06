import requests
from urllib.parse import urlparse
from typing import Optional
from .converter import BaseConverter

class GitHubConverter(BaseConverter):
    """Handles conversion of GitHub repositories."""
    
    def __init__(self, output_file: str, github_token: str = None):
        super().__init__(output_file)
        self.headers = {
            'Accept': 'application/vnd.github.v3+json'
        }
        if github_token:
            self.headers['Authorization'] = f'token {github_token}'

    def fetch_content(self, api_url: str, path: str = '') -> dict:
        """Fetch repository content from GitHub API."""
        url = f"{api_url}/{path}" if path else api_url
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def process_content(self, content_list: list, api_url: str, base_path: str = '') -> None:
        """Process and write repository content."""
        for item in content_list:
            # Skip if item path doesn't start with base_path (for subfolder filtering)
            if base_path and not item['path'].startswith(base_path):
                continue
                
            if item['type'] == 'file':
                # Skip binary files
                if not item['name'].endswith(('.md', '.py', '.js', '.java', '.cpp', '.h', '.css', 
                                            '.html', '.txt', '.yml', '.yaml', '.json', '.xml', '.sh')):
                    print(f"Skipping likely binary file: {item['path']}")
                    continue
                    
                response = requests.get(item['download_url'], headers=self.headers)
                try:
                    content = response.text
                    # If processing a subfolder, adjust the displayed path
                    display_path = item['path']
                    if base_path:
                        display_path = item['path'][len(base_path):].lstrip('/')
                    self.write_content(display_path, content)
                except Exception as e:
                    print(f"Error processing {item['path']}: {str(e)}")
                    
            elif item['type'] == 'dir':
                # Recursively process subdirectories
                subdir_content = self.fetch_content(api_url, item['path'])
                self.process_content(subdir_content, api_url, base_path)

    def convert(self, repo_url: str, subfolder: Optional[str] = None) -> None:
        """
        Convert GitHub repository to text format.
        
        Args:
            repo_url (str): GitHub repository URL
            subfolder (Optional[str]): Specific subfolder to process (e.g., "packages/mylib")
        """
        # Parse GitHub URL
        parsed = urlparse(repo_url)
        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) != 2:
            raise ValueError("Invalid GitHub URL format. Expected: https://github.com/owner/repo")
        
        owner, repo = path_parts
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
        
        # Clear output file if it exists
        self.output_file.write_text('')
        
        # If subfolder is specified, adjust the API URL
        if subfolder:
            base_path = subfolder
            api_url = f"{api_url}/{subfolder}"
        else:
            base_path = ''
            
        try:
            # Verify subfolder exists if specified
            if subfolder:
                self.fetch_content(api_url)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise ValueError(f"Subfolder '{subfolder}' not found in repository")
            raise
            
        # Start processing from root or subfolder
        content = self.fetch_content(api_url)
        self.process_content(content, api_url, base_path)