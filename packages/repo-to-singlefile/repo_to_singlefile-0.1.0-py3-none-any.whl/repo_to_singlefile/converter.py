from pathlib import Path
from typing import Set

class BaseConverter:
    """Base class for repository converters."""
    
    def __init__(self, output_file: str):
        self.output_file = Path(output_file)

    def write_content(self, file_path: str, content: str) -> None:
        """Write file content to the output file."""
        with open(self.output_file, 'a', encoding='utf-8') as f:
            f.write(f"\n### File: {file_path} ###\n")
            f.write(content)
            f.write("\n\n")

