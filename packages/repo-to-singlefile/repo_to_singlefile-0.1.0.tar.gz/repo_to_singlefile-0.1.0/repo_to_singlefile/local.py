from pathlib import Path
from typing import Set, Optional
import os
from .converter import BaseConverter

class LocalConverter(BaseConverter):
    """Handles conversion of local repositories."""
    
    def parse_gitignore(self, repo_path: Path) -> Set[str]:
        """Parse .gitignore patterns into a set of ignored patterns."""
        ignored = set()
        gitignore_path = repo_path / '.gitignore'
        
        if not gitignore_path.exists():
            return ignored
            
        with open(gitignore_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    ignored.add(line)
        
        return ignored

    def should_ignore(self, path: str, ignored_patterns: Set[str]) -> bool:
        """Check if a path matches any gitignore pattern."""
        if not ignored_patterns:
            return False
            
        for pattern in ignored_patterns:
            if pattern in path or path.endswith(pattern):
                return True
        return False

    def convert(self, repo_path: str, subfolder: Optional[str] = None) -> None:
        """
        Convert local repository to text format.
        
        Args:
            repo_path (str): Path to the local repository
            subfolder (Optional[str]): Specific subfolder to process (e.g., "packages/mylib")
        """
        repo_path = Path(repo_path)
        
        # If subfolder is specified, adjust the base path
        if subfolder:
            base_path = repo_path / subfolder
            if not base_path.exists():
                raise ValueError(f"Subfolder '{subfolder}' not found in repository")
        else:
            base_path = repo_path
            
        ignored_patterns = self.parse_gitignore(repo_path)
        
        # Clear output file if it exists
        self.output_file.write_text('')
        
        for root, _, files in os.walk(base_path):
            if '.git' in Path(root).parts:
                continue
                
            for file in files:
                file_path = Path(root) / file
                
                # Calculate relative path based on the base_path
                try:
                    rel_path = file_path.relative_to(base_path)
                except ValueError:
                    continue
                    
                if self.should_ignore(str(rel_path), ignored_patterns):
                    continue
                    
                try:
                    with open(file_path, 'r', encoding='utf-8') as source:
                        content = source.read()
                        self.write_content(str(rel_path), content)
                except UnicodeDecodeError:
                    print(f"Skipping binary file: {rel_path}")
                except Exception as e:
                    print(f"Error processing {rel_path}: {str(e)}")