"""
Command-line interface for Treecraft.
"""

import argparse
import sys
from treecraft.core.parser import TreeParser
from treecraft.core.generator import Generator

def get_parser():
    """Create and return the argument parser."""
    parser = argparse.ArgumentParser(
        prog="treecraft",
        description="Generate directory structures from text-based tree representations"
    )
    parser.add_argument(
        "input_file",
        help="Path to the input file containing the tree structure"
    )
    parser.add_argument(
        "-o", "--output",
        default=".",
        help="Output directory (default: current directory)"
    )
    return parser

def main():
    """Main entry point for the CLI."""
    parser = get_parser()
    args = parser.parse_args()

    try:
        with open(args.input_file, 'r') as f:
            content = f.read()

        tree_parser = TreeParser()
        generator = Generator()

        structure = tree_parser.parse(content)
        generator.generate(structure, args.output)

        print(f"✨ Successfully created directory structure in {args.output}")
        return 0

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())