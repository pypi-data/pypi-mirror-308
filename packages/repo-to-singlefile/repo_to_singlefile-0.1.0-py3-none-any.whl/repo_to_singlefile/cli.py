# repo_to_singlefile/cli.py
import argparse
import sys
from pathlib import Path
import tiktoken
from .local import LocalConverter
from .github import GitHubConverter

def count_tokens(file_path: str) -> tuple[int, int]:
    """
    Count tokens and characters in the output file using tiktoken.
    Returns a tuple of (token_count, char_count).
    """
    try:
        encoder = tiktoken.get_encoding("cl100k_base")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            tokens = encoder.encode(content)
            return len(tokens), len(content)
    except Exception as e:
        print(f"Error counting tokens: {str(e)}", file=sys.stderr)
        return 0, 0

def format_number(num: int) -> str:
    """Format number with thousands separator."""
    return f"{num:,}"

def print_summary(token_count: int, char_count: int) -> None:
    """Print a summary of the conversion including token and character counts."""
    print("\n" + "="*50)
    print("CONVERSION SUMMARY")
    print("="*50)
    print(f"Total tokens: {format_number(token_count)}")
    print(f"Total characters: {format_number(char_count)}")
    
    # Add cost estimates for common models
    print("\nEstimated costs (based on current OpenAI pricing):")
    gpt4_input_cost = (token_count / 1000) * 0.03
    gpt4_output_cost = (token_count / 1000) * 0.06
    gpt35_input_cost = (token_count / 1000) * 0.001
    gpt35_output_cost = (token_count / 1000) * 0.002
    
    print(f"GPT-4:")
    print(f"  - Input cost: ${gpt4_input_cost:.2f}")
    print(f"  - Output cost: ${gpt4_output_cost:.2f}")
    print(f"GPT-3.5:")
    print(f"  - Input cost: ${gpt35_input_cost:.2f}")
    print(f"  - Output cost: ${gpt35_output_cost:.2f}")
    print("="*50)

def main():
    parser = argparse.ArgumentParser(description='Convert a code repository into text format')
    parser.add_argument('repo', help='Local path or GitHub URL of the repository')
    parser.add_argument('output', help='Output file path')
    parser.add_argument('--github-token', help='GitHub personal access token for private repos', default=None)
    parser.add_argument('--subfolder', help='Specific subfolder to process (e.g., "packages/mylib")', default=None)
    
    args = parser.parse_args()
    
    try:
        if args.repo.startswith('http'):
            print(f"Processing GitHub repository: {args.repo}")
            if args.subfolder:
                print(f"Processing subfolder: {args.subfolder}")
            converter = GitHubConverter(args.output, args.github_token)
            converter.convert(args.repo, subfolder=args.subfolder)
        else:
            print(f"Processing local repository: {args.repo}")
            if args.subfolder:
                print(f"Processing subfolder: {args.subfolder}")
            converter = LocalConverter(args.output)
            converter.convert(args.repo, subfolder=args.subfolder)
            
        print(f"\nRepository content has been written to: {args.output}")
        
        # Count tokens and print summary
        token_count, char_count = count_tokens(args.output)
        print_summary(token_count, char_count)
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()