# Repo to Single File

A command-line tool that converts code repositories into text format, making them suitable for use as context in Large Language Models (LLMs). Supports both local repositories and GitHub remote repositories.

## Features

- Convert local Git repositories to text format
- Convert GitHub repositories to text format (public and private)
- Process specific subfolders in monorepos
- Respect `.gitignore` patterns for local repositories
- Skip binary files automatically
- Structured output with clear file demarcation
- Token counting with OpenAI tokenizer
- Cost estimation for GPT-3.5 and GPT-4

## Installation

```bash
pip install repo-to-singlefile
```

## Usage

### Basic Usage

1. Convert a local repository:
```bash
repo-to-singlefile /path/to/local/repo output.txt
```

2. Convert a public GitHub repository:
```bash
repo-to-singlefile https://github.com/owner/repo output.txt
```

3. Convert a private GitHub repository:
```bash
repo-to-singlefile https://github.com/owner/repo output.txt --github-token YOUR_GITHUB_TOKEN
```

### Monorepo Support

Process only specific subfolders in a repository:

1. Local monorepo:
```bash
repo-to-singlefile /path/to/repo output.txt --subfolder packages/mylib
```

2. GitHub monorepo:
```bash
repo-to-singlefile https://github.com/owner/repo output.txt --subfolder packages/mylib
```

### Output Format

The generated text file contains the contents of all text files in the repository, with clear headers separating each file:

```
### File: src/main.py ###
[content of main.py]

### File: src/utils.py ###
[content of utils.py]

...
```

After processing, you'll see a summary that includes:
- Total token count
- Total character count
- Estimated costs for GPT-3.5 and GPT-4 usage

Example summary:
```
==================================================
CONVERSION SUMMARY
==================================================
Total tokens: 15,234
Total characters: 45,678

Estimated costs (based on current OpenAI pricing):
GPT-4:
  - Input cost: $0.46
  - Output cost: $0.91
GPT-3.5:
  - Input cost: $0.02
  - Output cost: $0.03
==================================================
```

## Configuration

The tool automatically:
- Respects `.gitignore` patterns in local repositories
- Skips binary files
- Processes common text file extensions:
  - Python (.py)
  - JavaScript (.js)
  - Java (.java)
  - C++ (.cpp, .h)
  - Web (.html, .css)
  - Documentation (.md)
  - Config files (.yml, .yaml, .json)
  - Shell scripts (.sh)
  - Text files (.txt)
  - XML files (.xml)

## GitHub Authentication

For private repositories, you'll need a GitHub personal access token:

1. Generate a token at https://github.com/settings/tokens
2. Use the token with the --github-token option:
```bash
repo-to-singlefile https://github.com/owner/private-repo output.txt --github-token YOUR_TOKEN
```

## Error Handling

The tool provides clear error messages for common issues:
- Invalid repository paths or URLs
- Missing subfolders
- Permission denied errors
- Binary file skipping
- Token counting errors

## Development

### Setup Development Environment

1. Clone the repository:
```bash
git clone https://github.com/yourusername/repo-to-singlefile.git
cd repo-to-singlefile
```

2. Install dependencies:
```bash
pip install -e .
```

### Running Tests

```bash
pytest
```

## Common Issues

### Permission Denied
When accessing private GitHub repositories, make sure your token has the necessary permissions:
- For public repositories: No token needed
- For private repositories: Token needs `repo` scope

### Subfolder Not Found
When specifying a subfolder:
- Ensure the path is relative to the repository root
- Use forward slashes (/) even on Windows
- Check that the subfolder exists in the repository

### Large Repositories
For very large repositories:
- Consider processing specific subfolders
- Be aware of rate limits when using GitHub API
- Monitor token costs for large codebases

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License

## Contact

- Report bugs through GitHub issues
- Submit feature requests through GitHub issues
- For security issues, please see SECURITY.md