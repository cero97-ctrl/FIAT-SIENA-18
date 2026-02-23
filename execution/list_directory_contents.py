import argparse
import json
import sys
from pathlib import Path


def print_error(message: str, details: str, exit_code: int):
    """Prints a structured error message to stderr and exits."""
    error_data = {
        "status": "error",
        "error_message": message,
        "details": details.strip()
    }
    print(json.dumps(error_data, indent=2), file=sys.stderr)
    sys.exit(exit_code)


def generate_tree_string(path: Path, prefix: str = "") -> str:
    """Recursively generates a tree structure string."""
    output = ""
    try:
        # Get all items
        items = list(path.iterdir())

        # Filter out .git directory as it is not relevant for content structure
        items = [i for i in items if i.name != ".git"]

        # Sort: directories first, then files, alphabetically for deterministic output
        items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))

        count = len(items)
        for i, item in enumerate(items):
            is_last = (i == count - 1)
            connector = "└── " if is_last else "├── "

            output += f"{prefix}{connector}{item.name}\n"

            if item.is_dir():
                extension = "    " if is_last else "│   "
                output += generate_tree_string(item, prefix + extension)

    except PermissionError:
        output += f"{prefix}└── [Permission Denied]\n"
    except Exception as e:
        output += f"{prefix}└── [Error: {str(e)}]\n"

    return output


def main():
    """
    Main function to list directory contents.
    Generates a tree-like text structure of the specified directory.
    """
    parser = argparse.ArgumentParser(
        description="Generates a text file with the directory structure of a path."
    )
    parser.add_argument("--root-dir", required=True, help="The root directory to list.")
    parser.add_argument("--output-file", required=True, help="The output text file path.")
    args = parser.parse_args()

    root_dir = Path(args.root_dir)
    output_file = Path(args.output_file)

    # --- Validation ---
    if not root_dir.exists():
        print_error(f"Root directory not found: {root_dir}", "", 1)

    if not root_dir.is_dir():
        print_error(f"Path is not a directory: {root_dir}", "", 2)

    # --- Execution ---
    try:
        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)

        header = f"Directory structure for: {root_dir.resolve()}\n"
        header += "=" * 40 + "\n"

        tree_content = generate_tree_string(root_dir)
        full_content = header + tree_content

        output_file.write_text(full_content, encoding="utf-8")

        # --- Success Output ---
        output_data = {
            "status": "success",
            "structure_file_path": str(output_file)
        }
        print(json.dumps(output_data, indent=2))
        sys.exit(0)

    except Exception as e:
        print_error("An unexpected error occurred while generating the structure.", str(e), 3)


if __name__ == "__main__":
    main()
